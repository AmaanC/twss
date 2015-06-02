# Scrape from That's What She Said Stories
import re
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

startPage = 1
endPage = 1
charLimit = 10 # Anything less than 5 characters should be excluded
url = 'http://theoffice.wikia.com/wiki/List_of_the_times_somebody_says_%22That%27s_what_she_said%22'
exp = '"(.*?)"' # Get anything between quotes
r = re.compile(exp)
outputFile = '../data/twss-office.txt'
f = open(outputFile, 'w')

def strip(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

def clean(text):
    text = text.replace('”', '"').replace('“', '"').replace('...', ' ')
    return strip( '\n'.join(r.findall(text)) )

def processStory(story):
    print(story)
    text = ' '.join(story.stripped_strings) 
    return clean(text)

def getStories(page):
    print('On page ' + str(page))
    if page <= endPage:
        if page == startPage:
            stories = ''
        else:
            stories = '\n'
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html)
        storyList = filter(lambda x: bool(x) and len(x) > charLimit, list(processStory(story.contents[4]) for story in soup.select('.sortable tr')))
        stories += '\n'.join(storyList)
        stories += getStories(page + 1)
        return stories
    else:
        return ''

def main():
    allStories = getStories(startPage)
    f.write(allStories)
    print(allStories)

if __name__ == '__main__':
    main()