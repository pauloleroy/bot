
from bot import InstaBot
from gui import App
from dbclass import DBConnection
from queriesfile import MyQueries

CHROME_DRIVER_PATH = "C:\\Development\\chromedriver.exe"
bot = InstaBot(CHROME_DRIVER_PATH)
queries = MyQueries()
database = DBConnection(queries)
app = App(bot, database)
app.mainloop()