import streamlit as st
import os
from dotenv import load_dotenv
from search.search_api import search_web
from scraper.text_extractor import extract_text_from_urls
from llm.openai_client import get_llm_response
import json

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Ask the Web",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("Ask the Web")
st.markdown("""
    Ask any question and get answers with citations from the web.
    The app will search the web, analyze the content, and provide you with a detailed answer.
""")

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'sources' not in st.session_state:
    st.session_state.sources = None
if 'error' not in st.session_state:
    st.session_state.error = None

# Question input
question = st.text_input("Enter your question:", key="question_input")

# Search button
if st.button("Ask", type="primary"):
    if question:
        # Reset states
        st.session_state.error = None
        st.session_state.answer = None
        st.session_state.sources = None
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Search the web
            status_text.text("Searching the web...")
            search_results = search_web(question)
            progress_bar.progress(33)
            
            if not search_results:
                st.error("No search results found. Please try rephrasing your question.")
            else:
                st.session_state.search_results = search_results
                
                # Step 2: Extract text from URLs
                status_text.text("Extracting content from web pages...")
                urls = [result['link'] for result in search_results]
                texts = extract_text_from_urls(urls, search_results)
                progress_bar.progress(66)
                
                # Step 3: Get LLM response
                status_text.text("Generating answer...")
                answer, sources = get_llm_response(question, texts, search_results)
                progress_bar.progress(100)
                
                if answer.startswith("Sorry"):
                    st.error(answer)
                else:
                    st.session_state.answer = answer
                    st.session_state.sources = sources
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.error = str(e)
        finally:
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

# Display answer if available
if st.session_state.answer:
    st.markdown("### Answer")
    st.markdown(st.session_state.answer)
    
    if st.session_state.sources:
        st.markdown("### Sources")
        for source in st.session_state.sources:
            st.markdown(f"- [{source['title']}]({source['url']})")

# Debug section
with st.expander("Debug Information"):
    if st.session_state.search_results:
        st.json(st.session_state.search_results)
    if st.session_state.error:
        st.error(f"Error: {st.session_state.error}") 