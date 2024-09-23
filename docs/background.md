---
layout: base
title: Background
nav-include: true
nav-order: 1
---

## What is an LLM?
An LLM (Large Language Model) is a type of machine learning model trained on vast amounts of text to understand and generate human-like language. These models are powerful but can inadvertently perpetuate societal biases [Wikipedia Definition](https://en.wikipedia.org/wiki/Large_language_model).

## Why Red-Team LLM's?
Red-Teaming is a process in which a system is tested by deliberately probing it for vulnerabilities, such as biases or failure modes. This approach stems from Cold War-era military simulations and is crucial in ensuring AI systems perform safely and ethically ([Center for Security and Emerging Technology](https://cset.georgetown.edu/article/what-does-ai-red-teaming-actually-mean/)).

Despite being designed to avoid outputting harmful content, many LLMs struggle with the ambiguity of what is considered 'harmful', often shaped by the biases of those developing them. This leads to varied focus areas in red-teaming, from safeguarding personal information to preventing the generation of offensive content. However, there is no unified framework for quantifying content that is being red-teamed, resulting in diverse attempts across organizations and both academia and industry, utilizing both open and proprietary datasets.

## Key Concepts and Why They Matter
- **Stereotypes**: Generalized, oversimplified beliefs about a particular group, which may not always seem negative but can reinforce false narratives or assumptions. Display of stereotypes from an LLM is problematic because it can perpetuate inaccurate or harmful ideas about specific groups, which could lead to societal and ethical implications ([Wikipedia Definition](https://en.wikipedia.org/wiki/Stereotype),[Weidinger et al., 2021](https://arxiv.org/pdf/2112.04359)).
  - *Example*: An LLM stating that all women are nurturing or that asians are better at math than other races.
  
- **Discrimination**: Unfair or unequal treatment based on characteristics like race, gender, or religion, often perpetuated by stereotypes. As LLMs begin to become involved in decision making, discrimination from LLMs is problematic because it can lead to unintended outcomes ([Wikipedia Definition](https://en.wikipedia.org/wiki/Discrimination),[Weidinger et al., 2021](https://arxiv.org/pdf/2112.04359)).
  - *Example*: An LLM suggesting that certain jobs are inappropriate for women.
  
- **Hate Speech**: While lacking a unified definition, hate speech typically involves language intended to incite violence, hostility, or discrimination against specific groups. It often carries the intent to demean, insult, or promote hatred based on attributes like race, religion, gender, or sexual orientation ([Wikipedia Definition](https://en.wikipedia.org/wiki/Hate_speech),[Weidinger et al., 2021](https://arxiv.org/pdf/2112.04359)).
  - *Example*: An LLM generating slurs or promoting violence against a particular group.
  
- **Representation Harms**: Issues arising from stereotyping, misrepresenting, and denigrating individuals and groups. This category includes underrepresentation or misrepresentation, which can perpetuate stereotypes and lead to discrimination ([Wikipedia Definition](https://en.wikipedia.org/wiki/Representational_harm),[Weidinger et al., 2021](https://arxiv.org/pdf/2112.04359)) .
  - *Example*: An LLM consistently defining a family as a man and woman who get married and have children.

### Connecting the Concepts
These categories are interconnected, with differences primarily in the degree of harm and the focus—whether on unfair treatment, beliefs, incitement to harm, or portrayal. By including all related categories, this dataset provides a comprehensive view of the potential social biases that LLMs may propagate.
