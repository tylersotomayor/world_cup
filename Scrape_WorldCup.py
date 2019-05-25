#!/usr/bin/env python
# coding: utf-8

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': 'C:/Users/Aboody/Chromedriver/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store in dictionary.
    data = {
        "2018": WC18(browser),
        "2017": WC14(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# def scrape_WC14():

#     # Initiate headless driver for deployment
#     executable_path = {'executable_path': 'C:/Users/Aboody/Chromedriver/chromedriver'}
#     browser = Browser('chrome', **executable_path, headless=False)

#     # Run all scraping functions and store in dictionary.
#     data = {
#         "Teams": teamsList14,
#         "Matches": matchesPlayed14,
#         "Avg Fouls Commited": avgFoulsC14,
#         "Avg Fouls Suffered": avgFoulsS14,
#         "Penalties Caused": penaltiesCaused14
#     }

#     # Stop webdriver and return data
#     browser.quit()
#     return data

def WC18(browser):
    url = 'https://www.fifa.com/worldcup/statistics/teams/disciplinary'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the team names
    all_results = soup.find_all('tr')

    teamsList = []

    for result in all_results[1:]:
        digTeam = result.find('span', class_='fi-t__nText ').text
        teamsList.append(digTeam)

    table = soup.find('table', class_='fi-table fi-standings fi-statistics fi-statistics-teams dataTable no-footer')
    rows = table.find_all('tr')
    data = []
    matchesPlayed = []
    yellow = []
    indirectRed = []
    directRed = []
    foulsCommited = []
    foulsSuffered = []
    penaltiesCaused = []

    for row in rows:
        data.append([c.text for c in row.find_all('td')])
        
    for x in data[1:]:
        matchesPlayed.append(x[2])
        yellow.append(x[2])
        indirectRed.append(x[3])
        directRed.append(x[4])
        foulsCommited.append(x[5])
        foulsSuffered.append(x[7])
        penaltiesCaused.append(x[8])

    avgFoulsC = [round(float(x)/float(y), 2) for x,y in zip(foulsCommited, matchesPlayed)]
    avgFoulsS = [round(float(x)/float(y), 2) for x,y in zip(foulsSuffered, matchesPlayed)]

    return teamsList, matchesPlayed, avgFoulsC, avgFoulsS, penaltiesCaused

def WC14(browser):
    url = 'https://www.fifa.com/worldcup/archive/brazil2014/statistics/teams/disciplinary.html'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', class_='table tbl-statistics sortable')
    rows = table.find_all('tr')
    data = []
    teamsList14 = []
    matchesPlayed14 = []
    yellow14 = []
    indirectRed14 = []
    directRed14 = []
    foulsCommited14 = []
    foulsSuffered14 = []
    penaltiesCaused14 = []
    for row in rows:
        data.append([c.text for c in row.find_all('td')])
        
    for x in data[1:]:
        teamsList14.append(x[0])
        matchesPlayed14.append(x[2])
        yellow14.append(x[2])
        indirectRed14.append(x[3])
        directRed14.append(x[4])
        foulsCommited14.append(x[6])
        foulsSuffered14.append(x[7])
        penaltiesCaused14.append(x[8])

    avgFoulsC14 = [round(float(x)/float(y), 2) for x,y in zip(foulsCommited14, matchesPlayed14)]
    avgFoulsS14 = [round(float(x)/float(y), 2) for x,y in zip(foulsSuffered14, matchesPlayed14)]

    return teamsList14, matchesPlayed14, avgFoulsC14, avgFoulsS14, penaltiesCaused14

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())