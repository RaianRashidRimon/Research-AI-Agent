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

## Setup & Installation

### 1. Clone the repository

    git clone https://github.com/RaianRashidRimon/Research-AI-Agent.git

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Set up your API key

Create a '.env' file in the root folder where

GEMINI_API_KEY=your_own_gemini_api_key

## Usage
### Terminal Mode 

    python main.py

### Streamlit UI

    streamlit run ui.py

## Tech Stack


| Technology | Purpose |
|---|---|
| **LangGraph** | Multi-agent management |
| **LangChain** | Agent framework |
| **Google Gemini** | Underlying LLMUnderlying LLM |
| **Streamlit** | Web UI | 
| **DuckDuckGo Search** | Web search tool |
| **Wikipedia** | Encyclopedic search tool |
| **ArXiv** | Academic paper search |


## Future Improvements
1. Export research reports to PDF
2. Add more academic paper sources





















