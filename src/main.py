import sys,os
from pathlib import Path

sys.path.append(str(Path(os.path.dirname(__file__)).parent))
from fastapi import FastAPI
import uvicorn
from routers import book,publisher,author

app = FastAPI()

app.include_router(book.router)
app.include_router(author.router)
app.include_router(publisher.router)

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True,workers=1)