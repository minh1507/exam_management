from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os
load_dotenv()
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship('Role', back_populates='accounts')

DATABASE_URL = f"mysql+mysqlconnector://{
    os.getenv("DB_USER")}:{
        os.getenv("DB_PASSWORD")}@{
            os.getenv("DB_HOST")}:{
                os.getenv("DB_PORT")}/{
                    os.getenv("DB_NAME")}?charset=utf8mb4&collation={
                        os.getenv("DB_COLLATION")}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
