# Video Game Query API

This Flask-based API accepts user queries about video games and provides responses using OpenAI's GPT-4 model.

## Setup and Installation

1. Clone this repository

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key and CSV file path:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   CSV_FILE_PATH=data/games_description.csv
   ```

## Running the Application

To run the application, use the following command:

```sh
python run.py
```

The API will be accessible at `http://localhost:5000/query`.

## Using the API

Send a POST request to `http://localhost:5000/query` with a JSON payload containing a "query" field. For example:

```sh
curl -X POST -H "Content-Type: application/json" -d '{"query":"What is the player rating of Elden Ring?"}' http://localhost:5000/query
```

The API will return a JSON response with the answer to your query.