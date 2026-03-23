from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

PromptTemplate = ChatPromptTemplate.from_messages([
    ("""You are an expert information extraction assistant.

Your task is to read the provided paragraph and extract the most useful information about the movie in a clear, well-organized format.

RULES:

* Use only information found in the text.
* Do NOT invent or assume missing details.
* If something is not mentioned, write "Not specified".
* Keep answers concise and factual.
* Write in clean, readable sections.

Extract and present the information using the following format:

Movie Title:
Release Year:
Director:
Country:
Genre:

Main Characters:
(List important characters mentioned)

Cast:
(Actors only if mentioned)

Core Plot:
(Explain the main storyline in 2–3 sentences)

Themes & Social Messages:
(List key themes or ideas explored)

Based on Real Events:
(Yes / No / Not specified)

Awards & Achievements:
(Major awards or recognitions)

Cultural or Commercial Impact:
(Performance, popularity, or significance)

Unique Elements:
(Notable concepts, techniques, or standout ideas)

Quick Summary:
(A short 1–2 sentence summary)

## TEXT:

## {input_text}

Now extract the information.
"""),
('human', 
 
 """Now extract the information:
{paragraph}""")
]
)

para = input("Give your paragraph: ")

final_prompt = PromptTemplate.invoke(
    {"paragraph": para}
)

    
response = model.invoke(para)
print(response.content)