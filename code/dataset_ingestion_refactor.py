##purpose of this script is to aggregate and unify existing red-teaming prompts that attempt to tease out 
#stereotypes, discrimination, hate speech, and other representation harms** in text-based Large Language Models (LLMs)
#%% 
from huggingface_hub import login
import pandas as pd
from datasets import load_dataset, Dataset
import re
from dotenv import load_dotenv
import os
#%% 
# Load environment variables from the .env file
load_dotenv('/Users/simonetaylor/Documents/variables.env')
# Retrieve the token from the environment variable
hf_login_token = os.getenv('hf_login_token')
# Login to Hugging Face with the retrieved token
login(hf_login_token)
#%% 
##datsets to ingest can be found here
sheet_url = 'https://docs.google.com/spreadsheets/d/1a3ZjJ-t4a6QueDie7KSNGtZj8X0ovuAy22gFWAZzCT8/edit?gid=0'
csv_export_url = sheet_url.replace('/edit?gid=', '/export?format=csv&gid=')
sheet_info = pd.read_csv(csv_export_url)
sheet_info['datasets'] =sheet_info['HF Link'].apply(lambda x: x.replace('https://huggingface.co/datasets/',''))
#%% 
#shared columns names across all datasets
reformatted_columns = ['organization','categorization_(by org)','prompt_type','prompt_instructions','prompt','explanation','ai_response']
#%%
#huggingface
hi = load_dataset(sheet_info['datasets'][0], split = 'train')
hi = pd.DataFrame(hi)
hi = hi[(hi.category_name == 'Societal Harm') & ((hi.challenges_name == 'Demographic stereotypes')| (hi.challenges_name == 'Demographic negative biases'))]
hi = hi[(hi.category_name == 'Societal Harm') & ((hi.challenges_name == 'Demographic stereotypes')| (hi.challenges_name == 'Demographic negative biases'))]
hi = hi[hi.submission_grade != 'unsubmitted']
hi = hi[hi.submission_grade != 'rejected']
hi.reset_index(drop = True, inplace=True)
hi["organization"] = sheet_info.Organization[0]
hi['categorization_(by org)'] = hi.apply(lambda x: x['category_name'] + "_" + x['challenges_name'],axis =1)
hi['prompt_type'] = sheet_info['Prompt Type'][0]
hi['prompt_instructions'] = hi['contestant_message']
hi['prompt'] = hi.conversation
hi['explanation'] = hi['user_justification'].apply(', '.join)
hi['ai_response'] = hi['submission_message'].apply(', '.join)
hi  = hi[reformatted_columns]

#%% 
#cohere
cohere = load_dataset(sheet_info['datasets'][1],split = "english")
cohere = pd.DataFrame(cohere)
cohere = cohere[cohere['harm_category'].apply(lambda x: 'Discrimination & Injustice' in x)]
cohere.reset_index(drop = True, inplace=True)
cohere["organization"] = sheet_info.Organization[1]
cohere['categorization_(by org)'] = cohere['harm_category'].apply(lambda x: x.replace("[","").replace("]","").replace(", ","_").replace('"', ''))
cohere['prompt_type'] = sheet_info['Prompt Type'][1]
cohere['prompt_instructions'] = None
cohere['explanation'] = cohere['explanation']
cohere['ai_response'] = None
cohere  = cohere[reformatted_columns]

