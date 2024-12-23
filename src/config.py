# config.py
import os
from dotenv import load_dotenv

class Config:
    _instance = None  # Singleton instance
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.binance_api_key = os.getenv("BINANCE_API_KEY")
        self.binance_secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.bybit_api_key = os.getenv("BYBIT_API_KEY")  # New Bybit API key
        self.bybit_secret_key = os.getenv("BYBIT_SECRET")  # New Bybit secret key
    
    def get_binance_api_key(self):
        return self.binance_api_key
    
    def get_binance_secret_key(self):
        return self.binance_secret_key

    def get_bybit_api_key(self):
        return self.bybit_api_key  # Getter for Bybit API key
    
    def get_bybit_secret_key(self):
        return self.bybit_secret_key  # Getter for Bybit secret key

# Create a single instance of Config
config_instance = Config()