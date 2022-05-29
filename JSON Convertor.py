#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd;
import numpy as np;

recipes_structure = pd.read_csv("Indian_recipes_Kenny_354.csv")

recipes_structure.columns


# In[16]:


## Creating Mapping

header = recipes_structure.columns.tolist()
recipes = recipes_structure.values.tolist()
recipes_map = {}

for recipe in recipes:
  
    recipe_title = recipe[0]
    
    if( recipe_title not in recipes_map.keys()):
        recipes_map[recipe_title] = recipe


print(recipes_map)


# In[17]:


# Store as a JSON
import json

with open('recipes_output.json', 'w+') as f:
    json.dump(recipes_map, f)


# In[ ]:




