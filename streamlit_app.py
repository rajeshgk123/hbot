import streamlit as st
import openai

# Initialize OpenAI with your secret API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("🩺 Health Symptom Checker")

# Initialize chat history with a health-focused system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and qualified medical assistant. "
                "You should only answer questions related to health, physical and mental wellness, symptoms, treatment options, and medicines. "
                "You are not allowed to answer any questions unrelated to health or medicine. "
                "If the user asks about any other topic (like history, technology, sports, etc.), politely say: "
                "'I'm here to help with health and medicine only. Could you please ask something in that area?'"
            )
        }
    ]

# Display all previous messages
for msg in st.session_state.messages[1:]:  # Skip system prompt in UI
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Describe your symptoms...")

# Function to get AI response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Process user input
if user_input:
    # Add user's message to history and show
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response = get_response(st.session_state.messages)
    
    # Add assistant response to history and show
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Optional: Add footer disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This chatbot does not provide medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare provider for medical concerns.",
    unsafe_allow_html=True
)
