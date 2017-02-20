from flask import Flask
from flask import current_app
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask import session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Integer,String,MetaData,ForeignKey
import os
basedir = os.path.abspath(os.path.dirname(__file__))




class NameForm(Form):
    name = StringField("What's your name ?",validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'mydata.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SECRET_KEY']='HARD TO GUESS WHAT I SET'#设置密钥
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

"""
engine = create_engine('sqllite:///D:/memory',echo= True)
metadata = MetaData()
users_table = Table('users',metadata,
                    Column('id',Integer,primary_key=True),
                    Column('name',String),
                    Column('password',String)
                    )

metadata.create_all()
ins = users_table.insert()
new_user = ins.values(name='admin',password='admin')
conn = engine.connect()
conn.execute(new_user)
"""
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name

    users = db.relationship('User', backref='role')
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

db.drop_all()
db.create_all()
admin_role = Role(name='Admin')
db.session.add(admin_role)
db.session.commit()
#路由是处理URL和函数之间关系的程序。
@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        '''old_name = session.get('name')

        if old_name is not None and old_name != form.name.data:

            flash('Looks like you have changed your name !')'''
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data=''

        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False),current_time = datetime.utcnow())


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
