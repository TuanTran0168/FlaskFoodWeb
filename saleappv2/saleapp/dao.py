from builtins import print
from random import random

from cryptography.fernet import Fernet
from twilio.rest import Client

from saleapp.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from flask_login import current_user
from sqlalchemy import func
from saleapp import db
import hashlib
from saleapp.security import caesar_encrypt, caesar_decrypt, MY_AES_KEY
from saleapp.security import giai_ma_AES, ma_hoa_AES
from saleapp.security import send_OTP


def load_categories():
    return Category.query.all()


def load_products(cate_id=None, kw=None):
    query = Product.query

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register(name, username, password,  phonenumber,  avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    # fernet = Fernet(MY_KEY)
    # phonenumber = str(phonenumber).encode()
    # phonenumber = fernet.encrypt(phonenumber)
    phonenumber = ma_hoa_AES(phonenumber, MY_AES_KEY)

    u = User(name=name, username=username.strip(), password=password,  phonenumber =  phonenumber, image=avatar)
    db.session.add(u)
    db.session.commit()


def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
             .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
             .group_by(Category.id).all()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
              .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))\
              .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Product.id).order_by(-Product.id).all()


def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


def save_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


if __name__ == '__main__':
    from saleapp import app
    with app.app_context():

        # str = "gAAAAABkDW_rMPN42xeXpXAC2DuoJrf4BVF88sScGGLb30wzv1rGIuwbP9p-zBFyqYJf6D8KNQccy7zG_6iB6mfhpjFCo_IGNw=="
        # fernet = Fernet(MY_KEY)
        # print(fernet.decrypt(str).decode())
        #
        # text = "gAAAAABkDXL1btg8ONK2FiitGIV2ZvLLKqo1NlwRNf7NPWWPu2_cbenMRphX9GtLlawvrflYtMnwwhSo3tywLch8ZAAA2bvfSw=="
        # print(giai_ma_AES(text, MY_KEY))

        str = "HELLO XIN CHÀO MỌI NGƯỜI, NGÀY MẤY MÌNH NỘP BÀI NÀY VẬY"

        str_ma_hoa = ma_hoa_AES(str, MY_AES_KEY)
        print(str_ma_hoa)

        print(giai_ma_AES(str_ma_hoa, MY_AES_KEY))

        account_sid = 'AC99204c3540a27bd83aede03e43b83312'
        auth_token = '6660059774e9c35882ef7e4fa354ec56'

        account_sid = 'AC99204c3540a27bd83aede03e43b83312'
        auth_token = 'b82932d6b2ff01b12fee7df26de98c2c'
        messaging_service_sid = 'MGcebeadd059e80d3835f92442700abaaa'
        phone_number = "+84345809638"
        phone_number = "+84359505026"
        message = "U là trời otp nè: "

        print("BUG")
        # send_OTP(account_sid=account_sid, auth_token=auth_token,messaging_service_sid= messaging_service_sid, phone_number=phone_number, message=message)

        print("BUG 1")

        #captcha
        key = "6Leih_gkAAAAACZQmAtE8i3C3hjKBC7NbN1Jy27d"
        sckey ="6Leih_gkAAAAAMN_3bNw8sBaC8lXtDSd-k_-VePg"

        sdt = "gAAAAABkFdTML8ZpL0-BDdKXshX83nmpLVusLL5cE_82UW3usSFvAyFws1laj09O8mD7QvbRW2LjtlKO-vsT18eyI8_bRi9wSg=="
        print(giai_ma_AES(sdt, MY_AES_KEY))



