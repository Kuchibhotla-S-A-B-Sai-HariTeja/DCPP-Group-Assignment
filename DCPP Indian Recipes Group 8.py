#!/usr/bin/env python
# coding: utf-8

# ##### 29-May-22
# ## Data Cleaning and Pre-processing
# Kenny Devarapalli  
# Mrinal Chitranshu  
# Kuchibhotla SAB Hariteja  
# Madhab Chakraborty  
# Nagaraj G T  


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## All Recipes - Indian


is_link = 'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/'

driver = webdriver.Chrome(r"C:\Users\KennyD\ISB\chromedriver.exe")

driver.get(is_link)
time.sleep(2)

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



df = pd.DataFrame()
n=353
for link in recipe_links[354:]:
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
    time.sleep(10)



# Reading output of allrecipes/Indian
df1 = pd.read_csv(r"G:\ISB AMPBA\6. Data Pre-processing\Group Assignment\Indian_recipes_472.csv")




ingredient_columns = [col for col in df1.columns if 'ingredient ' in col]

unnamed_columns = [col for col in df1.columns if 'Unnamed' in col]

df1['Ingredients'] = df1[ingredient_columns].apply(lambda x: ','.join(x.dropna()), axis=1)

df1['Number of Ingredients'] = df1['Ingredients'].str.count(',')

df1 = df1.drop(ingredient_columns, axis=1)
df1 = df1.drop(unnamed_columns, axis=1)
df1.columns = df1.columns.str.title()


# To check if all Sugars have 'g' and no 'mg'
if df1['Sugars'].str.contains('mg').any():
    print ("mg is there")
else:
    print("No Sugar with 'mg'")



df1['Sugars (g)'] = df1['Sugars'].str.replace("g","").astype('float')
df1['Sugars (g)'].describe()




# To check if prep time contains 'hr' instead of 'min'
if df1['Prep'].str.contains('hr').any():
    print ("hr is there")



df1['Prep Time'] = df1['Prep'].fillna(0)
df1['Total Time'] = df1['Total'].fillna(0)


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



df1['Prep Time'] = df1['Prep'].apply(to_minutes)
df1['Total Time'] = df1['Total'].apply(to_minutes)



df1.to_csv(r"G:\ISB AMPBA\6. Data Pre-processing\Group Assignment\Indian_recipes_Kenny_434_cleaned.csv")


# ## Vegan Richa


lst_url = []
for row in table:
    for li in row.findAll('li'):
        time.sleep(13)
        lst_url.append(li.a['href'])

url = lst_url[0]
brkfst_url = []

for i in range(1,15):
    tmp_url = url +'page/{}/'.format(i)
    brkfst_url.append(tmp_url)

url = lst_url[1]
main_url = []

for i in range(1,29):
    tmp_url = url +'page/{}/'.format(i)
    main_url.append(tmp_url)

url = lst_url[2]
dess_url = []

for i in range(1,18):
    tmp_url = url +'page/{}/'.format(i)
    dess_url.append(tmp_url)

url = lst_url[3]
glut_url = []

for i in range(1,51):
    tmp_url = url +'page/{}/'.format(i)
    glut_url.append(tmp_url)
    
recipe_links = brkfst_url + main_url + glut_url + dess_url

recipe_details = {}

#df_fin = pd.DataFrame()

n=0
for url in recipe_links:
    n+=1    
        
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.find('h2',{'class':'wprm-recipe-name wprm-block-text-bold'})
    if title is not None:
        recipe_details['title'] = title.text
    else:
        recipe_details['title'] = np.nan
                      
    
    prep_time = soup.find('span',{'class':'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes'})
    if prep_time is not None:
        recipe_details['prep_time'] = prep_time.text
    else:
        recipe_details['prep_time'] = np.nan
        

    cook_time = soup.find('span',{'class':'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes'})
    if cook_time is not None:
        recipe_details['cook_time'] = cook_time.text
    else:
        recipe_details['cook_time'] = np.nan
        

    total_time = soup.find('span',{'class':'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes'})
    if total_time is not None:
        recipe_details['total_time'] = total_time.text
    else:
        recipe_details['total_time'] = np.nan
        

    cuisine = soup.find('span',{'class':'wprm-recipe-cuisine wprm-block-text-normal'})
    if cuisine is not None:
        recipe_details['total_time'] = cuisine.text
    else:
        recipe_details['total_time'] = np.nan
        

    course = soup.find('span',{'class':'wprm-recipe-course wprm-block-text-normal'})
    if course is not None:
        recipe_details['course'] = course.text
    else:
        recipe_details['course'] = np.nan

    calories = soup.find('span',{'class':'wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal'})
    if calories is not None:
        recipe_details['calories'] = calories.text
    else:
        recipe_details['calories'] = np.nan
        
    # Getting ingredients values
    ingredients = soup.find_all('li',{'class':'wprm-recipe-ingredient'})
    recipe_ingredients = {}    
    for i,row in enumerate(ingredients):
        recipe_ingredients['ingredient '+str(i+1)]=row.text
        
    # combining recipe attributes
    recipe_combined = {**recipe_details, **recipe_ingredients}
    
    df_row = pd.DataFrame(recipe_combined, index=[0])
    df_fin = df_fin.append(df_row)
        
    print(f'url {n} done')
    time.sleep(5)



