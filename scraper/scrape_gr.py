# Scrape from Goodreads
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

startPage = 1
endPage = 96
charLimit = 10 # Anything less than 10 characters should be excluded
url = 'https://www.goodreads.com/quotes/tag/sex?page='
outputFile = '../data/gr.txt'
f = open(outputFile, 'w')

def clean(text):
    attributionText = '―'
    attrIndex = text.index(attributionText)
    text = text[0:attrIndex]
    text = text.replace('”', '"').replace('“', '"').replace('...', ' ')
    return text.translate(str.maketrans('', '', string.punctuation)).lower().strip().replace('today i ', '').replace('today ', '').replace(' fml', '')

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
        storyList = filter(lambda x: bool(x) and len(x) > charLimit, list(processStory(story) for story in soup.select('.quoteText')))
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