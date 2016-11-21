import datetime
from mongoengine import *

class Stock(Document):
    ticker = StringField(required = True, max_length = 4)


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
    i = StringField(required = True, max_length = 8, unique_with = 'j')
    j = StringField(required = True, max_length = 8, unique_with = 'i')
    v = FloatField(required = True)

