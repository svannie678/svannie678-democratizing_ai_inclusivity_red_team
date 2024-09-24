###the purpose of this script is to analyze what "kinds" of prompts are in the data (and what's missing!)
#%% 
from huggingface_hub import login
import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
import os
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

#%% 
# Load environment variables from the .env file
load_dotenv('/Users/simonetaylor/Documents/variables.env')
# Retrieve the token from the environment variable
hf_login_token = os.getenv('hf_login_token')
# Login to Hugging Face with the retrieved token
login(hf_login_token)

#%% 
pd.set_option('display.max_colwidth', None)  

# %%
ds = load_dataset("svannie678/democratizing_ai_inclusivity_red_team_prompts")
df = pd.DataFrame(ds['train'])

#%% 
#first I need to preprocess the data at bit
#here I am doing 2 things: removing any common and uncessary strings (like if every prompt starts with #instruction)
#and concatinating (?) multi turn prompts into one strings

#manually review sample for string manipulations
#df_sample= df.groupby('organization').apply(lambda x: x.sample(n=3, random_state=55)).reset_index(drop=True)
#df_sample
#%% 
df['prompt'] = df['prompt'].apply(lambda x: x.replace("### Instruction:\n","").replace("Response:\n","").replace('\n### ',""))
df_multi_hi = df[df.organization == 'Humane Intelligence']
def extract_multiturn_prompts_hi(prompt_str):
    try:
        prompt_list = ast.literal_eval(prompt_str.strip("'"))
        user_responses = [entry['body'] for entry in prompt_list if entry['role'].startswith('user')]
        return ' '.join(user_responses)  # Join user responses into a single string
    except (SyntaxError, ValueError):
        return ''  # Return empty string if there's an error in parsing

# Apply the function to the prompts column
df_multi_hi['prompt'] = df_multi_hi['prompt'].apply(extract_multiturn_prompts_hi)
df = pd.concat([df_multi_hi,df[df.organization != 'Humane Intelligence']]).reset_index(drop = True)
#%% 
#look at summary stats by original dataset
#get word counts by org 
# Function to count words in a prompt
def count_words(prompt_str):
    # Remove any extra whitespace and split the string into words
    words = prompt_str.split()  # This will split by whitespace
    return len(words)  # Return the number of words

df['word_count'] = df['prompt'].apply(count_words)

#a few orgs have MUCH longer prompts than others (humane intelligence bc its multiturn, OpenSafetyLab, NVIDIA, Princeton collab)
#this is a reason not to emloy an unsupervised clustering approach
df.groupby('organization').word_count.describe().sort_values('mean')
# %%
#I'm going to use a keyword based approach to categorize this data
# going to see if i can identify keywords from within the data itself 
#identify top unique keywords from each group 

# # Function to get top 10 words for each category
def get_top_n_words_per_group(df, n=10):
    top_words = {}
    
    # Group by category
    grouped = df.groupby(['organization','categorization'])['prompt'].apply(list)

    
    for categorization, prompts in grouped.items():
        # Join all prompts in the group into a single string
        text = ' '.join(prompts)
        
        # Compute TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray().flatten()
        
        # Create a DataFrame for sorting
        tfidf_df = pd.DataFrame({'word': feature_names, 'tfidf': tfidf_scores})
        
        # Sort by TF-IDF score and get the top n words
        top_n_words = tfidf_df.sort_values(by='tfidf', ascending=False).head(n)
        
        top_words[categorization] = top_n_words
    
    return top_words

# Get top 10 words for each category
top_words_per_category = get_top_n_words_per_group(df, n=10)

# Display results
for categorization, top_words in top_words_per_category.items():
    print(f"{categorization}")
    print(top_words)
    print("\n") 
#%%
keywords_tfidf = {
    'race/ethnicity':['africa','albanian','asian','biracial','black','canadian','chinese','croatian','dutch','eastern','ethnic','filipino',
    'haudenosaunee','indian','kaffir','korean','malaysian','mexican','multiracial','nitchies','ockers','pajeet','palestinian',
    'pashtun','racial','russian','souper','squaw','taiwanese','tamil','thai','torontonian','wetback','white','wop\b'],
    
    'gender':['female','girl','mammies','man\b','maternity','men\b','mother','pregnant','sister','trans','woman','women'],
    
    'age': ['\bold'],

    'disability': ['\babled','accommodat','able bodied','able-bodied','\bdisabled','disabil','illness','mental','wheelchair'],

    'religion': ['amish','buddhist','christian','hindu','islam','jew','muslim'],

    'body': ['acne','fat\b','fit\b','obese','weight','ranga\b','skinny','tall\b','vain'],

    'sexuality': ['gay','lesbian','lgbtq','muncher','promiscuous'],

    'economic': ['homeless','money','poor\b','rich','stingy','uneducated','university'],
    'none of the above': []
}
keywords_domain_knowledge = {
    'race/ethnicity':['causasian','hispanic','latino','latinx','latina','arab','native american','indigenous','pacific islander','japanese','vietnamese',
    'aboriginal','nigga','nigger','niggs','chink\b','redskin','paki','white trash','beaner','race','irish','japanese','german','negro','italian','skin color',
    'middle east','cajun','people of color','gook','pikey','turks'],
    
    'gender':['male','husband','gender','non-binary','feminin','masculin','pregnant','sexist','wife','boyfriend','girlfriend'],

    'age': ['young','\bage','teen','elderly','senior','ageing','geriatric','codger','geezer','millennial','middle-age'],

    'disability':['deaf','blind','handicap','autistic','neurodiverse','mobility','impairment','dyslexia','adhd','ptsd',
    'cripple','retard','special needs','schizophren','prosthetic','accessibil'] ,

    'religion':['religion','cult\b','faith','agnostic','atheist','secular','spiritual','sikh','jain','shinto','tao','mormon','buddhis'] ,
    'body': ['appearance','curvy','muscular','proportion','piercing','tattoo','beauty','ugly','attractive','handsome','lardass',
    'anorex','scrawny','bulim','pudgy','hairy','fatty'] ,

    'sexuality': ['sexual','queer','kink','sex worker','prostitut','polyamorous','swinger','pervert','deviant','slut','whore','homo'] ,

    'economic': ['wealthy','affluent','middle class', 'upper class', 'working class','lower class', 'economic', 'financ',
    'beggar','freeloader','deadbeat','welfare queen','low-income'],
    'none of the above': []
}

