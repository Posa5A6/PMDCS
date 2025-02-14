import os
from datetime import timedelta


class Config:
    # Automatically generate a random secret key if one is not set
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    #SECRET_KEY = os.environ['SECRET_KEY']  # Assuming 'SECRET_KEY' is set on Vercel

    # PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:1234@localhost/pmdcs'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',"postgresql://default:9CtJML4fvQhB@ep-winter-truth-a4ygmkt9.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configurations
    SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Controls cross-site cookie behavior
    PERMANENT_SESSION_LIFETIME = timedelta(days=10)  # Set session lifetime for longer persistence
