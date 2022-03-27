import pandas as pd
import uuid


df_mal = pd.read_csv(r'Hispanic-Male-Names-Trimmed.csv')
df_fem = pd.read_csv(r'Hispanic-Female-Names-Trimmed.csv')

# join male and female name dataframes
df_mal_fem = pd.concat([df_mal, df_fem])

df_names = pd.DataFrame(df_mal_fem)

#print(df_names) # debug

# split each entry into elements
df_names[['1', '2']] = df_mal_fem['first name'].str.split(' ', 1, expand= True)
df_names[['3', '4']] = df_mal_fem['last name'].str.split(r'-|\s',1, expand= True)

# shift elements left to remove null spaces (i.e. missing middle initial)
df_names = df_names.T.apply(lambda x : sorted(x,key=pd.isnull)).T

# generate random unique identifier for each entry
df_names['ID'] = [uuid.uuid4() for entry in range(len(df_names.index))]

#print(df_names) # debug

# create dictionary of names as lists of elements with key UUID
names_DB = df_names.set_index('ID').T.to_dict('list')

#print(names_DB) # debug


#display(df_names)
#print(df_names[['1', 'first name']])


# gets search string from user
input = input("Enter search string: ")

# claim 1b - 4

# checks if input contains numbers
# infinite while loop, broken when input is valid (no numbers detected)
while True:
    # valid string boolean, default to True, changed to False when number is present
    isValid = True

    # loops through input string and checks for numbers
    for i in input:
        # if char is number, valid boolean is changed to False
        if i.isdigit() == True:
            isValid = False

    # if input is valid, exits the loop
    if isValid == True:
        break
    else:
        # resets input to a free variable and asks user for valid input
        del input
        print("String cannot contain numbers")
        input = input("Enter search string: ")



#part 1b-5
print(input)

# searches through name (1, 2, 3, 4) columns for values containing input
# jon will return jonathan
# jonathon will not return jonathan
# returns dataframe with only matching entries
"""PARAMS
input: user's string input
df: dataframe to search through
"""
def search(input: str, df, case=False):
    """Search all the text columns of `df`, return rows with any matches."""
    # columns to search through
    columns = df[['1', '2', '3', '4']]

    return df[
        columns.apply(
            # searches through columns for provided input
            lambda column: column.str.contains(input, regex=True, case=case, na=False)
        ).any(axis=1)
    ]

# prints results of search
print(search(input, df_names).to_string())