# Sentimental-Analyzer

# Smart Feedback Wall — Frontend

A sentiment analysis frontend that lets users type a message and see it classified as Positive, Neutral, or Negative using AI.

---

## How to Run

### Backend (FastAPI + PostgreSQL)

The frontend needs the backend running on `http://localhost:8000`.

**Option 1 — Docker (recommended)**
```bash
# Build the image (first time only)
docker build -t sentimental-backend .

# Run the container
docker run -p 8000:8000 -e database_url="postgresql://user:pass@host/db" sentimental-backend
```

**Option 2 — Local Python**
```bash
# Terminal 1
cd backend

# If you have Python 3.13 or newer:
pip install fastapi uvicorn psycopg psycopg-binary python-dotenv httpx

# If you have Python 3.12 or older:
pip install -r requirements.txt

# Set your database URL in a .env file:
# database_url=postgresql://user:pass@host/db

# Start server
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
# Terminal 2
cd frontend
python -m http.server 5500
```

Open **http://localhost:5500** in your browser.

## How It Works

The page has two sections:

**1. Input Form (top)** : User types a message (up to 500 characters) and clicks "Analyze Sentiment". The frontend sends a POST request to `http://localhost:8000/messages` with the message text.

**2. Feedback Wall (bottom)** : Displays all submitted messages as colored cards. Each card shows the message text, a timestamp, an emoji representing the sentiment (happy/neutral/sad), and a background color that matches the sentiment. The wall loads all messages from the backend on page load via a GET request, and new messages are instantly prepended to the top after submission.

### Sentiment Colors & Emojis

| Sentiment | Background Color | Emoji     |
|-----------|------------------|-----------|
| Positive  | `#7FA19D` (sage) | happy.png |
| Neutral   | `#746D91` (muted purple) | neutral.png |
| Negative  | `#C4A193` (rose) | sad.png   |

---

## File Structure

```
frontend/
├── index.html      # Page layout: header, form, feedback wall
├── style.css       # All styling (form card, wall cards, responsive)
├── script.js       # Form submit handler, fetch calls, card rendering
├── emojis/         # Sentiment emoji images
│   ├── happy.png
│   ├── neutral.png
│   └── sad.png
└── README.md
```

---

## Our Contributions

### Abhay — Input Interface

- Built the input form in `index.html` (textarea, submit button, character counter, labels)
- Wrote the form submission logic in `script.js` (event listener, input validation, character counting, loading state on button, POST request to backend API)
- Styled the form card, textarea, input group, and submit button in `style.css`

### Adithya — Output / Feedback Wall

- Built the feedback wall section in `index.html` (section, container, card structure)
- Wrote the message retrieval and card rendering logic in `script.js` (GET request to load messages, `addCard()` function for creating and appending cards, sentiment-to-color/emoji mapping, error handling when backend is unavailable)
- Styled the wall section, feedback cards, and card layout in `style.css`

---

## What We Learned

We learned how to collaborate on a shared codebase using Git and GitHub, including creating branches, working with pull requests, handling merges, and coordinating changes while working on the same frontend project. We also learned the importance of communication, task division, and brainstorming ideas as a team before implementation. On the technical side, we learned how to connect a static frontend to a FastAPI backend using fetch, handle asynchronous requests with async/await, dynamically create and update DOM elements with JavaScript, and design a responsive, accessible UI with CSS.

## Smart Feedback Wall — Backend

A REST API built with FastAPI and PostgreSQL called Neon that receives messages from the frontend, sends them to an AI/ML model for sentiment analysis, and stores the results in a cloud database.

## HOW IT WORKS

The backend exposes two endpoints:

POST /messages
Receives a message from the frontend, forwards it to the AI/ML model which runs VADER sentiment analysis and returns a label. The message and its sentiment label are saved to the Neon PostgreSQL database. The full saved message is returned to the frontend as JSON.

GET /messages
Fetches all saved messages from the database, ordered newest first, and returns them as a JSON array to the frontend.

## API CONTRACT

POST   /messages   Request: { "text": "your message" }   Response: Full message object with sentiment
GET    /messages   Request: None                          Response: Array of all messages

Response shape:
{
    "id": 1,
    "text": "great app!",
    "sentiment": "Positive",
    "timestamp": "2024-06-12T10:30:00Z"
}

Sentiment values are always exactly one of the following : Positive, Neutral, Negative

Request:
    { "message": "your text here" }

Response:
    { "sentiment": "Positive" }

If the ML service is unavailable the backend defaults to Neutral so the app never crashes.

## TECH STACK

```
FastAPI       — Web framework, handles HTTP requests and endpoints
Neon          — Cloud hosted PostgreSQL, stores messages permanently
psycopg2      — Connects Python to the Neon PostgreSQL database
Pydantic      — Validates incoming and outgoing data shapes
httpx         — Makes HTTP calls to the AI/ML microservice
python-dotenv — Reads the .env file for the database URL
uvicorn       — The server that runs FastAPI
```
---

## FILE STRUCTURE

```
backend/
├── main.py          — All API endpoints and ML service integration
├── database.py      — Neon connection and table initialisation
├── models.py        — Pydantic request and response models
├── requirements.txt — All dependencies
└── .env             — Database URL 
```
---

## WHAT WE LEARNED

On the technical side we learned how to build a API from scratch using FastAPI and connect it to a cloud PostgreSQL database called Neon. We also learned how to structure a backend into separate files such as main , database logic, and data models . We also learned how HTTP methods work (GET vs POST), how Pydantic validates data automatically, how to make HTTP calls from Python to another service using httpx, how to handle database connections safely with try and finally, and how environment variables ensure privacy . Lastly we learned how the backend coordinates between AI/ML and frontend and ensures smooth data flow.

Since this project was built by three teams simultaneously , before writing any code we agreed on a shared API contract so all three parts could connect at the end. We used Git and GitHub to collaborate through branches and pull requests. The biggest lesson was that communication matters as much as code a change in one part of the system affects everyone else, so we had to think beyond our own files and consider the whole picture.
