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

