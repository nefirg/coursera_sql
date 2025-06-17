#!/usr/bin/env python
# coding: utf-8

# # CMPINF 2120 – Applied Predictive Modelling
# 
# ## Recommender Systems
# ---
# In this project, we will be doing a fun exercise to implement collaborative filtering for recommender systems. We will also learn how the choice of similarity metric in collaborative filtering can affect its output of predicted ratings.
# 
# Packages you will need for the project are,
# 
# * pandas
# * numpy
# * scipy
# 
# Recall that the numpy package provides nd-arrays and operations for easily manipulating them.
# Likewise, scipy provides an addtional suite of useful mathematical functions and distributions for numpy arrays, including distance functions which we will use in this project
# 
# ```
# # This is formatted as code
# ```
# 
#  to compute the measure of similarity. We will only import the distance funcions we need for today's session as shown below. Note that cityblock is just another name for Manhattan distance metric seen in class.

# In[1]:


import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
from scipy.stats import pearsonr


# ## User-Based vs Item-Based Recommendation
# There are two types of collaborative filtering methods: user-based and item-based.
# 
# User-based recommendation assumes that similar users give similar ratings to each item. Whereas item-based recommendation assumes that similar items receive similar ratings from each user. You can think of them as a dual of each other.
# 
# In this project, we will walk through an example of user-based recommendation.
# 
# ## Data Input

# In[2]:


df = pd.read_csv("movies_example.csv")
df


# ### Accessing rows in dataframe

# The two ways to access dataframes rows are shown below,

# In[3]:


# Converting value equality test fo a Series of booleans
df['Name'] == 'The Matrix'


# In[4]:


# First way to access rows
df[df['Name'] == 'The Matrix']


# In[5]:


# Second way
df.iloc[0]


# ### Missing values in data frame

# To exlude missing values or NaNs in a dataframe, we can use the notnull() function.

# In[6]:


df['Frank'].notnull()


# In[7]:


df['Elaine'].notnull()


# You can also perform logical operations on the boolean Series returned as shown below,

# In[8]:


df['Frank'].notnull() & df['Elaine'].notnull()


# You can also select subset of rows and columns where the boolean value is True.

# In[9]:


df_notmissing = df[['Frank','Elaine']][df['Frank'].notnull() & df['Elaine'].notnull()]
df_notmissing


# ## Similarity Metrics & Predicted Ratings
# Different distance metrics can be used to measure the similarity. In this project, we will use Euclidean, Manhattan, Pearson Correlation and Cosine distance metrics to measure the similarity.
# 
# ### Euclidean

# In[10]:


sim_weights = {}
for user in df.columns[1:-1]:
    df_subset = df[['Frank',user]][df['Frank'].notnull() & df[user].notnull()]
    dist = euclidean(df_subset['Frank'], df_subset[user])
    sim_weights[user] = 1.0 / (1.0 + dist)
print ("similarity weights: %s" % sim_weights)


# Now let's find the predicted rating of 'Frank' for 'The Matrix'. We can get all ratings for a movie by accessing a row of the dataframe using iloc learnt earlier. We only slice the columns of ratings we need indicated by the index [1:-1]. In this case we do not need the first column 'Name' and the last column 'Frank'.

# In[11]:


ratings = df.iloc[0][1:-1]
ratings


# Now we will find our predicted rating by multiplying each user weight with its corresponding rating for the movie matrix.

# In[12]:


predicted_rating = 0.0
weights_sum = 0.0
for user in df.columns[1:-1]:
    predicted_rating += ratings[user] * sim_weights[user]
    weights_sum += sim_weights[user]

predicted_rating /= weights_sum
print ("predicted rating: %f" % predicted_rating)


# ### Manhattan (Cityblock)

# We repeat our method of finding predicted rating using cityblock distance now.

# In[13]:


sim_weights = {}
for user in df.columns[1:-1]:
    df_subset = df[['Frank',user]][df['Frank'].notnull() & df[user].notnull()]
    dist = cityblock(df_subset['Frank'], df_subset[user])
    sim_weights[user] = 1.0 / (1.0 + dist)
print ("similarity weights: %s" % sim_weights)

predicted_rating = 0
weights_sum = 0.0
ratings = df.iloc[0][1:-1]
for user in df.columns[1:-1]:
    predicted_rating += ratings[user] * sim_weights[user]
    weights_sum += sim_weights[user]

predicted_rating /= weights_sum
print ("predicted rating: %f" % predicted_rating)


# ### Pearson Correlation Coefficient

# In[14]:


sim_weights = {}
for user in df.columns[1:-1]:
    df_subset = df[['Frank',user]][df['Frank'].notnull() & df[user].notnull()]
    sim_weights[user] = pearsonr(df_subset['Frank'], df_subset[user])[0]
print ("similarity weights: %s" % sim_weights)

predicted_rating = 0.0
weights_sum = 0.0
ratings = df.iloc[0][1:-1]
for user in df.columns[1:-1]:
    predicted_rating += ratings[user] * sim_weights[user]
    weights_sum += sim_weights[user]

predicted_rating /= weights_sum
print ("predicted rating: %s" % predicted_rating)


# Why nan?
# Because anything divided by 0 is undefined. Computing it again with this modfication gives the following.

# In[15]:


predicted_rating = 0.0
weights_sum = 0.0
ratings = df.iloc[0][1:-1]
for user in df.columns[1:-1]:
    if (not np.isnan(sim_weights[user])):
        predicted_rating += ratings[user] * sim_weights[user]
        weights_sum += sim_weights[user]

predicted_rating /= weights_sum
print ("predicted rating: %f" % predicted_rating)


# In[ ]:




