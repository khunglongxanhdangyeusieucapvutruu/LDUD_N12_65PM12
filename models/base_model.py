import uuid
import datetime


class Printable:
  def json(self):
    return self.__dict__
class Importable:
  def __init__(self, price_in, nbr_products):
    if nbr_products is not None and (not isinstance(nbr_products, int) or nbr_products < 0 ):
      raise ValueError("Ban phai cung cap so luong phu hop cho san pham") 
    if price_in is not None and (not isinstance(price_in, int) or price_in < 0 ):
      raise ValueError("Ban phai cung cap so luong phu hop cho san pham") 
    self._price_in = price_in
    self._nbr_products = nbr_products

  def set_price_in(self, price_in):
    if price_in is not None and (not isinstance(price_in, int) or price_in < 0 ):
          raise ValueError("Ban can cung cap gia tien nhap vao phu hop cho san pham .") 
    self._price_in = price_in
  def get_price_in(self) -> int:
    return self._price_in
  def get_nbr_products(self) -> int:
    return self._nbr_products
  
  def set_nbr_products(self, number_of_products):
    if number_of_products is not None and (not isinstance(number_of_products, int) or number_of_products < 0 ):
      raise ValueError("Ban phai cung cap so luong phu hop cho san pham") 
    self._nbr_products = number_of_products
class Exportable:
  def __init__(self, price_out=None):
    if price_out is not None and (not isinstance(price_out, int) or price_out < 0 ):
      raise ValueError("Ban can cung cap gia tien ban ra phu hop cho san pham.") 
    self._price_out = price_out
  def get_price_out(self) -> int:
    return self._price_out
  def set_price_out(self, price_out):
    if price_out is not None and (not isinstance(price_out, int) or price_out < 0 ):
          raise ValueError("Ban can cung cap gia tien ban ra phu hop cho san pham.") 
    self._price_out = price_out

class Expirable:
  def __init__(self, exp=None, mfg=None ) -> None:
    if exp is not None and not isinstance(exp, datetime.datetime):
      raise ValueError("Ban can cung cap ngay gio cho EXP")
    
    if mfg is not None and not isinstance(mfg, datetime.datetime):
      raise ValueError("Ban can cung cap ngay gio cho  MFG")
    
    if exp is not None and mfg is not None and  exp < mfg:
      raise ValueError("MFG phai lon hon hoac bang EXP")

    self._exp = exp
    self._mfg = mfg


  def get_exp(self) -> datetime.datetime:
    return self._exp
  def get_mfg(self) -> datetime.datetime:
    return self._mfg
  
  def set_exp(self, exp):
      if exp is not None and self._mfg is not None and  exp < self._mfg:
        raise ValueError("EXP phai lon hon hoac bang MGF")
      
      self._exp = exp

  def set_mfg(self, mfg):
      if mfg is not None and self._exp is not None and  mfg > self._exp:
        raise ValueError("MFG phai nho hon hoac bang EXP")
      self._mfg = mfg

class Indexable:
  @staticmethod
  def __generate_id():
    return uuid.uuid4().hex
  def __init__(self) -> None:
    self._id = Indexable.__generate_id()
  def get_id(self):
    return self._id
  
class BaseProduct(Indexable):

  def __init__(self, name ) -> None:
    Indexable.__init__(self)
    if name == None:
      raise ValueError("Invalid product name.")
    self._name = name

  def get_id(self) -> str:
    return self._id
  
  def get_name(self) -> str:
    return self._name
  
  def set_name(self, name) -> None:
    self._name = name

