import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(os.getenv('DATA_BASE_URL'))
