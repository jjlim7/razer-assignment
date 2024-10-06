import os
from dotenv import load_dotenv
from app.utils import load_csv_data

load_dotenv()


class Config:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    CSV_FILE_PATH = os.environ.get("CSV_FILE_PATH")

    if CSV_FILE_PATH:
        GAME_DATA = load_csv_data(CSV_FILE_PATH)
    else:
        GAME_DATA = load_csv_data("data/games_description.csv")
