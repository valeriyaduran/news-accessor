import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=".env.dev")
session_maker = sessionmaker(bind=create_engine(url=os.getenv("POSTGRES_URL")))

base_newspaper_url = "https://news.google.com/newspapers"
partial_newspaper_url = "https://news.google.com/newspapers?nid="
