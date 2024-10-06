import csv
from typing import List, Dict
from fuzzywuzzy import fuzz
from flask import current_app
from app.openai_client import openai_client


def load_csv_data(file_path: str) -> List[Dict]:
    """
    Utility function to load game csv data
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


def get_relevant_context(query: str) -> str:
    """
    Get relevant context from games_data.
    Relevance is checked using fuzzywuzzy on the games' name, short description, and genre.
    """
    game_data = current_app.config["GAME_DATA"]

    context = ""
    for game in game_data:
        relevance_score = max(
            fuzz.partial_ratio(query.lower(), game["name"].lower()),
            fuzz.partial_ratio(query.lower(), game["short_description"].lower()),
            fuzz.partial_ratio(query.lower(), game["genres"].lower()),
        )

        if relevance_score > 60:
            for col in game.keys():
                if col == "name":
                    context += f"Game: {game['name']}\n"
                    continue
                context_col = " ".join(col.split("_")).capitalize()
                context += f"{context_col}: {game[col]}\n"
    return context


async def generate_response(query: str, context: str) -> str:
    """
    Generate OpenAI GPT response given query and with the relevant context.
    """
    prompt = f"Query: {query}\n\nResponse:"
    response = await openai_client.get_client().chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions about video games based on the provided context.",
            },
            {"role": "assistant", "content": f"Context: {context}"},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
