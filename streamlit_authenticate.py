import streamlit as st
import configparser
import requests
import json
import ast
import configparser
from streamlit_gsheets import GSheetsConnection

payload = {"text":" "}
headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic ",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

def authenticate(username, password, data):
    if username and password:
        x = data[data.username==username]["password"].values
        if str(x[0]) == password:
            return True
        return False
    else:
        st.sidebar.error('Enter both username or password')
        return False

def main():
    st.sidebar.title('Login')
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')

    conn = st.experimental_connection("gsheets", type=GSheetsConnection)

    data = conn.read(spreadsheet=st.secrets.connections.gsheets.spreadsheet, ttl=60, usecols=[0, 1])

    # st.write(st.secrets["Users"]["AVISHEK"])
    # st.write(st.secrets["Users"]["user2"])

    if st.sidebar.button('Login'):
        # config = read_config(config_filename)
        if authenticate(username, password, data):
            st.sidebar.success('Login successful')
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error('Invalid username or password')

    if st.session_state.get('authenticated'):
        st.title('Demo Application for beam.cloud')

        hostname = st.secrets.server.url
        AUTH_CRED = st.secrets.server.AUTH_CRED
        
        senti_text = st.text_input('Enter Text')
        send_bt = st.button("Send", type="primary")

        if send_bt:
            if senti_text:
                payload = {"text": senti_text}
                headers["Authorization"] += AUTH_CRED
                print(senti_text)
                with st.spinner("Processing sentiment for query :" ):
                    response = requests.request("POST", hostname, 
                            headers=headers,
                            data=json.dumps(payload)
                            )
                
                if response.ok:
                    st.write(ast.literal_eval(response.content.decode("utf-8"))['prediction'])
                else:
                    st.write("API request failed :", response)

            else:
                st.error("No input text entered", icon="🚨")

if __name__ == '__main__':
    main()
