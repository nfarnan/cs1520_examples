from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Column, ForeignKey


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(24))
    email: Mapped[str] = mapped_column(String(80))
    pw_hash: Mapped[str] = mapped_column(String(64))

    messages: Mapped[list["Message"]] = relationship(back_populates="author")

    follows: Mapped[list["User"]] = relationship(
        secondary="follows_table",
        primaryjoin="User.user_id==follows_table.c.follower_id",
        secondaryjoin="User.user_id==follows_table.c.followee_id",
        back_populates="followed_by",
    )
    followed_by: Mapped[list["User"]] = relationship(
        secondary="follows_table",
        secondaryjoin="User.user_id==follows_table.c.follower_id",
        primaryjoin="User.user_id==follows_table.c.followee_id",
        back_populates="follows",
    )

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return "<User {}>".format(self.username)


follows_table = db.Table(
    "follows_table",
    Column("follower_id", Integer, ForeignKey("user.user_id")),
    Column("followee_id", Integer, ForeignKey("user.user_id")),
)


class Message(db.Model):
    message_id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    text: Mapped[str]
    pub_date: Mapped[int]

    author: Mapped["User"] = relationship(back_populates="messages")

    def __init__(self, author_id, text, pub_date):
        self.author_id = author_id
        self.text = text
        self.pub_date = pub_date

    def __repr__(self):
        return "<Message {}".format(self.message_id)