keywords_chatgpt = {
    'race/ethnicity':['afro-','Chilean', 'Colombian', 'Dominican', 'Guatemalan', 'Honduran', 'Peruvian', 'Venezuelan',
    'Kurdish', 'Iranian', 'Iraqi', 'Saudi', 'Syrian', 'Turkish', 'Yemen'],
    
    'gender':['lady','lass','dame', 'feminism', 'gender','two-spirit','hermaphrodite','bitch','tomboy','bimbo','man-hater'],

    'age': ['youth', 'child', 'adolescent', 'young adult', 'baby boomer', 'generation x', 'generation z', 'aging population', 'octogenarian', 
    'nonagenarian', 'centenarian','over-the-hill','senile', 'pensioner'], 

    'disability':['psychological disorder', 'crazy', 'lunatic', 'insane', 'freak', 'gimp', 'spaz'],

    'religion':['judaism','sharia','evangelical', 'orthodox', 'catholic','protestant','\bzen','quaker','zoroastrian','pagan',
    'satanism','new age','wiccan','heretic','infidel','zealot','cultist','fanatic','devil worshipper','holy roller',
    'bible thumper','godless','religious nut','\bsect\b','snake handler','fundamentalist'] ,

    'body': ['beautiful','gorgeous','pretty','sexy','\bslim', 'chubby','stocky','short','bald', 'wrinkled', 
    'pockmarked', 'haggard','youthful','toothless', 'bag of bones','blimp'] ,

    'sexuality': ['fetish','BDSM\b', 'fag','dyke','cocksucker','pillow biter','fruitcake'] ,

    'economic': ['social class','poverty','debt\b','bankrupt','underprivileged','disadvantaged'],
    'none of the above': []
}

keywords = {}
all_keys = set(keywords_tfidf.keys()).union(set(keywords_domain_knowledge.keys())).union(set(keywords_chatgpt.keys()))

for key in all_keys:
    # Get values from both dictionaries, defaulting to an empty list if the key is missing
    values1 = keywords_tfidf.get(key, [])
    values2 = keywords_domain_knowledge.get(key, [])
    values3 = keywords_chatgpt.get(key, [])

    combined_values = list(set(values1 + values2 + values3))


    # Concatenate the values
    keywords[key] = values1 + values2 + values3

keywords
#%% 
def categorize_prompt(prompt, keywords):
    matches = []
    for category, kws in keywords.items():
        for kw in kws:
            if kw.lower() in prompt.lower():
                matches.append((category, kw))  # Store the category and the matched keyword
    return matches if matches else [('none of the above', '')]  # Return a tuple if no matches found

# Apply categorization
df['kw_categories'] = df['prompt'].apply(lambda x: categorize_prompt(x, keywords))

df['matched_category'] = df['kw_categories'].apply(lambda x: [match[0] for match in x])
df['matched_category'] = df['matched_category'].apply(lambda x: list(set(x)))
df['matched_keyword'] = df['kw_categories'].apply(lambda x: [match[1] for match in x])
df['matched_keyword'] = df['matched_keyword'].apply(lambda x: list(set(x)))

#%% 
df_sample= df.groupby('organization').apply(lambda x: x.sample(n=10, random_state=55)).reset_index(drop=True)
df_sample
# %%
#get overall counts and intersectional counts by category
category_counts = df['matched_category'].apply(pd.Series).stack().value_counts()
total_prompts = len(df)
category_proportions = category_counts / total_prompts

# Combine counts and proportions into a DataFrame for better readability
summary_stats = pd.DataFrame({
    'count': category_counts,
    'proportion': category_proportions
}).reset_index()

# Rename columns for clarity
summary_stats.columns = ['category', 'count', 'proportion']

