import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama  # Rename this if needed from parse_with_ollama
from prompt_templates import get_prompt

# Streamlit UI
st.title("Echo-Scrape")
url = st.text_input("Enter Website URL :")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the cleaned DOM in session
        st.session_state.dom_content = cleaned_content

        # Show DOM content
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse...")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Split DOM into chunks
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Combine or select the first N chunks (based on token limit)
            dom_chunks_combined = "\n".join(dom_chunks[:3])  # Adjust as needed

            # Generate final prompt with few-shot examples + user intent
            final_prompt = get_prompt(dom_chunks_combined)

            # Call local LLaMA model
            parsed_result = parse_with_ollama(final_prompt)

            # Display the result
            st.write("### 🔍 Parsed Results :\n")
            st.markdown(parsed_result)
