from flask import Blueprint, request, jsonify
from app.utils import get_relevant_context, generate_response

bp = Blueprint("main", __name__)


@bp.route("/query", methods=["POST"])
async def query_game_info():
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "Invalid input. 'query' field is required."}), 400

        user_query = data["query"]
        context = get_relevant_context(user_query)

        if not context:
            return (
                jsonify(
                    {"error": "No relevant information found for the given query."}
                ),
                404,
            )

        response = await generate_response(user_query, context)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
