__author__ = 'robert'

def get_lines(kind):
    end1 = "class "
    end2 = "(ndb.Model):"
    with open('datamodel.py') as f:
        lines = f.readlines()
    append = False
    chunk = []
    for line in lines:
        if append:
            if end1 in line and end2 in line:
                break
            chunk.append(line)
        if "class " + kind + "(ndb.Model):" in line:
            append = True

    return chunk

from random import seed, randint, choice, shuffle
seed(12435123)


def get_people(max_age, min_age, n):
    clubs = [(u'1885 Britomart',
              [u'music_jazz', u'music_soul', u'music_blues', u'music_funk']),
             (u"A'isha", [u'']),
             (u'Andrew Andrew', [u'music_funk', u'music_oldschool', u'music_hiphop']),
             (u'Be Club', [u'']),
             (u'Bungalow 8', [u'']),
             (u'CODE', [u'music_dubstep', u'music_house', u'music_dnb']),
             (u'Club DELUXE', [u'music_house', u'music_pop', u'music_rnb']),
             (u'Degree', [u'music_electro', u'music_dutch', u'music_house']),
             (u'Devo Nightclub', [u'']),
             (u'Flight Lounge', [u'']),
             (u"Freddy's Ice House", [u'']),
             (u'Globe Bar', [u'']),
             (u'Goldfinch', [u'']),
             (u'Havana Club', [u'']),
             (u'Hitch', [u'']),
             (u'Ibiza', [u'']),
             (u'Lenin Bar', [u'']),
             (u'No. 1 High School', [u'music_funk', u'music_disco', u'music_house']),
             (u'Provedor', [u'music_lounge']),
             (u'Spy', [u'music_house', u'music_livepercussion']),
             (u'The Carpark', [u'music_lounge']),
             (u'The Lounge', [u'music_hiphop', u'music_rnb']),
             (u'Third and Social', [u'music_soul', u'music_funk', u'music_house']),
             (u'Waterfront', [u'music_oldschool', u'music_hiphop', u'music_funk']),
             (u'Zen', [u''])]
    for i in range(n):
        age = randint(max_age, min_age)
        gender = choice(("Male","Male","Male","Male","Male", "Female", "Female", "Female", "Female", "Unknown", "Unknown"))
        club1, tags = choice(clubs)
        club2 = choice(clubs)[0]
        friends = choice([10, 100, 150, 200, 220, 250, 300, 500, 900]) + randint(1, 50)
        offers_claimed = choice([0,0,0,1,2,2,3])
        category = "professional"
        if age < 27:
            category = choice(["student", "young professional", "young professional"])
        elif 20 < age < 23:
            category = choice(["student", "student", "student", "student", "young professional"])
        elif age < 21:
            category = "student"
        if randint(1, 7) == 5 and gender == "Male":
            category = "tradesman"

        if randint(1,10) == 5:
            age = "Unknown"

        city = choice(["Auckland", "Auckland", "Auckland", "Christchurch", "Wellington"])

        yield {"age": age, "gender": gender, "tags": tags, "fav_clubs": [club1, club2], "friends": friends,
               "offers_claimed": offers_claimed, "category": category, "city": city}



PEOPLE = []
PEOPLE.extend(get_people(15, 25, 125))
PEOPLE.extend(get_people(25, 30, 40))
PEOPLE.extend(get_people(30, 35, 27))
PEOPLE.extend(get_people(35, 55, 30))
PEOPLE.extend(get_people(55, 85, 8))
shuffle(PEOPLE)
PEOPLE = {"people": PEOPLE}