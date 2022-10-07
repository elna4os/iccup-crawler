import re

import requests
from bs4 import BeautifulSoup

from .models import Player, TopHeroes, PreviousSeasonsStats

player_base_url = 'https://iccup.com/dota/gamingprofile'
default_image_str = 'default image0'


def parse_player(name: str) -> Player:
    # Read page
    url = f'{player_base_url}/{name}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Main stats
    left_col, right_col = soup.find_all('table', {'class': 'stata-body left'})
    left_col_tr = left_col.find_all('tr')
    right_col_tr = right_col.find_all('tr')
    rank_type = left_col_tr[1].find_all('td')[1].find_all('div')[0]['class'][0]
    pts = int(left_col_tr[1].find_all('td')[1].find_all('div')[0]['title'])
    win_num, lose_num, leave_num = map(
        int,
        left_col_tr[2].find_all('td')[1].getText().replace(' ', '').split('/')
    )
    couriers_killed = int(left_col_tr[3].find_all('td')[1].getText())
    neutrals_killed = int(left_col_tr[4].find_all('td')[1].getText())
    hours_in_game = int(re.sub(
        '\D',
        '',
        left_col_tr[5].find_all('td')[1].getText()
    ))
    win_ratio = int(right_col_tr[0].find_all('td')[1].getText()[:-1])
    best_stats = right_col_tr[2].find_all('td')[1].find_all('a')
    if best_stats:
        best_stats_hero = best_stats[0].find_all('img')[0]['title']
        best_stats_kill, best_stats_death, best_stats_assist = map(
            int,
            best_stats[0].find_all('span')[0].getText().replace(' ', '').split('-')
        )
    else:
        best_stats_hero = None
        best_stats_kill, best_stats_death, best_stats_assist = [0, 0, 0]
    max_win_streak = int(right_col_tr[3].find_all('td')[1].getText())
    current_streak = int(right_col_tr[4].find_all('td')[1].getText())

    # Top heroes block
    top_heroes_containers = soup.find_all('div', {'class': 'top-heroes-container'})
    top_hero = top_heroes_containers[0].find_all('div', {'class': 'top-hero'})[0].find_all('img')[0]['alt']
    top_killer = top_heroes_containers[0].find_all('div', {'class': 'top-hero'})[1].find_all('img')[0]['alt']
    top_assister = top_heroes_containers[0].find_all('div', {'class': 'top-hero'})[2].find_all('img')[0]['alt']
    longest_game = top_heroes_containers[1].find_all('div', {'class': 'top-hero'})[0].find_all('img')[0]['alt']
    top_farmer = top_heroes_containers[1].find_all('div', {'class': 'top-hero'})[1].find_all('img')[0]['alt']
    top_pusher = top_heroes_containers[1].find_all('div', {'class': 'top-hero'})[2].find_all('img')[0]['alt']

    # Previous seasons
    previous_seasons = []
    for prev_season_data in soup.find_all('div', {'class': 'season-num'}):
        kn, dn = map(
            int,
            prev_season_data.find_all('div', {'class': 'season-5x5'})[0].getText().replace(' ', '').split('-')
        )
        to_append = PreviousSeasonsStats(
            num=int(prev_season_data.find_all('div', {'class': 'pull-left'})[0].getText().split()[-1][1:]),
            rank_type=prev_season_data.find_all('div', {'class': 'season-5x5'})[0].find_all('div')[0]['class'][0],
            kills_num=kn,
            deaths_num=dn
        )
        previous_seasons.append(to_append)

    return Player(
        name=name,
        rank_type=rank_type,
        pts=pts,
        win_num=win_num,
        lose_num=lose_num,
        leave_num=leave_num,
        couriers_killed=couriers_killed,
        neutrals_killed=neutrals_killed,
        hours_in_game=hours_in_game,
        win_ratio=win_ratio,
        best_stats_hero=best_stats_hero,
        best_stats_kill=best_stats_kill,
        best_stats_death=best_stats_death,
        best_stats_assist=best_stats_assist,
        max_win_streak=max_win_streak,
        current_streak=current_streak,
        top_heroes=TopHeroes(
            top_hero=top_hero if top_hero != default_image_str else None,
            top_killer=top_killer if top_killer != default_image_str else None,
            top_assister=top_assister if top_assister != default_image_str else None,
            longest_game=longest_game if longest_game != default_image_str else None,
            top_farmer=top_farmer if top_farmer != default_image_str else None,
            top_pusher=top_pusher if top_pusher != default_image_str else None
        ),
        prev_seasons=previous_seasons
    )
