from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import (
    DECIMAL,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship


# ==========================================
# 1. IDENTIFIER
# ==========================================
class IdentifierBase(BaseModel):
    identifier_name: str
    description: Optional[str] = None
    identifier_type: Optional[str] = None


class IdentifierCreate(IdentifierBase):
    pass


class IdentifierResponse(IdentifierBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 2. COUNTRY
# ==========================================
class CountryBase(BaseModel):
    name: str
    iso_code: Optional[str] = None
    short_code: Optional[str] = None


class CountryCreate(CountryBase):
    pass


class CountryResponse(CountryBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. CONSUMER UNIT
# ==========================================
class ConsumerUnitBase(BaseModel):
    number_of_consumers: int
    country_name: str


class ConsumerUnitCreate(ConsumerUnitBase):
    pass


class ConsumerUnitResponse(ConsumerUnitBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 4. OWNERSHIP
# ==========================================
class OwnershipBase(BaseModel):
    identifier_name: str
    user_id_tnumber: str
    originator_first_name: Optional[str] = None
    originator_last_name: Optional[str] = None
    user_id_intranet: Optional[str] = None
    email: Optional[str] = None
    owner_first_name: Optional[str] = None
    owner_last_name: Optional[str] = None


class OwnershipCreate(OwnershipBase):
    pass


class OwnershipResponse(OwnershipBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 5. RELATIONSHIP
# ==========================================
class RelationshipBase(BaseModel):
    from_identifier_name: str
    to_identifier_name: str
    relationship_name: Optional[str] = None


class RelationshipCreate(RelationshipBase):
    pass


class RelationshipResponse(RelationshipBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 6. CHARACTERISTIC
# ==========================================
class CharacteristicBase(BaseModel):
    master_name: str
    name: str
    specifics: Optional[str] = None
    action_required: Optional[str] = None
    report_type: Optional[str] = None
    data_type: Optional[str] = None
    lower_routine_release_limit: Optional[Decimal] = None
    lower_limit: Optional[Decimal] = None
    lower_target: Optional[Decimal] = None
    target: Optional[Decimal] = None
    upper_target: Optional[Decimal] = None
    upper_limit: Optional[Decimal] = None
    upper_routine_release_limit: Optional[Decimal] = None
    test_frequency: Optional[int] = None
    precision: Optional[int] = None
    engineering_unit: Optional[str] = None


class CharacteristicCreate(CharacteristicBase):
    pass


class CharacteristicResponse(CharacteristicBase):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 7. IDENTIFIER CHARACTERISTIC
# ==========================================
class IdentifierCharacteristicBase(BaseModel):
    identifier_name: str
    master_name: str
    characteristic_name: str


class IdentifierCharacteristicCreate(IdentifierCharacteristicBase):
    pass


class IdentifierCharacteristicResponse(IdentifierCharacteristicBase):
    model_config = ConfigDict(from_attributes=True)


Base = declarative_base()


class Identifier(Base):
    __tablename__ = "Identifiers"

    identifier_name = Column(String(255), primary_key=True)
    description = Column(Text)
    identifier_type = Column(String(255))


class Country(Base):
    __tablename__ = "Countries"

    name = Column(String(255), primary_key=True)
    iso_code = Column(String(255))
    short_code = Column(String(255))

    consumer_units = relationship("ConsumerUnit", back_populates="country")


class ConsumerUnit(Base):
    __tablename__ = "ConsumerUnits"

    number_of_consumers = Column(Integer, primary_key=True)
    country_name = Column(
        String(255),
        ForeignKey("Countries.name", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )

    country = relationship("Country", back_populates="consumer_units")


class Ownership(Base):
    __tablename__ = "Ownership"

    identifier_name = Column(
        String(255),
        ForeignKey(
            "Identifiers.identifier_name", ondelete="CASCADE", onupdate="CASCADE"
        ),
        primary_key=True,
    )
    originator_first_name = Column(String(255))
    originator_last_name = Column(String(255))
    user_id_tnumber = Column(String(255), primary_key=True)
    user_id_intranet = Column(String(255))
    email = Column(String(255))
    owner_first_name = Column(String(255))
    owner_last_name = Column(String(255))


class Relationship(Base):
    __tablename__ = "Relationships"

    from_identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name", ondelete="CASCADE"),
        primary_key=True,
    )
    to_identifier_name = Column(
        String(255),
        ForeignKey("Identifiers.identifier_name", ondelete="CASCADE"),
        primary_key=True,
    )
    relationship_name = Column(String(255))


class Characteristic(Base):
    __tablename__ = "Characteristics"

    master_name = Column(String(255), primary_key=True)
    name = Column(String(255), primary_key=True)
    specifics = Column(String(255))
    action_required = Column(String(255))
    report_type = Column(String(255))
    data_type = Column(String(255))
    lower_routine_release_limit = Column(DECIMAL(10, 2))
    lower_limit = Column(DECIMAL(10, 2))
    lower_target = Column(DECIMAL(10, 2))
    target = Column(DECIMAL(10, 2))
    upper_target = Column(DECIMAL(10, 2))
    upper_limit = Column(DECIMAL(10, 2))
    upper_routine_release_limit = Column(DECIMAL(10, 2))
    test_frequency = Column(Integer)
    precision = Column(Integer)
    engineering_unit = Column(String(255))


class IdentifierCharacteristic(Base):
    __tablename__ = "IdentifierCharacteristics"

    identifier_name = Column(
        String(255),
        ForeignKey(
            "Identifiers.identifier_name", ondelete="CASCADE", onupdate="CASCADE"
        ),
        primary_key=True,
    )
    master_name = Column(String(255), primary_key=True)
    characteristic_name = Column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["master_name", "characteristic_name"],
            ["Characteristics.master_name", "Characteristics.name"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