#%%
#pku
pku = load_dataset(sheet_info['datasets'][2])
df_330k_train = pd.DataFrame(pku['330k_train'])
df_330k_test = pd.DataFrame(pku['330k_test'])
df_30k_train = pd.DataFrame(pku['30k_train'])
df_30k_test = pd.DataFrame(pku['30k_test'])
pku = pd.concat([df_330k_train, df_330k_test, df_30k_train, df_30k_test], ignore_index=True)
pku = pku[pku['category'].apply(lambda x: x.get('discrimination,stereotype,injustice', False))]
pku.drop_duplicates(subset=['prompt'],inplace=True)
pku.reset_index(drop = True, inplace=True)
pku["organization"] = sheet_info.Organization[2]
pku['categorization_(by org)'] = 'discrimination,stereotype,injustice'
pku['prompt_type'] = sheet_info['Prompt Type'][2]
pku['prompt_instructions'] = None
pku['explanation'] = None
pku['ai_response'] = pku['response']
pku  = pku[reformatted_columns]
# %%
#librAI
librAI = load_dataset(sheet_info['datasets'][3], split = 'train')
librAI = pd.DataFrame(librAI)
librAI =librAI[(librAI.risk_area == 'Discrimination, Exclusion, Toxicity, Hateful, Offensive') &
                ((librAI.types_of_harm == 'Social stereotypes and unfair discrimination')| (
                    (librAI.types_of_harm == 'Toxic language (hate speech)') & (librAI.specific_harms == 'Insult: Questions with the intention of disrespecting or offending someone/some group.')
                    ))]
librAI.reset_index(drop = True, inplace=True)
librAI["organization"] = sheet_info.Organization[3]
librAI['categorization_(by org)']  = librAI.apply(lambda x: x['risk_area'] + "_" + x['types_of_harm']+"_"+x['specific_harms'],axis =1)
librAI['prompt_type'] = sheet_info['Prompt Type'][3]
librAI['prompt_instructions'] = None
librAI['prompt'] = librAI['question']
librAI['explanation'] = None
librAI['ai_response'] = librAI['GPT4_response']
librAI  = librAI[reformatted_columns]

# %%
#jailbreakbench
jbb =load_dataset(sheet_info['datasets'][4],'behaviors')
jbb_h = pd.DataFrame(jbb['harmful'])
jbb_b = pd.DataFrame(jbb['benign'])
jbb = pd.concat([jbb_h, jbb_b],ignore_index=True)
jbb = jbb[jbb.Category == 'Harassment/Discrimination']
jbb.reset_index(drop = True, inplace=True)
jbb["organization"] = sheet_info.Organization[4]
jbb['categorization_(by org)']  = jbb.apply(lambda x: x['Category'] + "_" + x['Behavior'],axis =1)
jbb['prompt_type'] = sheet_info['Prompt Type'][4]
jbb['prompt_instructions'] = None
jbb['prompt'] = jbb['Goal']
jbb['explanation'] = None
jbb['ai_response'] = jbb['Target']
jbb  = jbb[reformatted_columns]

#% 
# %%
#babelscape
bs1 = load_dataset(sheet_info['datasets'][5], "alert")
bs2 = load_dataset(sheet_info['datasets'][5], "alert_adversarial")
bs1 = pd.DataFrame(bs1['test'])
bs2 = pd.DataFrame(bs2['test'])
bs = pd.concat([bs1, bs2],ignore_index=True)
bs.drop_duplicates(subset=['prompt'],inplace=True)
bs = bs[bs['category'].apply(lambda x: 'hate' in x)]
bs.reset_index(drop = True, inplace=True)
bs["organization"] = sheet_info.Organization[5]
bs['categorization_(by org)']  = bs['category']
bs['prompt_type'] = sheet_info['Prompt Type'][5]
bs['prompt_instructions'] = None
bs['explanation'] = None
bs['ai_response'] = None
bs  = bs[reformatted_columns]
#%% 
#allen
allen =load_dataset(sheet_info['datasets'][6])
allen_tr = pd.DataFrame(allen['train'])
allen_test = pd.DataFrame(allen['test'])
allen_v = pd.DataFrame(allen['validation'])
allen = pd.concat([allen_tr, allen_test,allen_v],ignore_index=True)
allen = allen[allen.source == 'sbic']
allen = allen[allen.response_id == 0]
allen.reset_index(drop = True, inplace=True)
allen["organization"] = sheet_info.Organization[6]
allen['categorization_(by org)']  = allen['source']
allen['prompt_type'] = sheet_info['Prompt Type'][6]
allen['prompt_instructions'] = None
allen['prompt'] = allen['context']
allen['explanation'] = allen['safety_annotation_reasons']
allen['ai_response'] = allen['response']
allen  = allen[reformatted_columns]

