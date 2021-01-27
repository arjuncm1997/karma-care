from karma import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80),default='NULL')
    address = db.Column(db.String(80),default='NULL')
    status=db.Column(db.String(80),default='NULL')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Login.query.get(user_id)

    def __repr__(self):
        return f"Login('{self.username}', '{self.password}','{self.usertype}','{self.email}', '{self.image_file}')"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)




class Products(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    aqowner = db.Column(db.String(80))
    name = db.Column(db.String(80))
    brand = db.Column(db.String(80))
    price = db.Column(db.String(80))
    image = db.Column(db.String(20), default='default.jpg')

class Aquacart(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    aqowner = db.Column(db.String(80))
    name = db.Column(db.String(80))
    brand = db.Column(db.String(80))
    price = db.Column(db.String(80))
    image = db.Column(db.String(20), default='default.jpg')
    status = db.Column(db.String(80))
    payment = db.Column(db.String(80))
    owner = db.Column(db.String(80))

class Aquabuyproduct(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    aqowner = db.Column(db.String(80))
    name = db.Column(db.String(80))
    brand = db.Column(db.String(80))
    price = db.Column(db.String(80))
    image = db.Column(db.String(20), default='default.jpg')
    status = db.Column(db.String(80))
    payment = db.Column(db.String(80))
    bowner = db.Column(db.String(80))
    staff = db.Column(db.String(80),default='no')
    qnty = db.Column(db.String(80))
    delname = db.Column(db.String(80))
    delmobile = db.Column(db.String(80))
    deladdress = db.Column(db.String(80))
    delivery = db.Column(db.String(80))
    deliverystatus = db.Column(db.String(80))
    staffid = db.Column(db.String(80))
    staffname = db.Column(db.String(80))

class Aquacredit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    aqowner = db.Column(db.String(200))
    buyid = db.Column(db.String)
    name = db.Column(db.String(200))
    card = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    expdate = db.Column(db.String(200))


class Classvideo(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(80))
    desc = db.Column(db.String(80))
    video = db.Column(db.String(200))


class Gallery(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')