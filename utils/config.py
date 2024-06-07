# Import the necessary module
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')
OPENAI_MAX_TOKEN = os.getenv('OPENAI_MAX_TOKEN')
