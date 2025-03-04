#!/usr/bin/env python3

from models import Company, Dev, Freebie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to the database
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Fetch a dev and check freebies attached to them
dev = session.query(Dev).first()
print(f"\nDeveloper: {dev.name}")
print(f"Freebies: {[freebie.item_name for freebie in dev.freebies]}")

# Check the oldest company
oldest = Company.oldest_company(session)
print(f"\nOldest Company: {oldest.name} (Founded in {oldest.founding_year})")

# Check for freebie’s details
freebie = session.query(Freebie).first()
print(f"\nFreebie Details: {freebie.print_details()}")

# Transfer a freebie to a dev
dev1 = session.query(Dev).filter_by(name="Wakio").first()
dev2 = session.query(Dev).filter_by(name="Maureen").first()
freebie = session.query(Freebie).filter_by(item_name="T-shirt").first()

print(f"\nBefore Transfer: {freebie.print_details()}")
dev1.give_away(dev2, freebie)
session.commit()

# Verify a freebie transfer
print(f"After Transfer: {freebie.print_details()}")
