

from numpy import dot
from numpy.linalg import norm
from cProfile import label
from distutils.spawn import spawn
from msilib.schema import ListBox
from pyparsing import col
from xlrd import open_workbook

import tkinter as tk
import dbm
import pickle 
from tkinter import Label, StringVar, messagebox
import math
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([math.pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + math.sqrt(sum_of_squares))
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

def topMatches(prefs, person, n, similarity=sim_jaccard):
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
def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        #print("-"*20)
        #print(item, rating)
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            #print(".")
            #print(similarity, item2)

            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            #print(scores[item2])
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    print("*"*20)
    return rankings
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
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result
def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(itemPrefs)))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result
