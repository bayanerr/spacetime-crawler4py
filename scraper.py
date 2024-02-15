import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from bs4.element import Comment
import sys

urlsVisited = {"www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu"}
counter = 0
longestFileLength = 0
longestFile = ""
tokens = {}
subdomains = {}

def init_globals():
    global urlsVisited
    global counter
    global longestFileLength
    global longestFile
    global tokens
    global subdomains

    urlsVisited = {"www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu"}
    counter = 0
    longestFileLength = 0
    longestFile = ""
    tokens = {}
    subdomains = {}



word_list = [
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'buft', 'by', "can't", 'cannot', 'could', "couldn't",
    'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have',
    "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's",
    'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
    "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself',
    "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of',
    'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves',
    'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
    'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the',
    'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're",
    "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's",
    'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would',
    "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours',
    'yourself', 'yourselves']

def tokenize(wordList):
    uniqueWords = set()

    #read the file
    for word in wordList:
        #get alphanumeric only and lower case 
        alphanumericOnly = re.compile("[^a-zA-Z0-9]")
        alphanumericString = alphanumericOnly.sub(' ', word)
        lowerCaseStrings = alphanumericString.split()

        #split by blankspace
        for eachString in lowerCaseStrings:
            uniqueWords.add(eachString.lower())
            if eachString.lower() not in word_list and len(eachString) > 1:
                if eachString.lower() not in tokens.keys():
                    tokens[eachString.lower()] = 1
                else:
                    tokens[eachString.lower()] += 1
    return uniqueWords
 
def print_frequencies(frequencies):
    #sort frequencies by value size
    sortedFrequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    size = len(sortedFrequencies)
    index = 0
    #going through all the sorted frequencies and keeping track of the index after as well
    i = 0
    while index < size:
        currentKey = sortedFrequencies[index][0]
        currentValue = sortedFrequencies[index][1]
        keys = [currentKey]
        updatedIndex = index + 1
        # if multiple value sizes are the same as each other
        # save them to a list, and then sort them alphabetically by key
        while (updatedIndex < size and currentValue == sortedFrequencies[updatedIndex][1]):
            keys.append(sortedFrequencies[updatedIndex][0])
            updatedIndex += 1
        keys.sort()
        for eachKey in keys:
            if i == 50:
                break
            value = frequencies[eachKey]
            print(eachKey + " = " + str(value))
            i += 1
        index = updatedIndex
    
    
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def scraper(url, resp):
    # Retrieves the next links to visit, removing those that are invalid
    #print("scraper function ", url, " : ", resp)
    global longestFileLength
    global longestFile

    links = extract_next_links(url, resp)
    #return [link for link in links if is_valid(link)]


    link_list = []
    for link in links:
        if is_valid(link, urlsVisited):
            link_list.append(link)
            #print("Link to be added: ", link)
    
    print("Scraper function ended: ", len(link_list), " , ", len(urlsVisited), " Longest file: ", longestFile, " ,length: ", longestFileLength)
    return link_list

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    global longestFileLength
    global longestFile
    next_links = []

    # checking if the status is ok
    # if not 200, print the error and return
    if resp.status != 200:
        print("The error is: ", resp.error)
        return []
    
    #trying to parse the file
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # findAll text reference: https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup        

        currentFile = soup.findAll(text=True)
        visible_texts = list(filter(tag_visible, currentFile))

        uniqueWords = tokenize(visible_texts) 

        if len(uniqueWords) < 20:
            return []

        currentFileLength = len(visible_texts)

        if currentFileLength <= 100:
            return []

        for link in soup.find_all('a'):
            next_links.append(link.get('href'))
    

        if currentFileLength > longestFileLength:
            longestFileLength = currentFileLength
            longestFile = url

        #if len(urlsVisited) >= 100:
        #    print_frequencies(tokens)
        #    print("Subdomains: ", subdomains)
        #    sys.exit()
        
    
    except Exception as e:
        print(f'Error extracting the following link: {e}\n')
    
    return next_links

def is_valid(url, urlsVisited):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    global counter
    parsed = urlparse(url)
    full_url = parsed.netloc + parsed.path
    try:
        parsed = urlparse(url)
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        # add ppsx?

        if parsed.scheme not in set(["http", "https"]):
            return False

        # https://www.ics.uci.edu, https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
        #if parsed.netloc not in set(["www.ics.uci.edu", 
        #    "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu"]):
        #    return False
        
        
        
        if re.match(".*.ics.uci.edu.*", parsed.netloc) or re.match(".*.cs.uci.edu.*", parsed.netloc) or re.match(".*.informatics.uci.edu.*", parsed.netloc) or re.match(".*.stat.uci.edu.*", parsed.netloc):
            pass
        else:
            return False
        
        if full_url in urlsVisited:
            return False



        if re.match(".*.ics.uci.edu.*", parsed.netloc):
            counter += 1

            if parsed.netloc not in subdomains.keys():
                
                subdomains[parsed.netloc] = 1
            else:
                subdomains[parsed.netloc] += 1
            
        if full_url not in urlsVisited:
            urlsVisited.add(full_url)
            print("TRUE: " + str(full_url))
            return True
        
    
    except TypeError:
        print ("TypeError for ", parsed)
        return False