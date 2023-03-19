from builtins import print

from click import confirm
from flask import render_template, request, redirect, session, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.recaptcha import validators
from twilio.rest import Client

# from saleapp.security import send_OTP
from select import error

from saleapp import app, dao, admin, login, utils, ACCOUNT_SID, AUTH_TOKEN, SERVICE_SID
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


# Gán đại chứ đếch có sdt của Hiếu ở đây :)
# Với cái twilio nó die tiếp :)
otp = ""
confirm_otp = ""
numPhoneVN = ""


# def get_otp():
#     form = ContactForm()
#     err_msg = ""
#     if request.method.__eq__('POST'):
#         if request.form.get('g-recaptcha-response'):
#             numPhone = request.form['numPhone']
#             numVN = "+84"
#             global numPhoneVN
#             numPhoneVN = numVN + numPhone[1: numPhone.__len__()]
#
#             global otp;
#             otp = random.randint(100000, 999999)
#             try:
#                 send_OTP(account_sid=account_sid, auth_token=auth_token,
#                          messaging_service_sid=messaging_service_sid, otp=otp,
#                          message=message, phone_number=numPhoneVN)
#                 # if check_send.sid:
#                 return redirect('/register')
#                 # else:
#                 #     err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
#             except:
#                 err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
#         else:
#             err_msg = "Vui lòng xác minh mình là con người!"
#
#     return render_template("confirmOTP.html", form=form, err_msg=err_msg)
#
#
# def register():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         password = request.form['password']
#         confirm = request.form['confirm']
#         global confirm_otp;
#         confirm_otp = request.form['confirm_otp']
#         if password.__eq__(confirm):
#             avatar = ''
#             if request.files:
#                 res = cloudinary.uploader.upload(request.files['avatar'])
#                 avatar = res['secure_url']
#
#             if confirm_otp.__eq__(otp):
#                 try:
#                     dao.register(name=request.form['name'],
#                                  username=request.form['username'],
#                                  password=password,
#                                  phonenumber=numPhoneVN,
#                                  avatar=avatar)
#
#                     return redirect('/login')
#                     # return confirm_otp + otp
#                 except:
#                     err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
#             else:
#                 err_msg = "Mã OTP không chính xác!"
#         else:
#             err_msg = 'Mật khẩu KHÔNG khớp!'
#
#     return render_template('register.html', err_msg=err_msg)

def send_otp(phone_num):
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)
    verification = client.verify \
        .services(SERVICE_SID) \
        .verifications \
        .create(to=phone_num, channel='sms')
    return verification


def check_otp(phone_num, code):
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
        .services(SERVICE_SID) \
        .verification_checks \
        .create(to=phone_num, code=code)
    return verification_check


def get_otp():
    form = ContactForm()
    err_msg = ""
    if request.method.__eq__('POST'):
        if request.form.get('g-recaptcha-response'):
            global numPhoneVN
            numPhone = request.form['numPhone']
            numVN = "+84"
            numPhoneVN = numVN + numPhone[1: numPhone.__len__()]

            check = dao.check_phone_number_by_sdt(numPhoneVN)

            if check:
                try:
                    sotp = send_otp(numPhoneVN)
                    if sotp.status:
                        return redirect('/register')
                except:
                    err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'

            else:
                err_msg = "Số điện thoại này đã được đăng ký!"
        else:
            err_msg = "Vui lòng xác minh mình là con người!"

    return render_template("confirmOTP.html", form=form, err_msg=err_msg)


def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        # global confirm_otp
        confirm_otp = request.form['confirm_otp']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:
                check = check_otp(numPhoneVN, confirm_otp)
                if check.status.__eq__('approved'):
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
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
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

    return render_template('login.html', form=form, err_msg=err_msg)


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


numPhoneVN_change_pass = ""

def get_otp_password():
    form = ContactForm()
    err_msg = ""
    if request.method.__eq__('POST'):
        if request.form.get('g-recaptcha-response'):
            global numPhoneVN_change_pass
            numPhoneVN_change_pass = request.form['numPhone']
            numVN = "+84"
            numPhoneVN_change_pass = numVN + numPhoneVN_change_pass[1: numPhoneVN_change_pass.__len__()]

            check = dao.check_phone_number_by_sdt(numPhoneVN_change_pass)

            if check==False:
                try:
                    sotp = send_otp(numPhoneVN_change_pass)
                    if sotp.status:
                        # return numPhoneVN_change_pass + "   CC    " + numPhoneVN
                        return redirect('/change_password')
                except:
                    err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
            else:
                err_msg = "ALO!"
        else:
            err_msg = "Vui lòng xác minh mình là con người!"

    return render_template("confirmOTP_password.html", form=form, err_msg=err_msg)


def change_pass():
    form = ContactForm()
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        # global confirm_otp
        confirm_otp = request.form['confirm_otp']


        if password.__eq__(confirm):
            try:
                check = check_otp(numPhoneVN_change_pass, confirm_otp)
                if check.status.__eq__('approved'):
                    try:
                        dao.update_password(phonenumber=numPhoneVN_change_pass, new_password=password)

                        return redirect('/login')
                        # return confirm_otp + otp
                    except:
                        err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau! -9999'
                else:
                    err_msg = "Mã OTP không chính xác!"
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau! - 8888' + numPhoneVN_change_pass + " ALO "
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'


    return render_template("change_password.html", form=form, err_msg=err_msg)

class ContactForm(FlaskForm):
    recaptcha = RecaptchaField(validators=[validators.Recaptcha(message='Invalid reCAPTCHA.')])


if __name__ == '__main__':
    from saleapp import app

    with app.app_context():
        check = check_otp("+84388853371", 488596)
        print(check.status)
