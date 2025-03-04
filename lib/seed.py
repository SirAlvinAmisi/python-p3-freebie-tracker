from models import Company, Dev, Freebie, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to the database
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()

# Create companies
company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Microsoft", founding_year=1975)
company3 = Company(name="Apple", founding_year=1976)

# Create devs
dev1 = Dev(name="Wakio")
dev2 = Dev(name="Maureen")

# Create freebies
freebie1 = Freebie(item_name="T-shirt", value=10, company=company1, dev=dev1)
freebie2 = Freebie(item_name="Mug", value=5, company=company2, dev=dev1)
freebie3 = Freebie(item_name="Sticker", value=2, company=company3, dev=dev2)

# Add all to session and commit
session.add_all([company1, company2, company3, dev1, dev2, freebie1, freebie2, freebie3])
session.commit()

print("Database seeded successfully!")
