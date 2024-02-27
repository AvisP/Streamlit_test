import os
import streamlit as st
from llama_index.core import Settings, VectorStoreIndex, StorageContext
import torch

st.write(torch.__version__)
st.write("App Deployment successful")
