import os
from os.path import abspath, dirname

from flask import Flask, render_template, redirect, url_for

#utils import
from .utils.dbmsManager import *
from .utils.firestore import getProviderName, getParkingsList, insertParking, deleteParking, updateParking

#session management
from flask_login import UserMixin
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, current_user

#app init
app = Flask(__name__)
STATIC_ROOT='../static'
app.config["DEBUG"] = True
app.config['SECRET_KEY']='asdf.1234_@q'

#login manager config
login_manager=LoginManager()
login_manager.init_app(app)

#User class used by flask login
class User(UserMixin):
    def __init__(self, id, email, password, region, province):
        self.id=id
        self.email=email
        self.password=password
        self.region=region
        self.province=province

#get User object by user id
@login_manager.user_loader
def load_user(user_id):
    conn=engine.connect()
    rs=conn.execute(select([providers]).where(providers.c.id==user_id))
    user=rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.password, user.region, user.province)

#get user by email
def user_by_email(email):
    conn=engine.connect()
    rs=conn.execute(select([providers]).where(providers.c.email==email))
    user=rs.fetchone()
    print(user)
    conn.close()
    return load_user(user.id)

#routes
@app.route('/')
@login_required
def home():
    print(getParkingsList(current_user.region, current_user.province))
    return render_template('home.html', navi="home", region=current_user.region, province=current_user.province, provider_name=getProviderName(current_user.region, current_user.province), parkings=getParkingsList(current_user.region, current_user.province))

@app.route('/add_parking', methods=['GET', 'POST'])
@login_required
def add_parking():
    if request.method=='POST':
        parking_id=insertParking(current_user.region, current_user.province, request.form['parking_name'], request.form['latitude'], request.form['longitude'], request.form['capacity'], request.form['price_per_hour'], request.form['type'], ('ElectricVehicleChargingStation' in request.form), ('GuardedByCameras' in request.form), ('GuardedByHuman' in request.form))
        return redirect(url_for('manage_parking', parking_id=parking_id))
    else:
        return render_template('add_parking.html', navi="add_parking", provider_name=getProviderName(current_user.region, current_user.province), parkings=getParkingsList(current_user.region, current_user.province))

@app.route('/manage_parking/<parking_id>', methods=['GET', 'POST'])
@login_required
def manage_parking(parking_id):
    if request.method=='POST':
        updateParking(current_user.region, current_user.province, parking_id, request.form['parking_name'], request.form['latitude'], request.form['longitude'], request.form['capacity'], request.form['price_per_hour'], request.form['type'], ('ElectricVehicleChargingStation' in request.form), ('GuardedByCameras' in request.form), ('GuardedByHuman' in request.form))
        return redirect(url_for('manage_parking', parking_id=parking_id))
    else:
        return render_template('parking.html', navi="parking", provider_name=getProviderName(current_user.region, current_user.province), region=current_user.region, province=current_user.province, parkings=getParkingsList(current_user.region, current_user.province), parking_id=parking_id)

@app.route('/delete_parking/<parking_id>')
@login_required
def delete_parking(parking_id):
    deleteParking(current_user.region, current_user.province, parking_id)
    return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        conn=engine.connect()

        #check user's email
        q=select([providers]).where(providers.c.email == request.form['email'])
        rs=conn.execute(q)

        #check query result safeness
        if rs.rowcount==0:
            return render_template('login.html',credenziali_errate="email")

        stored_password=rs.fetchone()['password']
        conn.close()

        #password hash check
        if(hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()==stored_password):
            user=user_by_email(request.form['email'])

            #flask-login, logged
            login_user(user)

            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#redirect unauthenticated user to login
@app.login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')
