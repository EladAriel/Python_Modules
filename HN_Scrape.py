"""
This script has been written based on the "Complete Python Developer in 2022: Zero to Mastery" course.
"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pprint

# Get response from website
res = requests.get('https://news.ycombinator.com/news')

# Use BeautifulSoup library to parse the website's HTML
soup = BeautifulSoup(res.text, 'html.parser')

# Get the link to each article and the number of votes for each article
links = soup.select('.titleline > a')
subtext = soup.select('.subtext')

# Sort items in Hacker News Dictionary
def sort_stories_by_votes(hndict):
    """

    :param hndict: Hacker News dictionary consist of articles' titles, links and votes
    :return: sorted dictionary by article votes
    """
    return sorted(hndict, key=lambda k:k['votes'], reverse=True)

# Sort News in Hacker News by link, title and number of votes for each article
def create_custom_hn(links, subtext):
    """

    :param links: List of articles' links from Hacker News HTML
    :param subtext: List of all lines in HTML that includes '.subtext'
    :return: Sorted dictionary of Hacker News articles by votes
    """
    hn = []
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace('points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

# Print the sorted dictionary of Hacker News articles
pprint.pprint(create_custom_hn(links, subtext))
