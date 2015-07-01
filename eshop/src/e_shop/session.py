'''
Created on Apr 13, 2015

@author: tristan
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

Session = None

def init_session():
    engine = create_engine('mysql+mysqldb://root:root101@localhost/e_shop?charset=utf8', echo='debug')
    session_factory = sessionmaker(bind=engine)
    global Session
    Session = scoped_session(session_factory)