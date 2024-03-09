import streamlit as st
import requests
import json
import ast
import base64
from PIL import Image
import io
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.mention import mention
# huggingface-cli download stabilityai/stable-diffusion-xl-base-1.0 --include "*.safetensors" --local-dir "C:/Edrive/Custom_SD/"
#cache_dir
## C:\Users\avish\.cache\huggingface\hub\models--stabilityai--stable-diffusion-xl-base-1.0\snapshots\462165984030d82259a11f4367a4eed129e94a7b

#https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline
# https://huggingface.co/docs/diffusers/v0.19.3/api/pipelines/stable_diffusion/stable_diffusion_xl
#https://github.com/ahgsql/StyleSelectorXL/blob/main/sdxl_styles.json
# https://github.com/huggingface/diffusers/issues/3117 ## Seed, callback function
# https://github.com/pcuenca/diffusers-examples/blob/main/notebooks/stable-diffusion-seeds.ipynb Experiments with seed

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
        if x:
            if str(x[0]) == password:
                return True
            return False
        else:
            st.sidebar.error('Register for username and password')
    else:
        st.sidebar.error('Enter both username or password')
        return False

def main():
    st.set_page_config(page_title="SDXL test to image demo",
                       page_icon=":home:")
    st.sidebar.title('Login')
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')
    with st.sidebar:
        mention(label = "Request Access",
            icon = "🔗",
            url="https://forms.gle/gHMJZkiKi4X9bR5KA")
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)

    data = conn.read(spreadsheet=st.secrets.connections.gsheets.spreadsheet, ttl=60, usecols=[0, 1])

    if st.sidebar.button('Login'):
        if authenticate(username, password, data):
            st.sidebar.success('Login successful')
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error('Invalid username or password')

    if st.session_state.get('authenticated'):
        st.title('Demo Application for SDXL beam')
        mention(label="Sample prompts",
            icon="💡",  # Some icons are available... like Streamlit!
            url="https://blog.segmind.com/prompt-guide-for-stable-diffusion-xl-crafting-textual-descriptions-for-image-generation/")
        hostname = st.secrets.server.url
        AUTH_CRED = st.secrets.server.AUTH_CRED

        with st.container():
            prompt = st.text_input("Enter your prompt", value="", max_chars=500)
            

            negative_prompt = st.text_input("Enter your negative prompt", value="", max_chars=500)
    
        with st.sidebar:
            st.sidebar.title("Settings")
            num_inference_steps = st.sidebar.slider(
                    "Inference Steps",
                    min_value=1,  # Minimum value
                    max_value=100,  # Maximum value
                    value=20, # Default value
                    step=1  # Step size
                )
            
            num_images_per_prompt = st.sidebar.slider(
                    "Number of Images per prompt",
                    min_value=1,  # Minimum value
                    max_value=8,  # Maximum value
                    value=2, # Default value
                    step=1  # Step size
                )
            
            guidance_scale = st.sidebar.slider(
                    "Guidance scale",
                    min_value=1.0,  # Minimum value
                    max_value=13.0,  # Maximum value
                    value=7.0, # Default value
                    step=0.1  # Step size
                )
            
            # enable_refiner = st.checkbox("Enable Refiner")
            enable_manual_seed = st.checkbox("Enable Manual Seed")

            if enable_manual_seed:
                seed_input = st.text_input("Manual seed number")
            else:
                seed_input = 0

        process_button = st.button("Process", type="primary")

        if process_button:
            with st.spinner('Processing Request (takes about 30 secs)...'):
                payload = {"prompt":prompt,
                "negative_prompt":None,
                "num_inference_steps":num_inference_steps,
                "guidance_scale":guidance_scale,
                "num_images_per_prompt":num_images_per_prompt,
                "seed_input":seed_input}
                headers["Authorization"] += AUTH_CRED
                response = requests.request("POST", hostname, 
                                    headers=headers,
                                    data=json.dumps(payload)
                                    )
            # print(response)
            if response.ok:
                dict_str = response.content.decode('utf-8')
                json_data = ast.literal_eval(dict_str)
                st.write("Positive prompt :" + prompt)
                st.write("Negative prompt :" + negative_prompt)
                for i in range(payload["num_images_per_prompt"]):
                    decoded_bytes = base64.b64decode(json_data["b64_image_"+str(i)])
                    image = Image.open(io.BytesIO(decoded_bytes))
                    st.image(image, caption="Image "+str(i))
            else:
                st.write(response)

if __name__ == '__main__':
    main()
