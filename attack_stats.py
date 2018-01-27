import inout
import json
import operator
import google_api
from attacker import Attacker
from pprint import pformat, pprint

SSID = '' # Stats Test Spreadsheet ID

logs = {"KINNICK_SOCIETY": "Kinnick Log.txt", "RSN": "RSN Log.txt", "RABID_UNICORNS": "Rabid Log.txt"}
"""dict: Names of the logs for each clan."""

# General Code
def parse_wars(wars):
    """Check to see if an Attacker instance exists, update attacks and return dictionary of attackers.
    
    Args: 
        wars (dict): dictionary of wars that are to be parsed {date: API Data}
    
    Return:
        dict: Attacker instances {Tag: Attacker Instance}.
        list: List of results from logged wars [[date, opponent, score]].
    """
    wars_logged = []
    attackers = {}
    for war in sorted(wars): 
        # print("Parsing War against {}".format(wars[war]["opponent"]["name"]))
        opponents = wars[war]["opponent"]["members"] #clan data for the war opponent
        members = wars[war]["clan"]["members"] #war data for clan stats being collected for
        
        opponent_th_levels = {opponent["tag"]: opponent["townhallLevel"] for opponent in opponents} 
        """Creates a dictionary of opponent ids and townhall level {tag: th level}"""
        
        start_number = len(attackers) #number of Attackers already in the dict to track attackers added. 
        
        for member in members:
            """Loop through the members and either adds them to the dictionary or updates that attacks"""
            if member["tag"] in attackers:
                attackers[member["tag"]].add_war(member.get("attacks"), opponent_th_levels)
            else: 
                attackers[member["tag"]] = Attacker(member, opponent_th_levels)
        # print("War against {} added {} attackers".format(wars[war]["opponent"]["name"], len(attackers)-start_number))
        
        wars_logged.append([war, wars[war]["opponent"]["name"], "{} - {}".format(wars[war]["clan"]["stars"],
                                                                                 wars[war]["opponent"]["stars"])])
    return attackers, wars_logged


def get_wars(war_log, num_of_wars, skip_last_wars):
    
    if not skip_last_wars:
        return {war: war_log[war]["warData"] for war in sorted(war_log)[-num_of_wars:]}# Dictionary of the wars that will be logged
    else:
        return {war: war_log[war]["warData"] for war in sorted(war_log)[-num_of_wars:-skip_last_wars]}# Dictionary of the wars that will be logged


#Code for updating Stats Spreadsheet    
def update_stats_ss(num_of_wars = 12, skip_last_wars = 0, clan = "KINNICK_SOCIETY"):
    """Update the Attack Stats Spreadsheet.
    
    Arguments:
        num_of_wars (int, optional): Number of wars to create stats for. Defaults to 12.
        skip_last_war (int, optional): Number of wars to skip at end of list. Defaults to 0.
        clan (string, optional): Name of the clan stats are being created for. Defaults to KINNICK_SOCIETY.
    """
    war_log = json.loads(inout.read_file(logs[clan])) # open the war log file

    wars = get_wars(war_log, num_of_wars, skip_last_wars)

    attackers, wars_logged = parse_wars(wars)
    
    save_to_spreadsheet(attackers, wars_logged)


def save_to_spreadsheet(attackers, wars_logged):
    """Call Google API to update the Spreadsheet
    
    Arguments:
        attackers (dictionary): dictionaries of the attackers to be stored in the SS {Tag: Attacker Instance}.
        wars_logged (list): List of the wars that have been logged.
    """
    elevens = [attackers[attacker].spreadsheet_list() for attacker in attackers if attackers[attacker].townhallLevel == 11]
    tens = [attackers[attacker].spreadsheet_list() for attacker in attackers if attackers[attacker].townhallLevel == 10]
    nines = [attackers[attacker].spreadsheet_list() for attacker in attackers if attackers[attacker].townhallLevel == 9]
    """Create a list of the attack information by townhall level to be added to a spreadsheet."""

    print(google_api.clear_range_values(SSID, "'Totals'!A3:R15","'Totals'!A19:R38","'Totals'!A42:R75", "'Wars'!A2:C"))
    """Clear the Ranges of the Attack Stats SS"""
    print(google_api.batch_update_cell_values(SSID, "USER_ENTERED", google_api.create_data_dict(elevens, "'Totals'!A3"), 
                                        google_api.create_data_dict(tens, "'Totals'!A19"), 
                                        google_api.create_data_dict(nines, "'Totals'!A42"), 
                                        google_api.create_data_dict(wars_logged, "'Wars'!A2")))
    """Add data to the attack stats spreadsheet."""
    print(google_api.batch_update(SSID, [google_api.sort_range(1653550080, 2, 0, len(elevens), 18, 3, "DESCENDING"), 
                                         google_api.sort_range(1653550080, 18, 0, len(tens), 18, 3, "DESCENDING"), 
                                         google_api.sort_range(1653550080, 41, 0, len(nines), 18, 4, "DESCENDING")]))
    """Sort each of the town hall levels by attack percentage."""







if __name__ == "__main__":
    attack_leaderboard()
    # update_stats_ss()
    
# http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html  