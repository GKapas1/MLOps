import pandas as pd

h1=pd.read_csv(r'data\H1.csv')
h1['Type']='Resort'
h2=pd.read_csv(r'data\H2.csv')
h2['Type']='City'
joined=pd.concat([h1,h2]).reset_index().drop('index',axis=1)
joined.to_csv(r'data\hotels.csv')