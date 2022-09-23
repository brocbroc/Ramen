"""Gives facts about the ramen_ratings table"""

import sqlite3

#Returns a list of the best brands for a specific location. Throws error if the input is not a valid location
def best_brand(location):
    con = sqlite3.connect("ramen.db")
    cursor = con.cursor()

    stats = dict()
    query = "SELECT number FROM ramen_ratings where country == '" + str(location) + "'"

    if cursor.execute(query).fetchall() == []:
        return 'error'

    brand_rating = dict()
    ratings = cursor.execute("SELECT brand, stars, country FROM ramen_ratings")

    for rating in ratings.fetchall():
        if rating[2] == location:
            if rating[0] not in brand_rating:
                brand_rating[rating[0]] = [0, 0]

            brand_rating[rating[0]][0] += 1
            brand_rating[rating[0]][1] += float(rating[1])

    highest = []
    highest_avg = 0

    for entry in brand_rating:
        avg = brand_rating.get(entry)[1] / brand_rating.get(entry)[0]

        if avg > highest_avg:
            highest_avg = avg
            highest = [entry]
        elif avg == highest_avg:
            highest.append(entry)

    stats['highest brand'] = highest
    con.close()
    return stats

#Returns a list of all the products fitting specified criteria. Throws error if input is not a valid brand
def all_products(location, brand):
    con = sqlite3.connect("ramen.db")
    cursor = con.cursor()

    if location != '' and (location,) not in cursor.execute("SELECT country FROM ramen_ratings").fetchall():
        print("$$$")
        return 'error'
    elif brand != '' and (brand,) not in cursor.execute("SELECT brand FROM ramen_ratings").fetchall():
        print("SSS")
        return 'error'

    ramen = cursor.execute("SELECT * FROM ramen_ratings").fetchall()

    if location != '':
        index = 0

        while index < len(ramen):
            entry = ramen[index]

            if entry[4] != location:
                ramen.remove(entry)
            else:
                index += 1

    if brand != '':
        index = 0

        while index < len(ramen):
            entry = ramen[index]

            if entry[1] != brand:
                ramen.remove(entry)
            else:
                index += 1

    con.close()
    return ramen
