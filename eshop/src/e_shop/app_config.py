'''
Created on Apr 13, 2015

@author: tristan
'''
from django.apps import AppConfig
from e_shop.session import init_session
import g
import uuid

class MyAppConfig(AppConfig):
    name =  'e_shop'
    def ready(self):
        AppConfig.ready(self)
        init_session()
        g.version = str(uuid.uuid4()).replace('-', '')