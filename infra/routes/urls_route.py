from fastapi import APIRouter, Header
from fastapi.security import HTTPBasic
from infra.handlers.create_long_url_handler import create_short_url_handler
from infra.handlers.get_long_url_handler import get_long_url_by_short_url_handler
from infra.handlers.delete_short_url_handler import delete_long_short_url_handler
from infra.handlers.redirect_to_long_url_handler import redirect_to_long_url_handler
from infra.handlers.get_all_short_url_used_handler import get_all_short_url_used_handler
from infra.handlers.get_all_platforms_and_browser_used_handler import get_all_platforms_and_browser_used_handler
from infra.handlers.get_all_records_clicks_used_handler import get_all_records_clicks_used_handler
from infra.handlers.dtos.shortened_url import ShortenedUrlRequestDTO


shortened = APIRouter()
redirect = APIRouter()
security = HTTPBasic()

@shortened.post('/')
def create_short_url(long_url: ShortenedUrlRequestDTO, token: str =Header(None, alias='Authorization')):
     return create_short_url_handler(long_url.long_url, token)

@shortened.get('/record/register')
def get_all_short_url_used(token: str =Header(None, alias='Authorization')):
     return get_all_short_url_used_handler(token)

@shortened.get('/record/platforms/used')
def get_all_platforms_and_browser_used(token: str =Header(None, alias='Authorization')):
     return get_all_platforms_and_browser_used_handler(token)

@shortened.get('/record/clicks/used/{hash_url}')
def get_all_records_clicks_used(hash_url:str,token: str =Header(None, alias='Authorization')):
     return get_all_records_clicks_used_handler(hash_url, token)

@shortened.get('/long-url-by/{hash_url}')
def get_long_url_by_short_url(hash_url: str, token: str =Header(None, alias='Authorization')):
     return get_long_url_by_short_url_handler(hash_url, token)

@shortened.delete('/delete-by/{hash_url}')
def delete_short_url(hash_url: str, token: str =Header(None, alias='Authorization')):
     return delete_long_short_url_handler(hash_url, token)

@redirect.get('/{hash_url}')
def redirect_sto_long_url(hash_url: str, header: str =Header(None, alias='User-Agent')):
     return redirect_to_long_url_handler(hash_url, header)
