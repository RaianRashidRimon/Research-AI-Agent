# 🔬 Multi-Agent Research Assistant
This is an AI tool that breaks down the research process into three specialized agents

   1. A Researcher
   2. A Writer
   3. A Fact Checker

Each with a focused role. Given a query, the serial pipeline autonomously searches the web, Wikipedia and ArXiv for academic papers and structures the findings into a clean summary & verifies key claims before presenting the final result. The assistant also maintains memory across sessions, so it remembers what it has researched before.

## How it works

    User Query → Researcher → Writer → Fact Checker → Final Output
<ins>**Researcher Agent:**</ins> Searches the web, Wikipedia and ArXiv to gather raw facts and sources

<ins>**Writer Agent:**</ins> Takes raw facts and structures them into a clean and readable summary with key points

<ins>**Fact Checker Agent:**</ins> Cross-checks claims against web search results, flags uncertain info and assigns a confidence score

## Features
* Multi-agent pipeline with three specialized AI agents
* Web search via DuckDuckGo
* Wikipedia search
* Academic paper search via ArXiv
* Memory across sessions. Remembers past research even after restarting
* Chat-style Streamlit UI with sidebar showing sources and flagged claims
* Confidence scoring. HIGH, MEDIUM or LOW based on how much could be verified
* Flagged claims. Uncertain or unverified statements are clearly highlighted
* Save reports to a local text file
