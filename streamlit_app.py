import streamlit as st
from google.cloud import storage
import json
import hashlib
import os

st.title("Recipes App")
bucket_name = "recipes-storage"

mode = st.sidebar.selectbox("Choose one", ["Read recipes", "Add a new recipe"])

if mode == "Read recipes":
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    for blob in bucket.list_blobs():
        data = json.loads(blob.download_as_string())
        st.markdown(f"# {data['name']}\n{data['description']}\n---\n")
else:
    key = st.sidebar.text_input("key", type="password")
    if key is not None and len(key) > 0:
        with open("write_credentials.json", "w") as f:
            f.write(key)

    if os.path.exists("write_credentials.json"):
        try:
            writer_storage_client = storage.Client.from_service_account_json("write_credentials.json")
        except:
            st.error("Invalid credentials.")

        os.remove("write_credentials.json")
        bucket = writer_storage_client.get_bucket(bucket_name)
        name = st.text_input("Name")
        labels = st.text_input("Labels (comma separated)").split(",")
        description = st.text_area("Description", height=20)

        submit = st.button("Submit")
        if submit:
            blob = bucket.blob(name)
            data = json.dumps({
                "name": name,
                "labels": labels,
                "description": description,
            })
            blob.upload_from_string(data, content_type='application/json')
