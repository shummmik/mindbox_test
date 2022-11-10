from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

ENGINE = create_engine("postgresql://{}:{}@{}:5432/{}".format(
    os.environ['APP_USER_DB'],
    os.environ['APP_PASSWORD_DB'],
    os.environ['APP_DB_HOST'],
    os.environ['APP_DB_NAME']
),
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=ENGINE)
