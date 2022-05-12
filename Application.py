from Document import *
from Database import *


database = Database()
print(database.database)

# get search string from user
input = input("Enter search string: ")
database.validateInput(input)
database.search(input)
database.printResults()

# separate results for backend demo
print("\n\n\n############### Select entry to search document ###############")

print(database.select_search_entry(3, database.database))
#database.search(input)

#doc = Document(r"C:\Users\School\Desktop\4155 Project\testtext.txt")

#doc.preview()
#doc.search("jon")