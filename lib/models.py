from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'
    
    # Deliverable: Returns a collection of devs who received freebies from this company
    @property
    def devs(self):
        return {freebie.dev for freebie in self.freebies}

    # Deliverable: Create a new freebie for a dev
    def give_freebie(self, dev, item_name, value):
        return Freebie(item_name=item_name, value=value, company=self, dev=dev)

    # Deliverable: Find the oldest company
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year.asc()).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'
    
     # Deliverable: Returns a collection of companies the dev has received freebies from
    @property
    def companies(self):
        return {freebie.company for freebie in self.freebies}

    # Deliverable: Check if a dev has received a specific freebie
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Deliverable: Transfer a freebie to another dev
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    company = relationship("Company", backref=backref("freebies", cascade="all, delete"))
    dev = relationship("Dev", backref=backref("freebies", cascade="all, delete"))

    def __repr__(self):
        return f"<Freebie {self.item_name}, worth {self.value}>"
    
    # Deliverable: Print details of a freebie
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