#now get the % of each category that is intersectional and main intersections
intersectional_prompts = df[df['matched_category'].apply(lambda x: len(x) > 1)]
intersectional_counts = intersectional_prompts.explode('matched_category')['matched_category'].value_counts()
intersectional_counts

summary_stats_intersectional = pd.DataFrame({
    'count': category_counts,
    'intersectional_count': intersectional_counts
}).fillna(0)  # Fill NaN values with 0 for categories that are not intersectional

summary_stats_intersectional.reset_index(inplace=True)
# Step 5: Calculate proportions
summary_stats_intersectional['intersectional_percentage'] = (summary_stats_intersectional['intersectional_count'] / summary_stats_intersectional['count']) 
# Reset index for better readability

summary_stats_intersectional.columns = ['category', 'count', 'intersectional_count', 'intersectional_percentage']
summary_stats = summary_stats.merge(summary_stats_intersectional,'right')
summary_stats = summary_stats.sort_values('count',ascending = False)
summary_stats
#%% 
#plot it
plt.figure(figsize=(10, 6),facecolor='#ede4dd')
plt.gca().set_facecolor('#ede4dd')
bar_width = 0.35
index = range(len(summary_stats))

# Bars for total counts (light purple)
plt.bar(index, summary_stats['count'], bar_width, color='#7A3C98', label='Total Count', alpha=0.7)

# Bars for intersectional counts (dark purple)

plt.bar([i + bar_width for i in index], summary_stats['intersectional_count'], bar_width, color='#D6A4E0', label='Intersectional Count', alpha=0.7)

# Set labels and title
plt.xlabel('Categories')
plt.ylabel('Number of Prompts')
plt.title('Distribution of Categories and Intersectional Counts')
plt.xticks([i + bar_width / 2 for i in index], summary_stats['category'], rotation=20)  # Tilt x-axis labels

# Add legend and layout adjustments
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
#%% 
#now I want to look at the keywords more closely
results = []

#Count occurrences for each keyword in each category
for category, keywords in keywords.items():
    print(category)
    for keyword in keywords:
        count = 0
        for index, row in df.iterrows():
            # Check if the keyword is present in the matched keywords (which is a list)
            if keyword in row['matched_keyword']:
                count += 1
        results.append({'category': category, 'keyword': keyword, 'count_word': count})

summary_df = pd.DataFrame(results)

print(summary_df)
#%% 
#get proportions of the top 10 words
summary_df_word = summary_df.merge(summary_stats_intersectional[['category','count']])
summary_df_word['word_prop'] = summary_df_word['count_word'] / summary_df_word['count']

#summary_df_word = summary_df_word.groupby('category').head(10)
summary_df_word = summary_df_word.sort_values(by='word_prop', ascending=False).groupby('category').head(10)
#%% 
#plot each categories top keywords
sns.set(style="whitegrid")

# Step 2: Create a bar chart for each category
categories = summary_df_word['category'].str.replace("/"," or ").unique()
summary_df_word['category'] = summary_df_word['category'].str.replace("/"," or ")
for category in categories:
    category_df = summary_df_word[summary_df_word['category'] == category]
    
    # Sort by word_prop in descending order
    category_df = category_df.sort_values(by='word_prop', ascending=False)
    category_df['word_prop'] = category_df.word_prop.round(2)*100


    # Create the bar plot
    plt.figure(figsize=(10, 6),facecolor='#ede4dd')
    plt.gca().set_facecolor('#ede4dd')
    sns.barplot(x='keyword', y='word_prop', data=category_df, palette='viridis')
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

    # Set plot title and labels
    plt.title(f'Top Keywords for the {category.capitalize()} Category', fontsize=16)
    plt.xlabel('Keyword', fontsize=12)
    plt.ylabel('Percentage of Prompts within Category', fontsize=12)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()  # Adjust layout to prevent clipping
    
    #plt.savefig(f'{category}_keyword.png', bbox_inches='tight')  # Save the figure
    plt.close() 
#%% 
#pull out prompt examples 
samples_list = []

# Step 2: Iterate through each keyword and collect samples
for index, row in summary_df_word.iterrows():
    category = row['category']
    keyword = row['keyword']
    
    # Filter prompts that contain the keyword
    matching_prompts = df[df['matched_keyword'].apply(lambda x: keyword in x)]
    
    # Randomly sample 1 or 2 prompts
    if not matching_prompts.empty:
        samples = matching_prompts.sample(min(2, len(matching_prompts)))  # Sample 1 or 2 prompts
        for _, sample_row in samples.iterrows():
            samples_list.append({
                'category': category,
                'keyword': keyword,
                'sample_prompt': sample_row['prompt']
            })

# Step 3: Create a DataFrame from the list
sample_df = pd.DataFrame(samples_list)
#%% 
# Display the sample DataFrame
sample_df
sample_df.to_csv('sample_dataframe.csv', index=False)
#%% 
#for right now I'm just manually copy and pasting examples into a markdown file but in theres gotta be a bettr way in the future
print(sample_df[sample_df['category'] == 'sexuality'].reset_index(drop = True).to_html(index = False))
# %%
