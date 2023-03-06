from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Literal
import os
from utils.insta_comment_scraper import comment_scraper
from fastapi import FastAPI, File, UploadFile
import re


port = os.environ.get('PORT', 8000)
app = FastAPI(PORT = port)

@app.get("/")
async def status_check():
  return "alive"

@app.post("/uploadfile")
async def process(username:str, password:str, file: UploadFile = File(...)):
    
    if not file:
        return {"message": "No upload file sent"}
    else:
        content = await file.read()
        url_list = re.split(',', content.decode('utf-8'))
        comment_list = []
        for url in url_list:
           comments = comment_scraper(url, username, password)
           comment_list.append(comments)
        return comment_list
          
    
@app.post("/url")
async def youtube_comments(url: str, username:str, password:str):
  print(url)
  comments = comment_scraper(url, username, password)
  return comments
