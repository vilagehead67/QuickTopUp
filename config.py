from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you_should_set_a_secret_key'
    MONGO_URI = os.getenv('MONGO_URI') or 'your_fallback_mongo_uri'
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME') or 'vtu_portal'
    
    MAIL_SERVER = os.getenv('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    VTU_API_BASE_URL = os.getenv("VTU_API_BASE_URL")  # replace with actual
    VTU_API_USERNAME = os.getenv("VTU_API_USERNAME")
    VTU_API_PASSWORD = os.getenv("VTU_API_PASSWORD")
    VTU_API_SECRET_KEY = os.getenv("VTU_API_SECRET_KEY")
    VTU_API_PUBLIC_KEY = os.getenv("VTU_API_PUBLIC_KEY")

    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

    UPLOAD_FOLDER = os.path.join('static', 'uploads')