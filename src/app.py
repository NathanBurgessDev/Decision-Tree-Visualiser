from utils.PageLayout import PageLayout
from DashInstance import app

"""
AUTHOR: Dominic Cripps
DATE CREATED: 17/02/2023
PREVIOUS MAINTAINER: Dominic Cripps
DATE LAST MODIFIED: 18/02/2023

--THE MAIN FILE TO RUN--

Get a reference to the app instance from 'DashInstance' it will
then use the class 'PageLayout' to update the app layout and
run it.
"""

if __name__ == "__main__":
    pageLayout = PageLayout("Results visualisation", app)
    pageLayout.runServer(True)
