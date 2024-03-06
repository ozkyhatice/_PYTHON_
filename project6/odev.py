#SORU1

def lab7_soru1_sorua_klasik(str_eleman):
    func1lista = []
    for index in range(len(str_eleman)):
         if str_eleman[index] != "_" :
             func1lista.append(str_eleman[index].lower())
    return "".join(func1lista)

def lab7_soru1_a_listcomp(str_eleman):
    func1listb = [ str_eleman[index].lower() for index in range(len(str_eleman)) if str_eleman[index] != "_" ]
    return "".join(func1listb)

def lab7_soru1_sorub_klasik(str_eleman):
    sozluk = {}
    for index in range(len(str_eleman)):
        if str_eleman[index] % 2:
            sozluk.setdefault(str_eleman[index], "Tek")
        else:
            sozluk.setdefault(str_eleman[index], "Cift")
    return sozluk

def lab7_soru1_sorub_listcomp(str_eleman):
    sozluk = { str_eleman[index] : "Tek" if str_eleman[index] % 2 else "Cift" for index in range(len(str_eleman)) }
    return sozluk





#SORU2
import re
import feedparser

FeedListesi = [
'http://feeds.feedburner.com/37signals/beMH',
'http://feeds.feedburner.com/blogspot/bRuz' ,
'http://battellemedia.com/index.xml'        ,
'http://feeds.feedburner.com/hotair/main'   ,
'http://blog.outer-court.com/rss.xml'
]

d = feedparser.parse('http://feeds.feedburner.com/37signals/beMH')

search_text = d.entries[0]['title'] + ' ' + d.entries[0]['summary'] + ' ' + d.entries[0]['description']
t1=re.findall(r'\W+',search_text)
t2=re.sub(r"\W+"," ",search_text)
t3=re.sub(r'\d+'," ",t2)
newlist=list()
for i in t3.split():
    newlist.append(i.lower())
print(newlist)

import re

# Strips out all of the HTML and splits the words by nonalphabetical characters 
# and returns them as a list.
def getwords(html):
    # Remove all the HTML tags
    #<a class="read-more" href="https://m.signalvnoise.com/reiterating-our-use-restrictions-policy/">
    txt=re.compile(r'<[^>]+>').sub('',html)

    # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)
    
    # Convert to lowercase
    return [word.lower() for word in words if word!='']
import urllib

# Kelimelerin adetlerini hesaplayan fonksiyon
def getwordcounts(url):
    # Parse the feed
    try:
        d = feedparser.parse(url)
    except urllib.error.URLError as e:
        print("Skipping - There is a problem with address {}".format(url))
        return None, None
    except Exception as e:
        print('Skippig {} due to error {}'.format(url, e))
        return None, None
    
    kelime_saymasi = {}

    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        search_text = e.title+' '+summary
        # Extract a list of words
        words = getwords(search_text)
        for word in words:
            kelime_saymasi.setdefault(word,0)
            kelime_saymasi[word] += 1
    try:
        return d.feed.title, kelime_saymasi
    except AttributeError:
        return None, None
for i in FeedListesi:
    print(getwordcounts(i))

#SORU3
import math
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([math.pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([math.pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - math.pow(sum1, 2) / n) * (sum2Sq - math.pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r

#getwordcounts fonksiyonuyla elde ettiğimiz sozlukler için sim_pearson fonksiyonunu kullanarak benzerlik hesaplanmalı