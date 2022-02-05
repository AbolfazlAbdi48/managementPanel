from .common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "metallurgy_db",
        'USER': "metallurgy_user",
        'PASSWORD': "123@456",
        'HOST': 'db',
        'PORT': 5432,
    }
}

ZARINPAL_GATEWAY_SETTINGS = {
    'MERCHANT': '8HACEEUH-AAWQ-CATE-9BGW-GWHBOZPPL6PO',
    'ZP_API_REQUEST': "https://banktest.ir/gateway/zarinpal/pg/rest/WebGate/PaymentRequest.json",
    'ZP_API_VERIFY': "https://banktest.ir/gateway/zarinpal/pg/rest/WebGate/PaymentVerification.json",
    'ZP_API_STARTPAY': "https://banktest.ir/gateway/zarinpal/pg/StartPay/{authority}",
    'description': 'شرکت توسعه وب و اپلیکیشن',
    'email': 'admin@local.host',
    'mobile': '09100000000',
    'CallbackURL': 'http://127.0.0.1/zarinpal-verify/'
}
