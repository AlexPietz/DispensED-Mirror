import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config_Disp(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'd\xb0w\x86\x07A\x1c\x8b>\x11\xb9\x01\x89\x85\x8b[Y}c#`e\x11n4?=\x98P\xfe\xb2`'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_CDN_FORCE_SSL = True
