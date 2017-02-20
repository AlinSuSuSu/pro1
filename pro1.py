from flask import Flask
from flask import current_app
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask import session,redirect,url_for

class NameForm(Form):
    name = StringField("What's your name ?",validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY']='HARD TO GUESS WHAT I SET'#设置密钥
bootstrap = Bootstrap(app)
moment = Moment(app)




#路由是处理URL和函数之间关系的程序。
@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),current_time = datetime.utcnow())


'''
Flask 提供的render_template函数将Jinjia2模板引擎集成到了程序中。
'''
@app.route("/user/<name1>")
def user(name1):
    return render_template('user.html',name = name1)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404



if __name__ == '__main__':
    app.run(debug = True )
