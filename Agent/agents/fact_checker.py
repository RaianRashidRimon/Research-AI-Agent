from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from tools import search_tool
from agents.writer import WriterOutput

class FactCheckerOutput(BaseModel):
    topic: str
    verified_summary: str
    key_points: list[str]
    flagged_claims: list[str]
    confidence: str
    sources: list[str]

def run_fact_checker(written: WriterOutput, memory, thread_id: str) -> FactCheckerOutput:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    parser = PydanticOutputParser(pydantic_object=FactCheckerOutput)

    system_prompt = """
    You are a specialist fact-checking agent. Your job is to verify the accuracy of a written summary.
    - Use the search tool to cross-check key claims
    - If a claim is verified, keep it in the summary
    - If a claim is uncertain or potentially wrong, add it to flagged_claims
    - Be conservative — if you cannot verify something, flag it
    - Set confidence to one of: "high", "medium" or "low" based on how much you could verify
    - Keep sources exactly as provided, add any new sources you used
    - Absolutely no hallucination — if you cannot verify something, flag it instead of making it up
    Wrap the output in this format and provide no other text\n{format_instructions}
    """.format(format_instructions=parser.get_format_instructions())

    agent = create_react_agent(
        model=llm,
        tools=[search_tool],
        prompt=system_prompt,
        checkpointer=memory,
    )

    user_message = f"""
    Topic: {written.topic}

    Summary to verify:
    {written.summary}

    Key Points to verify:
    {chr(10).join(f"- {point}" for point in written.key_points)}

    Sources:
    {chr(10).join(written.sources)}
    """

    config = {"configurable": {"thread_id": f"{thread_id}_fact_checker"}}
    raw_response = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config=config)

    content = extract_content(raw_response)

    try:
        return parser.parse(content)
    except Exception as e:
        print(f"[Fact Checker] Parse error: {e}")
        return FactCheckerOutput(
            topic=written.topic,
            verified_summary=written.summary,
            key_points=written.key_points,
            flagged_claims=[],
            confidence="low",
            sources=written.sources
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