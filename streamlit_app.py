import streamlit as st
st.title("Mera Video AI")
story = st.text_area("Kahani likho")
if st.button("Cartoon Banao"):
    url = f"https://image.pollinations.ai/prompt/{story} cartoon"
    st.image(url)