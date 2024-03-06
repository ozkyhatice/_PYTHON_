
import math
from numpy import dot
from numpy.linalg import norm
def sim_jaccard(prefs, person1, person2):  # Jaccard Distance (A, B) = |A intersection B| / |A union B|
    # Ortak izlenen filmleri alalim
    p1_intersect_p2 = {}
    for item in prefs[person1]:
        if item in prefs[person2]: 
            p1_intersect_p2[item] = 1

    # Sozluklerin birlesimlerini alalim
    p1_union_p2 = dict(prefs[person1]) # Sozlugu kopyalamaniz lazim!
    for item in prefs[person2]:
        if item not in p1_union_p2: 
            p1_union_p2[item] = 1

    # Bu iki kumenin uzunluklarini alalim
    p1_intersect_p2, p1_union_p2 = len(p1_intersect_p2), len(p1_union_p2)

    return float(p1_intersect_p2) / float(p1_union_p2) # return jaccard distance
def sim_cosine(prefs, person1, person2):

    # Ortak fimleri bulmak yerine butun filmleri ayni sirayla da alabilirdiniz (tanimoto gibi)
    person1_criticscores = []
    person2_criticscores = []

    for item in prefs[person1]:
        if item in prefs[person2]:
            person1_criticscores.append(prefs[person1][item])
            person2_criticscores.append(prefs[person2][item])

    # Ortak film yoksa 0 don - yoksa 0'a bolme islemi var
    if len(person1_criticscores) == 0:
        return 0
    
    # Kendi dot carpimi fonksiyonunuzu ya da norm fonksiyonlarinizi da yazabilirdiniz
    cosine = dot(person1_criticscores, person2_criticscores) / \
        (norm(person1_criticscores) * norm(person2_criticscores))

 
    return cosine

def topMatches(prefs, person, n=5, similarity=sim_jaccard):
    ''' Pref sözlüğünden person için en iyi eşleşmeleri döndürür.'''
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores

def getRecommendations(prefs, person, similarity = sim_cosine):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)
        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings
