from sqlalchemy import TIMESTAMP, Column, Date, Numeric, String, Text
from sqlalchemy.sql import func

from database import Base


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'customer_dataset'}

    customer_id = Column(String(50), primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    account_balance = Column(Numeric(15, 2), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
