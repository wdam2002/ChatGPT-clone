import streamlit as st
from openai import OpenAI

# App title
st.title("ChatGPT clone")

# Set client OpenAI API key
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

# Initialize default session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input for the chat
if prompt := st.chat_input("Message OpenAI chatbot..."):
    # Add user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve assistant's response from OpenAI's chat API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True,
        ):
            # Update the assistant's response dynamically as it comes in
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        # Display the final assistant's response
        message_placeholder.markdown(full_response)

    # Add assistant's response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
