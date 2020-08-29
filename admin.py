import streamlit as st
import pandas as pd
import os

st.title("Skillshop chatbot Admin")

choices = ['View Dataset','Add Queries','Add Bot Responses']
tags = ['timing','menu','offers','delivery','address','combo']

# files that are going to store the data
Q_DATASET = 'query_dataset.csv'
R_DATASET = 'bot_response_dataset.csv'

qdf = None
rdf = None

if os.path.exists(Q_DATASET):
    qdf = pd.read_csv(Q_DATASET)

if os.path.exists(R_DATASET):
    rdf = pd.read_csv(R_DATASET)
    


userchoice = st.sidebar.selectbox("menu",choices)

if userchoice == choices[0] :
    st.header("Select a dataset")
    # code section for displaying data
    if isinstance(qdf, pd.DataFrame):
        if st.sidebar.checkbox('view query dataset'):
            st.table(qdf)
    if isinstance(rdf, pd.DataFrame):
        if st.sidebar.checkbox('view response dataset'):
            st.table(rdf)
    
elif userchoice == choices[1]:
    st.header("Add new customer queries")
    # code section for adding queries
    dataset = []
    question = st.text_input("A customer query")
    tag = st.selectbox('select a tag',tags)
    clicked =  st.button("save this")
    if clicked and question:
        data = {'query':question,'tag':tag}
        dataset.append(data)
        tempdf = pd.DataFrame(dataset)
        
        if isinstance(qdf, pd.DataFrame):
            # save to existing file
            qdf = qdf.append(tempdf)
            qdf.to_csv(Q_DATASET,index=False)
            st.success("query saved successfully")
            st.table(qdf) # remove this
        else:
            # only runs for the very first time 
            tempdf.to_csv(Q_DATASET, index=False)
            st.success("query saved successfully")
        
else: 
    st.header("Add new bot responses")
    # code section for adding responses
    dataset = []
    tag = st.selectbox('select a tag',tags)
    reply = st.text_input("what would the bot reply")
    clicked =  st.button("save response")
    if clicked and reply:
        data = {'response':reply,'tag':tag}
        dataset.append(data)
        tempdf = pd.DataFrame(dataset)
        
        if isinstance(rdf, pd.DataFrame):
            # save to existing file
            rdf = rdf.append(tempdf)
            rdf.to_csv(R_DATASET,index=False)
            st.success("response saved successfully")
            st.table(rdf) # remove this
        else:
            # only runs for the very first time 
            tempdf.to_csv(R_DATASET, index=False)
            st.success("response saved successfully")
