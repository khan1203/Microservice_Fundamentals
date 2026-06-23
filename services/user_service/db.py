from sqlmodel import create_engine, Session
from config import settings 


DATABASE_URL = str(settings.DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite:/") else {}
)

def get_session():
    with Session(engine) as session:
        yield session 