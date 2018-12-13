from mongoengine import *
import random
import datetime

class Article(Document):
    title = StringField()
    text = StringField()
    link = StringField()
    bias = FloatField()
    date = DateTimeField()

    def __str__(self):
        return "Article: {}\nBias: {}\nText: {}\nLink: {}".format(self.title, self.bias, self.text, self.link)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()
        return super(Article, self).save(*args, **kwargs)

class Country(Document):
    name = StringField()
    articles = ListField(ReferenceField(Article))

    def __str__(self):
        return "Country: {}".format(self.name)
