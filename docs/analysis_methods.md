---
layout: base
title: Analysis Methods
nav-include: true
nav-order: 4
---
## Data Preparation
- **Data Loading**: All prompts were loaded into python via [HuggingFace datasets](https://huggingface.co/datasets/svannie678/red_team_repo_social_bias_prompts).
- **Data Cleaning**: Common and unnecessary strings (e.g., those starting with `#instruction`) were removed. Multi-turn prompts were concatenated into single strings for easier analysis.
- **Summary Statistics**: Summary statistics, like average prompt word count by dataset, were calculated to gain insights into the dataset's underlying structure.

## Analytical Approach
- **Preliminary Analysis**:I explored both supervised (keyword detection) and unsupervised (clustering) methods. I chose to focus on keyword analysis because the clustering results were unclear. Instead of grouping prompts by categories like age, race, or gender, they clustered mainly by length and scenario type.
- **Identifying Categories of Interest**: Groups of interest (like age,race, gender) were identified based on previous dataset categorizations.
- **Keyword Identification**: Keywords were generated through three methods:
  - **TF-IDF Analysis**: Ran out this traditional NLP approach based on pre-defined categories and selected the top 10 words per category. I then manually reviewed and kept relevant words (e.g., "black," "white"), while less meaningful words (e.g., "people," "flag") were disregarded.
  - **Previous Domain Knowledge**: I leveraged existing knowledge of stereotyping and discriminatory behaviors to add keywords like "deaf","blind" and "latinx".
  - **ChatGPT Assistance**: I prompted ChatGPT with the following request: “Here is a list of keywords I have to identify red-teaming prompts that mean to tease out stereotypes/discrimination/other representation harms in LLMs regarding a person's {category of interest}. Can you please add any words relating to {category of interest}? Please include derogatory terms.”

## Keyword Integration 
All identified keywords were combined into a single list. A prompt was tagged as relevant to a category if it contained at least one keyword, allowing prompts to be associated with multiple categories.
## Summary Statistics 
We calculated counts and proportions of prompts by category. Prompts that contained keywords from two or more categories were considered intersectional.

Additionally, counts for each keyword were compiled.

| Category            | Prompt Count | Percentage of Total (%) | Intersectional Count | Intersectional Percentage (%) |
|---------------------|-------|----------------|----------------------|-------------------------------|
| Race/Ethnicity      | 12998 | 32          | 2790                 | 21                        |
| None of the Above   | 10875 | 27          | 0                    | 0                         |
| Gender              | 9409  | 23          | 3326                 | 35                         |
| Religion            | 4922  | 12          | 1331                 | 27                         |
| Sexuality           | 3040  | 8          | 1004                 | 33                          |
| Disability          | 1794  | 4          | 909                  | 51                         |
| Body                | 1364  | 3           | 850                  | 62                         |
| Age                 | 1311  | 3           | 887                  | 68                          |
| Economic            | 919   | 2          | 589                  | 64                         |
