from flask import Flask
from flask import current_app

app = Flask(__name__)

#路由是处理URL和函数之间关系的程序。
@app.route('/')
def hello_world():
    return 'Hello ss!'

@app.route("/user/<name1>")
def user(name1):
    return 'hello,%s'% current_app.name

if __name__ == '__main__':
    app.run(debug = True )
