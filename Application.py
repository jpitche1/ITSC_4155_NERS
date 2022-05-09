from Document import *
from Database import *

doc = Document(r"C:\Users\School\Desktop\4155 Project\testtext.txt")

#doc.preview()
#doc.search("jon")

database = Database()
print(database.select_search_entry(3, database.database))
#database.validateInput()
#database.search()

#database.search()
#print(database.database)
#database.printResults()