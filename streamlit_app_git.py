import streamlit as st
import requests
import json
import ast

# url = "https://986ry.apps.beam.cloud"
# payload = {"text":"I don't like it!"}
# AUTH_CRED =
# headers = {
#   "Accept": "*/*",
#   "Accept-Encoding": "gzip, deflate",
#   "Authorization": "Basic " + AUTH_CRED,
#   "Connection": "keep-alive",
#   "Content-Type": "application/json"
# }

# response = requests.request("POST", url, 
#   headers=headers,
#   data=json.dumps(payload)
# )

# print(ast.literal_eval(response.content.decode("utf-8"))['prediction'])

payload = {"text":"I don't like it!"}
headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic ",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

st.title("Demo Application for beam.cloud")

with st.sidebar:
    auth_cred= st.text_input('Enter authorization text', 
                            value=None,
                            key="Auth text",
                            type="password",
                            help="Get key from deployed app in beam.cloud, Call API button, authorization")
    
    url_text = st.text_input('Enter url text', 
                            value=None,
                            key="URL text",
                            help="Get url from deployed app in beam.cloud, beside Overview")

senti_text = st.text_input('Enter text for sentiment analysis', 
                     value=None,
                     key="Input String")
send_bt = st.button("Send", type="primary")

if send_bt:

    if url_text is None:
        st.error("No url for beam entered", icon="🚨")
        
    if auth_cred is None:
        st.error("No authorization credential entered", icon="🚨")

    if senti_text:

        payload = {"text": senti_text}
        headers["Authorization"] += auth_cred
        response = requests.request("POST", url_text, 
                    headers=headers,
                    data=json.dumps(payload)
                    )
        st.write("Processing sentiment for query :", senti_text)
        if response.ok:
            st.write(ast.literal_eval(response.content.decode("utf-8"))['prediction'])
        else:
            st.write("API request failed :", response)

    else:
        st.error("No input text entered", icon="🚨")