import os

import uvicorn
from fastapi import FastAPI

from src.models import Player, Game
from src.parsing import parse_player, parse_game

APP = FastAPI(title='iCCup crawler')


@APP.get(
    '/players/{name}',
    response_model=Player
)
async def get_player(name: str) -> Player:
    return parse_player(name=name)


@APP.get(
    '/games/{id}',
    response_model=Game
)
async def get_game(id_: str) -> Game:
    return parse_game(id_=id_)


if __name__ == '__main__':
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 5000))
    uvicorn.run(APP, host=host)
