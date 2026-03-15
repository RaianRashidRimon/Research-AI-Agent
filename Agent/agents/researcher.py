from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from tools import search_tool, wiki_tool, read_tool, arxiv_tool

class ResearchOutput(BaseModel):
    topic: str
    raw_facts: list[str]
    sources: list[str]
    tools_used: list[str]

def run_researcher(query: str, memory, thread_id: str, history: list) -> ResearchOutput:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
    parser = PydanticOutputParser(pydantic_object=ResearchOutput)
    system_prompt = """
    You are a specialist research agent. Your only job is to gather raw facts and data.
    - Search the web and Wikipedia for information
    - Use the ArXiv tool to find relevant academic papers on the topic
    - Collect as many relevant facts as possible
    - Always record your sources including paper titles and links
    - Do NOT write summaries or opinions — only facts
    - If the user references something from earlier in the conversation, use the read_from_file tool to recall past research
    Wrap the output in this format and provide no other text\n{format_instructions}
    """.format(format_instructions=parser.get_format_instructions())

    agent = create_react_agent(
        model=llm,
        tools=[search_tool, wiki_tool, read_tool, arxiv_tool],
        prompt=system_prompt,
        checkpointer=memory,
    )

    messages = history + [{"role": "user", "content": query}]
    config = {"configurable": {"thread_id": f"{thread_id}_researcher"}}
    raw_response = agent.invoke({"messages": messages}, config=config)

    content = extract_content(raw_response)

    try:
        return parser.parse(content)
    except Exception as e:
        print(f"[Researcher] Parse error: {e}")
        return ResearchOutput(
            topic=query,
            raw_facts=[content],
            sources=[],
            tools_used=[]
        )

def extract_content(raw_response) -> str:
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
        if "```" in extracted:
            lines = extracted.splitlines()
            extracted = "\n".join(
                line for line in lines
                if not line.strip().startswith("```")
            ).strip()

        if extracted:
            return extracted
    return ""