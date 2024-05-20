from views.appUI import App
from utils import db

if __name__ == '__main__':
    db.create_tables()
    app = App()
    app.mainloop()