import re
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

maxPages = 2
url = 'http://www.twssstories.com/best?page='
exp = '"(.*?)"' # Get anything between quotes
r = re.compile(exp)

def strip(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

def processStory(story):
    return strip('\n'.join(r.findall(story.string)))

def getStories(page):
    stories = '\n'
    if page <= maxPages:
        html = urllib.request.urlopen(url + str(page))
        soup = BeautifulSoup(html)
        stories += '\n'.join(list(processStory(story) for story in soup.select('.content.clear-block p')))
        page += 1
        stories += getStories(page + 1)
    return stories

allStories = getStories(0)
print(allStories)