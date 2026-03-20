import pandas as pd
from pathlib import Path
from app.db.database import sessionmanager
from app.models.category import Category
from app.models.staff import Staff
from app.models.author import Author
from app.models.publisher import Publisher
from sqlalchemy import insert
from app.utils.security import hash_password

async def load_seed_data():
    # read authors
    authors_path= Path("data/authors.csv")
    df_authors= pd.read_csv(authors_path)

    # read categories
    categories_path = Path("data/categories.csv")
    df_categories = pd.read_csv(categories_path)

    # read publishers
    publishers_path = Path("data/publishers.csv")
    df_publishers = pd.read_csv(publishers_path)

    # read staff
    staff_path = Path("data/staff.csv")
    df_staffs = pd.read_csv(staff_path)

    df_authors["birth_year"] = df_authors["birth_year"].astype(str)
    df_staffs["phone"] = df_staffs["phone"].astype(str)
    df_staffs["password_hash"] = df_staffs["password_hash"].apply(hash_password)

    # Convert DataFrames to list of dicts
    authors_data = df_authors.to_dict(orient="records")
    categories_data = df_categories.to_dict(orient="records")
    publishers_data = df_publishers.to_dict(orient="records")
    staff_data = df_staffs.to_dict(orient="records")

    print("Seeding started...")
    async with sessionmanager.session() as session:
        async with session.begin():
            await session.execute(insert(Author).values(authors_data))
            await session.execute(insert(Category).values(categories_data))
            await session.execute(insert(Publisher).values(publishers_data))
            await session.execute(insert(Staff).values(staff_data))
    print("Seeding completed...")

