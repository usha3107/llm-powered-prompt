# LLM Prompt Router Service

This application is an intelligent prompt router service. It intercepts a user's prompt, classifies its intent using an LLM, and then dynamically routes the request to a highly-specialized system prompt tailored to that intent.

The application leverages the Groq API for extremely fast, free inference using LLaMA models.

## Features
- **Two-Stage Generation**: First classifies intent, then routes to an expert persona for response generation.
- **5 Extensible Labels**: Currently supports routing for `code`, `data`, `writing`, `career`, and `unclear`.
- **Robust Error Handling**: Automatically catches decommissioned models or API limit errors to avoid crashes.
- **Detailed Logging**: Every router decision is logged securely in JSONL format for easy analytics (`route_log.jsonl`).

## Requirements
- Docker and Docker Compose (if containerizing)
- Python 3.11+ (if running bare-metal)
- A free Groq API Key

## Setup Instructions

### 1. Configure the Environment
You must have an API key to run this application.
1. Sign up for a free API key at [console.groq.com/keys](https://console.groq.com/keys)
2. Copy the `.env.example` file and rename the copy to `.env`
   ```bash
   cp .env.example .env
   ```
3. Open the `.env` file and replace `your_api_key_here` with your actual Groq API key:
   ```
   GROQ_API_KEY=gsk_...
   ```

### 2. Local Bare-Metal Setup
To run the python script directly on your machine without Docker:
1. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the interactive router:
   ```bash
   python main.py
   ```

### 3. Docker / Containerized Setup
You can run the router service entirely within an isolated Docker container interactively.
1. Build and run the image using Docker Compose:
   ```bash
   docker-compose run prompt-router
   ```
   *Note*: We use `docker-compose run` (with interactive mode enabled in the config) instead of `docker-compose up` because `main.py` requires real-time user input (`input("User: ")`).

## Design Overview
- **`main.py`**: The entrypoint interactive loop that collects user input.
- **`classifier.py`**: Makes an initial lightweight API call to logically categorize the prompt (`llama-3.1-8b-instant`).
- **`router.py`**: Takes the classification and makes a secondary, heavier API call against a specialized expert persona (`llama-3.3-70b-versatile`). Handles error surfacing to the user.
- **`prompts.py`**: A dictionary containing the actual system contexts assigned to each persona label.
- **`logger.py`**: Appends the final routing decision and response into `route_log.jsonl`.
- **`docker-compose.yml`**: Configures the Docker environment to mount the current directory and forward Standard Input (`stdin`) so the user can physically type to the script while it's in a container.
