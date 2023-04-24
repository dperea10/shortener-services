from fastapi import Response, HTTPException
from fastapi.requests import Request
from user_agents import parse
from application.shortened.usecase.redirect_to_long_url_usecase import redirect_to_long_url_use

def redirect_to_long_url_handler(short_url: str, header:str):
   response = Response()
   try:
     long_url = redirect_to_long_url_use(short_url, header)
     response.headers["Location"] = long_url
     response.status_code = 302
     return response
   except Exception as e:
    raise HTTPException(status_code=500, detail="Error long url not found")
