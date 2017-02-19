from flask import Flask

app = Flask(__name__)

#路由是处理URL和函数之间关系的程序。
@app.route('/')
def hello_world():
    return 'Hello missa!'


if __name__ == '__main__':
    app.run(debug = True )
