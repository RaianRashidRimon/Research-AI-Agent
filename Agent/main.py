from dotenv import load_dotenv 
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tool_used: list[str]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

system_prompt = """
You are a research assistant that will help generate a thorough and complete response about the query from the human.
Answer the user query and use necessary tools.
Make sure your summary is detailed and complete — do not cut it short.
Wrap the output in this format and provide no other text\n{format_instructions}
""".format(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
)

query = input("What do you want to research? ")
raw_response = agent.invoke({"messages": [{"role": "user", "content": query}]})

# Find the last message with actual text content
content = ""
for msg in reversed(raw_response["messages"]):
    raw = msg.content

    if isinstance(raw, list):
        extracted = " ".join(
            block["text"] for block in raw
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        extracted = raw or ""

    extracted = extracted.strip()
    if extracted:
        content = extracted
        break

# Strip markdown code fences if present
if "```" in content:
    lines = content.splitlines()
    content = "\n".join(
        line for line in lines
        if not line.strip().startswith("```")
    ).strip()

try:
    structured_response = parser.parse(content)
    print("RESEARCH RESULT")
    print(f"\nTopic      : {structured_response.topic}")
    print(f"\nSummary    :\n{structured_response.summary}")
    print(f"\nSources    : {', '.join(structured_response.source)}")
    print(f"\nTools Used : {', '.join(structured_response.tool_used)}")
    print("\n" + "═" * 40)
except Exception as e:
    print(f"\n[Error] Failed to parse structured response: {e}")
    print(f"Raw output:\n{content}")