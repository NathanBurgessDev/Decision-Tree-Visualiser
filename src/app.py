from utils.PageLayout import PageLayout
from DashMain import app

if __name__ == "__main__":
    pageLayout = PageLayout("Results visualisation", app)
    pageLayout.runServer(True)
