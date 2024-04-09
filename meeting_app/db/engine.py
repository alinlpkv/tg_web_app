import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

engine = create_async_engine(os.getenv('DATA_BASE_URL'))
