
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column, relationship

from core.config import init_db, dbAlch

init_db()

class User(dbAlch.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    firstname = Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    lastname = Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email = Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password = Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    country = Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    countrycode = Mapped[str] = mapped_column(String(6), unique=True, nullable=False)
    phone = Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
