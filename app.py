import os
import streamlit as st
import google.generativeai as genai
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.retrievers import BaseRetriever
from langchain.schema import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.utilities import SerpAPIWrapper

from dotenv import load_dotenv
load_dotenv()  


#  Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")


serp = SerpAPIWrapper(serpapi_api_key=os.environ.get("SERPAPI_API_KEY")) # requires SERPAPI_API_KEY

class GoogleRetriever(BaseRetriever):
    def _get_relevant_documents(self, query, run_manager=None):
        results = serp.results(query)  
        docs = []
        for r in results.get("organic_results", [])[:5]:  # manually limit to 5
            docs.append(Document(
                page_content=r.get("snippet", ""),
                metadata={"source": r.get("link", "Google")}
            ))
        return docs

    async def _aget_relevant_documents(self, query, run_manager=None):
        return self._get_relevant_documents(query, run_manager)


#  Wikipedia retriever
wiki = WikipediaRetriever()

#  Combine them into an EnsembleRetriever
retriever = EnsembleRetriever(
    retrievers=[GoogleRetriever(), wiki],
    weights=[0.7, 0.3]
)


#  Streamlit UI
st.title("🔎 AI Research Assistant (Gemini-powered)")

# Initialize chat history (for query rewriting + context)
if "history" not in st.session_state:
    st.session_state.history = []  # [{"role": "user/ai", "content": "..."}]



#-----------------------------------------------------Rewrite the user query-----------------------------------------------------#
def transform_query(question: str) -> str:

    # Build history in Gemini-compatible format (only 'user' and 'model')
    history_for_model = []
    for h in st.session_state.history:
        if h["role"] == "user":
            history_for_model.append({"role": "user", "parts": [{"text": h["content"]}]})
        elif h["role"] == "ai":
            history_for_model.append({"role": "model", "parts": [{"text": h["content"]}]})

    # Add the new user question at the end
    history_for_model.append({"role": "user", "parts": [{"text": question}]})

    # Create a special rewriting model with system_instruction
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        system_instruction="""You are a query rewriting expert.
        Based on the provided chat history, rephrase the user's last question
        into a complete standalone research query.
        Only return the rewritten question and nothing else. if the question is already complete, return it as is.
        for eg : what is machine learning then return it as is.
        Please understand me again i can't get you this question is not complete so you have to rewrite it."""
    )

    # Generate rewritten query
    response = model.generate_content(history_for_model)

    return response.text.strip()


#----------------------------------------------------------------------------------------------------------------------------------#


query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    #  Rewrite query if needed
    rewritten_query = transform_query(query)

    with st.spinner(f"Retrieving information for: {rewritten_query}"):
        docs = retriever.get_relevant_documents(rewritten_query)

    summaries = []
    with st.spinner("Summarizing sources..."):
        for doc in docs[:4]:
            response = gemini_model.generate_content(
                f"Summarize in 2-3 sentences:\n\n{doc.page_content}"
            )
            summaries.append({"source": doc.metadata.get("source", "Unknown"), "text": response.text})

    with st.spinner("Generating final answer..."):
        combined_text = "\n".join([s['text'] for s in summaries])
        final = gemini_model.generate_content(
            f"""Write a detailed, user-friendly research answer 
            based on these summaries:\n{combined_text}. you have to answer only based on these summaries and not from your own knowledge.
            Ensure it's comprehensive and informative.
            Add references if possible."""
        )

    # Save both original + rewritten queries and answer into history
    st.session_state.history.append({"role": "user", "content": query})

    st.subheader("✅ Answer")
    st.write(final.text)

    st.subheader("📚 Sources")
    for s in summaries:
        st.markdown(f"- **{s['source']}**: {s['text']}")

# 📝 Display Chat History in Sidebar
st.sidebar.title("💬 Chat History")
for h in st.session_state.history:
    if h["role"] == "user":  #  Only show user questions
        st.sidebar.markdown(f"- {h['content']}")




# Option to clear history
if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.sidebar.success("Chat history cleared!")
