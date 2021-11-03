import requests, datetime

# team = input("Type the name of the team: ")
# search_query = input("What do you want todo: [please enter the following]: searchteams")
# req = f"https://www.thesportsdb.com/api/v1/json/1/{query}.php?t={t.capitalize()}"
class the_sportsdb_api:
    # BY SEARCH
    def search_by_team_name(team_name, query='searchteams'):
        """(str, str) --> list()
        Takes team name, and a querry and returns the list.
        """
        # We want to return information on for this keys. 
        teams_keys = ['strTeam', 'intFormedYear', 'strSport', 'strLeague', 'idLeague', 'strLeague2', 'idLeague2', 'strDivision',
                    'strManager', 'strStadium', 'strStadiumDescription', 'strStadiumLocation', 'intStadiumCapacity', 'strWebsite']

        url = f"https://www.thesportsdb.com/api/v1/json/1/{query.lower()}.php?t={team_name.capitalize()}" #making a request with specified paramenters from the user
        res = requests.get(url)
        text = res.json() #convert the response into json

        data_list =  [] 
        for i in range(len(text['teams'])):
            team_data = {} #store the data here after every loop.
            for j in range(len(teams_keys)):
                if teams_keys[j] in teams_keys: #check if a key is in the list 'team_keys' if true;
                    team_data[teams_keys[j]] = text['teams'][i][teams_keys[j]]
                else:
                    continue
            #before doing another interation for another obhject, append the data in the data_list
            data_list.append(list[team_data])
        #return list of dictionaries
        print(data_list)
        return data_list

    def search_by_player_name(first_name, last_name, search_players='searchplayers'):
        
        url = f"https://www.thesportsdb.com/api/v1/json/1/{search_players.lower()}.php?p={first_name.capitalize()}%20{last_name.capitalize()}"
        req = requests.get(url)
        result = req.json()
        
        # Assume that api returns only one list of players information; in anyway also assume that regardless of the player name 
        #The dict keys are always the same
        #loop through the dict keys and store them in the list format
        player_keys = []
        for key in result['player'][0].keys():
            player_keys.append(key)

        player_final_info = [] #store the final relevant players information
        for i in range(len(result['player'])):
            player_data = {}
            for j in range(len(player_keys)):
                if result['player'][i][player_keys[j]] != None:
                    if result['player'][i][player_keys[j]] != '': #if the dict value at index of j is not null add it to the dict `player_data`
                        player_data[player_keys[j]] = result['player'][i][player_keys[j]]
                    else:
                        continue
                else: # if the key `result['player][i][original_key[j]]` value is none or empty
                        # continue to the next key element
                    continue
            player_final_info.append([player_data])
        print(player_final_info)
        return player_final_info

    def search_by_event_name(first_team, second_team, year=datetime.datetime.today().year):
        season_year = str(year-1) + '_' + str(year) #deafault season will be current season.
        vs_str = '_vs_'
        url = f'https://www.thesportsdb.com/api/v1/json/1/searchevents.php?e={first_team.capitalize()}{vs_str}{second_team.capitalize()}&s={season_year}'
        req = requests.get(url)
        response = req.json()
        # This loop extracts keys from `dict object` and stores them in the list `event_keys`
        event_keys = []
        for key in response['event'][0].keys():
            event_keys.append(key)

        # loop through and check if a given key is empty or has value None.
        event_final_info = []
        for i in range(len(response['event'])):
            event_data = {}
            for j in range(len(event_keys)):
                #check if the `event_keys[j]` is not equal to None or empty
                if response['event'][i][event_keys[j]] != None:
                    if response['event'][i][event_keys[j]] != '':
                        event_data[event_keys[j]] = response['event'][i][event_keys[j]]
                    else:
                        continue
                else:
                    continue
            event_final_info.append(event_data)
        print(event_final_info)
        return event_final_info

# BY LIST
    def list_all_sports():
        url = 'https://www.thesportsdb.com/api/v1/json/1/all_sports.php'
        req = requests.get(url)
        response = req.json()
        
        sports_keys = []
        for keys in response['sports'][5].keys():
            sports_keys.append(keys)
        # list of available sports and their description
        for i in range(len(response['sports'])):
            for j in range(len(sports_keys)):
                if sports_keys[j] == "strSport":
                    print(response['sports'][i][sports_keys[j]])
                    
the_sportsdb_api.list_all_sports()
