from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

import dal_books
import dal_users
from router_books_jwt import router as book_router_jwt
from router_books import router as book_router
from router_users import router as user_router


app = FastAPI(title="Books And Users REST API")


@app.on_event("startup")
def startup():
    dal_books.create_table_books()
    dal_users.create_table_users()

'''
create me a web page that i can plug into my fastapi which will show table of all books 
and let me insert update delete get by id using the rest api 
make the page look nice decorated with nice animation
'''
@app.get("/")
def root():
    """Serve the Library Manager UI"""
    html_path = os.path.join(os.path.dirname(__file__), "books.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    return {"message": "Books And Users REST API is running"}


app.include_router(book_router)
app.include_router(book_router_jwt)
app.include_router(user_router)