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

from random import seed, randint, choice
seed(12435123)

def get_people(max_age, min_age, n):
    for i in range(n):
        age = randint(max_age, min_age)
        gender = choice(("Male","Male","Male","Male","Male", "Female", "Female", "Female", "Female", "Unknown", "Unknown"))
        if gender == "Unknown":
            age = "Unknown"
        yield {"age": age, "gender": gender}



PEOPLE = []
PEOPLE.extend(get_people(15, 25, 125))
PEOPLE.extend(get_people(25, 30, 40))
PEOPLE.extend(get_people(30, 35, 27))
PEOPLE.extend(get_people(35, 55, 30))
PEOPLE.extend(get_people(55, 85, 8))
PEOPLE = {"people": PEOPLE}