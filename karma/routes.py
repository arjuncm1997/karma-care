from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from karma import app,db,bcrypt,mail
from karma.models import *
from karma.forms import *
from random import randint
import os
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from flask_mail import Message
import string
import random       
from random import randint    

@app.route('/')
def  index():
    pro = Products.query.all()
    return render_template("index.html",pro = pro)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/playout')
def playout():
    return render_template("playout.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data, usertype= 'company',status='approve').first()
        user1 = Login.query.filter_by(email=form.email.data, usertype= 'user').first()
        user2 = Login.query.filter_by(email=form.email.data, usertype= 'admin').first()
        user3 = Login.query.filter_by(email=form.email.data, usertype= 'staff').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/cindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user3 and bcrypt.check_password_hash(user3.password, form.password.data):
            login_user(user3, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/sindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='public')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    return render_template("contact.html")

@app.route('/ucontact',methods=['GET', 'POST'])
def ucontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='user')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    return render_template("ucontact.html")

@app.route('/ccontact',methods=['GET', 'POST'])
def ccontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='company')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/cindex')

        except:
            return 'not add'  
    return render_template("ccontact.html")

@app.route('/scontact',methods=['GET', 'POST'])
def scontact():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        phone= request.form['phone']
        subject= request.form['subject']
        message= request.form['message']
        print(message)
        new1 = Feedback(name=name,email=email,phone=phone,subject=subject,message=message,usertype='staff')
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add'  
    return render_template("scontact.html")


@app.route('/registeruser',methods=['GET','POST'])
def registeruser():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! ', 'success')
        return redirect('/')
    return render_template("registeruser.html",form=form)


@app.route('/registercompany',methods=['GET','POST'])
def registercompany():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'company' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! Please wait for Approval ', 'success')
        return redirect('/login')
    return render_template("registercompany.html",form=form)



@app.route('/uindex')
def uindex():
    pro = Products.query.all()
    return render_template("uindex.html",pro=pro)

@app.route('/sindex')
def sindex():
    return render_template("sindex.html")



@app.route('/cindex')
def cindex():
    return render_template("cindex.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")





def sendemail(email,password):
    msg = Message(' Aqua Botanium Registeration',
                  recipients=[email])
    msg.body = f'''  Your Password is, {password}  '''
    mail.send(msg)




@app.route('/astaffadd',methods=['GET','POST'])
def astaffadd():
    form=RegistrationguideForm()
    if form.validate_on_submit():
        def randomString(stringLength=5):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        password =randomString()
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new = Login(username= form.username.data, email=form.email.data, password=hashed_password,phone = form.phone.data,usertype= 'staff' )
        db.session.add(new)
        db.session.commit()
        sendemail(email,password)
        flash('Your account has been created! ', 'success')
        return redirect('/admin')
    return render_template("astaffadd.html",form=form)

@app.route('/astaffview')
def astaffview():
    staff = Login.query.filter_by(usertype='staff').all()
    return render_template("astaffview.html",staff=staff)

@app.route('/acompanyapprove')
def acompanyapprove():
    com = Login.query.filter_by(usertype='company',status='NULL').all()
    return render_template("acompanyapprove.html",com=com)

@app.route('/acom')
def acom():
    com = Login.query.filter_by(usertype='company',status='approve').all()
    return render_template("acom.html",com=com)

@app.route('/acomapprove/<int:id>')
def acomapprove(id):
    com =Login.query.get_or_404(id)
    com.status = 'approve'
    db.session.commit()
    return redirect('/admin')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn





@app.route('/uproducts')
def uproducts():
    return render_template("uproducts.html")


@app.route('/ucartview')
def ucartview():
    aqcart = Aquacart.query.filter_by(owner=current_user.id).all()
    return render_template("ucartview.html", aqcart=aqcart)


