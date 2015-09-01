from app import app
from app.modles import Todo
from flask.ext.script import Manger

manger = Manger(app)

@manger.command
def save():
    todo = Todo(content = "study flask")
    todo.save()

if __name__ == '__main__':
    manger.run()
