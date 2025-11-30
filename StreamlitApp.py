import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file
with open(r'D:\Projects\mcqGenerator\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#Craeting an title for the app
st.title("MCQs creator Application With Langchain")

#Create a form using st.form
with st.form("user_inputs"):
    #File Uplaod
    uploded_file = st.file_uploader("Upload a PDF or txt file")

    #Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz tone
    # Quiz tone (dropdown instead of free text)
    tone = st.selectbox("Complexity level of Questions",["Simple", "Moderate", "Complex", "Advanced"],  # you can add more here
)


    #Add Button
    button = st.form_submit_button("Create MCQs")

    if button and uploded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploded_file)
                #Count tokens and cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain.invoke(
                    {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON),
                     }
                )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    #Extract the quiz from the response
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        df = pd.DataFrame(table_data)
                        df.index = df.index+1
                        st.table(df)
                        #Display the review in a text box as well
                        st.text_area(label = "Review", value=response["review"])
                    else:
                        st.error("Error in table Data")
                else:
                    st.write(response)