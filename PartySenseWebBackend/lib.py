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

PEOPLE = ['Brendan Bycroft', 'Abhishek Vadnerkar', 'John King', 'Terry Yang', 'Hannah Rutter', 'Adam Freeth', 'Duncan Jessep', 'Thomas Steinke', 'Jamie McCloskey', 'Jesse Sergent',
          'Will Gittoes', 'Edwin Flores', 'Aaron Gate', 'Martin Doms', 'Simonvan Velthooven', 'Joey Scarr', 'Chris Macic', 'Michael Arms', 'Daniel Seagar', 'Joey Sparks', 'Oliver Wilkinson',
          'Stephen Fitchett', 'Sam Bewley', 'Tim Bond','Chris Heyes', 'Michael McGee', 'Rebecca Rassie', 'Roman van Uden', 'Louis Crosby', 'Carlos Nazareno', 'Janina Voigt', 'Alexander Ray',
          'James Chanki Park', 'Nicola Jones', 'David Nutsford', 'Stephen Brett', 'Ulrike Klintworth', 'Westley Gough', 'Peter Chen', 'Morgan Philo', 'Andrei Miulescu', 'Thomas Halse', 'Rosie Taylor',
          'James Elvery', 'Blair Deuchar', 'Daniel Roberts', 'Matt Sillars', 'Harley Rayner', 'Joe Zhu', 'Edward James Brandli', 'Becca Aiken', 'James Morgan', 'Adrian Heyes', 'Tim McNamara',
          'Ryan Kamins', 'Heidi Newton', 'Geoff Clark', 'Francesca Nicklin', 'Geoffrey Hunter', 'Brett Robertson', 'Lisa Hepp', 'Qiulae Wong', 'Alicia Evans', 'Alice Rose King', 'Andrew Thompson',
          'Jesse Eedrah', 'Henry Donald', 'Nicholas Duncan', 'Lucy Westenra', "Richard 'Ngog' Lowe", 'Kawin Srirungrot', 'Eddie Ochoa', 'Prasad Bhonsule', 'Simon Heeney', 'Danielle Naus', 'Taina Rai',
          'Tim Macintosh', 'Caroline Mitchell-Lowe', 'Bojan Jovanovic', 'Daniel Allen', 'Liz Ung', 'Matthew Benton', "Craig 'Brick' Thornton", 'Kylie McKay', 'Holman Gao', 'Hamish Ellis', 'Thomas Lowe',
          'Uriah McCall', 'Bridget Hagar', 'SimonMoroney', 'Angus Dobson', 'Lachie Munro', 'Alyce Koudys', 'James Fraser', 'Aleisha Frazer', 'Richard Ellis', 'Lynette Graham', 'Guy Carter', 'Ben Stewart',
          'Rupert Nelson', 'Matthew Sinclair', 'Daniel Checketts', 'Matt Wentz', 'Lauren Collins', 'Henry Lane', 'Mhairi Rademaker', 'Henk Wang', 'Josh Keating', 'Hilary Salmon', 'Henry Jenkins', 'Mick Ou',
          'Graham Bracey', 'Richard Speer', 'Sally Joy','Danyol Supra Hicks', 'Jack Kwun Yu Chan', 'Sam Hitchy', 'Viranchi Upadhyay', 'Hussain Ali', 'David Leslie', 'Sam Webster', 'Cameron Jones', 'Blair James',
          'Ezra Fantl', 'Steven CaptainKeen Blake', 'Daniel Rowe', 'Cody Huxtable', 'Brent Matuschka', 'Olivia Spencer', 'Emma Fairhall', 'Henry Malthus', 'Averil Howie', 'Arun Charles Christopher Williams',
          'Churie Adam', 'Anny Elvery', 'Hamish McRae', 'Gina Cardwell', 'Gareth Salt', 'Simon Gordon', 'Jason Bhana', 'Alexander Macdonald', 'Kelly Wong', 'Sonya McGlone', 'Korinne Brown', 'Sam Gapes',
          'Nick Denz', 'Elijah May', 'Jeremy Burton', 'Michael Fifield', 'Matt Blackwell', 'Norman Quek', 'Lily Simpson', 'Rob Longuet-Higgins', 'Nadeesha Senarath', 'Clarence Ka Hang Tong', 'Morgan Miller',
          'Stefan Jammes', "Anna O'Callaghan", 'John Dolan', 'Tanmay Bhola', 'Mathew Morreau', 'Jordan Hills', 'Elizabeth Ashby', 'Emma Gin','Adi Ramakanth', 'Mike Adams', 'James Hill', 'Amber Keeley',
          'George Moore', 'Tim Johnson', 'Fiona Rowley', 'Dave Felton', 'Nisha Mehrotra', 'Michael Wilson', 'George Liddell', 'Nick Smith', 'Jack Farrant', 'Liam Zander', 'Lloyd Manning', 'Chloe McIntosh',
          'Michael Nation', 'David Allen', 'Jack Grigg', 'Tom Archibald', 'Patrick Timmins', 'David Sharp', 'Claire Murray', 'John Pocock', 'Adithya Sreekumar', 'Hugo Borren', 'Jonathan Glendenning', 'Matt Burbury-King',
          'Kerrie Coles', 'Andrew Mills', 'Martin Cannon', 'Tim Clemens', 'Jan Sintenie', 'Yi Zeng', 'Zac Gravatt', 'George Scott', 'Andrew Jackson', 'Finlay Wilkinson', 'Jono Entwistle', 'Jack Turley', 'Isaac Manuel',
          'Wim Looman', 'James Peat', 'Haroun Barazanchi', "Dylan D'Costa", 'Jacky Sung', 'Josie Norris', 'Anisha Dayaram', 'Nick Ess', 'Charlie Wilkinson', 'Tom Williams', 'Thomas Oldfield', 'Dane Hart']