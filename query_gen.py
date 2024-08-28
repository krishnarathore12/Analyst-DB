from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector


def query_gen(input, sql_tool):
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=([sql_tool]),
    )

    try:
        response = str(query_engine.query(input))
    except Exception as e:
        response = str(e)

    return response
