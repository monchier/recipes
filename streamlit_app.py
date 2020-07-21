import streamlit as st
from google.cloud import storage
import json
import hashlib
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

storage_client = storage.Client()

bucket_name = "recipes-storage"


bucket = storage_client.get_bucket(bucket_name)

mode = st.sidebar.selectbox("Choose one", ["Read recipes", "Add a new recipe"])

if mode == "Read recipes":
    for blob in bucket.list_blobs():
        data = json.loads(blob.download_as_string())
        st.markdown(f"# {data['name']}\n{data['description']}\n---")
else:

    user = st.sidebar.text_input("username")
    password = st.sidebar.text_input("password", type="password")
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    entered_password_digest = str(m.hexdigest())

    def get_password_digest(username):
        with open("people.json", "r") as f:
            people = json.load(f)
        for e in people:
            if e["username"] == username:
                return e["password"]
        return None

    password_digest = get_password_digest(user)
    #st.write(password_digest)
    #st.write(entered_password_digest)

    if password_digest != entered_password_digest:
        st.error("Wrong credentials!")
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
