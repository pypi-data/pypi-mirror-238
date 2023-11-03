import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
