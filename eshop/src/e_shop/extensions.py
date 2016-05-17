'''
Created on Apr 26, 2015

@author: tristan
'''
from django_jinja.builtins.extensions import StaticFilesExtension
import g

class StaticFileVersioningExtension(StaticFilesExtension):

    def __init__(self, environment):
        super(StaticFileVersioningExtension, self).__init__(environment)

    def _static(self, path):
        '''
            TODO
            absolute file path
            relative file path
            couldn't conclude file type from url
            query params have been in the url
        '''
        return super(StaticFileVersioningExtension, self)._static(path) + '?_=' + g.version
