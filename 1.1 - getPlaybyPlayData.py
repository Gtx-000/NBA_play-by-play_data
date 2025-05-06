

# get play by play data

# game_id = '0022101183'
from nba_api.stats.endpoints import playbyplayv2
import pandas as pd
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
import requests
import os
from nba_api.stats.endpoints import leaguegamefinder

# pbp = playbyplayv2.PlayByPlayV2(game_id)
# pbp = pbp.get_data_frames()[0]
# print(pbp.head())
# print(pbp.tail(10))

# get box score data
from nba_api.stats.endpoints import boxscoretraditionalv2
# player_stat_data = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
# stats_df = player_stat_data.get_data_frames()[0]
# print(stats_df.tail())

'''
Get 2021-22 Play-by-Play Data using Game Ids
从api直接获取的数据和从爬虫爬网站的方式获得的数据相同，之所以事件数目不同是因为有些事件的参与者不止一个人，
比如抢断就包括抢断人和被抢断人
从api获得的数据整合起来更好一些
'''

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

os.environ['NO_PROXY'] = 'stats.nba.com'

# def get_data(game_id):
#     play_by_play_url = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_"+game_id+".json"
#     response = requests.get(url=play_by_play_url, headers=headers).json()
#     play_by_play = response['game']['actions']
#     df = pd.DataFrame(play_by_play)
#     df['gameid'] = game_id
#     return df

# using this for testing purposes only
# sample_game_ids = [
#     '0022001070',
#     '0022001077',
#     '0022001068',
#     '0022001074']

# pbpdata = []

def get_new_season_play_by_play(season_, Regular_or_playoffs):

    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season_,
                                                   league_id_nullable='00',
                                                   season_type_nullable=Regular_or_playoffs)
    games = gamefinder.get_data_frames()[0]
    # print(games.head())

    # get a list of the distinct game_ids
    game_ids = games['GAME_ID'].unique().tolist()
    print(game_ids)

    record_flag = 0
    for game_id in game_ids:

        # if game_id == '0021300829':
        #     record_flag = 1

        # if record_flag == 1:
            pbp = playbyplayv2.PlayByPlayV2(game_id)
            pbp_pd = pbp.get_data_frames()[0]
            # print(pbp_pd)
            path = './2012-2013-Playoffs-PlayByPlay\\' + game_id + '.csv'
            print(path)
            # pbp_pd.to_csv(path)

        # break

# print(game_ids)
# print(max([int(x) for x in game_ids]))


def find_others(season_, Regular_or_playoffs):

    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season_,
                                                   league_id_nullable='00',
                                                   season_type_nullable=Regular_or_playoffs)
    games = gamefinder.get_data_frames()[0]
    # print(games.head())

    # get a list of the distinct game_ids
    game_ids = games['GAME_ID'].unique().tolist()

    already_have = []
    for root, dirs, files in os.walk('./2013-2014-Regular-PlayByPlay'):
        for file in files:
            already_have.append(file.split('.')[0])
    print(len(game_ids), len(already_have))
    buji = list(set(game_ids).difference(set(already_have)))
    print(len(buji))

    for game_id in buji:
    #     if int(game_id) < 22100415:
        pbp = playbyplayv2.PlayByPlayV2(game_id)
        pbp_pd = pbp.get_data_frames()[0]
        # pbpdata.append(pbp)

        # final_df = pd.concat(pbpdata, ignore_index=True)
        # print(final_df)
        path = './2013-2014-Regular-PlayByPlay\\' + game_id + '.csv'
        print(path)
        pbp_pd.to_csv(path)
            # break


if __name__ == '__main__':
    season_ = '2012-13'
    Regular_or_playoffs = 'Playoffs'  # Playoffs   # Regular Season
    get_new_season_play_by_play(season_, Regular_or_playoffs)
    # find_others(season_, Regular_or_playoffs)