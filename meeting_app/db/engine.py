import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

engine = create_engine(os.getenv('DATA_BASE_URL'))
