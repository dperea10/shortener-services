from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from application.shortened.usecase.delete_short_url_usecase import delete_short_url_use
from infra.handlers.dtos.response import ResponseDTO

def delete_long_short_url_handler(short_url: str, token: str) -> ResponseDTO:
    response = delete_short_url_use(short_url, token)
    if response.message == "Unauthorized":
     return JSONResponse(status_code=401, content=jsonable_encoder(response))
    if response.message == "UserNotfound":
     return JSONResponse(status_code=400, content=jsonable_encoder(response))
    if response.message == "RegisterNotFound":
     return JSONResponse(status_code=400, content=jsonable_encoder(response))
    if response.message == "RegisterFound":
     return JSONResponse(status_code=302, content=jsonable_encoder(response))
    if response.message == "UnexpectedError":
     return JSONResponse(status_code=500, content=jsonable_encoder(response))
    
    return JSONResponse(status_code=200,content=jsonable_encoder(response))
