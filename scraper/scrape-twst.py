# Scrape from That's What She Tweets
import string
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

startPage = 1
endPage = 155
charLimit = 10 # Anything less than 5 characters should be excluded
url = 'http://www.thatswhatshetweets.com/rated/best/alltime/page/'
outputFile = '../data/twst.txt'
f = open(outputFile, 'w')
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def strip(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

def clean(text):
    text = text.replace('”', '"').replace('“', '"')
    return strip(text)

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
        req = urllib.request.Request(url + str(page), headers=hdr)
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html)
        storyList = filter(lambda x: bool(x) and len(x) > charLimit, list(processStory(story) for story in soup.select('.joke p a')))
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