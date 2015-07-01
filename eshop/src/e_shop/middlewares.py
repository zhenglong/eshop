'''
Created on Apr 13, 2015

@author: tristan
'''
from e_shop.session import Session

class SessionManagerMiddleware(object):
    def process_request(self, request):
        Session(autocommit=True)
        
    def process_response(self, request, response):
        Session.remove()
        return response