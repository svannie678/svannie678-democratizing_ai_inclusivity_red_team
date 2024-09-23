---
layout: base
---

![AI Generated Capstone Project logo](/assets/css/images/logo_option_2.jpg)

Hi all! My name is Simone Van Taylor, and I am a Data Scientist with a deep passion for designing language models that don’t perpetuate harmful content like racism and misogyny.

For my 2024 [AI Safety Capstone Project](https://aisafetyfundamentals.com/), I aggregated, unified, and analyzed existing open-source red-teaming datasets aimed at identifying **stereotypes, discrimination, hate speech, and other representation harms** in text-based LLMs.

<a href="https://huggingface.co/datasets/svannie678/democratizing_ai_inclusivity_red_team_prompts" style="display: inline-block; background-color: #d1bbea; color: #000; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold;">
    Check out the prompts 🤗 
</a>
<br><br> <!-- Add line breaks for spacing -->
<a href="https://huggingface.co/datasets/svannie678/democratizing_ai_inclusivity_red_team_dataset_information" style="display: inline-block; background-color: #d1bbea; color: #000; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold;">
    Learn more about all the datasets considered 🤗
</a>

### Why?
- To minimize duplication of future efforts for red-teamers and model owners.
- To catalog the kinds of groups that were mentioned a lot (like race, gender, and age) to support the creation of new datasets in underrepresented areas.
- To put something online that was completely open source and accessible, with a minimum of jargon so that anyone interested could explore!

### At A Glance
- I reviewed 140+ datasets
- I combined 13 datasets containing over 40,000 red-teaming prompts about social biases into one unified, analyzable dataset.
- I categorized each prompt into the group type that it targeted and analyzed the prevalence of major categories like race, gender, and age
### Key Takeaways
![Bar Chart showing prevalance and intersectionality by Category](/assets/css/images/Distro_overview.png)

- Red-teaming prompts aimed at uncovering race or ethnicity biases were the most prevalent, comprising XX% of all prompts, with specific mentions of around YYY being the most common
- Prompts aimed at uncovering less prevalent forms of discrimination, such as age, represented only XX% of overall prompts; however, they were highly intersectional. About 70% of these prompts were also categorized in another group
- The keyword-based categorization approach was somewhat ad-hoc; approximately 25% of prompts did not fit into any predefined category

- [SafetyPrompts.com](https://safetyprompts.com/) is a GREAT resource for exploring open-source datasets regarding AI safety
- Anthropic’s [seminal dataset of red-teaming prompts](https://huggingface.co/datasets/Anthropic/hh-rlhf), released in 2022, is referenced and reused in many downstream datasets.
