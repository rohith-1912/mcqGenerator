import os
import json
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda

#Load environment varibles from thr .env file
load_dotenv()

#Access the environment variables
key = os.getenv("OPENAI_API_KEY")

# A higher temperature value increases a creative model's output, while a lower one makes it more deterministic
llm = ChatOpenAI(openai_api_key = key, model = "gpt-4o-mini", temperature = 0.7)

Template = """ 
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
    template= Template
)

quiz_chain = {
    "quiz": quiz_generation_prompt | llm
} # New way of access the chain and with the output_key as "quiz"

Template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=['subject', 'quiz'],
    template= Template2
)

review_chain = {
    "review" :quiz_evaluation_prompt | llm
}

def run_quiz_and_review(inputs):
    # 1) generate quiz (correct way)
    quiz_msg = quiz_chain["quiz"].invoke(inputs)
    quiz_text = getattr(quiz_msg, "content", quiz_msg)

    # 2) review quiz (send clean string, not AIMessage)
    review_msg = review_chain["review"].invoke({
        "subject": inputs["subject"],
        "quiz": quiz_text
    })
    review_text = getattr(review_msg, "content", review_msg)

    # 3) return ONLY clean strings, not AIMessage objects
    return {
        "quiz": quiz_text,
        "review": review_text
    }

generate_evaluate_chain = RunnableLambda(run_quiz_and_review)