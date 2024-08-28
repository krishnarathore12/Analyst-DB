import gradio as gr
import matplotlib.pyplot as plt
import io
import base64

import pandas as pd
from PIL import Image
from io import BytesIO
import streamlit as st
from sqlalchemy import create_engine, MetaData

from query_gen import query_gen
from sql_router import (
    set_default,
    sql_create,
)

from summary_gen import (
    summary_gen,
    goals_gen,
    visualize, explain,
)


set_default()
# sql_tool = sql_create()
# vector_tools = wiki_doc()


def base64_to_image(base64_string):
    byte_data = base64.b64decode(base64_string)

    return Image.open(BytesIO(byte_data))


def db_to_csv(db_path, csv_path):
    # Create SQLite database engine and reflect existing tables
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    metadata_obj = MetaData()

    # Reflect the existing table structure
    metadata_obj.reflect(bind=engine)
    city_stats_table = metadata_obj.tables["cars"]

    # Connect to the database and fetch all rows from 'city_stats' table
    with engine.connect() as connection:
        df = pd.read_sql_table(city_stats_table.name, connection)

    df.to_csv(csv_path, index=False)


menu = st.sidebar.selectbox("Choose an option", ["Summarize", "Question based Graph", "Chat with Database"])

if menu == "Summarize":
    st.subheader("Summarization of your data")
    file_uploader = st.file_uploader("Upload your database", type="db")
    if file_uploader is not None:
        path_to_save = "filename.db"
        csv_path = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        db_to_csv(path_to_save, csv_path)
        summary = summary_gen(csv_path)
        st.write(summary)
        goales = goals_gen(csv_path)
        i = 0
        for goal in goales:
            st.write(goal)
            charts = visualize(summary, goal)
            img_string = charts[i].raster
            img = base64_to_image(img_string)
            st.image(img)

elif menu == "Question based Graph":
    st.subheader("Query your data to generate graph")
    file_uploader = st.file_uploader("Upload your database", type="db")
    if file_uploader is not None:
        path_to_save = "filename.db"
        csv_path = "filename1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        db_to_csv(path_to_save, csv_path)

        text_area = st.text_area("Query your data to generate graph", height=200)
        if st.button("Generate Graph"):
            if len(text_area) > 0:
                st.info("Your query: " + text_area)
                summary = summary_gen(csv_path)
                user_query = text_area
                charts = visualize(summary, user_query)
                img_string = charts[0].raster
                img = base64_to_image(img_string)
                st.image(img)
                explaination = explain(charts[0])
                st.write(explaination)

elif menu == "Chat with Database":
    st.subheader("Query your Database")
    file_uploader = st.file_uploader("Upload your database", type="db")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages = []
    if file_uploader is not None:
        path_to_save = "filename.db"
        sql_path = "filename"
        csv_path = "filename1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        db_to_csv(path_to_save, csv_path)

        sql_tool = sql_create(sql_path)


        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask me anything"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
        if prompt is not None:

            with st.chat_message("assistant"):
                answer = query_gen(prompt, sql_tool)
                response = st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # if 'messages' not in st.session_state:
        #     st.session_state.messages = []
        #
        # with st.chat_input("Query your data to generate answers") as chat:
        #     text_area = chat.content
        #
        # if st.button("Generate Answer"):
        #     if text_area:
        #         st.session_state.messages.append({"role": "user", "content": text_area})
        #         sql_tool = sql_create(sql_path)
        #         response = query_gen(text_area, sql_tool)
        #         st.session_state.messages.append({"role": "bot", "content": response})
        #
        #     # Display chat messages
        # for message in st.session_state.messages:
        #     st.chat_message(message["role"]).markdown(message["content"])
        #
        #
