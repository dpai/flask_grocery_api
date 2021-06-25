
import os
os.environ['DATABASE_URI'] = f"sqlite:///grocery_test.db"
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grocery_api.models import shop, grocery, product, vendor
from grocery_api.database import SessionLocal, engine, Base

db = SessionLocal()

Base.metadata.create_all(bind=engine)

shop1 = shop.Shop("Test1", "Wisonsin")
db.add(shop1)
db.commit()
db.close()