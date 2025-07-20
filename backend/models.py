from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List
from sqlalchemy import Table, Enum, Numeric
from enum import Enum as PyEnum
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Gym(Base):
    __tablename__ = "gyms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(db.String(255), nullable=False)
    contact_number: Mapped[str] = mapped_column(db.String(20), nullable=True)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)


    subscriptions: Mapped[List["GymSubscription"]] = db.relationship("GymSubscription", back_populates="gym", cascade="all, delete-orphan")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=True)
    join_date: Mapped[date] = mapped_column(db.Date, default= date.today, nullable=False)
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)
    subscriptions: Mapped[List["GymSubscription"]] = db.relationship("GymSubscription", back_populates="member", cascade="all, delete-orphan")


class SubscriptionPlan(PyEnum):
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"

class GymSubscription(Base):
    __tablename__ = "gym_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    gym_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False)
    member_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    subscription_name: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan,name= "subscription_name") , nullable=False)
    start_date: Mapped[date] = mapped_column(db.Date, default= date.today, nullable=False)
    end_date: Mapped[date] = mapped_column(db.Date, nullable=True)

    gym = db.relationship("Gym", back_populates="subscriptions")
    member = db.relationship("Member", back_populates="subscriptions")

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    gym_subscription_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("gym_subscriptions.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column(db.Date, default=date.today, nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)  # e.g. "completed", "pending", "failed"
    method: Mapped[str] = mapped_column(db.String(50), nullable=True)   # e.g. "credit_card", "paypal"

    gym_subscription = db.relationship("GymSubscription", backref="payments")

