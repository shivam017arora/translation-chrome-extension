# Translation Chrome Extension

This project is a Chrome extension that allows users to translate text between languages via a simple browser interface. It communicates with a backend API to fetch and store translations.

# Demo
<img width="340" alt="demo" src="https://github.com/shivam017arora/translation_chrome_extension/assets/26146104/50e6a482-83d2-4863-90e0-9a8d999f3848">

### Prerequisites

- Python 3.x
- Flask
- Sqlite3
- Google Chrome or any Chromium-based browser

### Installing

A step by step series of examples that tell you how to get a development environment running.

1. **Clone the repository**

```sh
git clone https://github.com/yourusername/translation_chrome_extension.git
cd translation_chrome_extension
```

2. **Set up a virtual environment** (optional, but recommended)

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the requirements**

```sh
pip install -r requirements.txt
```

4. **Set up environment variables**

Copy the `.env.example` file to create a `.env` that will store your environment variables.

```sh
cp .env.example .env
```

Edit the `.env` file with your specific configurations.

5. **Initialize the database**

```sh
python sql.py
```

6. **Run the Flask application**

```sh
python serv.py
```

This will start the backend server on `http://localhost:8912/`.

### Setting up the Chrome Extension

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable `Developer mode` by toggling the switch in the top right corner.
3. Click on `Load unpacked` and select the directory containing the Chrome extension (`plasmo-assessment-ai`). This is where the output of yarn dev is placed.
The extension should now appear in the list of extensions, and you can pin it to the toolbar for easy access.

## Running the tests

To run the automated tests for this system:

```sh
pytest test_api.py
```

# API DOCUMENTATION

## Base URL
`http://localhost:8912`

## Supported Languages
- English
- Spanish
- French
(Additional languages can be added as per requirement.)

## Endpoints

### GET /translations
Retrieves a translation for the given word and target language.

#### Query Parameters:
- `word`: The word to be translated (required).
- `language`: The target language for translation (required).

#### Success Response:
- **Code:** 200 OK
- **Content:** 
  ```json
  {
    "word": "hello",
    "language": "spanish",
    "translation": "hola"
  }
  ```

#### Error Response:
- **Code:** 400 BAD REQUEST
- **Content:** `{ "error": "Please provide both 'word' and 'language' parameters." }`
- **Code:** 404 NOT FOUND
- **Content:** `{ "error": "Translation not found." }`

### POST /translations
Adds a new translation to the database.

#### Body Parameters (application/json):
- `word`: The word to be translated (required).
- `language`: The target language for translation (required).
- `translation`: The translated word (required).

#### Success Response:
- **Code:** 201 CREATED
- **Content:** 
  ```json
  {
    "id": 1,
    "word": "goodbye",
    "language": "spanish",
    "translation": "adios"
  }
  ```

#### Error Response:
- **Code:** 400 BAD REQUEST
- **Content:** `{ "error": "Please provide 'word', 'language', and 'translation' fields." }`
- **Code:** 409 CONFLICT
- **Content:** `{ "error": "Translation already exists." }`

### PUT /translations
Updates an existing translation in the database.

#### Body Parameters (application/json):
- `word`: The word to be translated (required).
- `language`: The target language for translation (required).
- `translation`: The new translation (required).

#### Success Response:
- **Code:** 200 OK
- **Content:** 
  ```json
  {
    "word": "goodbye",
    "language": "french",
    "translation": "au revoir"
  }
  ```

#### Error Response:
- **Code:** 400 BAD REQUEST
- **Content:** `{ "error": "Please provide 'word', 'language', and 'translation' fields." }`

### DELETE /translations
Deletes a translation from the database.

#### Query Parameters:
- `word`: The word whose translation is to be deleted (required).
- `language`: The target language for the translation (required).

#### Success Response:
- **Code:** 200 OK
- **Content:** `{ "message": "Translation deleted successfully" }`

#### Error Response:
- **Code:** 400 BAD REQUEST
- **Content:** `{ "error": "Please provide both 'word' and 'language' parameters." }`
- **Code:** 404 NOT FOUND
- **Content:** `{ "error": "Translation not found." }`

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of an API request.

- **200 OK:** The request has succeeded.
- **201 CREATED:** The request has been fulfilled and has resulted in one or more new resources being created.
- **400 BAD REQUEST:** The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).
- **404 NOT FOUND:** The server can't find the requested resource.
- **409 CONFLICT:** The request could not be completed due to a conflict with the current state of the target resource.
