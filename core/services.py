import os
import gspread
from typing import List, Dict, Any
from django.conf import settings
from abc import ABCMeta
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

def render():
  url = "https://financontrol.onrender.com/"
  try:
      response = requests.get(url)
      if response.status_code == 200:
          print(f"Requisição bem-sucedida: {response.status_code}")
      else:
          print(f"Erro ao acessar o site: {response.status_code}")
  except Exception as e:
      print(f"Erro na requisição: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(render, 'interval', minutes=1)

def initialize_gspread() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  credentials = {
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
  return gspread.service_account_from_dict(credentials)  # Note: we could move this to settings to do this once.

class Model(ABCMeta):
  def __new__(cls, name, bases, attrs):
    new_class = super().__new__(cls, name, bases, attrs)
    new_class.objects = ModelObjects(new_class)
    return new_class
  
class ModelObjects:
  def __init__(self, cls):
      self.cls = cls
      self.sheet = settings.GSPREAD_CLIENT.open(cls.Meta.db_name)
      self.worksheet = self.sheet.worksheet(cls.Meta.db_table)

  def all(self) -> List[Dict[str, Any]]:
      all_records = self.worksheet.get_all_records()
      all_records = self.__set_type_attrs(all_records)
      return all_records
  
  def get(self, **kwargs) -> Dict[str, Any]:
    all_records = self.all()
    for record in all_records:
      if all(record.get(k) == v for k, v in kwargs.items()):
        return record
    return None
  
  def filter(self, **kwargs) -> List[Dict[str, Any]]:
    all_records = self.all()
    return [record for record in all_records if all(record.get(k) == v for k, v in kwargs.items())]
  
  def __set_type_attrs(self, queryset) -> List[Dict[str, Any]]:
    type_attrs = {attr: type for attr, type in vars(self.cls).items() if not attr.startswith("_") and callable(getattr(self.cls, attr)) and attr != "Meta"} 
    for record in queryset:
      for attr, type in type_attrs.items():
        if type == datetime:
          record[attr] = datetime.strptime(record[attr], "%Y-%m-%d")
        else:
          record[attr] = type(record[attr])  
    return queryset
