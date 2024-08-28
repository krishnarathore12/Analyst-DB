from llama_index.core import VectorStoreIndex, SQLDatabase
from llama_index.readers.wikipedia import WikipediaReader
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from sqlalchemy import insert
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
import pandas as pd


def set_default():
    llm = Groq(model="Llama3-70b-8192", api_key="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")
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    Settings.embed_model = embed_model
    Settings.llm = llm


def sql_create(sql_path):
    # Create SQLite database engine and reflect existing tables
    engine = create_engine(f"sqlite:///{sql_path}.db", future=True)
    metadata_obj = MetaData()

    # Reflect the existing table structure
    metadata_obj.reflect(bind=engine)
    city_stats_table = metadata_obj.tables["cars"]

    # Connect to the database and fetch all rows from 'city_stats' table
    with engine.connect() as connection:
        cursor = connection.execute(city_stats_table.select())
        print(cursor.fetchall())


    sql_database = SQLDatabase(engine, include_tables=["cars"])

    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["cars"],
    )

    sql_tool = QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=(
            "Useful for translating a natural language query into a SQL query over"
            " a table containing: cars, their specification , and details about the engine of"
            " each car"
        ),
    )

    return sql_tool


# def wiki_doc():
#     cities = ["Toronto", "Berlin", "Tokyo"]
#     wiki_docs = WikipediaReader().load_data(pages=cities)
#
#     vector_indices = []
#     for wiki_doc in wiki_docs:
#         vector_index = VectorStoreIndex.from_documents([wiki_doc])
#         vector_indices.append(vector_index)
#
#     vector_query_engines = [index.as_query_engine() for index in vector_indices]
#
#     vector_tools = []
#     for city, query_engine in zip(cities, vector_query_engines):
#         vector_tool = QueryEngineTool.from_defaults(
#             query_engine=query_engine,
#             description=f"Useful for answering semantic questions about {city}",
#         )
#         vector_tools.append(vector_tool)
#
#     return vector_tools
