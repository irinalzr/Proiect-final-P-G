from db_conn import get_db
from fastapi import Depends, FastAPI
from models import Country, CountryCreate, CountryResponse
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hey"}


@app.get("/countries/", response_model=list[CountryResponse])
def read_all_products(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return countries


@app.post("/countries/", response_model=CountryResponse)
def create_product(product: CountryCreate, db: Session = Depends(get_db)):
    db_country = Country(**product.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country
