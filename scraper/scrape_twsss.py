# Scrape from That's What She Said Stories
import re
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

startPage = 0
endPage = 152
charLimit = 10 # Anything less than 5 characters should be excluded
url = 'http://www.twssstories.com/best?page='
exp = '"(.*?)"' # Get anything between quotes
r = re.compile(exp)
outputFile = '../data/twsss.txt'
f = open(outputFile, 'w')

def strip(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

def clean(text):
    text = text.replace('”', '"').replace('“', '"')
    return strip( '\n'.join(r.findall(text)) )

def processStory(story):
    text = ' '.join(story.stripped_strings) 
    return clean(text)

def getStories(page):
    print('On page ' + str(page))
    if page <= endPage:
        if page == startPage:
            stories = ''
        else:
            stories = '\n'
        html = urllib.request.urlopen(url + str(page))
        soup = BeautifulSoup(html)
        storyList = filter(lambda x: bool(x) and len(x) > charLimit, list(processStory(story) for story in soup.select('.content.clear-block p')))
        stories += '\n'.join(storyList)
        stories += getStories(page + 1)
        return stories
    else:
        return ''

def main():
    print(__name__)
    allStories = getStories(startPage)
    f.write(allStories)
    print(allStories)

main()