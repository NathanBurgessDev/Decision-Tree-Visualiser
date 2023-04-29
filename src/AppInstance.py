"""
AUTHOR: Ethan Temple-Bets
DATE CREATED: 23/03/2023
PREVIOUS MAINTAINER: Ethan Temple-Betts
DATE LAST MODIFIED: 23/03/2023

A singleton class that will hold the dash.Dash app instance
"""
class AppInstance(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(AppInstance, self).__new__(self)
        return self.instance

    app = None