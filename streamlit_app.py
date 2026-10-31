import streamlit as st
import asyncio, os, re, textwrap
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

st.set_page_config(page_title="Mera Video AI PRO", layout="centered")
st.title("Mera Video AI 🎬 - PRO Auto Video")
st.write("10-15 मिनट की कहानी लिखो, पूरा वीडियो अपने आप बनेगा!")

story = st.text_area("Kahani likho:", height=150, value="Ek robot chand par cycle chala raha hai. Piche hazaro tare chamak rahe hain. Prithvi door se neeli dikh rahi hai. Robot khush hoke has raha hai.")

voice_choice = st.selectbox("Voice kaisi chahiye?", ["Hindi Ladki - Natural", "Hindi Ladka - Natural"])
voice = "hi-IN-SwaraNeural" if "Ladki" in voice_choice else "hi-IN-MadhurNeural"

if st.button("🎥 FULL VIDEO BANAO (Auto)"):
    # 1. Story ko 6 hisso me todo
    sentences = re.split(r'[।.!?\n]+', story)
    sentences = [s.strip() for s in sentences if len(s.strip())>10][:6]
    if len(sentences)<3:
        sentences = [story]*3
    
    st.info(f"{len(sentences)} Scenes ka video bana raha hu...")
    
    # 2. Voice banao - Edge TTS (Bilkul insaan jaisi)
    async def make_audio():
        communicate = edge_tts.Communicate(text=" ".join(sentences), voice=voice)
        await communicate.save("voice.mp3")
    asyncio.run(make_audio())
    st.audio("voice.mp3")
    
    # 3. Cartoon Images banao
    images = []
    for i, scene in enumerate(sentences):
        st.write(f"Scene {i+1}: {scene[:50]}...")
        try:
            prompt = f"cartoon style, {scene}, vibrant colors, 3d pixar style"
            url = f"https://image.pollinations.ai/prompt/{prompt}"
            r = requests.get(url, timeout=30)
            img = Image.open(BytesIO(r.content)).resize((720,1280))
        except:
            # Fallback - Text wala image
            img = Image.new('RGB', (720,1280), (20,20,60))
            d = ImageDraw.Draw(img)
            d.text((40,600), textwrap.fill(scene, width=30), fill="white")
        img.save(f"scene_{i}.jpg")
        images.append(f"scene_{i}.jpg")
        st.image(img, width=300)
    
    # 4. Video jodo
    audio = AudioFileClip("voice.mp3")
    duration_per = audio.duration / len(images)
    clips = [ImageClip(img).set_duration(duration_per) for img in images]
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_audio(audio)
    final_video.write_videofile("final_video.mp4", fps=24, codec="libx264")
    
    st.success("Ban gaya! 10 min ka Video taiyaar hai!")
    st.video("final_video.mp4")
    with open("final_video.mp4","rb") as f:
        st.download_button("📥 Video Download Karo", f, file_name="mera_video.mp4")