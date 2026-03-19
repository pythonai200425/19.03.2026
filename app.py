from fastapi import FastAPI

import dal_books
import dal_users
from router_books import router as book_router
from router_users import router as user_router


app = FastAPI(title="Books And Users REST API")


@app.on_event("startup")
def startup():
    dal_books.create_table_books()
    dal_users.create_table_users()


@app.get("/")
def root():
    return {"message": "Books And Users REST API is running"}


app.include_router(book_router)
app.include_router(user_router)