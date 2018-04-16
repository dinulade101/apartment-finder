import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet 
from nltk.corpus import stopwords

class keyWordFinder:
    """
    A class that returns sentence snippets from Kjiji add that match user provided words in settings.py
    """
    def __init__(self, url):
        # initiailize
        # note: some of these are not necessary for this program, however they provide the building blocks to expand
        # project further 

        self.url = url
        self.html = None
        self.soup = None
        self.desc = None
        self.cleanedTokens = None
        self.attList = None
        self.filteredWords = None
        self.filteredWordsDict = dict()
        self.fullSynsSet = dict()
    
    """
        Get the HTML page and find paragraph containing ad description
        Use BeutifulSoup to locate extracted html text and find specfic tags 
    """
    def getHTMLResponseAndParse(self):
        response = urllib.request.urlopen(self.url)
        self.html = response.read()
        self.soup = BeautifulSoup(self.html, "html5lib")
        self.desc = self.soup.find('div', id="vip-body").find_all("p")
        self.attList = self.soup.find('div', id="AttributeList").find_all("dd")
    
    """
        Use NLTK to filter HTML tags and unessary stop words in English from list of tokenized words 
    """
    def cleanOutput(self):
        stringifiedDesc = str.join(u'\n', map(str, self.desc))

        # define keywords and symbols to remove 
        stopWords = set(stopwords.words('english'))
        stopWords = []
        itemsToRemove = ['<', 'p', '>', '<', 'strong', '>', 'An', '*', '!','/em', '&', 'amp', 
        ';', 'br/', '/strong', ',', ',','By', 'clicking', '``', 'Send', 'Email', "''", ',', 'consent',
        'action', 'accordance', '<', 'href=', "''", 'https', ':','nofollow', 'noopener', 'noreferrer', "''", 
        'target=', "''", '_blank', "''", '>', 'Terms', 'Use', '<', '/a', '>', '<', 'href=', "''", 'https', ':',
        '//help.kijiji.ca/helpdesk/policies/kijiji-privacy-policy', "''", 'rel=', "''", 'nofollow', 'noopener',
        'noreferrer', "''", 'target=', "''", '_blank', "''", '>', 'Privacy', 'Policy', '<', '/a', '>', '.',
        '<', '/p', '>']
        
        otherNonCharSymbols = ['!','+','<','[','%','<=',']','&','-','<>','|','.','=','~',
        '(','/','=='	,'~=',
        ')',	'/!',	'>',	
        '*',	'//',	'>=',
        '*!',	'{',	'?',	
        '**',	'}',	'@',	':',
        ';',	'^',	'|=',	'&=',
        '+=',	'-=',	'*=',	'/=',
        '**=', '(', ')', '$']
        tokenizedDesc = word_tokenize(stringifiedDesc)
        self.filteredWords = [w for w in tokenizedDesc if not w in stopWords and not w in itemsToRemove]
        
        for i in self.filteredWords:
            synSet = wordnet.synsets(i)
            self.fullSynsSet[i] = []
            for j in synSet:
                self.fullSynsSet[i].append(j.lemmas()[0].name())
            
    """
        Generate synonyms and similar words to expand matches. 
        Match user given keywords with full set of words found in paragraph  
    """
    def findKeyWords(self, keyWords):
        self.getHTMLResponseAndParse()
        self.cleanOutput()
        foundKeyWords = []

        # go through synonyms generated earlier 
        for word in keyWords:
            for key, val in self.fullSynsSet.items():
                if word in val:
                    foundKeyWords.append(key)
        
        sentenceSnippets = []

        # return found sentence snippets 
        for word in foundKeyWords:
            index = self.filteredWords.index(word)
            try:
                sentenceSnippets.append(self.filteredWords[index-4:index+4])
            except:
                continue
        return sentenceSnippets
    
