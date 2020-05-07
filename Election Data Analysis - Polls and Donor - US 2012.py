'''
Election Data - Polls and Donor - US 2012
1.) Who was being polled and what was their party affiliation?
2.) Did the poll results favor Romney or Obama?
3.) How do undecided voters effect the poll?
4.) Can we account for the undecided voters?
5.) How did voter sentiment change over time?
6.) Can we see an effect in the polls from the debates?
'''

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
%matplotlib inline
import requests
from io import StringIO
from datetime import datetime

#grabs election poll data from url

url = 'http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv'
source = requests.get(url).text
poll_data = StringIO(source)

#create poll dataset from above site

poll_df = pd.read_csv(poll_data)
poll_df.info()

poll_df.head()


#1.) Who was being polled and what was their party affiliation?
#Shows Affiliation split for 2012 election

sns.catplot('Affiliation', data= poll_df, kind= 'count')

#Shows Affiliation split for 2012 election by registred voters

sns.catplot('Affiliation', data= poll_df, hue= 'Population', kind='count')

poll_df.head()

#shows the percentage split of how voters are likely to vote

avg = pd.DataFrame(poll_df.mean())

avg.drop(['Number of Observations', 'Question Text', 'Question Iteration'], axis=0 , inplace=True)

avg.head()

#shows the standard deviation percentage

std = pd.DataFrame(poll_df.std())

std.drop(['Number of Observations', 'Question Text', 'Question Iteration'], axis=0 , inplace=True)

std.head()

avg.plot(yerr=std, kind='bar', legend= False,)

poll_avg = pd.concat([avg, std], axis=1)

poll_avg.columns = ['Average', 'STD']

poll_avg

poll_df.head()

#spread of polls by date

poll_df.plot(x='End Date', y=['Obama', 'Romney', 'Undecided', 'Other'], linestyle='', marker = 'o')

#dataset showing point differnce between candidtates

poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100
poll_df.head()

poll_df = poll_df.groupby(['Start Date'], as_index = False).mean()

poll_df.drop(['Question Text', 'Question Iteration', 'Number of Observations'], axis=1 , inplace=True)

poll_df.head()

#dataset showing point differnce between candidtates over time

poll_df.plot('Start Date', 'Difference', figsize=(12,4), marker='o', linestyle='-', color='blue' )

#function to find dabate start dates and end dates to drill into percentage
#point shifts during those debates

row_in = 0
xlimit = []

for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in += 1
    else:
        row_in += 1

print (min(xlimit))
print (max(xlimit))

#Detailed chart showing point changes during debates

poll_df.plot('Start Date', 'Difference', figsize=(12,4), marker='o', linestyle='-', color='blue', xlim=(325,352) )

#Oct 03
plt.axvline(x=325+2, linewidth = 3, color='red')
#Oct 11
plt.axvline(x=325+10, linewidth = 3, color='red')
#Oct 22
plt.axvline(x=325+21, linewidth = 3, color='red')

#data frame to detail donors / donations for candidtates

donor_df = pd.read_csv('Election_Donor_Data.csv')

donor_df.info()

donor_df.head()

donor_df['contb_receipt_amt'].value_counts()

don_mean = donor_df['contb_receipt_amt'].mean()

don_std = donor_df['contb_receipt_amt'].std()

print (f'The average donation was £{round(don_mean, 2)} with a std £{round(don_std,2)}')

#this shows refunds

top_donor = donor_df['contb_receipt_amt'].copy()

top_donor.sort_values(ascending=False, inplace=True)

top_donor

#refunds omitted from dataset

top_donor = top_donor[top_donor > 0]

top_donor.sort_values(ascending=False, inplace=True)

top_donor.value_counts().head(10)

com_don = top_donor[top_donor < 2500]

com_don.hist(bins=100)

#Adds which party a candidate represents

candidates = donor_df.cand_nm.unique()

candidates

party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

donor_df['Party'] = donor_df.cand_nm.map(party_map)

donor_df = donor_df[donor_df.contb_receipt_amt > 0]

donor_df

#number of donations per candidate

donor_df.groupby('cand_nm')['contb_receipt_amt'].count()

donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

#Value of donations accepted

cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

i =0

for don in cand_amount:
    print(f'The candidtate {cand_amount.index[i]} raised {round(don,0)} dollars \n')
    i += 1

    cand_amount.plot(kind='bar')

#Donation by group

    donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')

#Dataset to show donations by occupation

occupation_df = donor_df.pivot_table('contb_receipt_amt', index = 'contbr_occupation', columns='Party', aggfunc ='sum')

occupation_df.head()

occupation_df = occupation_df[occupation_df.sum(1) > 1000000]

occupation_df.plot(kind='bar')

occupation_df.plot(kind='barh', figsize=(10,10), cmap='seismic')

#combines duplicate CEO's and omit irrelivant data

occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS', 'INFORMATION REQUESTED'], axis=0, inplace=True)

occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']

occupation_df.drop('C.E.O.', inplace = True)

occupation_df.plot(kind='barh', figsize=(10,10), cmap='seismic')
