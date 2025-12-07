from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            declarative_base,
                            relationship
                            )
from sqlalchemy.sql.functions import current_timestamp
from typing import List

Base = declarative_base()


class Cities(Base):
    tablename = 'cities'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String, nullable=False, unique=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    restaurants: Mapped[List["Restaurants"]] = relationship(
        back_populates="city", cascade="all, delete-orphan")


class Restaurants(Base):
    tablename = 'restaurants'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id'),
                                         ondelete="CASCADE",
                                         nullable=False)

    city: Mapped["Cities"] = relationship(back_populates="restaurants")
    foods: Mapped[List["Foods"]] = relationship(
        back_populates="restaurant", cascade="all, delete-orphan")
    # city: Mapped["Parent"] = relationship(back_populates="children")


class Foods(Base):
    tablename = "foods"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    diets: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column(index=True)
    lang: Mapped[str] = mapped_column(index=True)
    menu_type: Mapped[str] = mapped_column()
    menu_type_id: Mapped[int] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=current_timestamp, nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey(
        'restaurants.id'), ondelete="CASCADE", nullable=False)

    restaurant: Mapped["Restaurants"] = relationship(back_populates="foods")
