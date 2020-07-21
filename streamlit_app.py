import streamlit as st
from google.cloud import storage
import json

storage_client = storage.Client()

bucket_name = "recipes-storage"


bucket = storage_client.get_bucket(bucket_name)


mode = st.sidebar.selectbox("Choose one", ["Read recipes", "Add a new recipe"])

if mode == "Read recipes":
    for blob in bucket.list_blobs():
        data = json.loads(blob.download_as_string())
        st.markdown(f"# {data['name']}\n{data['description']}\n---")
else:
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
