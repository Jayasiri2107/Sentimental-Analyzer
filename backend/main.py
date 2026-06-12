from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

from backend.database import init_db, insert_message, fetch_messages
from backend.models import inputMessage, outputMessage

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
    row = insert_message(body.text, sentiment)

    if not row:
        raise HTTPException(status_code=500, detail="Failed to save message")

    return outputMessage(
        id=row[0],
        text=row[1],
        sentiment=row[2],
        timestamp=row[3]
    )


@app.get("/messages", response_model=list[outputMessage])
def get_messages_route():
    rows = fetch_messages()
    return [
        outputMessage(
            id=r[0],
            text=r[1],
            sentiment=r[2],
            timestamp=r[3]
        )
        for r in rows
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
