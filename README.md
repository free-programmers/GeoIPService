# GeoIP-API

### api service for converting IP address to geo Location ...

### images

<img src="./doc/Images/index.png">
<img src="./doc/Images/public-ip.png">
<img src="./doc/Images/ip-2-location.png">

### Tech stack:

    Python3
    Flask 3.x
        Flask-wtf
        Flask-sqlalchemy
        Flask-migrate
        Flask-session
        Flask-babel
        Flask-mail
        Flask-caching
        Flask-limiter
        Flask-captcha2
        Flask-shell-ipython
    Redis
    Mysql
    Boostrap 5.3x
    Html
    Css
    Js
    highlight js
    Jquery


## how to run :

### 0.0 create a virtual env

    python -m venv venv

### 0.1 activate virtual env

    linux-mac :
            source ./venv/bin/active
    windows:
            ./venv/Scripts/activate

### 0.2 install dependency:

    pip install -r requirements.txt

### 0.3 complete config.ini file

    mv config.sample.ini config.ini
    change data in config.ini file (like database name, ...)

### Migrate to db

before running the below commands connect to you database and create a database (don't forget to put database name in
config.ini file)

    flask db init
    flask db migrate 
    flask db upgrade

    or just run MakeMigrate bash script (sudo chmod +x ./MakeMigrate then just run ./MakeMigrate)

or go create database your self via flask interactive shell

    flask shell
    from GeoIpCore.extensions import db
    
    db.create_all() # database creation command
    exit() # exit from ipython

### run App

    python app.py
    or
    flask run [--debug(for debug) --reload(reload template) --port 8080(for port)]
        [...] is optional

---

### at this point web app is up and running

but there is no data in database so let add some data to database

## warning : before running any of below script you should first fill up .env file and also migrate changes to db !

### 0.0 for adding automatically data

        cd ./GeoIpUpdater
        python fetchAndInsertdata.py 
                
        - this script automatically fetch a dataset from github
            and then update database with new data

### 0.1 just insert data

#### if you have data your self just run below script

        cd ./GeoIpUpdater
        python InsertDataByFile.py

        - this script insert data to database base on an input file ( file is required )

## Deploy to Server:

### This Web App configure for Deploy to <a href='https://liara.ir'>liara.ir</a> - if you want to deploy to other Pass Service providers make sure to change configuration base of service provider that you use.

#### For See How Deploy To liara.ir see <a href='./doc/Deploy/liara.ir'>Here</a>

