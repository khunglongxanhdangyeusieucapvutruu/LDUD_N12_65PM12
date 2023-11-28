import uuid
import datetime
import models.base_model as base

class Product(base.BaseProduct, base.Expirable, base.Importable, base.Exportable, base.Printable):
  
  @staticmethod
  def _generate_id():
    return uuid.uuid4().hex

  def __init__(self, name, 
               price_out=None, 
               price_in=None,
               nbr_products=None,
               exp=None, mfg=None ) -> None:
    base.BaseProduct.__init__(self,name=name)
    base.Expirable.__init__(self,exp=exp,mfg=mfg)
    base.Importable.__init__(self,price_in=price_in, nbr_products=nbr_products)
    base.Exportable.__init__(self,price_out=price_out)

  def json(self):
    product = self
    return {
        "id" : product.get_id(),
        "name" : product.get_name(),
        "price_in": product.get_price_in(),
        "price_out": product.get_price_out(),
        "exp": product.get_exp(),
        "mfg": product.get_mfg(),
        "nbr_products": product.get_nbr_products(),
      }


class OrderProduct(base.BaseProduct, base.Importable):
  def __init__(self, 
               name, 
               price_in=None,
               nbr_products=None, 
               total_price=None, 
               final_price=None):
    base.BaseProduct.__init__(self,name=name)
    base.Importable.__init__(self,price_in=price_in, nbr_products=nbr_products)

    if total_price is not None and total_price < 0:
      raise ValueError("Total price must be greater than zero.")
    if final_price is not None and final_price < 0:
      raise ValueError("Final price must be greater than zero.")
    self._total_price = total_price
    self._final_price = final_price


  def get_total_price(self):
    return self._total_price
  def get_final_price(self):
    return self._final_price
  
  def set_total_price(self, total_price):
    if total_price is not None and total_price < 0:
      raise ValueError("Total price must be greater than zero.")
    self._total_price = total_price
    
  def set_final_price(self, final_price):
    if final_price is not None and final_price < 0:
      raise ValueError("Final price must be greater than zero.")
    self._final_price = final_price
    
  
  
def date(str_like_date):
  return datetime.datetime.strptime(str_like_date, '%d/%m/%Y')

def get_user_input(message, parse_to=int, error_message="Invalid data, try again."):
  while True:
    try:
      data = parse_to(input(message))
      return data
    except Exception as err:
      if (error_message):
        print(error_message)
      else:
        print(err)



