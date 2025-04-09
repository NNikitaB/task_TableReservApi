from fastapi import FastAPI,HTTPException,Depends
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
#from app.api.v1.endpoints.routers import routers
#from app.database.db import create_tables
from contextlib import asynccontextmanager
#add CORS
from fastapi.middleware.cors import CORSMiddleware




origins = [
    "http://localhost:3000",
]

@asynccontextmanager
async def init_db(app: FastAPI):
#    await create_tables()
    yield

#db_created = create_tables()

app = FastAPI(title=" Service API",lifespan=init_db)#,on_startup=[create_tables])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


#app.include_router(routers)


@app.get("/")
async def root():
    return {"message": "Service API created by NNikitaB"}



#if __name__ == "__main__":
#    uvicorn.run(f"{__name__}:app",host="127.0.0.1", port=8080, reload=True)

