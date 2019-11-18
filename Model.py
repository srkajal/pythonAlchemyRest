from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable = False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable =False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, comment, category_id):
        self.comment = comment
        self.category_id = category_id

    def __prep__(self, comment, category):
        return "comment: " + comment.comment + "category:" +category.name  

class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class CategorySchema(ma.Schema):
    name = fields.String(required=True)
    id = fields.Integer()

class CommentSchema(ma.Schema):
    id = fields.Integer()
    comment = fields.String(required=True)
    creation_date = fields.DateTime()
    category_id = fields.Integer()