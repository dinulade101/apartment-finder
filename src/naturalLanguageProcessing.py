import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet 
from nltk.corpus import stopwords

class keyWordFinder:

    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None
        self.desc = None
        self.cleanedTokens = None
        self.attList = None
        self.filteredWords = None
        self.filteredWordsDict = dict()
        self.fullSynsSet = dict()
    
    def getHTMLResponseAndParse(self):
        response = urllib.request.urlopen(self.url)
        self.html = response.read()
        self.soup = BeautifulSoup(self.html, "html5lib")
        self.desc = self.soup.find('div', id="vip-body").find_all("p")
        self.attList = self.soup.find('div', id="AttributeList").find_all("dd")
    
    def cleanOutput(self):
        stringifiedDesc = str.join(u'\n', map(str, self.desc))
        stopWords = set(stopwords.words('english'))
        stopWords = []
        itemsToRemove = ['<', 'p', '>', '<', 'strong', '>', 'An', '*', '!','/em', '&', 'amp', ';', 'br/', '/strong', ',', ',','By', 'clicking', '``', 'Send', 'Email', "''", ',', 'consent', 'action', 'accordance', '<', 'href=', "''", 'https', ':','nofollow', 'noopener', 'noreferrer', "''", 'target=', "''", '_blank', "''", '>', 'Terms', 'Use', '<', '/a', '>', '<', 'href=', "''", 'https', ':', '//help.kijiji.ca/helpdesk/policies/kijiji-privacy-policy', "''", 'rel=', "''", 'nofollow', 'noopener', 'noreferrer', "''", 'target=', "''", '_blank', "''", '>', 'Privacy', 'Policy', '<', '/a', '>', '.', '<', '/p', '>']
        otherNonCharSymbols = ['!','+','<','[','%','<=',']','&','-','<>','|','.','=','~',
'(','/','=='	,'~=',
')',	'/!',	'>',	
'*',	'//',	'>=',
'*!',	'{',	'?',	
'**',	'}',	'@',	':',
';',	'^',	'|=',	'&=',
'+=',	'-=',	'*=',	'/=',
'**=']
        tokenizedDesc = word_tokenize(stringifiedDesc)
        self.filteredWords = [w for w in tokenizedDesc if not w in stopWords and not w in itemsToRemove]
        
        for i in self.filteredWords:
            synSet = wordnet.synsets(i)
            self.fullSynsSet[i] = []
            for j in synSet:
                self.fullSynsSet[i].append(j.lemmas()[0].name())
            
        #self.fullSynsSet.extend(self.filteredWords)
        print(self.fullSynsSet)
       
    def findKeyWords(self, keyWords):
        self.getHTMLResponseAndParse()
        self.cleanOutput()
        foundKeyWords = []
        for word in keyWords:
            for key, val in self.fullSynsSet.items():
                if word in val:
                    foundKeyWords.append(key)
        
        #print("found key words",foundKeyWords)
        sentenceSnippets = []

        #remove duplicate entries from foundKeyWords


        for word in foundKeyWords:
            #print("hello")
            index = self.filteredWords.index(word)
            #print("index", index)
            try:
                sentenceSnippets.append(self.filteredWords[index-4:index+4])
            except:
                continue
        #print(sentenceSnippets)
        return sentenceSnippets
    

'''
response = urllib.request.urlopen('https://www.kijiji.ca/v-house-rental/edmonton/griesbach-community-1-month-free-499-security-deposit/1295432610?enableSearchNavigationFlag=true')

html = response.read()

soup = BeautifulSoup(html,"html5lib")

desc = soup.find('div', id="vip-body").find_all("p")
#text = soup.get_text()

attList = soup.find('div', id="AttributeList").find_all("dd")
#print(attList)


print(type(desc))
stringifiedDesc = str.join(u'\n', map(str, desc))

stopWords = set(stopwords.words('english'))

itemsToRemove = ['<', 'p', '>', '<', 'strong', '>', 'An', '!', '&', 'amp', ';', 'br/', '/strong', ',', ',','By', 'clicking', '``', 'Send', 'Email', "''", ',', 'consent', 'action', 'accordance', '<', 'href=', "''", 'https', ':','nofollow', 'noopener', 'noreferrer', "''", 'target=', "''", '_blank', "''", '>', 'Terms', 'Use', '<', '/a', '>', '<', 'href=', "''", 'https', ':', '//help.kijiji.ca/helpdesk/policies/kijiji-privacy-policy', "''", 'rel=', "''", 'nofollow', 'noopener', 'noreferrer', "''", 'target=', "''", '_blank', "''", '>', 'Privacy', 'Policy', '<', '/a', '>', '.', '<', '/p', '>']

tokenizedDesc = word_tokenize(stringifiedDesc)

filteredWords = [w for w in tokenizedDesc if not w in stopWords and not w in itemsToRemove]

fullSynsSet = []

for i in filteredWords:
    synSet = wordnet.synsets(i)
    for j in synSet:
        fullSynsSet.append(j.lemmas()[0].name())


print(fullSynsSet)
'''
'''
tokens = [t for t in text.split()]

freq = nltk.FreqDist(tokens)

if "pet" in freq.items():
    print("yes")

tokenized = sent_tokenize(text)
'''
