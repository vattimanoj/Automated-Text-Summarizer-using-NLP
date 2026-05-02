import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("AUTOMATED TEXT SUMMARIZER - BACKEND SERVER")
    print("=" * 60)
    print("Server URL: http://localhost:8000")
    print("API Docs:   http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
