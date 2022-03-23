import pandas as pd 
import uuid


df_mal = pd.read_csv(r'Hispanic-Male-Names-Trimmed.csv')
df_fem = pd.read_csv(r'Hispanic-Female-Names-Trimmed.csv')

# join male and female name dataframes
df_mal_fem = pd.concat([df_mal, df_fem])
df_names = pd.DataFrame()

print(df_names) # debug

# split each entry into elements
df_names[['1', '2']] = df_mal_fem['first name'].str.split(' ', 1, expand= True)
df_names[['3', '4']] = df_mal_fem['last name'].str.split(r'-|\s',1, expand= True)

# shift elements left to remove null spaces (i.e. missing middle initial)
df_names = df_names.T.apply(lambda x : sorted(x,key=pd.isnull)).T

# generate random unique identifier for each entry
df_names['ID'] = [uuid.uuid4() for entry in range(len(df_names.index))]

print(df_names) # debug

# create dictionary of names as lists of elements with key UUID
names_DB = df_names.set_index('ID').T.to_dict('list')

print(names_DB) # debug