class ManageProduct:
  def __init__(self):
    self.__products = []
    self.__import_orders = []

  def add_product(self, product):
    if not isinstance(product, Product):
      raise ValueError("Param must be a type of Product")
    self.__products.append(product)

  def get_products(self):
    products = []
    for product in self.__products:
      products.append(product.json())
    for product in products:
      print("Ma hang: ",product["id"])
      print("Ten hang: ",product["name"])
      print("Gia ban: ", product["price_out"])
      print("Gia nhap: ",product["price_in"])
      print("Ton kho: ",product["nbr_products"])
      print("Ngay san xuat: ",product["mfg"])
      print("Ngay het han: ",product["exp"])
      print("\n")
    return products
    
  def search_by_name(self, name : str):
    products = []
    for product in self.__products:
      if product.get_name() and name.lower() in product.get_name().lower():
         products.append(product.json())
    return products
  
  def sum_price_in(self):
    total_prices = {}
    for entry in self.__import_orders:
    # Lấy ngày và danh sách hàng hoá từ mỗi mục
      date, product_list = entry
    # Lặp qua từng hàng hoá trong danh sách hàng hoá
      for product in product_list:
          # Lấy tên hàng hoá và giá trị cuối cùng (tổng số tiền)
        product_name, _, _, _, total_price = product

        if product_name in total_prices:
          total_prices[product_name] += total_price
            # Nếu hàng hoá chưa có trong từ điển, thêm nó vào với tổng tiền nhập
        else:
          total_prices[product_name] = total_price
    return total_prices

  def search_import_orders(self, month : int, year : int):
    if month <= 0 or month > 12:
      raise ValueError('Month must be between 1 and 12')
    if year <= 0:
      raise ValueError('Year must be a positive integer')
    found_orders = []
    for order in self.__import_orders:
      import_date = order.get_import_date()
      _year = import_date.year
      _month = import_date.month
      if _year == year and _month == month and isinstance(order, base.Printable):
        found_orders.append(order.json())

    return found_orders
  
  def sort_sum_price_in(self, reverse=False):
    sorted_data = sorted(self.sum_price_in().items(), key=lambda x: x[1], reverse=reverse)    
    
    return dict(sorted_data)

  #7
  def show_top5_high_low_pricein(self):
    product_list = list(self.sort_sum_price_in().items())
    if len(product_list)==0:
      print("không có hàng hoá")
    else:
      high_product = product_list[:5]
      low_product = product_list[-5:]
      print ("top 5 hang hoa co tong nhap cao nhat va thap nhat: ")
      for item in high_product:
        product_name, total_price = item
        print(f"Tên sản phẩm: {product_name}, Tổng giá: {total_price}")
      print("\n")
      for item in low_product:
        product_name, total_price = item
        print(f"Tên sản phẩm: {product_name}, Tổng giá: {total_price}")
    return product_list
  #8: DONE
  def set_new_price_out(self):
    exp_product=[]
    for product in self.__products:
      date_about_to_exp = product.get_exp() - product.get_mfg()
      if (date_about_to_exp.days < 14):
        new_price_out = product.get_price_out()*0.45
        product._price_out = new_price_out
        exp_product.append(product)
      elif (14 < date_about_to_exp.days <= 31):
        new_price_out = product.get_price_out()*0.8
        product._price_out = new_price_out
        exp_product.append(product)
      else:
        print("Cac hang hoa van con han su dung")
    return exp_product
  #10: DONE
  def edit_product(self, id:str):

    product = None

    for p in self.__products:
      if p.get_id() == id:
        product = p
        break

    if product is None:
      raise ValueError("ID product not exist")

    new_name = get_user_input("Enter new product name: ", parse_to=str, error_message="Invalid name, try again!")
    new_price_in = get_user_input("Enter new price in: ", parse_to=int, error_message="Invalide price, it must be an integer.")
    new_price_out = get_user_input("Enter new price out: ", parse_to=int, error_message="Invalide price, it must be an integer")
    new_nbr_products = get_user_input("Enter new number of product: ", parse_to=int, error_message="Invalide, number of products must be an integer")
    exp = get_user_input("Enter expiration day (dd/MM/yyyy): ", parse_to=date, error_message="You must enter a valid date formated as dd/MM/yyyy")

    mfg = get_user_input("Enter manufacturing day (dd/MM/yyyy): ", parse_to=date, error_message="You must enter a valid date formated as dd/MM/yyyy")
    product._name = new_name 
    product._price_out = new_price_in
    product._price_in = new_price_out
    product._nbr_products = new_nbr_products
    product._exp = exp
    product._mfg = mfg 
    return product      

  #11
  def del_product(self, id:str):
    product = None

    for p in self.__products:
      if p.get_id() == id:
        product = p
        break
    if product is None:
      ValueError("ID product not exist")
    else:
      self.__products.remove(product)
  #12
  def add_import_order(self, import_date, product_list):
    self.__import_orders.append([import_date, product_list])
  
  def print_invoices(self):
    for invoice in self.__import_orders:
      print("\nNgay nhap hang:", invoice[0])
      print("----Danh sach don hang---------")
      for item in invoice[1]:
        print("Ten hang:", item[0])
        print("Gia nhap:", item[1])
        print("So luong nhap:", item[2])
        print("Thanh tien:", item[3])
        print("Tong tien:", item[4])
        print("\n")
      print("-----------------------------")



# p = Product(name="Hellp", price_in=10214, price_out=1324, 
#              nbr_products=102, mfg=datetime.datetime.now(), 
#              exp=datetime.datetime.now())
# manager = ManageProduct()

# manager.add_product(p)
# print(manager.get_products()) 

