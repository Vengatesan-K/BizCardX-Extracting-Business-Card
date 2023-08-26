import streamlit as st
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\VENKA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import easyocr
import re
import base64
import numpy as np
import cv2
import tempfile
import pandas as pd
import math
import os
import base64
from streamlit_extras.mention import mention
import plotly.graph_objs as go
import psycopg2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import keras_ocr
from streamlit_option_menu import option_menu
reader = easyocr.Reader(['en']) 

conn = psycopg2.connect(host="localhost", user="postgres", password="vengatesh", port=5432, database="Bizcardx")
cur = conn.cursor() 

st.set_page_config(page_title='Business Card',
                   page_icon = "▶️", 
                   layout="wide")

with st.sidebar:
    mention(
    label="Business card",
    icon="Streamlit",  # Some icons are available... like Streamlit!
    url="https://github.com/Vengatesan-K/BizCardX-Extracting-Business-Card",)


def extract_and_highlight(image):
    # Perform OCR with detailed output
    extracted_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Extract word bounding box coordinates and texts
    word_boxes = []
    for i, word_text in enumerate(extracted_data['text']):
        if word_text.strip() != '':
            x, y, w, h = extracted_data['left'][i], extracted_data['top'][i], extracted_data['width'][i], extracted_data['height'][i]
            word_boxes.append(((x, y, x + w, y + h), word_text))

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    for box, word_text in word_boxes:
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
        draw.rectangle([x1 - 2, y1 - 2, x2 + 2, y2 + 2], outline='yellow', width=2)

    return image

def image_to_text(image_path):
     reader = easyocr.Reader(['en'])
     result = reader.readtext(image_path)
   
     details =[]
     for i in range(len(result)):
         details.append(result[i][1])
     name = []
     designation = []
     contact =[]
     email =[]
     website = []
     street =[]
     city =[]
     state =[]
     pincode=[]
     company =[]
    
     for i in range(len(details)):
        match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)',details[i])    
        match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', details[i])
        match3 = re.findall('^[E].+[a-z]',details[i])
        match4 = re.findall('([A-Za-z]+) ([0-9]+)',details[i])
        match5 = re.findall('([0-9]+ [a-zA-z]+)',details[i])    
        match6 = re.findall('.com$' , details[i])
        match7 = re.findall('([0-9]+)',details[i])
        if details[i] == details[0]:
            name.append(details[i])        
        elif details[i] == details[1]:
            designation.append(details[i])
        elif '-' in details[i]:
            contact.append(details[i])
        elif '@' in details[i]:
            email.append(details[i])
        elif "www " in details[i].lower() or "www." in details[i].lower():
            website.append(details[i])
        elif "WWW" in details[i]:
            website.append(details[i] +"." + details[i+1])
        elif match6:
            pass
        elif match1:
            street.append(match1[0][0])
            city.append(match1[0][1])
            state.append(match1[0][2])
        elif match2:
            street.append(match2[0][0])
            city.append(match2[0][1])
        elif match3:
            city.append(match3[0])
        elif match4:
            state.append(match4[0][0])
            pincode.append(match4[0][1])
        elif match5:
            street.append(match5[0]+' St,')
        elif match7:
            pincode.append(match7[0])
        else:
            company.append(details[i])
     if len(company)>1:
        comp = company[0]+' '+company[1]
        print(comp)
     else:
        comp = company[0]
     if len(contact) >1:
        contact_number = contact[0]
        alternative_number = contact[1]
     else:
        contact_number = contact[0]
        alternative_number = None
    
     with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    
     encoded_image = base64.b64encode(image_data).decode('utf-8')
    
     image_details = {'Name':name[0],'Designation':designation[0],'Company_name':comp,
                     'Contact':contact_number,'Alternative':alternative_number,'Email':email[0],
                     'Website':website[0],'Street':street[0],'City':city[0],'State':state[0],
                     'Pincode':pincode[0],'image': encoded_image}
     
        
     return image_details


