import datetime
from mongoengine import *

class Stock(Document):
    ticker = StringField(required = True, max_length = 8)
    status_ts = StringField(required = True, max_length = 16)
    status_cov = StringField(required = True, max_length = 16)
    dps = IntField()


class Portfolio(Document):
    name = StringField(required = True, max_length = 120)
    stocks = ListField(ReferenceField(Stock))


class User(Document):
    name = StringField(required = True, unique = True, max_length = 64)
    email = EmailField(unique = True)
    password = StringField(required = True, default = True, min_length = 8)
    timestamp = DateTimeField(default = datetime.datetime.now())
    portfolios = ListField(ReferenceField(Portfolio))


class MatrixItem(Document):
    i = StringField(required = True, max_length = 8)
    j = StringField(required = True, max_length = 8)
    v = FloatField(required = True)
    matrix_name = StringField(max_length = 64, unique_with = ['i','j'])
