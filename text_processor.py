# -*- coding: utf-8 -*-
from pandas import read_csv ## For importing .csv files
from fuzzywuzzy import fuzz ## For fuzzy string matching
import string ## Needed to write a string normalization function
 

print "\n\n\nFixing Caro's dupes."
slave_list = read_csv("the list retail_caro.csv")
master_list = read_csv("all SF accounts_caro.csv")

#slave_list = slave_list[0:100]
#master_list = master_list[0:500] ## Use these two lines to reduce the size of your data. Useful for fast testing and protoyping new features

threshold_value = 70  ## Tune this by hand to get good agreement. Probably you want a value between 70 and 90. It works like this:
#>>> fuzz.partial_ratio("this is a test", "this is a test!")
#    100

## Define a function that strips trailing/leading whitespace, punctuation, and also makes everything lowercase
def normalize(s):
    s = str(s)
    for p in string.punctuation:
        s = s.replace(p, '')
    return s.lower().strip()

set_of_matches = {
                  company 
	             for company in slave_list['Company Name'].values 
                  for account in master_list['Account Name'].values 
		         if normalize(company) in normalize(account)  ## Check normalized substrings first
		          or normalize(account) in normalize(company)
				or fuzz.partial_ratio(company, account) > threshold_value ## Check this last because it's slowest 
				}
## Note that set_of_matches is of datatype set, which natively enforces uniqueness

clean_df = slave_list[~slave_list['Company Name'].isin(set_of_matches)] ## Check membership and remove rows that matched
matches_df = slave_list[slave_list['Company Name'].isin(set_of_matches)] ## And give the complement, for completeness

print clean_df ## Print it to the terminal so we can see what's going on
print matches_df

clean_df.to_csv("threshold =", threshold_value, "Companies that don't appear in master list.csv") ## Write our results to file
matches_df.to_csv("threshold =", threshold_value, "Companies that appear in master list.csv")

print "checksum: total original rows in slave list = ", len(slave_list)
print "sum of clean_df rows and matches_df rows =", len(clean_df) + len(matches_df)