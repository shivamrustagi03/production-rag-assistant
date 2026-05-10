from pathlib import Path
import shutil

import streamlit as st

from app.core.config import load_config
from app.generation.response_generator import ResponseGenerator
from app.retrieval.search import build_retriever
from app.utils.helpers import ensure_directory


st.set_page_config(page_title="Production RAG Assistant", layout="wide")
st.title("Production RAG Assistant")

config = load_config()
upload_dir = ensure_directory(config.raw_data_dir / "uploads")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None

with st.sidebar:
    st.header("Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload PDF or text files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )
    if uploaded_files and st.button("Ingest documents", type="primary"):
        for uploaded_file in uploaded_files:
            destination = upload_dir / uploaded_file.name
            with destination.open("wb") as file:
                shutil.copyfileobj(uploaded_file, file)
        with st.spinner("Indexing uploaded documents..."):
            st.session_state.retriever = build_retriever(config, rebuild=True)
        st.success("Documents indexed.")

    if st.button("Load existing index"):
        with st.spinner("Loading vector store..."):
            st.session_state.retriever = build_retriever(config)
        st.success("Retriever ready.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

query = st.chat_input("Ask a question about your documents")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving context and generating answer..."):
            retriever = st.session_state.retriever or build_retriever(config)
            st.session_state.retriever = retriever
            chunks = retriever.retrieve(query, config.retrieval_top_k)
            response = ResponseGenerator(config).answer(query, chunks)
            st.markdown(response["answer"])
            if response["sources"]:
                st.caption("Sources: " + ", ".join(response["sources"]))
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response["answer"],
                "sources": response["sources"],
            }
        )