#%% 
#anthropic red team
anthropic = load_dataset("Anthropic/hh-rlhf", data_dir="red-team-attempts")
anthropic = pd.DataFrame(anthropic['train'])
anthropic = anthropic[anthropic['tags'].astype(str).apply(lambda x: 'Discrimination & injustice' in x)]
anthropic.reset_index(drop = True, inplace=True)
anthropic["organization"] = sheet_info.Organization[7]
anthropic['categorization_(by org)'] = anthropic['tags'].astype(str).apply(lambda x: x.replace("[","").replace("]","").replace(", ","_").replace('"', ''))
anthropic['prompt_type'] = sheet_info['Prompt Type'][7]
anthropic['prompt_instructions'] = None
anthropic['prompt'] = anthropic['transcript']
anthropic['explanation'] = anthropic['task_description']
anthropic['ai_response'] = None
anthropic  = anthropic[reformatted_columns]

#%% 
#co for AI
coai =load_dataset(sheet_info['datasets'][8])
coai_tr = pd.DataFrame(coai['train'])
coai_test = pd.DataFrame(coai['test'])
coai_v = pd.DataFrame(coai['validation'])
coai = pd.concat([coai_tr, coai_test,coai_v],ignore_index=True) 
coai = coai[coai.category == 'Biased Opinion']
coai.reset_index(drop = True, inplace=True)
coai["organization"] = sheet_info.Organization[8]
coai['categorization_(by org)']  = coai['category']
coai['prompt_type'] = sheet_info['Prompt Type'][8]
coai['prompt_instructions'] = None
coai['prompt'] = coai['context']
coai['explanation'] = None
coai['ai_response'] = coai['response']
coai  = coai[reformatted_columns]

#%% 
#NVIDIA
nvidia =load_dataset(sheet_info['datasets'][9])
nvidia_tr = pd.DataFrame(nvidia['train'])
nvidia_test = pd.DataFrame(nvidia['test'])
nvidia = pd.concat([nvidia_tr, nvidia_test],ignore_index=True) 
nvidia = nvidia[(nvidia.labels_0 == 'Hate/Identity Hate')|
                (nvidia.labels_1 == 'Hate/Identity Hate')|
                (nvidia.labels_2 == 'Hate/Identity Hate')|
                (nvidia.labels_3 == 'Hate/Identity Hate')|
                (nvidia.labels_4 == 'Hate/Identity Hate')]
nvidia.reset_index(drop = True, inplace=True)
nvidia["organization"] = sheet_info.Organization[9]
nvidia['categorization_(by org)']  = 'Hate/Identity Hate'
nvidia['prompt_type'] = sheet_info['Prompt Type'][9]
nvidia['prompt_instructions'] = None
nvidia['prompt'] = nvidia['text']
nvidia['explanation'] = None
nvidia['ai_response'] = nvidia['text_type']
nvidia  = nvidia[reformatted_columns]

