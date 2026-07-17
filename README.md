# CT200 QA System

A FastAPI backend that parses the CardioTrack CT-200 manual into a structured tree, supports document versioning, generates QA test cases using Groq LLM, and detects stale outputs when document content changes.

## Tech Stack

- FastAPI
- Pydantic
- SQLite
- Groq (Llama 3.3 70B)
- Pytest

## Setup

```bash
git clone <repo-url>
cd ct200-qa-system

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## Environment Variable

Create `.env`

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

## Run

```bash
python create_db.py

python -m uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Versioning Flow

### Ingest V1

```http
POST /ingest/v1
```

### Ingest V2

```http
POST /ingest/v2
```

### Compare Versions

```http
GET /compare
```

## Main APIs

### Browse

```http
GET /sections
GET /node/{id}
GET /search?q=text
GET /changes/{logical_node_id}
```

### Selections

```http
POST /selections
GET /selections/{selection_id}
```

### Generate Test Cases

```http
POST /generate/{selection_id}
```

### Staleness

```http
GET /generation/{generation_id}/staleness
```

### Retrieval

```http
GET /generations/{generation_id}
GET /selection/{selection_id}/generations
GET /node/{node_id}/generations
```

## Tests

```bash
pytest
```

## Known Limitations

- Title-based node matching may fail if headings are renamed.
- Hash-based staleness detection treats all content changes equally.
- LLM output quality depends on the model response.

