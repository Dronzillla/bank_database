from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Query


# Create engine
db_url = "sqlite:///data.db"
engine = create_engine(db_url)

# Bind session to our engine and get session object
Session = sessionmaker(bind=engine)
session = Session()

# Create base for creating class objects
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    # Inherit id for each class
    id = Column(Integer, primary_key=True)


class Person(BaseModel):
    __tablename__ = "person"
    name = Column(String)
    surname = Column(String)
    personal_code = Column(String, unique=True)
    phone = Column(String)
    # Specify reverse relationship for a person
    accounts = relationship("Account", back_populates="person")

    def __str__(self) -> None:
        return f"Person - id: {self.id}, name: {self.name}, surname: {self.surname}, personal_code: {self.personal_code}, phone: {self.phone}"


class Bank(BaseModel):
    __tablename__ = "bank"
    name = Column(String)
    address = Column(String)
    code = Column(String, unique=True)
    swift = Column(String)
    # Specify reverse relationship for bank account
    accounts = relationship("Account", back_populates="bank")

    def __str__(self) -> None:
        return f"Bank - id: {self.id}, name: {self.name}, address: {self.address}, code: {self.code}, swift: {self.swift}"


class Account(BaseModel):
    __tablename__ = "account"
    balance = Column(Float)
    # Create relationship with bank
    bank_id = Column(Integer, ForeignKey("bank.id"))
    bank = relationship("Bank", back_populates="accounts")
    # Create relationship with person
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person", back_populates="accounts")

    def __str__(self) -> None:
        return f"Account - id: {self.id}, balance: {self.balance}, bank_id: {self.bank_id}, person_id: {self.person_id}"


Base.metadata.create_all(engine)
