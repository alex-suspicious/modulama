from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

def get( key="" ):
	return os.getenv(key)