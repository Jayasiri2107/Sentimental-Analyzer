from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from database import get_connection, init_db
from models import inputMessage, outputMessage

ml_url = "https://sentimental-rlvx.onrender.com/classify"

def analyze_sentiment(text: str) -> str:
    try:
        response = httpx.post(
            ml_url,
            json={"message": text}, 
            timeout=5.0
        )
        return response.json()["sentiment"]
    
    except Exception as e:
        print(f"Error: {e}")
        return "Neutral"
    

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/messages", response_model=outputMessage)
def post_message(body: inputMessage):

    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    sentiment = analyze_sentiment(body.text)

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (text, sentiment)
            VALUES (%s, %s)
            RETURNING id, text, sentiment, timestamp
            """,
            (body.text, sentiment),
        )

        row = cursor.fetchone()
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return outputMessage(
        id=row[0],
        text=row[1],
        sentiment=row[2],
        timestamp=row[3]
    )


@app.get("/messages", response_model=list[outputMessage])
def get_messages():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, text, sentiment, timestamp
            FROM messages
            ORDER BY timestamp DESC
            """
        )

        rows = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return [
        outputMessage(
            id=r[0],
            text=r[1],
            sentiment=r[2],
            timestamp=r[3]
        )
        for r in rows
    ]