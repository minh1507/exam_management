from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    order = Column(Integer, nullable=False)


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
