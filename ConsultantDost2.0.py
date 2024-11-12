import streamlit as st
import os
from langchain_groq import ChatGroq
groq_api_key=os.environ.get("GROQ_API_KEY")
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.chat_history import(
       BaseChatMessageHistory,
       InMemoryChatMessageHistory
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from layout import footer

st.set_page_config( #first called
    page_title="Consultant Dost",
    page_icon="https://cdn-icons-png.flaticon.com/128/1189/1189175.png", #deleted markdown syntax
)
st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
            font-family: 'Arial', sans-serif;
        }
        header {
            background-color: #005B96;
            color: #FFFFFF;
            padding: 20px;
            text-align: center;
            font-weight: bold;
        }
        footer {
            background-color: #F2F2F2;
            color: #000000;
            text-align: center;
            padding: 20px;
        }
        a {
            color: #005B96;
            text-decoration: none;
        }
        a:hover {
            color: #003F6B;
        }
        .stButton>button {
            background-color: #005B96;
            color: #FFFFFF;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #003F6B;
        }
        .button-secondary {
            background-color: #F2F2F2;
            color: #000000;
            padding: 10px 20px;
            border: 1px solid #005B96;
            font-weight: bold;
            cursor: pointer;
        }
        .button-secondary:hover {
            background-color: #E0E0E0;
        }
        .card {
            background-color: #FFFFFF;
            border: 1px solid #005B96;
            padding: 20px;
            margin: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

def display_chathistory(session_id):
    if session_id in st.session_state:
        imcmh=st.session_state[session_id]
        msgs=imcmh.messages
        n=1
        for msg in msgs:
            if n%2!=0 and n!=1:
                user_msg=st.chat_message("user")
                user_msg.write(msg.content)
            elif n%2==0 and n!=2:
                ai_msg=st.chat_message("assistant")
                ai_msg.write(msg.content)
            n=n+1
def process_conv(user_query,model_name,temp,session_id):
    llm = ChatGroq(
           model=model_name,
           temperature=temp,
    )
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in st.session_state:
               st.session_state[session_id]=InMemoryChatMessageHistory()
        return st.session_state[session_id]

    with_message_history = RunnableWithMessageHistory(llm,get_session_history)
    config = {"configurable":{"session_id":session_id}}
    if session_id not in st.session_state:
        frmttd_query=st.session_state["instruction"]
        response = with_message_history.invoke(
          [HumanMessage(content=frmttd_query),],
          config=config
        )
    else:
        response = with_message_history.invoke(
            [HumanMessage(content=user_query),],
            config=config
            )
    # st.write(st.session_state)
    return response.content
with st.sidebar:
        st.title("Settings")
        api_key = st.text_input("Enter Your API Token here")
        model = st.selectbox("Select model", ("llama-3.1-70b-versatile","llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it", "llama-3.2-11b-text-preview"))
        temp = st.slider("Temperature",0.0,1.0,0.0)
st.title("Consultant Dost")
st.write("""
###### Meet Your Friend Who Can Help You In Your Consultancy Career.
""")
# name = st.text_input("Enter Your Name Here(Optional)")
st.write(f"""## ![alt-text](https://cdn-icons-png.flaticon.com/128/1189/1189175.png) Welcome:smiley:""")
st.write("""### How can I help you today?""")
st.write("""###### *Navigate to the left sidebar for more settings and info* """)

agent_name="Consultant Dost"
other_qualities = "Your journey to this esteemed position has been shaped by a unique set of qualities and experiences. You possess visionary thinking, allowing you to anticipate market trends and steer your organization towards innovative solutions and long-term growth. Your resilience helps you navigate challenges effectively, embracing setbacks as learning opportunities. Strong communication skills foster an environment of open idea-sharing, enhancing collaboration and team cohesion. Your emotional intelligence enables you to build strong relationships, connect with diverse teams, and motivate individuals, leading to a high-performing culture. You excel in strategic decision-making, making informed choices based on data analysis and market research, ensuring your company stays ahead of the competition. Your adaptability allows you to quickly embrace new technologies and changing circumstances, maintaining the MNC's relevance in a fast-paced global market. Committed to diversity and inclusion, you advocate for diverse hiring practices and inclusion initiatives, fostering a culture where every voice is heard and valued. Your dedication to continuous learning inspires your team to pursue their own development, creating a culture of excellence. With a global perspective gained from working in various countries, you lead diverse teams and navigate international markets successfully. Prioritizing ethical leadership, you establish trust with stakeholders and cultivate a corporate culture that values integrity and transparency. These qualities, combined with your passion for driving success and making a positive impact, have led you to this pivotal leadership role in a top-performing MNC.You are simple, don't brag about yourself"
prompt=f"Imagine you are a 54 yoe who leads a top performing MNC. \
                                    You have gone through all the level like associate analyst, analyst, consultant, manager, \
                                        senior manager etc., You are a very helpful, empathetic mentor who guides and loves to help \
                                        everyone in this consulatncy career. You explain, mentor and guide effectively with \
                                        high efficiency, skilled at everything that MNCs need including excellent character & positivity. feel free to use your name that is {agent_name}\
                                    to make reponse personal to enhance interaction + {other_qualities}. Maintain neat, clear and precise formatting of text"
if "instruction" not in st.session_state:
    st.session_state["instruction"]=f"""
                                Prompt: {prompt}\n
                                """

session_id="chat_history"
if session_id in st.session_state:
    display_chathistory(session_id)
else:
    with st.spinner("Initializing Your Dost..."):
        response = process_conv("",model,temp,session_id)
        # st.chat_message("ai").write(response)
user_query = st.chat_input("Type your input to your dost here")
uq=user_query
if user_query:
    st.chat_message("user").write(user_query)
    with st.chat_message("ai"):
         with st.spinner("Thinking..."):
            response = process_conv(uq,model,temp,session_id)
            st.markdown(response)
# footer()
