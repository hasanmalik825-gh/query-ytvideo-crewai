from fastapi import FastAPI
import uvicorn
from routes import index_router, query_ytvideo_router
from middleware.middleware import add_middleware
from constants import PORT

app = FastAPI()

app.middleware("http")(add_middleware)
app.include_router(index_router)
app.include_router(query_ytvideo_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)