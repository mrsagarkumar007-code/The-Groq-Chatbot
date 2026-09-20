import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write("A fully integrated, memory-enabled AI assistant.")

# The Sidebar (API Key Security)
with st.sidebar:
    st.header("⚙️ Configuration")

    user_api_key = st.text_input(
        'Enter the Groq API Key:',
        type='password'
    )

    st.info('Your key is required to wake up the AI Brain')

    # ----- Persona -----
    persona = st.text_area(
        "System Prompt:",
        value="You are a helpful assistant."
    )

    # ----- Reset Chat -----
    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()


# ------ 2. The Memory Vault -------
if 'messages' not in st.session_state:
    st.session_state.messages = []


# ----- 3. Display History ---------
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])


# 4. Chat Input and Logic
if user_query := st.chat_input('Say something to the AI...'):

    if not user_api_key:
        st.error('Please enter your api key in the sidebar first!')

    else:

        # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Store the user message in the vault
        st.session_state.messages.append({
            'role': 'user',
            'content': user_query
        })


        # Initialise the Brain
        llm = ChatGroq(
            model='openai/gpt-oss-20b',
            temperature=0.7,
            api_key=user_api_key
        )


        # ----- Add Persona Before LLM Call -----
        messages_for_llm = [
            {
                'role': 'system',
                'content': persona
            }
        ] + st.session_state.messages


        with st.spinner('AI is thinking....'):

            response = llm.invoke(messages_for_llm)

            bot_answer = response.content


        # Store AI response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': bot_answer
        })


        # Display AI response
        with st.chat_message('assistant'):
            st.markdown(bot_answer)
