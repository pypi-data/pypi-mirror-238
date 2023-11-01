import openai
from IPython.display import Markdown, display
def askGPT4(prompt):
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
    {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

def ask(prompt):
    display(Markdown(askGPT4(prompt)))