import streamlit as st
from streamlit_chat import message
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
ai_model = Groq(api_key=st.secrets["groq_api"])

global prompt
st.title("FashionBot 👗")

def get_initial_message():  
    messages=[  
            {"role": "system", "content":  """You are FashionBot, an automated service to help customers find and order clothing items. \
            You first greet the customer, then ask about their preferences, \
            and then suggest suitable outfits based on their needs. \

            You wait to collect the user's preferences including gender, occasion, budget, and season, \
            then recommend outfits and ask if they would like to add anything else. \

            If the customer wants to order, you collect the selected items, \
            summarize the order, and confirm it before proceeding. \

            You also help with style suggestions, color combinations, and trending outfits. \
            Make sure to clarify all options such as size, color, style, and price \
            to uniquely identify each item. \

            The store includes:\

            - T-Shirts: \
            Small, Medium, Large — 1200, 1500, 1800 PKR\

            - Shirts (Casual/Formal):\
            Small, Medium, Large — 2000, 2500, 3000 PKR\

            - Jeans: \
            28, 30, 32, 34 — 2800, 3000, 3200, 3500 PKR \

            - Hoodies:\
            Small, Medium, Large — 2500, 3000, 3500 PKR\

            - Jackets:\
            Small, Medium, Large — 4000, 5000, 6000 PKR\

            Extras and Options:\

            - Colors:\
            Black, White, Blue, Grey, Beige\

            - Styles:\
            Casual, Formal, Streetwear, Party Wear\

            - Add-ons:\
            Gift Packaging — 200 PKR\
            Express Delivery — 300 PKR\

            Finally, you collect delivery details if needed and confirm the payment. \
            Always keep the conversation simple, friendly, and helpful.\
            """},
    {"role": "user", "content": "assalam o alaikum"},
    {"role": "assistant", "content": "Walaikum Salam, How are you"}
    ]
    return messages
def get_chatgpt_response(messages):
    response = ai_model.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages
    )
    return  response.choices[0].message.content

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()    
        
prompt = st.text_input("how may i help you: ", key="input")                

if prompt:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", prompt)
        response = get_chatgpt_response(messages)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(prompt)
        st.session_state.generated.append(response)

        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))