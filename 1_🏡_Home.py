import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import base64
from streamlit_extras.mention import mention
st.set_page_config(page_title='Business Card',
                   page_icon = "▶️", 
                   layout="wide")

with st.sidebar:
    mention(
    label="Business card",
    icon="Streamlit",  
    url="https://github.com/Vengatesan-K/BizCardX-Extracting-Business-Card")
    st_lottie("https://lottie.host/01055e13-5f2a-4940-9636-9070f5eb3bc7/4kWxu5mB3C.json",height=200)  
    
reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
        div.Sidebar   {padding-top:0rem;}
    </style>
"""
#st.markdown(reduce_header_height_style, unsafe_allow_html=True)

hide_st_style ="""
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """      
#st.markdown(hide_st_style,unsafe_allow_html=True)
col1,col2=st.columns([7,3])
with col1:
 st.image('poi2.png')
 st.write("Extracting text from business cards using OCR in Python serves the purpose of automating the process of data entry and organization. Business cards often contain important contact information, such as names, phone numbers, emails, and addresses. Manually transcribing this information from each business card can be time-consuming and error-prone.")
 st.caption(" By using OCR and storing the extracted information in a database, you can achieve several benefits :")  
 st.markdown('__<p style="text-align:left; font-size: 15px; color: ##dfcfbd">Efficiency and Automation </P>__',
                unsafe_allow_html=True)
 st.write("Using OCR to extract text from business cards automates the data entry process. It significantly reduces the time and effort required to input contact information manually. This is especially valuable when dealing with a large number of business cards.")
 st.markdown('__<p style="text-align:left; font-size: 15px; color: ##dfcfbd">Data Organization </P>__',
                unsafe_allow_html=True)
 st.write("Storing extracted information in a database allows you to keep all your contacts organized in one place. This makes it easier to search, retrieve, and manage contact details. You can also implement features like tagging, categorization, and searching to further enhance organization.")
 st.markdown('__<p style="text-align:left; font-size: 15px; color: ##dfcfbd">Data Enrichment</P>__',
                unsafe_allow_html=True)
 st.write("Beyond basic contact information, you can enrich the extracted data by linking it to social media profiles, company information, or additional notes. This can provide a more comprehensive view of your contacts.")
 st.markdown('__<p style="text-align:left; font-size: 15px; color: ##dfcfbd">Summary</P>__',
                unsafe_allow_html=True)
 st.write("The purpose of extracting text from business cards using OCR in Python and storing it in a database is to streamline and improve the management of contact information. This automation saves time, reduces errors, and enables efficient organization and utilization of the collected data.")

with col2:
     
     st_lottie("https://lottie.host/0b3e5824-b0f3-46ba-82fa-2c1274b766b6/vJ5bNI8F5d.json",height=200)   
     
     #st.header(":mailbox: Get In Touch With Me!")
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #F7F5F5">:mailbox: Get In Touch With Me!</P>__',
                unsafe_allow_html=True)

     contact_form = """
     <form action="https://formsubmit.co/YOUREMAIL@EMAIL.COM" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
     </form>
     """

     st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
     def local_css(file_name):
        with open(file_name) as f:
          st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


     local_css("style.css")
