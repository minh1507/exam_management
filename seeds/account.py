from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()
from src.model.account import Account
from sqlalchemy.exc import IntegrityError
from src.commons.hashing import HashingUltil

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

def account_seed():
    # Define the records you want to add or update
    records = [
        {"id": "1", "username": 'admin', "password": HashingUltil.hash("123456"), "role_id": "1"},
    ]

    for record in records:
        # Check if the record already exists
        existing_record = session.query(Account).filter_by(id=record['id']).first()
        
        if existing_record:
            # Update existing record
            for key, value in record.items():
                setattr(existing_record, key, value)
        else:
            # Create new record
            new_record = Account(**record)
            session.add(new_record)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error occurred while committing the session.")
