from lida import Manager, TextGenerationConfig, llm

lida = Manager(text_gen=llm("cohere", api_key="mHI3dzX9yrZNpXcTBBCzAbwRm6C9g4EyX0ZvYbww"))  # !! api key
# textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)


def goals_gen(filename):
    summary = lida.summarize(filename)
    goal = lida.goals(summary, n=2)

    return goal


def summary_gen(file_name):
    summary = lida.summarize(file_name)

    return summary


def visualize(summary, goal):
    library = "seaborn"
    charts = lida.visualize(summary=summary, goal=goal, library=library)
    return charts

def explain(chart):
    explanation = lida.explain(code=chart.code)
    return explanation
