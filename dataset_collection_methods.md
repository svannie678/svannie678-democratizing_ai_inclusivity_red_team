---
layout: default
title: Dataset Collection Methods
---
## Primary Data Sources
To construct a comprehensive dataset, I utilized four primary data sources:
- Existing Knowledge of Red-Teaming Efforts and Major Frontier Organizations.
  
- [SafetyPrompts.com](https://safetyprompts.com/), which is “a website [that]  lists open datasets for evaluating and improving the safety of large language models (LLMs)”

- [Redteaming Resistance Benchmark](https://huggingface.co/spaces/HaizeLabs/red-teaming-resistance-benchmark) from Haize Labs.

- A comprehensive search for "red-team" within Hugging Face Datasets.

## Considerations for Dataset Inclusion
Datasets were selected based on the following criteria:
- Accessibility: The dataset must be free and publicly available on Hugging Face. Future versions may expand to include datasets hosted on GitHub.
  
- Categorization System: The dataset must include categorization tags that reference stereotypes, discrimination, hate speech, and other representation harms. Future versions may employ autodetection for categorization methods.
  
- Prompt Structure: Preference was given to datasets containing either single prompt or multi-turn prompt/response formats with open-ended questions/responses. This excludes multiple choice, and other formats. Notable bias datasets like [BBQ](https://arxiv.org/abs/2110.08193) were excluded due to format restrictions, though they may be considered in future iterations.

- Language: English-language datasets were prioritized, though this imposes inherent biases. Future versions may expand to include other languages.
  
## Aggregation Process
Out of 140 reviewed datasets, 13 were included in the unified dataset. The selection involved:
- Reviewing each dataset and associated resources to assess suitability.
- Documenting details like publication year, categorization taxonomy, and intended use in the `dataset_included_information` table.
- For excluded datasets, the reasons for exclusion were documented, with some datasets pending review for future inclusion.




