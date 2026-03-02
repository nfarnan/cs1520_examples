from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Text


class Base(DeclarativeBase):
    pass


# note this should only be created once per project
# to define models in multiple files, put this in one file, and
# import db into each model, as we import it in flaskr.py
db = SQLAlchemy(model_class=Base)


class Entry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    text: Mapped[str]

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return "<Entry {}>".format(self.id)