@app.route('/uaqadd/<int:id>',methods=['GET','POST'])
def uaqadd(id):
    cart = Aquacart.query.get_or_404(id)
    if request.method=='POST':
        no= request.form['no']
        print(no)
        price = int(cart.price)*int(no)
        new1 = Aquabuyproduct(aqowner=cart.aqowner,name=cart.name,brand=cart.brand,price=price,image=cart.image,qnty=no,bowner=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            return redirect('/uaqcartbuy/'+str(new1.id))

        except:
            return 'not add'  


@app.route('/uaqcartadd/<int:id>')
def uaqcartadd(id):
    cart = Products.query.get_or_404(id)
    new = Aquacart(aqowner=cart.aqowner,name = cart.name,brand= cart.brand,price=cart.price,image=cart.image,owner=current_user.id)
    db.session.add(new)
    db.session.commit()
    return redirect('/uindex')


@app.route('/uaqcartremove/<int:id>')
def uaqcartremove(id):
    delete = Aquacart.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/ucartview')
    except:
        return 'can not delete'


@app.route('/uaqcartbuy/<int:id>',methods=['GET','POST'])
def uaqcartbuy(id):
    buy = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        mobile= request.form['mobile']
        address= request.form['address']
        buy.delname=name
        buy.delmobile=mobile
        buy.deladdress = address
        db.session.commit()
        return redirect('/uaqpayment/'+str(buy.id))
    return render_template("uaqcartbuy.html",buy=buy)

@app.route('/uaqpayment/<int:id>')
def uaqpayment(id):
    buy = Aquabuyproduct.query.get_or_404(id)
    return render_template("uaqpayment.html",buy=buy)



@app.route('/aqcredit/<int:id>',methods=['GET','POST'])
def aqcredit(id):
    buy1 = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        name= request.form['name']
        number= request.form['number']
        cvv= request.form['cvv']
        date= request.form['date']
        buy1.status = 'complete'
        buy1.payment = 'creditcard'
        new1 = Aquacredit(aqowner=buy1.aqowner,name=name,card=number,cvv=cvv,expdate=date,buyid=current_user.id)
        try:
            db.session.add(new1)
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("uaqpayment.html")


@app.route('/aqcod/<int:id>',methods=['GET','POST'])
def aqcod(id):
    buy2 = Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.status = 'complete'
        buy2.payment = 'Cod'
        try:
            db.session.commit()
            sendmail()
            return redirect('/sucess')

        except:
            return 'not add'  
    return render_template("uaqpayment.html")


@app.route('/sucess')
def sucess():
    return render_template("sucess.html")



def sendmail():
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f''' your transaction completed successfullyy '''
    mail.send(msg)


@app.route('/ubuyproduct')
def ubuyproduct():
    pdt = Aquabuyproduct.query.filter_by(bowner=current_user.id).all()
    return render_template("ubuyproduct.html",pdt=pdt)

@app.route('/abuyproduct')
def abuyproduct():
    buy = Buyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    return render_template("abuyproduct.html",buy=buy,user=user)

@app.route('/staffadd/<int:id>',methods=['GET','POST'])
def staffadd(id):
    buy = Buyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    buy2=Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.staff = 'add'
        buy2.staffid = request.form['staff']
        staf = Login.query.get_or_404(buy2.staffid)
        buy2.staffname = staf.username
        try:
            db.session.commit()
            return redirect('/admin')

        except:
            return 'not add' 
    return render_template("abuyproduct.html",buy=buy,user=user)

@app.route('/aboughtproduct')
def aboughtproduct():
    buy = Buyproduct.query.filter_by(status='complete',staff='add').all()
    return render_template("aboughtproduct.html",buy=buy)


@app.route('/saqpendingpdts')
def saqpendingpdts():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    return render_template("saqpendingpdts.html",buy=buy)

@app.route('/sdel/<int:id>',methods=['GET','POST'])
def sdel(id):
    buy = Buyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    buy2=Buyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.delivery = request.form['del']
        try:
            db.session.commit()
            return redirect('/sindex')

        except:
            return 'not add' 
    return render_template("spendingpdts.html",buy=buy)

@app.route('/saqdel/<int:id>',methods=['GET','POST'])
def saqdel(id):
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',staffid=current_user.id).all()
    buy2=Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.delivery = request.form['del']
        try:
            db.session.commit()
            return redirect('/saqpendingpdts')

        except:
            return 'not add' 
    return render_template("saqpendingpdts.html",buy=buy)


@app.route('/cproductadd',methods=['POST','GET'])
def cproductadd():
    form=Product()
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            view = pic
        gallery = Products(aqowner= current_user.id,name=form.name.data,brand=form.brand.data,price=form.price.data,image=view )
       
        db.session.add(gallery)
        db.session.commit()
        return redirect('/cindex')
            
    return render_template('cproductadd.html',form=form)

@app.route('/cproductview')
def cproductview():
    pdt = Products.query.filter_by(aqowner=current_user.id).all()
    return render_template("cproductview.html",pdt=pdt)

@app.route('/cproductupdate/<int:id>', methods=['GET', 'POST'])
def cproductupdate(id):
    material = Products.query.get_or_404(id)
    form = Product()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            material.image = picture_file
        material.name = form.name.data
        material.brand = form.brand.data
        material.price = form.price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/cproductview')
    elif request.method == 'GET':
        form.name.data = material.name
        form.brand.data = material.brand
        form.price.data = material.price
    image_file = url_for('static', filename='pics/' + material.image)
    return render_template('cproductupdate.html',form=form, material=material)

@app.route('/cpdtremove/<int:id>')
def cpdtremove(id):
    delete = Products.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/cproductview')
    except:
        return 'can not delete'

@app.route('/aaqproductview')
def aaqproductview():
    pdt = Products.query.all()
    return render_template("aaqproductview.html",pdt=pdt)



@app.route('/aaqbuyproduct')
def aaqbuyproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    return render_template("aaqbuyproduct.html",buy=buy,user=user)

@app.route('/staffaddaq/<int:id>',methods=['GET','POST'])
def staffaddaq(id):
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='no').all()
    user = Login.query.filter_by(usertype='staff').all()
    buy2=Aquabuyproduct.query.get_or_404(id)
    if request.method=='POST':
        buy2.staff = 'add'
        buy2.staffid = request.form['staff']
        staf = Login.query.get_or_404(buy2.staffid)
        buy2.staffname = staf.username
        try:
            db.session.commit()
            return redirect('/admin')

        except:
            return 'not add' 
    return render_template("aaqbuyproduct.html",buy=buy,user=user)

