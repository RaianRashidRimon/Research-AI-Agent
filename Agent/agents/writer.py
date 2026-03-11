from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from agents.researcher import ResearchOutput

class WriterOutput(BaseModel):
    topic: str
    summary: str
    key_points: list[str]
    sources: list[str]

def run_writer(research: ResearchOutput, memory, thread_id: str) -> WriterOutput:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    parser = PydanticOutputParser(pydantic_object=WriterOutput)

    system_prompt = """
    You are a specialist writing agent. Your only job is to take raw research facts and turn them into a clean, well-structured and readable summary.
    - Write in clear and professional language
    - Organize the information logically
    - Extract the most important key points as a list
    - Do NOT search for new information — only work with what you are given
    - Keep sources exactly as provided
    - Do not make stuff on your own or hallucinate — if something is unclear, just skip it
    Wrap the output in this format and provide no other text\n{format_instructions}
    """.format(format_instructions=parser.get_format_instructions())

    agent = create_react_agent(
        model=llm,
        tools=[],
        prompt=system_prompt,
        checkpointer=memory,
    )

    user_message = f"""
    Topic: {research.topic}

    Raw Facts:
    {chr(10).join(f"- {fact}" for fact in research.raw_facts)}

    Sources:
    {chr(10).join(research.sources)}
    """

    config = {"configurable": {"thread_id": f"{thread_id}_writer"}}
    raw_response = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config=config)

    content = extract_content(raw_response)

    try:
        return parser.parse(content)
    except Exception as e:
        print(f"[Writer] Parse error: {e}")
        return WriterOutput(
            topic=research.topic,
            summary=content,
            key_points=[],
            sources=research.sources
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