import streamlit as st
from groq import Groq

# Fix indentation
ai_model = Groq(api_key=st.secrets["groq_api"])

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
   
    {"role": "assistant", "content": "Walaikum Salam, How are you"}
    ]
    return messages

def get_chatgpt_response(messages):
    response = ai_model.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = get_initial_message()

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ✅ Chat input (fixed at bottom)
prompt = st.chat_input("How may I help you?")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Update messages
    st.session_state.messages = update_chat(st.session_state.messages, "user", prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Generating..."):
            response = get_chatgpt_response(st.session_state.messages)
            st.write(response)

    # Save response
    st.session_state.messages = update_chat(st.session_state.messages, "assistant", response)