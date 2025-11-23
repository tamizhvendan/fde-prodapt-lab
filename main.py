import os
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import text
from db import get_db_session
from file_storage import upload_file
from models import JobBoard, JobPost
from config import settings

app = FastAPI()

@app.get("/api/health")
async def health():
  try:
    with get_db_session() as session:
        session.execute(text("SELECT 1"))
        return {"database": "ok"}
  except Exception as e:
    print(e)
    return {"database": "down"}

@app.get("/api/job-boards")
async def api_job_boards():
    with get_db_session() as session:
       jobBoards = session.query(JobBoard).all()
       return jobBoards
    
# @app.post("/api/job-boards")
# async def api_create_new_job_board(request: Request):
#    body = await request.body()
#    raw_text = body.decode()
#    print(request.headers.get('content-type'))
#    print(raw_text)
#    return {}

# from typing import Annotated
# @app.post("/api/job-boards")
# async def api_create_new_job_board(slug: Annotated[str, Form()]):
#    return {"slug": slug}

class JobBoardForm(BaseModel):
   slug : str = Field(..., min_length=3, max_length=20)
   logo: UploadFile = File(...)

   @field_validator('slug')
   @classmethod
   def to_lowercase(cls, v):
     return v.lower()

# @app.post("/api/job-boards")
# async def api_create_new_job_board(job_board_form: Annotated[JobBoardForm, Form()]):
#    return {"slug": job_board_form.slug}

@app.post("/api/job-boards")
async def api_create_new_job_board(job_board_form: Annotated[JobBoardForm, Form()]):
   logo_contents = await job_board_form.logo.read()
   file_url = upload_file("company-logos", job_board_form.logo.filename, logo_contents, job_board_form.logo.content_type)
   return {"slug": job_board_form.slug, "file_url" : file_url}

if not settings.PRODUCTION:
   app.mount("/uploads", StaticFiles(directory="uploads"))

@app.get("/api/job-boards/{job_board_id}/job-posts")
async def api_company_job_board(job_board_id):
  with get_db_session() as session:
     jobPosts = session.query(JobPost).filter(JobPost.job_board_id.__eq__(job_board_id)).all()
     return jobPosts

@app.get("/api/job-boards/{slug}")
async def api_company_job_board(slug):
  with get_db_session() as session:
     jobPosts = session.query(JobPost) \
        .join(JobPost.job_board) \
        .filter(JobBoard.slug.__eq__(slug)) \
        .all()
     return jobPosts
  
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")