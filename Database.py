import pandas as pd
import random
import uuid


class Database:
    userInput = []
    results = []

    def __init__(self):
        df_mal = pd.read_csv(r'Hispanic-Male-Names-Trimmed.csv')
        df_fem = pd.read_csv(r'Hispanic-Female-Names-Trimmed.csv')

        # join male and female name dataframes
        df_mal_fem = pd.concat([df_mal, df_fem])

        df_names = pd.DataFrame(df_mal_fem)

        # print(df_names) # debug

        # split each entry into elements
        df_names[['1', '2']] = df_mal_fem['first name'].str.split(' ', 1, expand=True)
        df_names[['3', '4']] = df_mal_fem['last name'].str.split(r'-|\s', 1, expand=True)

        # drop old columns
        df_names = df_names.drop(['last name', 'first name', 'gender', 'race'], axis=1)

        # shift elements left to remove null spaces (i.e. missing middle initial)
        df_names = df_names.T.apply(lambda x: sorted(x, key=pd.isnull)).T

        # generate random unique identifier for each entry
        df_names['ID'] = [uuid.uuid4() for entry in range(len(df_names.index))]

        # print(df_names) # debug

        # create dictionary of names as lists of elements with key UUID
        names_DB = df_names.set_index('ID').T.to_dict('list')

        df_names['role'] = None
        df_names['meaning'] = None
        df_names['descriptor'] = None
        df_names['title'] = None

        # generate dummy tags 
        roles = ["doctor", "teacher", "nurse", "clerk", None]
        meanings = ["full of sorrow", "warrior", "daisy flower", "pillar of strength", None]
        descriptors = ["kind", "shrewd", "troubled", "enthusiastic", None]
        titles = ["Sr.", "Jr.", None, None, None]

        for i in range(len(df_names)):
            df_names.iloc[i, df_names.columns.get_loc('role')] = roles[random.randint(0, 4)]
            df_names.iloc[i, df_names.columns.get_loc('meaning')] = meanings[random.randint(0, 4)]
            df_names.iloc[i, df_names.columns.get_loc('descriptor')] = descriptors[random.randint(0, 4)]
            df_names.iloc[i, df_names.columns.get_loc('title')] = titles[random.randint(0, 4)]


        self.database = df_names

    # ST 7
    def addEntry(self, userInput: str):
        # append empty row to df
        self.database.loc[self.database.shape[0]] = None

        i = 0
        j = 1
        for ele in userInput.split():
            if str(j) in self.database.columns:
                self.database.iloc[self.database.index[-1], i] = ele
                i += 1
                j += 1
            else:
                self.database.insert(i, str(j), None)
                self.database.iloc[self.database.index[-1], i] = ele
                i += 1
                j += 1

        # create uuid
        self.database.iloc[-1, self.database.columns.get_loc('ID')] = uuid.uuid4()

        return self.database

    def removeEntry(self, entryId: str):
        self.database.drop(self.database.index[self.database['ID'] == entryId], inplace=True)
        return self.database

    def validateInput(self, userInput: str):
        # gets search string from user
        if not userInput:
            print("Input cannot be empty")
            userInput = input("Enter search string: ")

        # claim 1b - 4

        # checks if input contains numbers
        # infinite while loop, broken when input is valid (no numbers detected)
        while True:
            # valid string boolean, default to True, changed to False when number is present
            isValid = True

            # loops through input string and checks for numbers
            for i in userInput:
                # if char is number, valid boolean is changed to False
                if i.isdigit():
                    isValid = False

            # if input is valid, exits the loop
            if isValid:
                break
            else:
                # resets input to a free variable and asks user for valid input
                del userInput
                print("String cannot contain numbers")
                userInput = input("Enter search string: ")

        wordIndex = 0
        loopIndex = 0
        elementString = ""
        for i in userInput:
            # checks if char is last in string
            if loopIndex == len(userInput) - 1:
                if i.isspace():
                    if wordIndex > 0:
                        self.userInput.append(elementString)
                        wordIndex = 0
                        elementString = ""
                else:
                    elementString = elementString + i
                    self.userInput.append(elementString)
                    wordIndex += 1

            # all other cases
            else:
                if i.isspace():
                    if wordIndex > 0:
                        self.userInput.append(elementString)
                        wordIndex = 0
                        elementString = ""
                else:
                    elementString = elementString + i
                    wordIndex += 1

            loopIndex += 1

    # ST 11 task 1
    # input is keypress that returns df row
    def select_search_entry(self, row: int, df):
        entryID = df['ID'].iloc[row]

        searchTerm = ""
        for r in range(10):
            if str(r) in self.database.columns:
                if self.database[str(r)].iloc[row] is not None:
                    searchTerm += self.database[str(r)].iloc[row] + " "
        searchTerm = searchTerm.strip()

        return searchTerm, entryID

    # searches through name (1, 2, 3, 4) columns for values containing input
    # jon will return jonathan
    # jonathon will not return jonathan
    # returns dataframe with only matching entries
    """PARAMS
    input: user's string input
    df: dataframe to search through
    """
    def search(self, case=False):

        # checks if there is user input yet. If not then get user input
        if not self.userInput:
            self.validateInput()

        """First name search"""
        """Search first name("1") column of `df`, return rows with any matches."""
        # column to search through
        columns = self.database[['1', '2', '3', '4']]

        results = self.database[
            columns.apply(
                # searches through columns for provided input
                lambda column: column.str.contains(self.userInput[0], regex=True, case=case, na=False)
            ).any(axis=1)
        ]

        self.results.append(results)

        if len(self.userInput) > 1:

            """Last name search"""
            """Search last name("3") column of `df`, return rows with any matches."""
            # column to search through
            columns = self.database[['3']]

            results = self.database[
                columns.apply(
                    # searches through columns for provided input
                    lambda column: column.str.contains(self.userInput[1], regex=True, case=case, na=False)
                ).any(axis=1)
            ]

            self.results.append(results)

    def printResults(self):
        if not self.results:
            self.search()

        if not self.results[0].to_string():
            print("NO PRIMARY RESULTS:\n")
        else:
            print("PRIMARY RESULTS:\n")
            print(self.results[0].to_string())

        if len(self.results) > 1:
            if not self.results[1].to_string():
                print("NO SECONDARY RESULTS:\n")
            else:
                print("SECONDARY RESULTS:\n")
                print(self.results[1].to_string())