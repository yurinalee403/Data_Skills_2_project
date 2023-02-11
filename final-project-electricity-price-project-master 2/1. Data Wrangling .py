

import requests
import json
import pandas as pd
import pprint
import json
import io
import ast

# Wdata wrangling

######## Retrieve market sales price of coal data from the EIA  from 2011-2021 ##


api_key = "A3f13WWmSnPcxwsaeWLMz792rEI6lwJHl5nTq2gb"


def load_parse_coal(url, params):
  
  urlData = requests.get(url, params=params).content

  # we need the file to json becaise type is bytes.
  urlJson = json.loads(urlData.decode('utf-8'))
  # changing data to lst
  lst = urlJson['response']['data']
  # lst to dataframe
  df = pd.DataFrame(lst)
  # drop the na 
  df = df.dropna()
  # drop the price which include 'w'. There were three market type and we want to focus on only total
  df = df[df['price'] != 'w']
  df = df[df['marketTypeDescription'] == 'Total']
  # rename the cloumn name
  df = df.rename(columns={'stateRegionId':'State'})
  # get only three columns amd save as df
  df = df[['period', 'State','price']]
  # Get a new column: the average price of  Coal  for the static plot
  df['avg'] = df.groupby(['period', 'State'])['price'].transform('mean') 

  return df


# 1. coal (market sales price, dollars per short ton)

# parameters to get coal data 
params = {
    "frequency": "annual",
    "facets": {},
    "start": "2011",
    "end": "2021",
    "offset": 0,
    "length": 5000,
}

# coal url
url = "https://api.eia.gov/v2/coal/market-sales-price/data/?api_key=" + api_key + "&data[]=price&data[]=sales"

coal = load_parse_coal(url, params)




# want to using the state abbrevation not the combined multiple states as a regionalstates
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
             'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
             'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
             'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
         'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

# keep only the states 
df2=coal.loc[coal['State'].isin(states)]





######## Retrieve  price of Natural gas  data from the EIA  from 2011-2021  ##########


url = 'https://api.eia.gov/v2/natural-gas/pri/sum/data?api_key=GdD5jQeStX1PAuc3a3ZqSUERNPilxXjfcyL0sBs3&data[]=value&frequency=annual&start=2001&end=2021&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=21077'
r = requests.get(url)
r

j = r.json()

df = pd.DataFrame(j['response']['data'])
df.head()

#df.to_csv('data.csv')
df.columns


df_resi = df[df['process-name']== 'Price Delivered to Residential Consumers']
df_new = df_resi.filter(['period', 'area-name','value', 'units'], axis = 1).reset_index(drop=True)
df_new.head(5)
#df_new.to_csv('data_new.csv')


df2 = df_new[df_new['units'] == '$/MCF'].dropna()
df2.replace('USA-', '', regex=True, inplace=True)
df2.head(5)
#df2.to_csv('dt3.csv')

df2['area-name'].values

us_state_to_abbrev = {
    'WASHINGTON':'WA',
    'NEW YORK':'NY',
    'MASSACHUSETTS':'MA',
    'COLORADO':'CO',
    'CALIFORNIA':'CA',
    'TEXAS':'TX',
    'OHIO':'OH',
    'MINNESOTA':'MN',
    'FLORIDA':'FL'
}

df2['area-name'] = df2['area-name'].replace(us_state_to_abbrev)
df2 = df2.rename(columns = {'area-name' :'stateid'})
df2.to_csv('natural_gas.csv', index = False)




######## Retrieve  price of Electrocity  data from the EIA  from 2011-2021  ##########



headers = {"X-Params": str({
    "frequency": "annual",
    "data": [
        "price"
    ],
    "facets": {},
    "start": "2001",
    "end": "2021",
    "sort": [
        {
            "column": "period",
            "direction": "desc"
        }
    ],
    "offset": 0,
    "length": 5000,
    "api-version": "2.0.4"
    })
    }

response = requests.get('https://api.eia.gov/v2/electricity/retail-sales/data/?api_key=xkfbZlNGAVXcYw3BvHVWzEKm506dWzVOaKaWhX8v&data[]=price&frequency=annual'
                       )
urlData = response.content



urlData


urlData = urlData.decode('utf-8').replace('null','None')


dct = ast.literal_eval(urlData)['response']['data']


df = pd.DataFrame(dct)


df.head(20)


df.to_csv('E_Price.csv')





















