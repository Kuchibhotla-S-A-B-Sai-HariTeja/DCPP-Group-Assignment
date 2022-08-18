import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests


# ## All Recipes - Indian


is_link = 'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/'

driver = webdriver.Chrome(r"C:\Users\KennyD\ISB\chromedriver.exe")

driver.get(is_link)
time.sleep(2)

# For Clicking the Load More button
for i in range(20):
    driver.find_element(By.XPATH, "//a[@class='category-page-list-related-load-more-button manual-link-behavior']").click()
    time.sleep(5)
    
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html, 'html.parser')

table = soup.findAll('a',{'class':['card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom',
                                   'recipeCard__titleLink elementFont__titleLink margin-8-bottom']})

recipe_links = []
for row in table:
    if 'https://www.allrecipes.com/recipe/' in row['href']:
        recipe_links.append(row['href'])

no_of_recipes = len(recipe_links)

n=0

df = pd.DataFrame()
for link in recipe_links:
    n+=1
    url = link
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    
    # Initializing dictionary
    recipe_details = {}
    
    # Getting the headline
    headline = soup.find('h1',{'class':'headline heading-content elementFont__display'})
    if headline is not None:
        recipe_details['Title'] = headline.text
    else:
        recipe_details['Title'] = np.nan
    
    # Getting the description
    description = soup.find('p',{'class':'margin-0-auto'})
    if description is not None:
        recipe_details['Description'] = description.text
    else:
        recipe_details['Description'] = np.nan
    
    # Getting the rating
    rating = soup.find('span',{'class':'ugc-ratings-item elementFont__details'})
    if rating is not None:
        recipe_details['Rating'] = rating.text.split(' ')[1]
    else:
        recipe_details['Rating'] = np.nan
    
    # Getting the reviews
    review = soup.find('a',{'class':'ugc-ratings-link elementFont__detailsLink--underlined ugc-reviews-link'})
    if review is not None:
        recipe_details['Review'] = int(review.text.split(' ')[1].replace(',',''))
    else:
        recipe_details['Review'] = np.nan
    
    # Getting the author data
    author = soup.find('a',{'class':'author-name author-text__block elementFont__detailsLinkOnly--underlined elementFont__details--bold'})
    if author is not None:
        recipe_details['Author'] = author.text
        recipe_details['Author source'] = author['href']
    else:
        recipe_details['Author'] = np.nan
        recipe_details['Author source'] = np.nan
    
    # Getting recipe time
    table = soup.find_all('div',{'class':'recipe-meta-item-body elementFont__subtitle'})
    value_list = [row.text for row in table]
    table = soup.find_all('div',{'class':'recipe-meta-item-header elementFont__subtitle--bold elementFont__transformCapitalize'})
    heading_list = [row.text[:-1] for row in table]
    recipe_time = dict(zip(heading_list, value_list ))
    
    # Getting recipe nutrition values
    table = soup.find_all('span',{'class':'elementFont__details--bold elementFont__transformCapitalize'})
    nutrition_list = [row.text for row in table]
    table = soup.find_all('span',{'class':'nutrient-value'})
    nutrition_values = [row.text for row in table]
    recipe_nutrition = dict(zip(nutrition_list, nutrition_values ))
    
    # Getting ingredients values
    ingredients = soup.find_all('span',{'class':['ingredients-item-name elementFont__body']})
    recipe_ingredients = {}
    for i,row in enumerate(ingredients):
        recipe_ingredients['ingredient '+str(i+1)]=row.text
        
    # Getting calories data
    calories = soup.find_all('div',{'class':'nutrition-top light-underline elementFont__subtitle'})
    if calories is not None:
        recipe_details['calories'] = float(calories[0].text.split('Calories: ')[1])
    else:
        recipe_details['calories'] = np.nan
    
    # combining recipe attributes
    recipe_combined = {**recipe_details, **recipe_time, **recipe_nutrition, **recipe_ingredients}
    
    df_row = pd.DataFrame(recipe_combined, index=[0])
    df = df.append(df_row)
    
    print(f'url {n} done, {no_of_recipes-n} left')
    time.sleep(5)

ingredient_columns = [col for col in df.columns if 'ingredient ' in col]

unnamed_columns = [col for col in df.columns if 'Unnamed' in col]

df['Ingredients'] = df[ingredient_columns].apply(lambda x: ','.join(x.dropna()), axis=1)

df['Number of Ingredients'] = df['Ingredients'].str.count(',')

df = df.drop(ingredient_columns, axis=1)
df = df.drop(unnamed_columns, axis=1)
df.columns = df.columns.str.title()

## Cleaning text data and converting to numeric

df['Sugars (g)']        = df['Sugars'].str.replace("g","").astype('float')
df['Carbohydrates (g)'] = df['Carbohydrates'].str.replace("g","").astype('float')
df['Protein (g)']       = df['Protein'].str.replace("g","").astype('float')
df['Dietary Fiber (g)'] = df['Dietary Fiber'].str.replace("g","").astype('float')
df['Fat (g)']           = df['Fat'].str.replace("g","").astype('float')
df['Vitamin A (IU)']    = df['Vitamin A Iu'].str.replace("IU","").astype('float')
df['Vitamin C (mg)']    = df['Vitamin C'].str.replace("mg","").astype('float')
df['Folate (mcg)']      = df['Folate'].str.replace("mcg","").astype('float')
df['Calcium (mg)']      = df['Calcium'].str.replace("mg","").astype('float')
df['Iron (mg)']         = df['Iron'].str.replace("mg","").astype('float')
df['Magnesium (mg)']    = df['Magnesium'].str.replace("mg","").astype('float')
df['Potassium (mg)']    = df['Potassium'].str.replace("mg","").astype('float')
df['Sodium (mg)']       = df['Sodium'].str.replace("mg","").astype('float')

cols = ['Sugars','Carbohydrates','Protein','Dietary Fiber','Fat','Vitamin A Iu','Vitamin C','Folate',
       'Calcium','Iron','Magnesium','Potassium','Sodium']

df.drop(cols, axis=1, inplace=True)

# Imputing null values with 0
df['Prep Time']  = df['Prep'].fillna(0)
df['Total Time'] = df['Total'].fillna(0)

df = df.fillna(0)

# Converting time to seconds based on text 'min'
def to_minutes(time_string):
    time_string = str(time_string)
    if 'hr' in time_string and 'min' in time_string:
        hours, minutes = time_string.split(' ')[0],time_string.split(' ')[2]       
        return int(hours) * 60 + int(minutes)
    elif 'hr' in time_string:
        return int(time_string.split(' ')[0]*60)
    elif 'min' in time_string:
        return int(time_string.split(' ')[0])
    else: return 0


df['Prep Time']  = df['Prep'].apply(to_minutes)
df['Total Time'] = df['Total'].apply(to_minutes)

df.to_json("all_recipies.json",orient="records")