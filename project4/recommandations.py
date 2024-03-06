#recommendations.py
from math import sqrt
from numpy import dot
from numpy.linalg import norm

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# Returns the Pearson correlation coefficient for p1 and p2
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
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r
    
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


def sim_tanimoto(prefs, person1, person2):
    # Tum filmlerin oldugu bir liste olusturalim
    all_items = []
    for person in prefs:
        for movie in prefs[person]:
            if movie not in all_items:
                all_items.append(movie)

    # Klasik dongulerle yapildiginda
    pSum = 0
    sumsq1 = 0
    sumsq2 = 0
    for item in all_items:
        a = 1 if item in prefs[person1] else 0
        b = 1 if item in prefs[person2] else 0
        pSum = pSum + a*b
        sumsq1 = sumsq1 + a*a
        sumsq2 = sumsq2 + b*b

    # Aynisi fakat list Comprehension ile
    # pSum = sum([1 for item in all_items if item in prefs[person1] and item in prefs[person2]])
    # sumsq1 = sum([1 for item in all_items if item in prefs[person1]])
    # sumsq2 = sum([1 for item in all_items if item in prefs[person2]])
    return pSum / (sumsq1 + sumsq2 - pSum)



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