@app.route('/aaqboughtproduct')
def aaqboughtproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add').all()
    return render_template("aaqboughtproduct.html",buy=buy)

@app.route('/cboughtproduct')
def cboughtproduct():
    buy = Aquabuyproduct.query.filter_by(status='complete',staff='add',aqowner = current_user.id).all()
    return render_template("cboughtproduct.html",buy=buy)


@app.route('/apfeed')
def apfeed():
    feedback1=Feedback.query.filter_by(usertype='public').all()
    return render_template("apfeed.html",feedback=feedback1)

@app.route('/asfeed')
def asfeed():
    feedback1=Feedback.query.filter_by(usertype='staff').all()
    return render_template("asfeed.html",feedback=feedback1)

@app.route('/aufeed')
def aufeed():
    feedback1=Feedback.query.filter_by(usertype='user').all()
    return render_template("aufeed.html",feedback=feedback1)

@app.route('/aaqfeed')
def aaqfeed():
    feedback1=Feedback.query.filter_by(usertype='company').all()
    return render_template("aaqfeed.html",feedback=feedback1)






@app.route('/uprofile/<int:id>',methods=['GET','POST'])
def uprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/uindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("uprofile.html",form=form)

@app.route('/sprofile/<int:id>',methods=['GET','POST'])
def sprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/sindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("sprofile.html",form=form)

@app.route('/cprofile/<int:id>',methods=['GET','POST'])
def cprofile(id):
    form = Profile()
    login = Login.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            login.image_file = picture_file
        login.username = form.username.data
        login.address = form.address.data
        login.phone = form.phone.data
        login.email = form.email.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/cindex')
    elif request.method == 'GET':
        form.username.data = login.username
        form.address.data = login.address
        form.phone.data = login.phone
        form.email.data = login.email
        form.pic.data = login.image_file
    image_file = url_for('static', filename='pics/' + login.image_file)
    return render_template("cprofile.html",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/login')
    return render_template('resetrequest.html', title='Reset Password', form=form)



@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = Login.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)
