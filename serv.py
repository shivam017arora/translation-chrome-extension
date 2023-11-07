"""
Task 1: Backend API Development for Word Translations
Develop a backend API that the Chrome extension can communicate with to fetch translations.
The API should have endpoints to:
1. Retrieve translations for a given word and target language.
2. Add new translations to the database.
3. Update existing translations.
4. Delete translations.

Requirements:
● 1. The API should support at least three languages for translation.
● 2. Implement proper error handling and validation.
● 3. Ensure the API responses follow RESTful design principles.
● 4. Include appropriate API documentation.
"""

from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
from pydantic import Extra
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from chain import translate
from dotenv import dotenv_values
load_dotenv('.env')
from sql import Translation

config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app, origins='chrome-extension://mjkkemognlhghilfdkbnjafhelmfbgap')

#make health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Healthy"}), 200

@app.route('/translations', methods=['GET'])
def get_translation():
    word = request.args.get('word')
    language = request.args.get('language')

    print(word, language)

    # Validation
    if not word or not language:
        abort(400, description="Please provide both 'word' and 'language' parameters.")

    # Retrieve the translation from the database
    translation_entry = Translation.find(word, language)
    # translation_entry = None

    if translation_entry:
        # The translation already exists in the database, use it
        translation = translation_entry[3]
    else:
        # If not found in the database, use the translate function to get it and save
        translation = translate(word, language)
        if translation:
            Translation(word, language, translation).save()
        else:
            abort(404, description="Translation not found.")

    return jsonify({
        "word": word,
        "language": language,
        "translation": translation
    }), 200

@app.route('/translations', methods=['POST'])
def add_translation():
    data = request.get_json()

    word = data.get('word')
    language = data.get('language')
    translation = data.get('translation')

    # Validation
    if not word or not language or not translation:
        abort(400, description="Please provide 'word', 'language', and 'translation' fields.")

    # Check if the translation already exists
    existing_translation = Translation.find(word, language)
    if existing_translation:
        abort(409, description="Translation already exists.")

    # Add the translation to the database
    new_translation_id = Translation(word, language, translation).save()

    return jsonify({"id": new_translation_id, "word": word, "language": language, "translation": translation}), 201

@app.route('/translations', methods=['PUT'])
def update_translation():
    data = request.get_json()

    word = data.get('word')
    language = data.get('language')
    new_translation = data.get('translation')

    # Validation
    if not word or not language or not new_translation:
        abort(400, description="Please provide 'word', 'language', and 'translation' fields.")

    # Update the translation
    Translation.update(word, language, new_translation)

    return jsonify({"word": word, "language": language, "translation": new_translation}), 200

# API endpoint for deleting a translation
@app.route('/translations', methods=['DELETE'])
def delete_translation():
    word = request.args.get('word')
    language = request.args.get('language')

    # Validation
    if not word or not language:
        abort(400, description="Please provide both 'word' and 'language' parameters.")

    # Check if the translation exists before attempting to delete
    existing_translation = Translation.find(word, language)
    if not existing_translation:
        abort(404, description="Translation not found.")

    # Delete the translation
    Translation.delete(word, language)

    return jsonify({"message": "Translation deleted successfully"}), 200

# Error handler for 404
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Error handler for 400
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8912)
