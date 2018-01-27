import requests
import json
from pprint import pprint
import lxml.html
import os


class APIError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

# Master Key
API_TOKEN = "" #Token for the Clash of Clans API
tags = {"RABID_UNICORNS": "%23JC0L922Y", "KINNICK_SOCIETY": "%23UVRY9PV", "RSN": "%23PCUR9P9Y"} #tags for the clans
HEADERS = {'Accept': 'application/json','authorization':'Bearer: ' + API_TOKEN}

def clan_data(clan):
    try:
        clan_data_url = "https://api.clashofclans.com/v1/clans/{}".format(tags[clan])
    except KeyError:
        clan_data_url = "https://api.clashofclans.com/v1/clans/%23{}".format(clan[1:])
    finally:
        response = requests.get(clan_data_url, headers=HEADERS)
        if response.status_code != 200:
            raise APIError(response.status_code, response.text)
        else:
            #print(clanResponse.json()['items'])
            return response.json()

def clan_members_list(clan):
    """gets a list of all clan members from the Clash of Clans API and returns the parsed JSON"""
    clan_member_url = 'https://api.clashofclans.com/v1/clans/{}/members'.format(tags.get(clan))
    response = requests.get(clan_member_url,headers=HEADERS)
    if response.status_code != 200:
        raise APIError(response.status_code, response.text)
    else:
        return response.json()['items']

def member_info(tag):
    """pulls the api for individual characters and returns the parsed JSON"""
    member_info_url = 'https://api.clashofclans.com/v1/players/%23{}'.format(tag[1:])
    response = requests.get(member_info_url,headers=HEADERS)
    if response.status_code != 200:
        raise APIError(response.status_code, response.text)
    else:
        return response.json()

def war_data(clan):
    war_url = 'https://api.clashofclans.com/v1/clans/{}/currentwar'.format(tags.get(clan))
    response = requests.get(war_url,headers=HEADERS)
    if response.status_code !=200:
        raise APIError(response.status_code, response.text)
    else:
        return response.json()

def war_log(clan):
    war_log_url = 'https://api.clashofclans.com/v1/clans/{}/warlog?limit=1'.format(tags.get(clan))
    response = requests.get(war_log_url, headers=HEADERS)
    if response.status_code != 200:
        raise APIError(response.status_code, response.text)
    else:
        return response.json()


    
def append_file(file, content):
    """Add data to the end of the given file.
    
    Arguments: 
        file (string): The name of the file to write to. 
        content (string): The data to be written. 
    
    Returns:
        int: Number of characters written.
    """
    with open(os.path.join("text files", file), "a") as f:
        return f.write(content)


def write_file(file, content):
    """Write data to  the given file.
    
    Arguments: 
        file (string): The name of the file to write to. 
        content (string): The data to be written. 
    
    Returns:
        int: Number of characters written.
    """
    with open(os.path.join("text files", file), "w") as f:
        return f.write(content)


def read_file(file):
    """Open a file and return the text within it.
    
    Arguments:
        file (string): The name of the file to open. 
    
    Returns:
        string: Text found within the file. 
    """
    with open(os.path.join("text files", file), "r") as f:
        return f.read()
    




    
    
    
    
    