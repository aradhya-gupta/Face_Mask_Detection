import streamlit as st
from multiapp import MultiApp   
from apps import imageDetector, videoDetector

app = MultiApp()

st.markdown("""
# Face Mask Detection : COVID-19
 This is a computer vision project that aims at detecting whether people in an image or a video dataset are wearing masks or not. COVID-19 has spread like a wild fire and this application can help in the fight against the deadly virus by ensuring that people wear masks.
""")

st.sidebar.markdown(""" ### COVID-19 Official Guidelines 
Wearing a mask is essential in the fight against COVID-19. 
[Link](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/when-and-how-to-use-masks) to the official guidelines provided by WHO. """)
st.sidebar.image('corona.gif')
app.add_app("Detection in image", imageDetector.app)
app.add_app("Detection in video", videoDetector.app)

app.run()
