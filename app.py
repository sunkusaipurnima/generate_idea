import json
import os
import textwrap
from dotenv import load_dotenv
import streamlit as st
import cohere

load_dotenv()
#setup the cohere client
api_key=st.secrets.get("COHERE_API_KEY", os.getenv("COHERE_API_KEY"))
co=cohere.ClientV2(api_key)

def generate_idea(industry, temperature):
    prompt=f"""
    Generate a startup idea given the industry.Return the startup idea and without any additional commentry.

    Industry:Workplace
    Startup Idea: A platform that generates slide deck content automatically based on given outline.RecursionError

    Industry: HomeDecor
    Startup Idea: An app that calculates the best position for your indoor plants for your apartment based on sunlight.RecursionError

    Industry:Healthcare
    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting for whole week.RecursionError

    Industry:Education
    Startup Idea: An online primary school that allows students to mix and match their own curriculum based on their interests and goals.

    Industry: {industry}
    Startup Idea:"""

    # call the cohere chat

    response = co.chat(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model='command-a-03-2025',
        temperature=temperature,
    )
    return response.message.content[0].text

def generate_name(idea,temperature):
    prompt=f"""
    Generate a startup name given startup idea. Return the startup name and without any additional commentry.

    startup idea: A platform that generates slide deck content automatically based on given outline.
    startup name: Deckerize

    startup idea: An app that calculates the best position for your indoor plants for your apartment based on sunlight.
    startup name: Planteasy

    startup idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting for whole week.
    startup name: Hearspan

    startup idea: An online primary school that allows students to mix and match their own curriculum based on their interests and goals.
    startup name: Prime Age

    startup idea: {idea}
    startup name:"""

    # call the cohere chat
    response = co.chat(
        messages=[
            {"role":"user","content":prompt}
        ],
        model='command-a-03-2025',
        temperature=temperature,
    )

    return response.message.content[0].text

# Frontend code

st.title("🚀 Startup Idea Generator")

form=st.form(key='user_settings')

with form:
    st.write('Enter an industry name Example: Healthcare, Education, Finance')

    industry_input=st.text_input('Industry',key='industry_input')

    #Create a two column view
    col1,col2=st.columns(2)

    with col1:
        num_input=st.slider(
            "Number of ideas",
            value=3,
            min_value=1,
            max_value=10,
            key='num_input',
            help='Choose to generate 1 to 10 ideas'
        )
    with col2:
        #User Input: the temperature values representing level of creativity
        creativity_input=st.slider(
            "Creativity",
            value=0.5,
            min_value=0.0,
            max_value=1.0,
            key='creativity_input',
            help='Lower values generate more "predictable" output, while higher values generate more "creative" output.'
        )    

    #Submit button to start generating ideas
    generate_button=form.form_submit_button('Generate Idea') 

    if generate_button:
        if industry_input=='':
            st.error('Industry input cannot be empty.')
        else:
            my_bar=st.progress(0.05)
            st.subheader("Startup Ideas")

            for i in range(num_input):
                st.markdown("---")
                startup_idea=generate_idea(industry_input,creativity_input ) 
                startup_name=generate_name(startup_idea,creativity_input)
                st.markdown('###'+startup_name)
                st.write(textwrap.fill(startup_idea, width=80)) 
                my_bar.progress((i+1)/num_input)

