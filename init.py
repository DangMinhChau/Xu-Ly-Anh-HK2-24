from views.appUI import App
import  config
from database import  db
if __name__ == '__main__':
    db.create_tables()
    app = App()
    app.mainloop()