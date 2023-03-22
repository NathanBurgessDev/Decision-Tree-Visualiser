"""
AUTHOR: Dominic Cripps
DATE CREATED: 19/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 21/03/2023

A singleton class that will hold settings set throughout the users session,
it will allow the user to store multiple models and keep all relevant information
in one class, avoiding circular dependencies.
"""
class UserSession(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UserSession, self).__new__(self)
        return self.instance

    modelInformation = {}
    selectedModel = None
    
    selectedTree = None
    selectedBoundary = None
