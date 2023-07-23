from flask import render_template, flash, session, request, Flask
from Installer import installer
import Installer.form as InstallerForm


from GeoIpApi.model import CountryInfo, IPV4, IPV6
from GeoIpCore.model import BaseTable
from GeoIpWeb.model import ContactUS



def test_db_info_ok(host="localhost", username="root", password="123654", namedb="OK", port="3306"):
    app = Flask(__name__)
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}:{port}"
    app.config['SQLALCHEMY_DATABASE_NAME'] = "namedb"
    db.init_app(app)


    BaseTable.metadata= db.metadata
    IPV6.metadata = db.metadata
    IPV4.metadata = db.metadata
    ContactUS.metadata = db.metadata
    CountryInfo.metadata = db.metadata

    print(db.metadata)
    print(db.Table)
    with app.app_context():
        print(db.create_all(), "oK")


test_db_info_ok(host="localhost", username="root", password="123654", port=3306, namedb="pk")


@installer.route("/", methods=["GET"])
def index():
    form = InstallerForm.DatabaseINIT()
    return render_template("installer/install-index.html", form=form)