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

MY_AES_KEY = b'ykWaetYMhda53pQkaSOjsDHLzousmpH0SUUH6ul-TJM='

SITE_KEY_V2 = "6Leih_gkAAAAACZQmAtE8i3C3hjKBC7NbN1Jy27d"
SECRET_KEY_V2 ="6Leih_gkAAAAAMN_3bNw8sBaC8lXtDSd-k_-VePg"

SITE_KEY_V3 = "6LequfgkAAAAANl1Q3A-bKNvwLoGJcrqpfcQH7R4"
SECRET_KEY_V3 ="6LequfgkAAAAABY-xRwg6c27dCD4dwZrGzodvw7x"

app.config['RECAPTCHA_PUBLIC_KEY'] = SITE_KEY_V2
app.config['RECAPTCHA_PRIVATE_KEY'] = SECRET_KEY_V2

# HIẾU
ACCOUNT_SID = 'AC99204c3540a27bd83aede03e43b83312'
AUTH_TOKEN = '6bc48bbceb5f69c56d77af1bd1e4b8f7'
SERVICE_SID = 'VAe815928dddcd3ab7340649abcc495092'

# THÁI
ACCOUNT_SID = 'ACf8ff9e78fefda1261dd98b54970530c5'
AUTH_TOKEN = 'e5076e5c6f314e19dc56442326dbf69b'
SERVICE_SID = 'VAab73f1b83ab67aa2999c05582b3d22b5'

# TUẤN
# ACCOUNT_SID = 'ACb04b4c9fbcb0ca833a22416d555297ff'
# AUTH_TOKEN = 'a39e20e969810aec428fd17e085a8303'
# SERVICE_SID = 'VA0b119692923771c078df14bbecf6100c'

@babel.localeselector
def load_locale():
    return 'vi'