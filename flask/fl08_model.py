from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Column, ForeignKey


# Setup


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define models


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User {self.id} {self.username} {self.email}>"

    def __str__(self):
        return f"{self.username}"


class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="person")

    def __init__(self, name):
        self.name = name


class Address(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))

    person: Mapped["Person"] = relationship("Person", back_populates="addresses")

    def __init__(self, email):
        self.email = email


tags_table = db.Table(
    "tags_table",
    Column("tag_id", Integer, ForeignKey("tag_table.id")),
    Column("page_id", Integer, ForeignKey("page_table.id")),
)


class Page(db.Model):
    __tablename__ = "page_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    tags: Mapped[list["Tag"]] = relationship(secondary=tags_table, back_populates="pages")

    def __init__(self, name):
        self.name = name


class Tag(db.Model):
    __tablename__ = "tag_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50))

    pages: Mapped[list["Page"]] = relationship(secondary=tags_table, back_populates="tags")

    def __init__(self, name):
        self.name = name


# CLI functions and helpers


def displayResult(num, res):
    print(f"\nQ{num}:\n{str(res)}\n{repr(res)}\n{type(res)}\n\n")


@app.cli.command("initdb")
def initdb_command():
    """Reinitializes the database"""
    db.drop_all()
    db.create_all()

    # Populate users
    db.session.add(User("admin", "admin@example.com"))
    db.session.add(User("peter", "peter@example.org"))
    db.session.add(User("guest", "guest@example.com"))

    # Populate 1-N example
    nick = Person("Nick")
    db.session.add(nick)
    nick.addresses.append(Address("nlf4@pitt.edu"))

    cs_addr = Address("nlf4@cs.pitt.edu")
    db.session.add(cs_addr)
    cs_addr.person = nick

    # Populate M-N example
    p1 = Page("p1")
    t1 = Tag("t1")
    t2 = Tag("t2")
    t3 = Tag("t3")

    db.session.add(p1)
    p1.tags.append(t1)
    p1.tags.append(t2)
    p1.tags.append(t3)

    p2 = Page("p2")
    t1.pages.append(p2)
    t2.pages.append(p2)
    t2.pages.append(Page("p3"))

    # Commit
    db.session.commit()
    print("Initialized the database.")


@app.cli.command("check")
def default():
    """Demonstrates model queries and relationships"""
    # Queries

    stmt = db.select(User).where(User.username == "peter")

    # Returns a User
    displayResult(
        1,
        db.session.execute(stmt).scalar()
    )

    # Returns an SQLAlchemy Row
    displayResult(
        2,
        db.session.execute(stmt).first()
    )

    # Returns a User
    displayResult(
        3,
        db.session.execute(stmt).first()[0],
    )

    # Returns a list of Rows
    displayResult(
        4,
        db.session.execute(stmt).all()
    )

    # Returns a Row
    displayResult(
        5,
        db.session.execute(stmt).all()[0]
    )

    # Returns None
    displayResult(
        6,
        db.session.execute(
            db.select(User).where(User.username == "missing")
        ).scalar(),
    )

    # Convert returned iterable to list of Users
    displayResult(
        7,
        list(db.session.execute(
            db.select(User).where(User.email.endswith("@example.com"))
        ).scalars())
    )

    # Ordered list
    displayResult(
        8,
        list(db.session.execute(
            db.select(User).order_by(User.username)
        ).scalars())
    )

    # Returns query to be run
    displayResult(
        9,
        stmt
    )

    # 1-N example
    print("Person:")
    per = db.session.execute(db.select(Person)).scalar()
    print(f"\tName: {per.name}")
    print("\tAddresses:")
    for a in per.addresses:
        print(f"\t\t {a.email}")

    print("Emails:")
    eml = db.session.execute(db.select(Address)).scalars()
    for e in eml:
        print(f"\taddr: {e.email};  owner: {e.person.name}")

    # M-N example
    print("\n\nPages:")
    pages = db.session.execute(db.select(Page)).scalars()
    for p in pages:
        print(f"\tname: {p.name}")
        for t in p.tags:
            print(f"\t\ttag: {t.name}")

    print("\n\nTags:")
    tags = db.session.execute(db.select(Tag)).scalars()
    for t in tags:
        print(f"\tname: {t.name}")
        for p in t.pages:
            print(f"\t\tpage: {p.name}")
