from typing import Optional, List

from pydantic import BaseModel


class TopHeroes(BaseModel):
    top_hero: str = None
    top_killer: str = None
    top_assister: str = None
    longest_game: str = None
    top_farmer: str = None
    top_pusher: str = None


class PreviousSeasonsStats(BaseModel):
    num: int
    rank_type: str
    kills_num: int
    deaths_num: int


class Player(BaseModel):
    name: str
    rank_type: str
    pts: int
    win_num: int
    lose_num: int
    leave_num: int
    couriers_killed: int
    neutrals_killed: int
    hours_in_game: int
    win_ratio: int
    best_stats_hero: str = None
    best_stats_kill: int
    best_stats_death: int
    best_stats_assist: int
    max_win_streak: int
    current_streak: int

    top_heroes: TopHeroes

    prev_seasons: Optional[List[PreviousSeasonsStats]] = None


class PlayerInGameStats(BaseModel):
    name: str
    hero_name: str
    streak: int
    reward: int


class Game(BaseModel):
    id_: str
    date: str
    name: str
    host: str
    duration: str
    server: str
    map_version: str

    sentinel_heroes: List[PlayerInGameStats]
    scourge_heroes: List[PlayerInGameStats]

    winner: Optional[str] = None
