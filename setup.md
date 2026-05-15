# ClosedLoop OS - Setup Guide

Welcome to ClosedLoop OS! This guide will walk you through setting up and running the project locally, step-by-step. It is designed for beginners, so don't worry if everything is new to you.

## Project Structure Overview

This project has two main parts:
- **Backend (API)**: A Python application built with FastAPI and LangGraph. It runs in `apps/api`.
- **Frontend (Web)**: A React application built with Next.js. It runs in `apps/web`.

We also use several infrastructure services that we'll run using Docker Compose:
- **PostgreSQL / pgvector**: For our database.
- **Redis**: For caching and messaging.
- **Redpanda (Kafka compatible)**: For streaming events.
- **Neo4j**: A graph database.

---

## Prerequisites

Before we start, you will need a few things installed on your computer:
1. **Docker & Docker Compose**: This is used to run the databases and message queues easily. (Download [Docker Desktop](https://www.docker.com/products/docker-desktop)).
2. **Python 3.10+**: Needed to run the backend.
3. **Node.js 20+**: Needed to run the frontend.
4. **Git**: To version control and download the code if you haven't already.

---

## Step 1: Environment Variables Setup

Environment variables are settings your application needs to run, like database passwords and API keys. We keep these in a file named `.env` locally.

1. In the root directory (`d:\closedloop-os`), look for a file named `.env.example`.
2. Make a copy of this file and name it exactly `.env` in the same directory.
3. Open the new `.env` file in VS Code.

Here is what these variables mean and where you can get them:

```env
# ==== Core Settings ====
APP_NAME=ClosedLoop OS
# The URL where your frontend will run
APP_URL=http://localhost:3000
# The URL where your backend API will run
API_URL=http://localhost:8000
# Secret keys for security - you can leave these as "change-me" for local development,
# but generating your own is recommended.
JWT_SECRET=change-me
ENCRYPTION_KEY=change-me

# ==== Infrastructure ====
# The database connections. When using Docker compose, the default values below work perfectly.
DATABASE_URL=postgresql+asyncpg://closedloop:closedloop@localhost:5432/closedloop
REDIS_URL=redis://localhost:6379/0
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# ==== AI Configuration (Azure OpenAI) ====
# You need to get these values from your Azure Portal if you want to use the AI features.
# If you don't have these, some features might not work, but the app will still start.

# URL of your Azure OpenAI resource (e.g., https://your-resource-name.openai.azure.com/)
AZURE_OPENAI_ENDPOINT=
# The API Key found in your Azure OpenAI portal under 'Keys and Endpoint'
AZURE_OPENAI_API_KEY=
# The API version being used
AZURE_OPENAI_API_VERSION=2024-10-21
# The names of your model deployments in Azure OpenAI Studio
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

---

## Step 2: Running Infrastructure using Docker Compose

We will use Docker to start up all the databases and services we need.
1. Open a new Terminal in VS Code (`Terminal -> New Terminal`).
2. Run the following command from the root directory (`d:\closedloop-os`):

   ```bash
   cd infra
   docker-compose up -d postgres redis redpanda neo4j
   ```
   *Note: Using `-d` runs them in the background.*

You can verify they are running by typing `docker ps` or checking Docker Desktop.

---

## Step 3: Setting up the Backend (API)

The backend is built in Python. We need to install its dependencies and start it.

1. Open a new Terminal in VS Code.
2. Navigate to the API folder by typing:
   ```bash
   cd apps/api
   ```
3. Create a Python Virtual Environment to keep the project's packages isolated:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
5. Install the Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```

Your backend API is now running at `http://localhost:8000`.

---

## Step 4: Setting up the Frontend (Web)

The frontend uses Node.js and Next.js. We need to install the Node modules and start it.

1. Open a new Terminal in VS Code.
2. Navigate to the Web folder by typing:
   ```bash
   cd apps/web
   ```
3. Install the dependencies using npm:
   ```bash
   npm install
   ```
4. Start the frontend Next.js server:
   ```bash
   npm run dev
   ```

Your frontend is now running at `http://localhost:3000`.

---

## Step 5: Testing it out!

- Open a web browser and go to `http://localhost:3000`. You should see the ClosedLoop OS interface!
- The backend API provides automatic documentation. You can view the API endpoints by going to `http://localhost:8000/docs`.

### Summary

To completely restart the project in the future, you will need to:
1. Make sure Docker is running the database services (`docker-compose start`).
2. Run the Backend API in one terminal (`cd apps/api`, activate venv, run `uvicorn`).
3. Run the Frontend in another terminal (`cd apps/web`, run `npm run dev`).
