from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from application.shortened.usecase.get_short_url_usecase import get_long_url_by_short_url_use
from infra.handlers.dtos.response import ResponseDTO

def get_long_url_by_short_url_handler(hash_url: str, token: str) -> ResponseDTO:
    response = get_long_url_by_short_url_use(hash_url, token)
    if response.message == "Unauthorized":
     return JSONResponse(status_code=401, content=jsonable_encoder(response))
    if response.message == "UserNotfound":
     return JSONResponse(status_code=400, content=jsonable_encoder(response))
    if response.message == "RegisterFound":
     return JSONResponse(status_code=302, content=jsonable_encoder(response))
    if response.message == "UnexpectedError":
     return JSONResponse(status_code=500, content=jsonable_encoder(response))
    
    return JSONResponse(status_code=200,content=jsonable_encoder(response))
