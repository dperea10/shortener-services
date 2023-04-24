from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from application.shortened.usecase.create_long_url_usecase import create_short_url_use
from infra.handlers.dtos.response import ResponseDTO

def create_short_url_handler(long_url: str, token: str) -> ResponseDTO:
    response = create_short_url_use(long_url, token)
    if response.message == "Unauthorized":
     return JSONResponse(status_code=401, content=jsonable_encoder(response))
    if response.message == "UserNotfound":
     return JSONResponse(status_code=400, content=jsonable_encoder(response))
    if response.message == "RegisterFound":
     return JSONResponse(status_code=302, content=jsonable_encoder(response))
    if response.message == "UnexpectedError":
     return JSONResponse(status_code=500, content=jsonable_encoder(response))
    
    return JSONResponse(status_code=201,content=jsonable_encoder(response))
