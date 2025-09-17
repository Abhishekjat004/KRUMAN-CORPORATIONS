# KRUMAN-CORPORATIONS

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

## 🔎 AI Research Assistant (Gemini-powered)
## 📌 Idea Behind the Application

• Large Language Models (LLMs) are powerful, but they often hallucinate answers—generating information that sounds correct but is actually wrong.
To avoid misleading outputs, this project ensures that the assistant does not rely only on its own knowledge.
Instead, it retrieves real information from trusted sources like Google Search and Wikipedia, and then uses Gemini to summarize and generate a reliable answer.

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

# ⚙️ How It Works (Architecture / Approach)

## 1. User Query Input & Rewriting

• User enters a question.

• If the query is incomplete or a follow-up, Gemini rewrites it into a clear standalone research query.

• Additionally, users often ask incomplete or follow-up questions. For example:

  First question: “What is the impact on education after coming of AI?”

  Second question: “I can’t understand your content, can you explain again?”

  A normal system would wrongly search the second question directly. In this project, the assistant rewrites the query into a complete standalone research question before searching, ensuring context-aware, accurate retrieval.

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

## 2. Information Retrieval

• The rewritten query is sent to two retrievers:

• Google Search Retriever (via SerpAPI)

• Wikipedia Retriever

• Results are combined using an Ensemble Retriever with weighted importance.

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

## 4. Summarization

• Each retrieved document is summarized into 2–3 sentences using Gemini.

• Final Answer Generation

• Gemini generates a comprehensive research answer, strictly based on retrieved sources.

• References are included to improve trust and transparency.

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

## 5. Chat History

• Only the user’s questions are displayed in the sidebar (like ChatGPT’s sidebar).

• Option available to clear history.

## ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ##

# 🛠️ Tools & Frameworks Used

1. Streamlit
 → Interactive web UI

2. Google Generative AI (Gemini)
 → Query rewriting, summarization, and final answer generation

3. LangChain
 → Retrieval orchestration and document management

4. SerpAPI
 → Google Search API integration

  [WikipediaRetriever (LangChain)] → Wikipedia content retrieval

5. Python-dotenv
 → Secure API key management
