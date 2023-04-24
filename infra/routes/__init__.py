from fastapi import FastAPI
from infra.routes.user_route import user
from infra.routes.urls_route import shortened, redirect

prefix = '/service/v1/short-url'
app = FastAPI()

app.include_router(user, prefix=prefix, tags=['Auth'])
app.include_router(shortened, prefix=prefix, tags=['Admin Treatment'])

app.include_router(redirect, tags=['User Redirect'])

