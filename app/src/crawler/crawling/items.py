import scrapy


class PlayerProfile(scrapy.Item):
    name = scrapy.Field()
    rank_type = scrapy.Field()
    rank_num = scrapy.Field()
    win_num = scrapy.Field()
    lose_num = scrapy.Field()
    leave_num = scrapy.Field()
    couriers_killed = scrapy.Field()
    neutrals_killed = scrapy.Field()
    hours_in_game = scrapy.Field()
    win_ratio = scrapy.Field()
    best_stats_kill = scrapy.Field()
    best_stats_death = scrapy.Field()
    best_stats_assist = scrapy.Field()
    best_stats_hero = scrapy.Field()
    max_win_streak = scrapy.Field()
    current_streak = scrapy.Field()

    top_hero = scrapy.Field()
    top_killer = scrapy.Field()
    top_assister = scrapy.Field()
    longest_game = scrapy.Field()
    top_farmer = scrapy.Field()
    top_pusher = scrapy.Field()

    prev_seasons = scrapy.Field()


class GameInfo(scrapy.Item):
    id_ = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    host = scrapy.Field()
    length = scrapy.Field()
    server = scrapy.Field()
    map_version = scrapy.Field()

    sentinel_heroes = scrapy.Field()
    scourge_heroes = scrapy.Field()

    players_stats = scrapy.Field()
