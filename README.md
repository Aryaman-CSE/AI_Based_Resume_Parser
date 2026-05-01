# AI Resume Parser

An AI-powered resume parsing application built using Python, FastAPI, and NLP.

## Features
- Upload resume in PDF format
- Extracts:
  - Name
  - Email
  - Phone
  - Skills
  - Education
- Uses spaCy for NLP processing
- REST API built with FastAPI

## Project Structure
- main.py → FastAPI entry point
- resume_parser.py → Resume parsing logic
- requirements.txt → Python dependencies

## How to Run
1. Create virtual environment
2. Install dependencies
3. Run FastAPI server using uvicorn

## API Endpoint
POST `/parse-resume`
