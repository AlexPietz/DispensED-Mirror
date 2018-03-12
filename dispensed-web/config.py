import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config_Disp(object):
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  b'd\xb0w\x86\x07A\x1c\x8b>\x11\xb9\x01\x89\x85\x8b[Y}c#`e'
                  b'\x11n4?=\x98P\xfe\xb2`')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_CDN_FORCE_SSL = True

# Mail server settings
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
# Default mail sender
    MAIL_DEFAULT_SENDER = 'team@dispensed.ed'
# Default mail recipient
    MAIL_DEFAULT_RECIPIENT = 'stefi.genkova@gmail.com'

    if (os.environ.get('DEMO')):
        # Mail server settings
        MAIL_SERVER = 'localhost'
        MAIL_PORT = 2525
        MAIL_USE_TLS = False
        MAIL_USE_SSL = False
        MAIL_USERNAME = None
        MAIL_PASSWORD = None
        # Default mail sender
        MAIL_DEFAULT_SENDER = 'team@dispens.ed'
        # Default mail recipient
        MAIL_DEFAULT_RECIPIENT = 'pietz@tardis.ed.ac.uk'
