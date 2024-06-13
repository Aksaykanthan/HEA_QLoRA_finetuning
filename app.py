import streamlit as st
from streamlit_chat import message


st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Chat Bot</h1>", unsafe_allow_html=True)




if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []




st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("Llama3", "Custom Model"))
counter_placeholder = st.sidebar.empty()
clear_button = st.sidebar.button("Clear Conversation", key="clear")


if model_name == "Llama3":
    model = "Llama3-turbo"
else:
    model = "Custom Model"


if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []

    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")



def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})


    response = "completion.choices[0].message.content"
    st.session_state['messages'].append({"role": "assistant", "content": response})

    

    return response


response_container = st.container()

container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output= generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)



if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
