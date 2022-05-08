import json
import re
from os.path import join
from datetime import datetime, timedelta
from time import sleep, time


import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from config import correctifs

### Tool to import matches from data.json
class MatchesEngine:
    def __init__(self, data_unmatched_file, id_file, data_matched_path) -> None:
        self.data_matched_path = data_matched_path
        self.data_unmatched_file = data_unmatched_file
        self.score_threshold = 0.8
        with open(data_unmatched_file) as f:
            self.data = json.loads(f.read())
        
        self.id_file = id_file
        with open(id_file) as f:
            self.id_data = json.loads(f.read())
            if not "matched" in self.id_data:
                self.id_data["matched"] = []

    def purge(self, days_back):
        min_date = datetime.now() - timedelta(days=days_back)
        removed_keys = []
        for key in self.data:
            date = self.data[key]["date"]
            date = datetime(
                year=int(date["year"]),
                month=int(date["month"]),
                day=int(date["day"])
            )
            if date < min_date:
                print(f"{self.data[key]['teamNames']['t1']} VS {self.data[key]['teamNames']['t2']} is too old to be keeped. Removed.")
                removed_keys.append(key)
        
        for key in removed_keys:
            self.data.pop(key, None)

        with open(self.data_unmatched_file, "w") as f:
            f.write(json.dumps(self.data, indent=4))

    def __len__ (self):
        return len(self.data)
    
    def export(self, match_processed, match_id):
        with open(join(self.data_matched_path, match_id + ".json"), "w") as f:
            f.write(json.dumps(match_processed, indent=4))
        
        self.id_data['matched'] += [match_id]
        with open(self.id_file, "w") as f:
            f.write(json.dumps(self.id_data, indent=4))

    def isUnmatched(self, match_id):
        return match_id not in self.id_data["matched"]

    def __getitem__ (self, key):
        return self.data[key]

    def find (self, teamsNames, date : datetime):
        def score(key):
            data_date = self.data[key]['date']
            if f"{date.day}-{date.month}-{date.year}" != f"{data_date['day']}-{data_date['month']}-{data_date['year']}":
                return 0.0
            teamsNamesData = [self.data[key]['teamNames']['t1'], self.data[key]['teamNames']['t2']]
            return self.matchTeamsNames(teamsNames, teamsNamesData)
        scores = list(map(score, self.data))
        key, best_score = max(zip(self.data, scores), key= lambda x : x[1])
        data_teamsNames = [self.data[key]['teamNames']['t1'], self.data[key]['teamNames']['t2']]
        if best_score >= self.score_threshold:
            print(f"Find match with {data_teamsNames} (score = {best_score}).")
            return key
        print(f"No match found. {data_teamsNames} achieved the best score of {best_score}.")
        return None

    def matchTeamsNames(self, teamsNames1, teamsNames2):
        a = matchStringsScore(teamsNames1[0], teamsNames2[0]) + matchStringsScore(teamsNames1[1], teamsNames2[1])
        b = matchStringsScore(teamsNames1[0], teamsNames2[1]) + matchStringsScore(teamsNames1[1], teamsNames2[0])
        return max((b, a))/2.0

### Tool to send Request
class RequestSender:
    def __init__(self, time_between_request, proxy=None) -> None:
        self.last_request_time = 0
        if proxy != None :
            self.proxy = { 'https' : f"https://{proxy['credentials']['username']}:{proxy['credentials']['password']}@{proxy['address']}:{proxy['port']}" }
        self.deltaT = time_between_request
        self.headers = {'User-Agent' : generate_user_agent(os=('win', 'mac'))}
        # headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}


    def sendRequest(self, url : str, data = {}, method="GET"):
        assert method in ["GET", "POST"], "Method must be in ['GET', 'POST']"

        # Waiting to avoid flood ban
        while time() - self.last_request_time < self.deltaT:
            print(f"Waiting {(time() - self.last_request_time):0.1f}s/{self.deltaT}s.",end='\r')
            sleep(0.1)
        
        # Sending request
        if method == "GET":
            print(f"Sending {method} request to {url}.")
            rep = requests.get(url, headers=self.headers)
        if method == "POST":
            print(f"Sending {method} request to {url} with {data}.")
            rep = requests.post(url, data, headers=self.headers)

        self.last_request_time = time()
        return BeautifulSoup(rep.content, 'html.parser') if method == "GET" else json.loads(rep.text)


def matchStringsScore(str1 : str, str2 : str) -> float:
    str1, str2 = format_string(str1), format_string(str2)
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    metrics_and_coeffs = [
        (_matchLetters, 1.0),
        (_matchOrder, 2.0)
    ]

    scores = list(map(lambda X : X[0](str1, str2)*X[1], metrics_and_coeffs))
    return sum(scores)/sum([coeffs for _, coeffs in metrics_and_coeffs])

def format_string(text : str) -> str:
    for word in correctifs:
        if word in text:
            text = text.replace(word, correctifs[word])
    text = re.sub('[\W_]', '', text.lower())
    return text


def _matchLetters(str1 : str, str2 : str) -> float:
    letter_present = map(lambda letter : int(letter in str2), str1)
    return sum(letter_present)/len(str1)


# def _matchOrder(str1 : str, str2 : str) -> float:
#     i = 0
#     for letter2 in str2:
#         if i >= len(str1): # Cas rare quand par ex str1 = "G2" et str2 = "G2 Esport" : on sortait de G2
#             return 1.0
#         letter1 = str1[i]
#         if letter1 == letter2:
#             i += 1
#     return i / len(str1)

def _isInside(a : int, b : int, x : int) -> bool:
    return a < x and x < b

def _areConsecutives(L : list[int], a : int, b : int):
    for x in L:
        if a >= b or _isInside(a, b, x):
            return False
    return True

def _scoreList (L : list[int]) -> int:
    res = [_areConsecutives(L, L[i], L[i+1]) for i in range(len(L) - 1)]
    return sum(res)

def _newElement(all_patterns, element):
    if len(element) == 0:
        return all_patterns
    all = []
    for x in element:
        for pattern in all_patterns:
            all.append(pattern.copy() + [x])
    return all

def _matchOrder(str1 : str, str2 : str) -> float:
    if len(str1) == 1:
        return 0.0
    
    all_patterns = [[]]
    for letter1 in str1 :
        positions = [i for i, letter2 in enumerate(str2) if letter1 == letter2]
        all_patterns = _newElement(all_patterns, positions)
    s = list(map(_scoreList, all_patterns))
    return max(s)/(len(str1)-1)


if __name__ == "__main__":
    a = _scoreList([1, 5, 5, -1, 19, 22])
    a = _matchOrder("CFSFT", "Folli Stone Frange")
    print(a)
    print(format_string("Ceci est un test Pour voir . + et ouais mon gars !"))