def main():
    st.header(":red[B]usiness :red[C]ard :red[R]eader")
    st.caption("Upload an image to extract it using the sidebar file uploader.")  
    
    uploaded_image = st.sidebar.file_uploader("Upload a business card image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # Create a temporary file to save the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
            temp_image_path = temp_image_file.name
            temp_image_file.write(uploaded_image.read())

            highlighted_image = extract_and_highlight(Image.open(temp_image_path))
            col1,col2 = st.columns([4,6])
            with col2:

                pipeline = keras_ocr.pipeline.Pipeline()
                img = keras_ocr.tools.read(temp_image_path)
                predictions = pipeline.recognize([img])[0]

    # Plot the predictions
                fig, ax = plt.subplots()
                keras_ocr.tools.drawAnnotations(image=img, predictions=predictions, ax=ax)
                ax.set_xlabel('Highlighted Image')
                st.pyplot(fig, use_container_width=True)

                plt.close("all")

            with col1:
                image = Image.open(temp_image_path)
                st.image(image, caption='Uploaded Image', use_column_width=True)

            tab1,tab2,tab3 = st.tabs(['Extract details','Upload','Remove text'])
            with tab1:
             if st.button('Preview'):
                  extracted_details = image_to_text(temp_image_path)
                  table_data = [[key, value] for key, value in extracted_details.items()]
                  rowEvenColor = '#77aac3'
                  rowOddColor = 'white'
                  fig = go.Figure(data=[go.Table(header=dict(values=["<b>Details</b>", "<b>Value</b>"],line_color='grey',font=dict(color='black', size=15),
                  fill_color='lightblue'),cells=dict(values=list(zip(*table_data)),line_color='darkslategray',
                  fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor,rowEvenColor,rowOddColor,rowEvenColor,rowOddColor,rowEvenColor,rowOddColor,rowEvenColor]*12],font=dict(color='black', size=12)))])
                #fig.update_layout(width=700)
                  st.plotly_chart(fig,use_container_width=True)
            with tab2:    
             if temp_image_path is not None:
                if st.button('Insert to SQL'):
                 try:
           
                   extracted_details = image_to_text(temp_image_path)

                   insert_query = """
                    INSERT INTO BUSINESS_CARD(
                    NAME, DESIGNATION, COMPANY_NAME, CONTACT, ALTERNATE,
                    EMAIL, WEBSITE, ADDRESS, CITY, STATE, PINCODE, IMAGE
                    ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            # Execute the INSERT query
                   cur.execute(insert_query, (
                   extracted_details['Name'], extracted_details['Designation'],
                   extracted_details['Company_name'], extracted_details['Contact'],
                   extracted_details['Alternative'], extracted_details['Email'],
                   extracted_details['Website'], extracted_details['Street'],
                   extracted_details['City'], extracted_details['State'],
                   extracted_details['Pincode'], extracted_details['image']
            ))
            
            # Commit the changes and close the connection
                   
            
                   st.success('Data inserted successfully')
                   query =("SELECT name, designation,company_name ,contact, alternate, email, website, address, city,state,pincode FROM business_card")
                   cur.execute(query)
                   result = cur.fetchall()
                   df = pd.DataFrame(result, columns=['name', 'designation','company_name' ,'contact', 'alternate', 'email', 'website', 'address', 'city','state','pincode'])
                   table_data = go.Table(
                   header=dict(values=df.columns,fill_color='lightblue',font=dict(color='black', size=15)),
                   cells=dict(values=[ df.name, df.designation, df.company_name, df.contact, df.alternate, df.email, df.website,df.address,df.city,df.state,df.pincode]))
                   layout = dict(width=800, height=600)
                   fig2 = go.Figure(data=[table_data], layout=layout)
                   st.plotly_chart(fig2,use_container_width=True)
                   
                   conn.commit()
                   cur.close()
                   conn.close()
                   #st.write(df)
                 except Exception as e:
                     st.error(f"An error occurred: {e}")
                     
            with tab3:
                def midpoint(x1, y1, x2, y2):
                   x_mid = int((x1 + x2)/2)
                   y_mid = int((y1 + y2)/2)
                   return (x_mid, y_mid)
                pipeline = keras_ocr.pipeline.Pipeline()
                def inpaint_text(img_path, pipeline):
    # read image
                  img = keras_ocr.tools.read(img_path)
    # generate (word, box) tuples 
                  prediction_groups = pipeline.recognize([img])
                  mask = np.zeros(img.shape[:2], dtype="uint8")
                  for box in prediction_groups[0]:
                    x0, y0 = box[1][0]
                    x1, y1 = box[1][1] 
                    x2, y2 = box[1][2]
                    x3, y3 = box[1][3] 
        
                    x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
                    x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
        
                    thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
        
                    cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
                    thickness)
                    img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
                  return(img)                               

                if st.button('Clear'):
                     image_path = keras_ocr.tools.read(temp_image_path)  # Replace with your image's path

                     inpainted_img = inpaint_text(image_path, pipeline)
                   
            
            # Display the inpainted image using Matplotlib's pyplot
                     fig1, ax = plt.subplots(figsize=(2, 1))
                     ax.imshow(inpainted_img)
                     ax.axis('off')  # Turn off axis labels and ticks
                     st.pyplot(fig1, use_container_width=False)
                     
                     if st.button("Save Image"):
                       save_path = os.path.join(os.getcwd(), "inpainted_image.png")
                       fig1.savefig(save_path, dpi=300)  # Save the figure as PNG
                       st.success("Image saved as {}".format(save_path))
            
                plt.close("all")
                    
if __name__ == "__main__":
    main()
