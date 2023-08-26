# BizCardX-Extracting-Business-Card
Extracting Business card texts and stored in Data Warehouse

> Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.

__Essentials__

| Tool/Lib | Purpose |
| --- | --- |
| Python | Scripting,  to create function for retrieve the business card datas and store it into SQL |
| EasyOCR | To recognize and extract text from images or scanned documents. |
| PostgresSQL |  To store the extracted information along with the uploaded business card image. |
| Streamlit | Using Streamlit to create a simple UI where users can upload a image, view the card details, and modify the text and migrate the data to warehouse. |
| Pandas | For show as a dataframe in UI. |
| Plotly | Graphing library makes interactive, publication-quality graphs. |
| Keras-OCR | Recognize the text in image and highlight the datas.then using for inpainting the image |

__Implementation__

- [x] Using easyOCR to extract the relevant information from the uploaded business card image.

- [x] After information has been extracted, displayed it in a clean and organized manner in the Streamlit GUI. Using widget like plotly table to present the information.

- [x] Using database management system PostgresSQL to store the extracted information along with the uploaded business card image.

- [x]  Creating SQL queries to create tables, insert data, and retrieve data from the database, Update the data and Allow the user to delete the data through the streamlit UI

__Features__

- [x] Able to upload business card image and extract information include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code.

- [x] Those utilizing the system can choose to record the extracted data into a database, together with the image of the business card that has been uploaded.
  
- [x] The database has the capability to hold multiple entries, with each entry having its own corresponding business card image and extracted information.

- [x] Presenting the extracted information in a structured and organized way, users have the ability to seamlessly populate the database by simply clicking a button.


 
