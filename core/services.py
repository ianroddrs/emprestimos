import os
import gspread
from typing import List, Dict, Any
from django.conf import settings
from abc import ABC, ABCMeta

def initialize_gspread() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.

def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }

class GSpreadModelBaseManager:
  def __init__(self, model_class):
      self.model_class = model_class

  def all(self) -> List[Dict[str, Any]]:
      """
      Retorna todos os registros da planilha associados ao modelo.
      """
      instance = self.model_class()
      return instance.worksheet.get_all_records()
  
  def get(self, **kwargs) -> Dict[str, Any]:
    """
    Retorna um registro que atende aos critérios especificados.
    """
    all_records = self.all()
    for record in all_records:
      if all(record.get(k) == v for k, v in kwargs.items()):
        return record
    return None
  
  def filter(self, **kwargs) -> List[Dict[str, Any]]:
    """
    Retorna registros que atendem aos critérios especificados.
    """
    all_records = self.all()
    return [record for record in all_records if all(record.get(k) == v for k, v in kwargs.items())]
  
class GSpreadModelMeta(ABCMeta, type):
  """
  Metaclass para configurar automaticamente o `objects` para as classes filhas.
  """
  def __new__(cls, name, bases, attrs):
      # A classe é criada e agora o manager é atribuído automaticamente
      new_class = super().__new__(cls, name, bases, attrs)
      
      # Atribui automaticamente o manager `objects` para a classe filha
      new_class.objects = GSpreadModelBaseManager(new_class)
      
      return new_class

class GSpreadModel(ABC,metaclass=GSpreadModelMeta):
  dt_name = 'emprestimos'
  worksheet_name = None
  objects = None

  def __init__(self):
    self.sheet = settings.GSPREAD_CLIENT.open(self.dt_name)
    self.worksheet = self.sheet.worksheet(self.worksheet_name)

  @classmethod
  def _get_attrs(cls) -> List[str]:
    # Lista os atributos definidos apenas na classe filha
    return [
        attr for attr in cls.__dict__.keys()
        if not attr.startswith("_") and callable(getattr(cls, attr, None))
    ]
  
