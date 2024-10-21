import streamlit as st
import time
#import vertexai  
from vertexai.generative_models import GenerativeModel


#vertexai.init(project="mokshagenai", location="us-central1")

model = GenerativeModel("gemini-1.5")


llm_models = [
    "GPT-3",
    "Bard",
    "LLaMA",
    "gemini-1.5",
]

# Simulated function to load a model
@st.cache_resource
def load_model(model_name):
    time.sleep(2)  # Simulate model loading time
    if model_name == "gemini-1.5":
        return GenerativeModel("gemini-1.5-flash-001")
    else:
        return f"{model_name} loaded!"

# Create a selectbox for selecting a model
selected_model = st.sidebar.selectbox(
    'Which LLM model would you like to use?',
    options=[None] + llm_models, 
    format_func=lambda x: x if x is not None else 'Select a model'
)

model = load_model(selected_model)

# Create a text input box
user_input = st.text_input("Enter your text:")

# Display the selected model
st.write('You selected:', selected_model)

if st.button("Get Response"):
    if selected_model == "gemini-1.5" and isinstance(model, GenerativeModel):
        response = model.generate_content(user_input)
        st.write("Response from the model:")
        st.write(response.text)
