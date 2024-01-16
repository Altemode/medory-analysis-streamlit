import pandas as pd 
import numpy as np
import streamlit as st
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
import gettext
import functools as ft
import requests

# # # Define the function to consume the weather API
# # def fetch_weather_data():
# #     url = "https://api.weatherapi.com/v1/current.json"
# #     params = {
# #         "key": "1e9bd85382054a8493d123938240301",
# #         "q": "Athens"  # Replace with your preferred city
# #     }
# #     response = requests.get(url, params=params)
# #     data = response.json()
# #     return data
# # location_dict= {}
# # current_dict = {}
# # my_list = []
# # # Define the function to save data to a file
# # def save_to_file(data):
# #     with open("weather_data.txt", "a") as file:
# #         #data
# #         for key, value in data.items():
# #             if key == "location":
# #                 #st.write(value)
# #                 location_dict[key] = value
# #         for key, value in data.items():
# #             if key == "current" and value != "condition":
# #                 #st.write("data[key]",data[key])
# #                 #st.write("value",value)

# #                 current_dict[key] = value
                
# #                 for key, value in data.items():
# #                     st.write(key)
# #                     if key != "condition":
# #                         current_dict[key] = value
# #                 my_list = list(current_dict.values())
# #                 #current_dict
            
# #         df_current = pd.DataFrame(my_list)
# #         #df_current = df_current.T
# #         df_current
# #         # df = pd.DataFrame.from_dict(data, orient='index')
# #         # df
# #         file.write(str(data))
# #         #file.write("\n")

# # st.write("HELLO")
# # data = fetch_weather_data()
# # save_to_file(data)

# # df = pd.read_csv("weather_data.txt")

# from google.cloud import storage
# from google.cloud import bigquery
# from google.oauth2 import service_account

# from google.cloud import bigquery
# from google.oauth2 import service_account

# # Replace with your own JSON file path and BigQuery dataset and table details
# json_file_path = "testJson.json"
# project_id = "jumps-metrics-streamlit"
# dataset_id = "jump_metrics_dataset_id"
# table_id = "jumps_trials_table"
# # Set up credentials (replace 'path/to/your/credentials.json' with your service account key file)
# credentials = service_account.Credentials.from_service_account_file(
#     "jumps-metrics-streamlit-7e71be4a6fd3.json",
# )

# # Create a BigQuery client
# client = bigquery.Client(project=project_id, credentials=credentials)

# # Specify the dataset and table to which you want to upload the data
# dataset_ref = client.dataset(dataset_id)
# table_ref = dataset_ref.table(table_id)

# # Load the JSON file into BigQuery
# job_config = bigquery.LoadJobConfig()
# job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
# job_config.autodetect = True  # This allows BigQuery to automatically detect the schema
# with open(json_file_path, "rb") as source_file:
#     job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
# job.result()  # Wait for the job to complete
# st.write(f"Loaded {job.output_rows} rows into {table_id}")

uploaded_file = st.file_uploader("Choose a file")
df_ap = pd.read_csv(uploaded_file)
df_ap
# df = pd.read_csv("/home/geo/Desktop/greek_weather_data.csv")
# st.write(df, use_container_width=True)