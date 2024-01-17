# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
import streamlit as st
import openai

# Set up Streamlit sidebar with app title and API key input
with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')

    # Check if API key is already provided in Streamlit secrets
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        # If API key is not provided, prompt user to enter it
        openai.api_key = st.text_input(
            'Enter your OpenAI API key:', type='password')

        # Validate the format of the entered API key
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter a valid API key!', icon='⚠️')
        else:
            # If valid API key, indicate success and prompt for chat message
            st.success('Proceed to entering your prompt message!', icon='👉')

# Initialize default session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages history
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
        for response in openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            # Update the assistant's response dynamically as it comes in
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        # Display the final assistant's response
        message_placeholder.markdown(full_response)

    # Add assistant's response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
