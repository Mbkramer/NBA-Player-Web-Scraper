# NBA player websraper
# By Max Kramer
# DATE: 11/01/2024
# Description: Scrape basic player data for all NBA players to from NBA reference.com

# Install modules
from bs4 import BeautifulSoup
import requests
import csv
import numpy as np
import os

################################################################################################
# Data Structures 
################################################################################################

################################################################################################
# Define nba_player data:
#
# the nba player class will be used to difine a player
# name = name of player
# path = url extension to specfic player season stats 
# nba_debut = the year marking this players entry into the nba
# last_season = the last year this player played in the NBA
# positions = all positions this player played in the NBA
# height = players height during the nba
# weight = players weight during the nba
# birthdate = the day this player was born
# college = the college that this player attended prioir to the NBA
################################################################################################
class nba_player:
    def __init__(self, name, ID, nba_debut, last_season, positions, height, weight, birthdate, college):
        self.name = name.replace('*', '')
        self.ID = ID
        self.nba_debut = nba_debut
        self.last_season = last_season
        self.positions = positions
        self.height = height
        self.weight = weight
        self.birthdate = birthdate.replace(',', '').strip()
        self.college = college.replace(',', '')

    def __str__(self):
        return self.name + "," + self.ID + "," +  self.nba_debut + "," +  self.last_season + "," +  self.positions + "," +  self.height + "," +  self.weight + "," +  self.birthdate + "," +  self.college + "\n"

    def print(self):
        return self.name + "," + self.ID + "," +  self.nba_debut + "," +  self.last_season + "," +  self.positions + "," +  self.height + "," +  self.weight + "," +  self.birthdate + "," +  self.college + "\n"

#List of lists holding nba_player classes arranged alphabetically
all_nba_players = []

################################################################################################
# Get player data from https://www.basketball-reference.com/players/{}/#players. 
# go through all player sites to extract player data into our nba_player class and all_nba_players list
################################################################################################

#get all player stats from basketball reference
def get_player_web_data():

    # no players have a name starting with x so 25 total entries
    players_by_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
    url_base = "https://www.basketball-reference.com/players/{}/#players"

    for letter in players_by_letter:
        url = url_base.format(letter)
        result = requests.get(url)

        with open("WEB_HTML/{}.html".format(letter), "w+") as f:
            f.write(result.text)

#csv of all name players
def get_player_csv_data(path):

    player_list = []

    with open(path) as page:

        reader_obj = csv.reader(page)

        for row in reader_obj: 
            player_list.append(nba_player(row[0], row[8], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    all_nba_players.append(player_list)

def innit_players():
    
    #TODO find a way to not hardcode this? currently no players with x last name but that could change
    players_by_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
    base_string = "WEB_HTML/{}.html"

    for letter in players_by_letter:

        with open(base_string.format(letter)) as f: 
            page = f.read()

        soup = BeautifulSoup(page, 'html.parser')

        player_list = []
        table = soup.find('table', id="players")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:

            hold_player =[]

            cols = row.find_all(['th', 'td'])
            link = row.find('a', href=True)

            path = link['href']
            ID = path[11:-5]
            
            cols = [ele.text.strip() for ele in cols]
            link = [ele.text.strip() for ele in link]
            
            hold_player.append([ele for ele in cols if ele])

            if len(hold_player[0]) == 8:
                player_list.append(nba_player(hold_player[0][0], ID, hold_player[0][1], hold_player[0][2], hold_player[0][3], hold_player[0][4], hold_player[0][5], hold_player[0][6], hold_player[0][7]))
            
            if len(hold_player[0]) == 7:
                player_list.append(nba_player(hold_player[0][0], ID, hold_player[0][1], hold_player[0][2], hold_player[0][3], hold_player[0][4], hold_player[0][5], hold_player[0][6], "NA"))

        all_nba_players.append(player_list)

#store all_nba_player list into a folder of csv files
def convert_all_nba_players_to_csv():

    with open("nba_players.csv", "w+") as f:
        for player_list in all_nba_players:
                for player in player_list:
                    f.write(player.print())

################################################################################################
# Prints
################################################################################################

# Now it just prints the all_nba_player list ;)
def print_all_nba_players_list():
    
    os.system('clear')
    print("Here are the results from scraping www.basketball-reference.com for player data.\n")
    count = 0

    for player_list in all_nba_players:
        print("There have been " + str(len(player_list)) + " nba players with last names starting with " + player_list[0].ID[0])
        count += len(player_list)

    print("total number of NBA players is " + str(count) + "\n")
    count = 0
        
################################################################################################
# Main Method
################################################################################################

def main():

    os.system('clear')

    user_input = ""
    print("\nWelcome to the nba web_scraper! Follow the commands below to get a csv of all NBA players from www.basketball-reference.com")
    print("The program works through three main steps executed in order:\n\n 1. Scrape the web for NBA player data. \n 2. Store this data locally via a list. \n 3. Convert this list into csv format.\n")
    print("WARNING! You will get shut out of the site if you srape data too frequently (Roughly 30 times within an hour)\nOnce the WEB_HTML folder is populated with html files a-z excluding x, you will no longer need to scrape web data.")
    print("You can leave the program at anytime by typing EXIT\n")

    while user_input != "exit":

        print("To scrape the web for all nba player data type SEARCH.")
        print("To interpret all of the html files in WEB_HTML, and store into a list of all nba players type READ.")
        print("To get a csv of all NBA players type CSV.")
        print("Leave the program by typing EXIT\n")
        
        user_input = input("\nEnter your colmmand: ").lower()

        if user_input == "search":
            get_player_web_data()
        
        if user_input == "read":
            if len(all_nba_players) == 0:
                innit_players()
            print_all_nba_players_list()

        if user_input == "csv":
            convert_all_nba_players_to_csv()


if __name__ == "__main__":
    main()