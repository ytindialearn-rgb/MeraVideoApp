import streamlit as st
import requests
from gtts import gTTS
import os
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Mera Video AI")
st.title("Mera Video AI 🎬 - Voice + Video")

story = st.text_area("Kahani likho (ek hi line me):", "Ek chota bandar ped par aam kha raha hai, uske niche hathi so raha hai")

if st.button("Video Banao 🎥"):
    if story:
        sentences = story.split(",")
        if len(sentences) < 2:
            sentences = [story, story]
            
        st.write("1. Voice bana raha hu...")
        tts = gTTS(text=story, lang='hi', slow=False)
        tts.save("voice.mp3")
        st.audio("voice.mp3")

        st.write("2. Cartoon bana raha hu...")
        images = []
        for i, part in enumerate(sentences[:3]):
            if part.strip() == "": continue
            url = f"https://image.pollinations.ai/prompt/{part.strip()} cartoon 2d story, colorful?width=1024&height=768&nologo=true"
            try:
                resp = requests.get(url, timeout=30)
                img = Image.open(BytesIO(resp.content))
                images.append(img)
                st.image(img, caption=f"Scene {i+1}: {part}")
            except:
                pass
        
        st.success("Ban gaya! Ab neeche se images ko save karke kisi bhi Video Maker App (InShot) me jod do, aur ye voice.mp3 laga do. Full Auto Video next update me!")
        st.balloons()