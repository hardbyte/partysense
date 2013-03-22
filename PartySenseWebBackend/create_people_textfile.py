__author__ = 'robert'

terminal_data = """['Brendan Bycroft', 'Abhishek Vadnerkar', 'John King', 'Terry Yang', 'Hannah Rut
ter', 'Adam Freeth', 'Duncan Jessep', 'Thomas Steinke', 'Jamie McCloskey', 'Jess
e Sergent', 'Will Gittoes', 'Edwin Flores', 'Aaron Gate', 'Martin Doms', 'Simon
van Velthooven', 'Joey Scarr', 'Chris Macic', 'Michael Arms', 'Daniel Seagar', '
Joey Sparks', 'Oliver Wilkinson', 'Stephen Fitchett', 'Sam Bewley', 'Tim Bond',
'Chris Heyes', 'Michael McGee', 'Rebecca Rassie', 'Roman van Uden', 'Louis Crosb
y', 'Carlos Nazareno', 'Janina Voigt', 'Alexander Ray', 'James Chanki Park', 'Ni
cola Jones', 'David Nutsford', 'Stephen Brett', 'Ulrike Klintworth', 'Westley Go
ugh', 'Peter Chen', 'Morgan Philo', 'Andrei Miulescu', 'Thomas Halse', 'Rosie Ta
ylor', 'James Elvery', 'Blair Deuchar', 'Daniel Roberts', 'Matt Sillars', 'Harle
y Rayner', 'Joe Zhu', 'Edward James Brandli', 'Becca Aiken', 'James Morgan', 'Ad
rian Heyes', 'Tim McNamara', 'Ryan Kamins', 'Heidi Newton', 'Geoff Clark', 'Fran
cesca Nicklin', 'Geoffrey Hunter', 'Brett Robertson', 'Lisa Hepp', 'Qiulae Wong'
, 'Alicia Evans', 'Alice Rose King', 'Andrew Thompson', 'Jesse Eedrah', 'Henry D
onald', 'Nicholas Duncan', 'Lucy Westenra', "Richard 'Ngog' Lowe", 'Kawin Srirun
grot', 'Eddie Ochoa', 'Prasad Bhonsule', 'Simon Heeney', 'Danielle Naus', 'Taina
 Rai', 'Tim Macintosh', 'Caroline Mitchell-Lowe', 'Bojan Jovanovic', 'Daniel All
en', 'Liz Ung', 'Matthew Benton', "Craig 'Brick' Thornton", 'Kylie McKay', 'Holm
an Gao', 'Hamish Ellis', 'Thomas Lowe', 'Uriah McCall', 'Bridget Hagar', 'Simon
Moroney', 'Angus Dobson', 'Lachie Munro', 'Alyce Koudys', 'James Fraser', 'Aleis
ha Frazer', 'Richard Ellis', 'Lynette Graham', 'Guy Carter', 'Ben Stewart', 'Rup
ert Nelson', 'Matthew Sinclair', 'Daniel Checketts', 'Matt Wentz', 'Lauren Colli
ns', 'Henry Lane', 'Mhairi Rademaker', 'Henk Wang', 'Josh Keating', 'Hilary Salm
on', 'Henry Jenkins', 'Mick Ou', 'Graham Bracey', 'Richard Speer', 'Sally Joy',
'Danyol Supra Hicks', 'Jack Kwun Yu Chan', 'Sam Hitchy', 'Viranchi Upadhyay', 'H
ussain Ali', 'David Leslie', 'Sam Webster', 'Cameron Jones', 'Blair James', 'Ezr
a Fantl', 'Steven CaptainKeen Blake', 'Daniel Rowe', 'Cody Huxtable', 'Brent Mat
uschka', 'Olivia Spencer', 'Emma Fairhall', 'Henry Malthus', 'Averil Howie', 'Ar
un Charles Christopher Williams', 'Churie Adam', 'Anny Elvery', 'Hamish McRae
', 'Gina Cardwell', 'Gareth Salt', 'Simon Gordon', 'Jason Bhana', 'Alexander Mac
donald', 'Kelly Wong', 'Sonya McGlone', 'Korinne Brown', 'Sam Gapes', 'Nick Denz
', 'Elijah May', 'Jeremy Burton', 'Michael Fifield', 'Matt Blackwell', 'Norman Q
uek', 'Lily Simpson', 'Rob Longuet-Higgins', 'Nadeesha Senarath', 'Clarence Ka H
ang Tong', 'Morgan Miller', 'Stefan Jammes', "Anna O'Callaghan", 'John Dolan', '
Tanmay Bhola', 'Mathew Morreau', 'Jordan Hills', 'Elizabeth Ashby', 'Emma Gin',
'Adi Ramakanth', 'Mike Adams', 'James Hill', 'Amber Keeley', 'George Moore', 'Ti
m Johnson', 'Fiona Rowley', 'Dave Felton', 'Nisha Mehrotra', 'Michael Wilson', '
George Liddell', 'Nick Smith', 'Jack Farrant', 'Liam Zander', 'Lloyd Manning', '
Chloe McIntosh', 'Michael Nation', 'David Allen', 'Jack Grigg', 'Tom Archibald',
 'Patrick Timmins', 'David Sharp', 'Claire Murray', 'John Pocock', 'Adithya Sree
kumar', 'Hugo Borren', 'Jonathan Glendenning', 'Matt Burbury-King', 'Kerrie Cole
s', 'Andrew Mills', 'Martin Cannon', 'Tim Clemens', 'Jan Sintenie', 'Yi Zeng', '
Zac Gravatt', 'George Scott', 'Andrew Jackson', 'Finlay Wilkinson', 'Jono Entwis
tle', 'Jack Turley', 'Isaac Manuel', 'Wim Looman', 'James Peat', 'Haroun Barazan
chi', "Dylan D'Costa", 'Jacky Sung', 'Josie Norris', 'Anisha Dayaram', 'Nick Ess
', 'Charlie Wilkinson', 'Tom Williams', 'Thomas Oldfield', 'Dane Hart']"""

if __name__ == "__main__":
    people_list = "".join(terminal_data.splitlines())
    with open("people_list.txt",'w') as f:
        f.write(people_list)