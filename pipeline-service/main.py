from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.customer import Customer
from services.ingestion import run_customer_ingestion

app = FastAPI()


@app.post('/api/ingest')
async def ingest_customers():
    status, rows_count = run_customer_ingestion()
    return {
        "status": status,
        "records_processed": rows_count,
    }


@app.get('/api/customers')
def get_customers(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=25),
    db: Session = Depends(get_db),
):
    total = db.query(Customer).count()
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit,
    }


@app.get('/api/customers/{customer_id}')
def get_customer_by_id(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id).first()
    if customer:
        return {"data": customer}
    raise HTTPException(status_code=404, detail='Customer not found')
