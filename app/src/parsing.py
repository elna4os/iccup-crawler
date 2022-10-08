import re

import requests
from bs4 import BeautifulSoup

from .models import Player, TopHeroes, PreviousSeasonsStats, Game, PlayerInGameStats

player_base_url = 'https://iccup.com/dota/gamingprofile'
game_base_url = 'https://iccup.com/dota/details/'
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
    hours_in_game_str = left_col_tr[5].find_all('td')[1].getText()
    if hours_in_game_str == '< 1':
        hours_in_game = 0
    else:
        hours_in_game = int(re.sub('\D', '', hours_in_game_str))
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


def parse_game(id_: str) -> Game:
    # Read page
    url = f'{game_base_url}/{id_}.html'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Meta
    meta = soup.find_all('div', {'class': 't-im width420'})[0].find_all('div', {'class': 't-corp2'})
    date = meta[0].find_all('div', {'class': 'field2'})[0].getText()
    name = meta[1].find_all('div', {'class': 'field2'})[0].getText()
    host = meta[2].find_all('div', {'class': 'field2'})[0].getText()
    duration = meta[3].find_all('div', {'class': 'field2'})[0].getText()
    server = meta[4].find_all('div', {'class': 'field2'})[0].getText()
    map_version = meta[5].find_all('div', {'class': 'field2'})[0].getText()

    # Helper stats
    helper_stats = soup.find_all('div', {'class': 'pg-dota-stat'})[0].find_all(
        'div',
        {'class': lambda x: x.startswith('t-corp2')}
    )

    # Sentinel
    sentinel = soup.find_all('div', {'class': 'right-info team-looser'})[0].find_all(
        'div',
        {'class': 'list-info'}
    )[0].find_all('div', {'class': 'block-info'})
    sentinel_stats = []
    for i, player in enumerate(sentinel):
        player_name = player.find_all('a')[1].getText()
        hero_name = helper_stats[i].find_all('img')[1]['title']
        streak = int(player.find_all('span', {'class': 'streak-count'})[0].getText())
        reward = int(player.find_all('div', {'class': 'details-points'})[0].getText())
        sentinel_stats.append(PlayerInGameStats(
            name=player_name,
            hero_name=hero_name,
            streak=streak,
            reward=reward
        ))

    # Scourge
    scourge = soup.find_all('div', {'class': 'left-info team-winner'})[0].find_all(
        'div',
        {'class': 'list-info'}
    )[0].find_all('div', {'class': 'block-info'})
    scourge_stats = []
    for i, player in enumerate(scourge):
        player_name = player.find_all('a')[1].getText()
        hero_name = helper_stats[i + 5].find_all('img')[1]['title']
        streak = int(player.find_all('span', {'class': 'streak-count'})[0].getText())
        reward = int(player.find_all('div', {'class': 'details-points'})[0].getText())
        scourge_stats.append(PlayerInGameStats(
            name=player_name,
            hero_name=hero_name,
            streak=streak,
            reward=reward
        ))

    # Winner
    winner = None
    sentinel_reward = sum([x.reward for x in sentinel_stats])
    scourge_reward = sum([x.reward for x in scourge_stats])
    if sentinel_reward > 0:
        winner = 'sentinel'
    elif scourge_reward > 0:
        winner = 'scourge'

    return Game(
        id_=id_,
        date=date,
        name=name,
        host=host,
        duration=duration,
        server=server,
        map_version=map_version,
        sentinel_heroes=sentinel_stats,
        scourge_heroes=scourge_stats,
        winner=winner
    )
