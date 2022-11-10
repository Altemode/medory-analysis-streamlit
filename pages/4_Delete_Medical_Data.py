import pandas as pd 
import streamlit as st
from supabase import create_client, Client
from streamlit_option_menu import option_menu
import numpy as np
import random
from random import randrange
from datetime import timedelta
from datetime import datetime


st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Still Loading..")