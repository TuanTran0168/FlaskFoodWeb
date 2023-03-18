from flask import render_template, request, redirect, session, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.recaptcha import validators
from saleapp.security import send_OTP
from select import error

from saleapp import app, dao, admin, login, utils, account_sid, auth_token, messaging_service_sid, message
from flask_login import login_user, logout_user, login_required
from saleapp.decorators import annonymous_user
import cloudinary.uploader
from werkzeug.utils import redirect
import random


def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id, kw)

    return render_template('index.html', products=products)


def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

otp = 0
numPhoneVN = ""
def get_otp():
    if request.method.__eq__('POST'):
        numPhone = request.form['numPhone']
        numVN = "+84"
        global numPhoneVN
        numPhoneVN = numVN + numPhone[1: numPhone.__len__()]
        global otp;
        otp = random.randint(100000, 999999)
        send_OTP(account_sid=account_sid, auth_token=auth_token, messaging_service_sid=messaging_service_sid ,otp=otp,
                 message=message, phone_number=numPhoneVN)
        return redirect('/register')

    return render_template("confirmOTP.html")

def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        confirm_otp = request.form['confirm_otp']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            if confirm_otp.__eq__(otp):
                try:
                    dao.register(name=request.form['name'],
                                 username=request.form['username'],
                                 password=password,
                                 phonenumber=numPhoneVN,
                                 avatar=avatar)

                    return redirect('/login')
                    # return confirm_otp + otp
                except:
                    err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
            else:
                err_msg = "Mã OTP không chính xác!"
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def login_my_user():
    form = ContactForm()
    err_msg = ""
    if request.method.__eq__('POST'):
        if request.form.get('g-recaptcha-response'):
            username = request.form['username']
            password = request.form['password']

            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user=user)

                n = request.args.get("next")
                return redirect(n if n else '/')
            else:
                err_msg = "Sai tài khoản hoặc mật khẩu!"
        else:
            err_msg = "Vui lòng xác minh mình là con người!"

    return render_template('login.html', form = form, err_msg=err_msg)


def logout_my_user():
    logout_user()
    return redirect('/login')


def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "iPhone 13",
    #         "price": 13000,
    #         "quantity": 2
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "iPhone 14",
    #         "price": 13000,
    #         "quantity": 2
    #     }
    # }

    return render_template('cart.html')


def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    data = request.json
    id = str(data['id'])

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']

        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})


def comments(product_id):
    data = []
    for c in dao.load_comments(product_id=product_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.image
            }
        })

    return jsonify(data)


def add_comment(product_id):
    try:
        c = dao.save_comment(product_id=product_id, content=request.json['content'])
    except:
        return jsonify({'status': 500})

    return jsonify({
        'status': 204,
        'comment': {
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.image
            }
        }
    })

class ContactForm(FlaskForm):
    recaptcha = RecaptchaField(validators=[validators.Recaptcha(message='Invalid reCAPTCHA.')])

if __name__ == '__main__':
    from saleapp import app
    with app.app_context():
        print(otp)
        print()