df_gluten = pd.read_csv(r"G:\ISB AMPBA\6. Data Pre-processing\Group Assignment\Vegan_Richa_Glutenfree.csv")
df_gluten = df_gluten.drop('Unnamed: 0',axis=1)



df_gluten = df_gluten[~df_gluten['title'].isnull()]

ingredient_columns = [col for col in df_gluten.columns if 'ingredient ' in col]
df_gluten['Ingredients'] = df_gluten[ingredient_columns].apply(
    lambda x: ','.join(x.dropna()), axis=1)

df_gluten = df_gluten.drop(ingredient_columns, axis=1)
df_gluten.head()


df_gluten.columns = ['Title','Prep Time','Cook Time','Cuisine','Course','Calories','Ingredients']
df_gluten.head()



df_richa = pd.read_csv(r"G:\ISB AMPBA\6. Data Pre-processing\Group Assignment\Vegan_Richa_Breakfast_Main_Dessert.csv")

df_richa = df_richa[~df_richa['Title'].isnull()]

ingredient_columns = [col for col in df_richa.columns if 'ingredient ' in col]
df_richa['Ingredients'] = df_richa[ingredient_columns].apply(
    lambda x: ','.join(x.dropna()), axis=1)

df_richa = df_richa.drop(ingredient_columns, axis=1)
df_richa.head()



df_gluten.insert(loc=1, column='Author', value='Vegan Richa')

df_richa = df_richa.append(df_gluten)

df_kenny = df1[['Title','Author','Prep Time','Total Time','Calories','Ingredients']]

df_kenny.insert(loc=4, column='Cusine', value='Indian')
df_kenny.insert(loc=5, column='Course', value=np.nan)

df_kenny.columns = ['Title','Author','Prep Time','Cook Time','Cuisine','Course','Calories','Ingredients']
df_combined = df_kenny.append(df_richa)


df_combined.to_csv(r"G:\ISB AMPBA\6. Data Pre-processing\Group Assignment\Combined_food_recipes.csv")


# ## EDA

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='darkgrid')

df1['Diabetic Safe'] = np.where(df1['Sugars (g)']<6,'Safe','Not Safe')
df1['Diabetic Safe'].value_counts()


# # Top 10 Most Loved Food Recipe

data_Rating=df1[df1.Rating.isna()!=True]

plt.figure(figsize=(12,5))

ax=sns.barplot(y=data_Rating.sort_values(by='Rating', ascending=False).head(10).Title, 
            x=data_Rating.sort_values(by='Rating', ascending=False).head(10).Rating,
           palette='Set2')
for p in ax.patches:
    width = p.get_width()
    plt.text(60+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.0f}'.format(width),
             ha='center', va='center')

plt.xticks()

plt.xlabel('No. of ratings')
plt.ylabel('Food Recipe')
plt.title('Top 10 Most Loved Food Recipe', fontweight="bold")
plt.show()


# # Top 10 Food Recipe with high sugar content (To be avoided by diabetic)

plt.figure(figsize=(12,5))

ax=sns.barplot(y=df1.sort_values(by='Sugars (g)', ascending=False).head(10).Title, 
            x=df1.sort_values(by='Sugars (g)', ascending=False).head(10)['Sugars (g)'],
           palette='Set2')
for p in ax.patches:
    width = p.get_width()
    plt.text(2+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.0f}'.format(width),
             ha='center', va='center')

plt.xticks()
plt.xlabel('Sugar Content')
plt.ylabel('Food Recipe')
plt.title('Top 10 Food Recipe to be avoided by diabetic', fontweight="bold")
plt.show();


# # Top 10 Food Recipe with lowest sugar content

# In[30]:


plt.figure(figsize=(12,5))

ax=sns.barplot(y=df1.sort_values(by='Sugars (g)').head(10).Title, 
               x=df1.sort_values(by='Sugars (g)').head(10)['Sugars (g)'],
               palette='Set2')

plt.xticks()
plt.xlabel('Sugar Content')
plt.ylabel('Food Recipe')
plt.title('Top 10 Food Recipe to be avoided by diabetic', fontweight="bold")
plt.show();


# # Distribution based on total time taken in food preparation (Range=5 hours)

plt.figure(figsize=(12,5))
plt.hist(df_combined['Prep Time'],bins=50,range=[0,300]);


# # Distribution based on total time taken in food preparation (Range=2 hours)


plt.figure(figsize=(12,5))
plt.hist(df_combined['Prep Time'],bins=50,range=[0,120]);


# ## Distribution of Recipes based on number of ingredients required

plt.figure(figsize=(12,5))
df_combined['Number of Ingredients'] = df_combined['Ingredients'].str.count(',')

plt.hist(df_combined['Number of Ingredients'],bins=50,range=[0,120]);


## End




