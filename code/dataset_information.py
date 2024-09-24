##purpose of this script is to load in google sheets all datasets considered, and the dataset information for the datasets that 
#are included in the final unified set and push to huggingface
#%% 
from huggingface_hub import login
import pandas as pd
from datasets import  Dataset
from dotenv import load_dotenv
import os
#%% 
# Load environment variables from the .env file
load_dotenv('/Users/simonetaylor/Documents/variables.env')
# Retrieve the token from the environment variable
hf_login_token = os.getenv('hf_login_token')
# Login to Hugging Face with the retrieved token
login(hf_login_token)

# %%
##datsets to ingest can be found here
sheet_url = 'https://docs.google.com/spreadsheets/d/1a3ZjJ-t4a6QueDie7KSNGtZj8X0ovuAy22gFWAZzCT8/edit?gid=0'
csv_export_url = sheet_url.replace('/edit?gid=', '/export?format=csv&gid=')
dataset_information = pd.read_csv(csv_export_url)
dataset_information['datasets'] =dataset_information['HF Link'].apply(lambda x: x.replace('https://huggingface.co/datasets/',''))

# %%
##datasets considered can be found here
sheet_url = 'https://docs.google.com/spreadsheets/d/1a3ZjJ-t4a6QueDie7KSNGtZj8X0ovuAy22gFWAZzCT8/edit?gid=1303803115'
csv_export_url = sheet_url.replace('/edit?gid=', '/export?format=csv&gid=')
datasets_considered = pd.read_csv(csv_export_url)
# %%
##just to make column names consistant across other datasets 
dataset_information.columns = [x.lower() for x in dataset_information.columns]
dataset_information.columns = [x.replace(" ","_") for x in dataset_information.columns]
datasets_considered.columns = [x.lower() for x in datasets_considered.columns]
datasets_considered.columns = [x.replace(" ","_") for x in datasets_considered.columns]

# %%
ds_info = Dataset.from_pandas(dataset_information)
ds_considered = Dataset.from_pandas(datasets_considered)
#%% 
# Push the first split ('datasets_included') to the same repository
ds_info.push_to_hub("svannie678/democratizing_ai_inclusivity_red_team_dataset_information", config_name="dataset_included_information")
# Push the second split ('data') to the same repository
ds_considered.push_to_hub("svannie678/democratizing_ai_inclusivity_red_team_dataset_information", config_name="datasets_considered")


# %%
