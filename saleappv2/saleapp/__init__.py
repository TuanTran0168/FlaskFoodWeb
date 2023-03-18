from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/foodappdb?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

cloudinary.config(cloud_name='dhwuwy0to', api_key='569153767496484', api_secret='ghXq0iY8RhWbqBcJaide7W-34RY')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)

site_key_V2 = "6Leih_gkAAAAACZQmAtE8i3C3hjKBC7NbN1Jy27d"
secret_key_V2 ="6Leih_gkAAAAAMN_3bNw8sBaC8lXtDSd-k_-VePg"

site_key_V3 = "6LequfgkAAAAANl1Q3A-bKNvwLoGJcrqpfcQH7R4"
secret_key_V3 ="6LequfgkAAAAABY-xRwg6c27dCD4dwZrGzodvw7x"

app.config['RECAPTCHA_PUBLIC_KEY'] = site_key_V2
app.config['RECAPTCHA_PRIVATE_KEY'] = secret_key_V2

account_sid = 'AC99204c3540a27bd83aede03e43b83312'
auth_token = '0aa01e87475a6428ebcd1b21f603619a'
messaging_service_sid = 'MGcebeadd059e80d3835f92442700abaaa'
message = "U là trời otp nè: "

@babel.localeselector
def load_locale():
    return 'vi'
