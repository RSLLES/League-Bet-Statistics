
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from utils import RequestSender, MatchesEngine, matchStringsScore
from interpretors.InterpretorsEngine import InterpretorsEngine
import config

############
### CODE ###
############

def main():
    requestSender = RequestSender(config.time_between_request)
    nitrogen_matches = MatchesEngine(
        data_unmatched_file="data/data_unmatched.json",
        id_file="data/id_history.json",
        data_matched_path="data/processed/"
    )
    min_date = datetime.now() - timedelta(days=config.past_days_to_scrape)
    nitrogen_matches.purge(config.past_days_to_scrape + 1)
    if len(nitrogen_matches) == 0:
        print("There is no match left in data_unmatched.json. Exit.")
        exit()
    
    for match in scrape_matches(min_date, requestSender):
        teamsNames = get_teams_names(match)
        print(f"Searching for {teamsNames}'s match in unmatched data file ...")
        if match_id := nitrogen_matches.find(teamsNames, match['date']):
            if not nitrogen_matches.isUnmatched(match_id):
                print("Match already processed. Skipped.")
                continue
            match_bets = nitrogen_matches[match_id]
            try:
                interpretors = InterpretorsEngine(match_bets)
                for timeline, teams_side in scrape_games(match, requestSender):
                    for line in parse_timeline(timeline, interpretors.teams(), teams_side):
                        interpretors(line)
                    interpretors.next_game()
                print(f"Export {match_id}")
                nitrogen_matches.export(interpretors.export(), match_id)
            except Exception as e:
                print(e)
                print("Continue with next match")

def get_teams_names(match : dict):
    return match['teams'].split(' vs ')

def search_in_dic(text : str, dic : dict, default : str, raise_exc : bool) -> str :
    for key in dic:
        # Transform in dictionnary
        if type(dic[key]) == list:
            over = dic[key]
        elif type(dic[key]) == str:
            over = [dic[key]]
        elif type(dic[key]) == int:
            continue
        else:
            raise ValueError(f"Values in dictionnary should be strings or list of strings. Here, dic[{key}] = {dic[key]}.")

        for e in over:
            if text == e:
                return key

    if not raise_exc:
        if default:
            print(default)
        return None
    raise ValueError(default)

def parse_timeline(timeline : list[BeautifulSoup], teams : list[str], side : dict[str]) -> BeautifulSoup:
    # Attribution des couleurs
    normal = matchStringsScore(teams['t1'], side['blue']) + matchStringsScore(teams['t2'], side['red'])
    reverse = matchStringsScore(teams['t2'], side['blue']) + matchStringsScore(teams['t1'], side['red'])
    
    teams_side_to_idx = {
        'blue' : 't1',
        'red' : 't2'
    } if normal > reverse else {
        'blue' : 't2',
        'red' : 't1'
    }

    for tr in timeline:
        if not tr.has_attr('onmouseout'):
            continue
        tds = tr.find_all("td")

        # Action
        action_td = tds[config.timeline['actions']['idx']]
        try:
            action_td = action_td.find('img')[config.timeline['actions']['attr']]
        except:
            action_td = None
            
        action = search_in_dic(
            text = action_td, 
            dic = config.timeline['actions'], 
            default=None,
            raise_exc=False)

        if not action:
            continue

        # Time
        time = tds[config.timeline['timecode']['idx']].text

        # Color
        img_color = tds[config.timeline['colors']['idx']]
        try:
            img_color = img_color.find('img')[config.timeline['colors']['attr']]
        except:
            img_color = None
        color = search_in_dic(
            text = img_color, 
            dic = config.timeline['colors'], 
            default=f"Img nor red or blue : {img_color}",
            raise_exc=True)
        

        yield {
            'time' : time,
            'team' : teams_side_to_idx[color],
            'action' : action
        }

def format_teams_side(divs : list[BeautifulSoup]) -> dict[str]:
    return {
        'blue' : divs[0].find("a").text,
        'red' : divs[1].find("a").text
    }

def scrape_games(match : dict, requestSender : RequestSender):
    id, id_last_game = match['id'], float("inf")
    while id < id_last_game:
        # Request game
        game = requestSender.sendRequest(url=config.url_timeline(id))

        # get Teams Color
        teams_side = game.select(config.selectors['teams_names'])
        teams_side = format_teams_side(teams_side)

        # Get Timeline
        timeline = game.select_one(config.selectors['timeline']).find_all("tr")

        # Extract id_last_game
        id_last_game = match['id'] + getNbGame(game) if id_last_game == float("inf") else id_last_game

        # Return game
        yield timeline, teams_side
        id += 1

def getNbGame(game : BeautifulSoup):
    buttons = game.select(config.selectors['nav_menu'])
    game_buttons = list(filter(lambda button : "Game" in button.text, buttons))
    return len(game_buttons)

def scrape_matches(min_date : datetime, requestSender : RequestSender):
    min_date_among_scrapped = datetime.now()
    i = 0
    while min_date_among_scrapped > min_date:
        # Iterating over scrapped matchs
        matchs = requestSender.sendRequest(
            url = config.url_last_match,
            data =  {'start' : str(i)},
            method = "POST"
        )
        for match in matchs:
            date = datetime.strptime(match['game_date'], config.date_format)
            min_date_among_scrapped = min(min_date_among_scrapped, date)
            yield {
                'date' : date,
                'id' : int(match['game_id']),
                'teams' : match['game_name']
            }
        i += len(matchs)



if __name__ == "__main__":
    main()
