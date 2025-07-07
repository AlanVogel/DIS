# DIS (Document Ingestion and QA System)

## Overview
This project is a web-based application that ingests documents (PDFs and images) and enables users to ask questions based on the extracted text. It leverages FastAPI for the API, Redis for document storage, FAISS for similarity search, and OCR (via easyocr) for image text extraction. The system supports named entity recognition (NER) using SpaCy and provides a question-answering (QA) capability using a pre-trained transformer model.

Key features:
- Upload and process PDF and image files (`.pdf`, `.jpg`, `.jpeg`, `.png`).
- Extract text using OCR for images and PyMuPDF for PDFs.
- Store and index documents for efficient retrieval.
- Answer questions with entity extraction (e.g., dates, job titles).
- Token-based authentication and rate limiting.

## Prerequisites
- **Python 3.12+**
- **Docker** (for containerized deployment)
- Internet connection (for downloading models during setup)
- Resume Dataset: Download from [Kaggle datasets](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)

## Installation

### 1. Clone the Repository and create data folder
```bash
git clone https://github.com/your-username/document-qa-system.git
cd document-qa-system
mkdir data
```
### 2. Install Dependencies

Ensure you have the required Python packages and system dependencies. Use the provided requirements.txt or install manually:
```bash
pip install -r requirements.txt
```
### 3. Set Up Docker
Ensure Docker and Docker Compose are installed.
The project uses a docker-compose.yml file to manage services (e.g., Redis, FastAPI app).

### 4. Move PDF or Images data to folder data
Use some of the pdf files from [Kaggle datasets](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) and place it inside a `./data`

### 5. Build and Run

Start the application and Redis service using Docker Compose:
```bash
docker compose up -d --build
```
This will:
    - Build the FastAPI application image.
    - Start a Redis container at redis:6379.
    - Download necessary models (e.g., SpaCy en_core_web_sm, SentenceTransformer all-MiniLM-L6-v2) on first run.

## Configuration
`Secret Key`: Update `utils/security.py` with a secure `SECRET_KEY` (currently set to `"your-secret-key"`).
`Redis`: The Redis host is set to `"redis"` in `redis_service.py`, matching the Docker service name. Adjust if using a different host.

## Usage
### 1. Obtain an Access Token
Authenticate to get a bearer token:
```bash 
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```
Response example:
```bash 
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","token_type":"bearer"}
```
### 2. Upload Documents
Upload PDF or image files:
```bash 
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer <your-access-token>" \
  -F "files=@/path/to/document.pdf"
```
Supported formats: `.pdf`, `.jpg`, `.jpeg`, `.png`.
Rate limit: 5 uploads per minute.

### 3. Ask Questions
Query the system with a question:
```bash 
curl -X POST "http://localhost:8000/ask" \
  -H "Authorization: Bearer <your-access-token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the work history?"}'
```
Response example:
```bash
{"question":"What is the work history?","answer":"Finance Manager 03/2017","entities":[{"text":"Finance Manager","label":"JOB_TITLE"},{"text":"03/2017","label":"DATE"}]}
```
Rate limit: 10 queries per minute.

## Project Structure
```bash
    src/
        extraction/: Strategies for text extraction (image_extraction.py, pdf_extraction.py, extraction_strategy.py).
        services/: Business logic (document_service.py, qa_service.py, rag_service.py, redis_service.py, ner_service.py).
        utils/: Helper functions (security.py, sanitizer.py, logger.py).
        main.py: FastAPI application entry point.
        schema.py: Pydantic models.
    Dockerfile: Defines the application container.
    docker-compose.yml: Orchestrates services.
```
