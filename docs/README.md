# Amazon US Customer Reviews Topic Modeling

## Overview
This project aims to analyze Amazon US customer reviews to discover prevalent topics using Natural Language Processing (NLP) techniques, specifically Latent Dirichlet Allocation (LDA). The findings will help inform product adjustments and marketing strategies based on customer feedback.

## Table of Contents
- [Introduction](##introduction)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Results](#results)
- [Conclusions](#conclusions)
- [How to Run the Code](#how-to-run-the-code)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Introduction
This project utilizes the Amazon US Customer Reviews Dataset to perform topic modeling, aiming to uncover common themes in customer feedback. The analysis employs LDA for topic extraction and visualization techniques like word clouds and bar charts to represent the results.

## Data Sources
The dataset is obtained from [Kaggle](https://www.kaggle.com/) and contains US customer reviews for Amazon products.

## Methodology
1. **Data Preprocessing:** Clean the dataset by removing irrelevant data and ensuring consistency in textual data.
2. **Topic Modeling:** Apply LDA to extract common topics from the reviews.
3. **Visualization:** Use word clouds and bar charts to represent the most common topics and their frequency.
4. **Reporting:** Outline the methods used, topics discovered, and their influence on product adjustments or marketing strategies.
5. **Presentation:** Create a presentation explaining the findings and recommending actions based on prevalent topics in customer feedback.

## Results
The results section will contain visual representations of the discovered topics and their frequencies, along with an analysis of these findings.

## Conclusions
Based on the prevalent topics discovered from the customer reviews, we provide actionable insights and recommendations for product improvements and marketing strategies.

## How to Run the Code
1. Clone the repository.
2. Install the required dependencies.
3. Run the `select_file()` function to load and process the dataset.
4. View the generated visualizations and analyze the extracted topics.

## Installation
1. Clone this repository:
    ```bash
    https://github.com/collinsmayweather/capstone-project.git
    cd amazon-reviews-topic-modeling
    ```
2. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the script:
    ```bash
    python topic_modeling.py
    ```
2. Select the dataset file when prompted.
3. The script will preprocess the data, perform topic modeling, and display visualizations of the discovered topics.

## Contributing
We welcome contributions to this project. Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors
- Scolastica Nzyoki
- Mercy Njambi
- Brenda Murage
- Purity Njau
- Collins Too

## Acknowledgments
We thank Kaggle for providing the dataset and the open-source community for the tools and libraries used in this project.