#%%
#Aurora
def extract_prompt_aurora(text):
    match = re.search(r'### Instruction:\n(.*?)\n### Response:', text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Extract and strip leading/trailing spaces
    return None  # Return None if no match is found

def extract_response_aurora(text):
    match = re.search(r'\n### Response:\n(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip()  # Extract and strip leading/trailing spaces
    return None  # Return None if no match is found
#Apply the function to each row in the 'transcript' column and create a new 'prompt' column

aurora =load_dataset(sheet_info['datasets'][10])
aurora =  pd.DataFrame(aurora['train'])
aurora = aurora[aurora.category == 'hate speech, discrimination and vulgar language']
aurora.reset_index(drop = True, inplace=True)
aurora['prompt'] = aurora['text'].apply(extract_prompt_aurora)
aurora['ai_response'] = aurora['text'].apply(extract_response_aurora)
aurora["organization"] = sheet_info.Organization[10]
aurora['categorization_(by org)']  = 'hate speech, discrimination and vulgar language'
aurora['prompt_type'] = sheet_info['Prompt Type'][10]
aurora['prompt_instructions'] = None
aurora['explanation'] = None
aurora  = aurora[reformatted_columns]

#%% 
#salad bench
salad_a = load_dataset(sheet_info['datasets'][11], "attack_enhanced_set")
salad_b = load_dataset(sheet_info['datasets'][11], "base_set")
salad_d = load_dataset(sheet_info['datasets'][11], "defense_enhanced_set")
salad_a = pd.DataFrame(salad_a['train'])
salad_a['prompt'] = salad_a['augq']
salad_a= salad_a[['prompt','1-category','2-category','3-category']]
salad_b = pd.DataFrame(salad_b['train'])
salad_b['prompt'] = salad_b['question']
salad_b= salad_b[['prompt','1-category','2-category','3-category','source']]
salad_d = pd.DataFrame(salad_d['train'])
salad_d['prompt'] = salad_d['baseq']
salad_d= salad_d[['prompt','1-category','2-category','3-category']]
salad = pd.concat([salad_a, salad_b,salad_d],ignore_index=True)
salad = salad[(salad['1-category'] == 'O1: Representation & Toxicity')
                       &  ((salad['2-category'] == 'O2: Unfair Representation') 
                           | ((salad['2-category'] == 'O1: Toxic Content') & ((salad['3-category'] == 'O1: Hate Speech'))))]
salad.drop_duplicates(subset=['prompt'],inplace=True)
salad.reset_index(drop = True, inplace=True)
salad["organization"] = sheet_info.Organization[11]
salad['categorization_(by org)']  = salad.apply(lambda x: x['1-category'] + "_" + x['2-category']+ "_"+ x['3-category'],axis =1)
salad['prompt_type'] = sheet_info['Prompt Type'][11]
salad['prompt_instructions'] = None
salad['explanation'] = None
salad['ai_response'] = None
salad  = salad[reformatted_columns]
#%% 
#sorry bench
sorry = load_dataset(sheet_info['datasets'][12])
sorry = pd.DataFrame(sorry['train'])
##subset to categories of interest
sorry = sorry[(sorry.category == '2')|
              (sorry.category == '31')|
              (sorry.category == '36')]
sorry.reset_index(drop = True, inplace=True)
sorry["organization"] = sheet_info.Organization[12]
sorry['prompt_type'] = sheet_info['Prompt Type'][12]
sorry['prompt_instructions'] = None
category_mapping = {
    '2': "Social-group Insulting Words",
    '31': "Advice on Discrimination Behavior",
    '36': "Social Stereotype Promotion"
}
sorry['categorization_(by org)'] = sorry['category'].map(category_mapping)
sorry['prompt'] = sorry['turns'].apply(lambda x: ''.join(map(str, x)))
sorry['explanation'] = sorry['prompt_style']
sorry['ai_response'] = None
sorry  = sorry[reformatted_columns]
#%%
#final combined refined dataset
df = pd.concat([hi,cohere,pku,librAI,jbb,bs,allen,coai,nvidia,aurora,salad,sorry],ignore_index=True)
df = df.astype(str)
#rename columns so we can cross walk across the dataset information dataframes and this one
df['categorization'] = df['categorization_(by org)']
df = df[['organization','categorization','prompt_type','prompt_instructions','prompt','explanation','ai_response']]
#%% 
#push to huggingface datasets
ds_data = Dataset.from_pandas(df)
ds_data.push_to_hub("svannie678/democratizing_ai_inclusivity_red_team_prompts")
# %%
