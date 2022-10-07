import os

import uvicorn
from fastapi import FastAPI

from src.models import Player
from src.parsing import parse_player

APP = FastAPI(title='iCCup crawler')


@APP.get(
    '/players/{name}',
    response_model=Player
)
async def get_players(name: str) -> Player:
    return parse_player(name=name)


if __name__ == '__main__':
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 5000))
    uvicorn.run(APP, host=host)
