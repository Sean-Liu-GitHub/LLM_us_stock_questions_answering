import streamlit as st
from elasticsearch import Elasticsearch
from openai import OpenAI
import json

def create_index(es_client, index_name, index_settings, doc_file):
    # create index
    es_client.indices.create(index=index_name, body=index_settings)
    
    # create document from json
    with open(doc_file, 'rt') as f_in:
        docs_raw = json.load(f_in)

    documents = []

    for ticker_dict in docs_raw:
        for doc in ticker_dict['documents']:
            doc['ticker'] = ticker_dict['ticker']
            documents.append(doc)
    
    # apply document
    for doc in documents:
        es_client.index(index=index_name, document=doc)

def elastic_search(es_client, index_name, query, ticker):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "ticker": ticker
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs

def build_prompt(query, search_results):
    prompt_template = """
You're a investment advicer. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(es_client, index_name, query, ticker):
    search_results = elastic_search(es_client, index_name, query, ticker)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer

def main(): 
    # Connect to Elasticsearch
    es_client = Elasticsearch(['http://elasticsearch:9200'])
    index_name = "us-stock-q&a"

    # Set up index if it doesn't exist
    if es_client.indices.exists(index=index_name):
        print("Index exists.")
    else:
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "section": {"type": "text"},
                    "question": {"type": "text"},
                    "ticker": {"type": "keyword"} 
                }
            }
        }
        doc_file = 'documents.json'
        create_index(es_client, index_name, index_settings, doc_file)

    # Test connection
    if es_client.ping():
        print("Elasticsearch connected.")
    else:
        st.error('Could not connect to Elasticsearch.')

    # Streamlit application layout
    st.title("US Stock Questions Answering")

    # Input box
    user_input_question = st.text_input("Enter your question:")
    user_input_ticker = st.text_input("Enter related ticker:")

    # Function that handles the button click
    def on_click():
        with st.spinner("Processing..."):
            output = rag(es_client, index_name, user_input_question, user_input_ticker)
            st.success("Done!")
            st.write(output)

    # Ask button
    if st.button("Ask"):
        on_click()

if __name__ == "__main__":
    main()