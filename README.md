# LLM Project - US Stocks Questions Answering Bot
**The bot helps users to quickly find insights from the [Financial Q&A - 10k](https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k?resource=download) dataset by utilizing Large Language Model(LLM).**

**Step:**
1. Enter your question
2. Choose the ticker (US stocks only)
3. Click Ask

![ScreenRecording](https://hackmd.io/_uploads/Sk--MUy50.gif)



## Introduction
This project is for me to practice how to use **Generative AI** in the questions answering senario.
**The project design**
* Use [Financial Q&A - 10k](https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k?resource=download) from Kaggle as the knowledge base. 
The dataset contains 10,000 question-answer pairs derived from company financial reports.
* Create a **RAG(Retrieval augmented generation)** system for answering questions about those financial data.

## Methodology
![LLM - Methodology - crop](https://hackmd.io/_uploads/SkaPAwkqR.jpg)

## Built With
* **Elasticsearch** - to search related data from the knowledge base
* **Kibana** - index management
* **Open AI API** - use **gpt-4o** model to find the best answer based on the search result from Elasticsearch.
* **Streamlit** - web app library
* **Docker** - containerize all services
* **Language** - Python

## Getting Started

### Prerequisites
* [Install Docker Compose](https://docs.docker.com/compose/install/)
* [OPEN AI API Account](https://openai.com/index/openai-api/)
You may need to register an Open AI account and buy credits to use the API because it is not free. I spent usd 5 which is the minimum amount.

### Installation

1. Get an API Key from [Open AI API](https://openai.com/index/openai-api/)
2. Clone the repo
   ```sh
   git clone https://github.com/Sean-Liu-GitHub/LLM_us_stock_questions_answering.git
   ```
3. Create a "secrets.toml" file in "streamlit/.streamlit" in the cloned project folder
4. In the "secrets.toml" file, assign your api key to OPENAI_API_KEY secret. This is for streamlit app to connect Open AI API.
    ```
    # streamlit/.streamlit/secrets.toml
    OPENAI_API_KEY=your_api_key
    ```
4. Run docker compose
It will take some time to start the app in the first time because it needs to set up the documents in Elasticsearch.
   ```
   docker compose up --build
   ```

## Roadmap

- [x] Set up elasticsearch and index
- [x] Created a RAG
- [ ] Keep elasticsearch updated with new Q&A data.



<!-- CONTACT -->
## Contact

Sean Liu - [LinkedIn](https://www.linkedin.com/in/sean-liu-65bbb8b2/) - sean.liu.job@gmail.com

Project Link: [https://github.com/Sean-Liu-GitHub/LLM_us_stock_questions_answering](https://github.com/Sean-Liu-GitHub/LLM_us_stock_questions_answering)

## Reference
* [DataTalks Club](https://datatalks.club/) - [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
