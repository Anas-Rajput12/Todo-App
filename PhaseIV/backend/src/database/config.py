import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL - defaults to a local SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# For Neon PostgreSQL, the URL would typically look like:
# postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require