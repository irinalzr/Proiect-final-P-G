from db_conn import get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Country, CountryCreate, CountryResponse
from models import ConsumerUnit, ConsumerUnitCreate, ConsumerUnitResponse
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
def create_country(product: CountryCreate, db: Session = Depends(get_db)):
    db_country = Country(**product.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@app.put("/countries/{name}", response_model=CountryResponse)
def update_country(name: str, country: CountryCreate, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(Country.name == name).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    for key, value in country.model_dump().items():
        setattr(db_country, key, value)

    db.commit()
    db.refresh(db_country)
    return db_country

@app.delete("/countries/{name}")
def delete_country(name: str, db: Session = Depends(get_db)):
    db_country = db.query(Country).filter(Country.name == name).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    
    db.delete(db_country)
    db.commit()
    return {"detail": "Country deleted"}


@app.get("/ConsumerUnits/", response_model=list[ConsumerUnitResponse])
def read_all_products(db: Session = Depends(get_db)):
    countries = db.query(ConsumerUnit).all()
    return countries

@app.post("/ConsumerUnits/", response_model=ConsumerUnitResponse)
def create_consumer_unit(consumer_unit: ConsumerUnitCreate, db: Session = Depends(get_db)):
    db_consumer_unit = ConsumerUnit(**consumer_unit.model_dump())
    db.add(db_consumer_unit)
    db.commit()
    db.refresh(db_consumer_unit)
    return db_consumer_unit

@app.put("/ConsumerUnits/{name}", response_model=ConsumerUnitResponse)
def update_consumer_unit(name: str, consumer_unit: ConsumerUnitCreate, db: Session = Depends(get_db)):
    db_consumer_unit = db.query(ConsumerUnit).filter(ConsumerUnit.name == name).first()
    if db_consumer_unit is None:
        raise HTTPException(status_code=404, detail="Consumer unit not found")

    for key, value in consumer_unit.model_dump().items():
        setattr(db_consumer_unit, key, value)

    db.commit()
    db.refresh(db_consumer_unit)
    return db_consumer_unit

@app.delete("/ConsumerUnits/{name}")
def delete_consumer_unit(name: str, db: Session = Depends(get_db)):
    db_consumer_unit = db.query(ConsumerUnit).filter(ConsumerUnit.name == name).first()
    if db_consumer_unit is None:
        raise HTTPException(status_code=404, detail="Consumer unit not found")
    
    db.delete(db_consumer_unit)
    db.commit()
    return {"detail": "Consumer unit deleted"}