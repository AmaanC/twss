# Scrape from FML
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

startPage = 0
endPage = 290
charLimit = 10 # Anything less than 10 characters should be excluded
url = 'https://www.fmylife.com/intimacy?page='
outputFile = '../data/fml.txt'
f = open(outputFile, 'w')

def clean(text):
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
        storyList = filter(lambda x: bool(x) and len(x) > charLimit, list(processStory(story) for story in soup.select('.article > p')))
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