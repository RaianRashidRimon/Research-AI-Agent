from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime
import os

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

def read_from_txt(filename: str = "research_output.txt"):
    if not os.path.exists(filename):
        return "No previous research found."
    
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    if not content.strip():
        return "Research file is empty."
    
    return content

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

read_tool = Tool(
    name="read_from_file",
    func=read_from_txt,
    description="Reads previously saved research from a text file. Use this to recall past research.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

arxiv_tool = ArxivQueryRun()