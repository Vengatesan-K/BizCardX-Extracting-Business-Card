import streamlit as st
import psycopg2
import plotly.graph_objs as go
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
import pandas as pd
conn = psycopg2.connect(host="localhost", user="postgres", password="vengatesh", port=5432, database="Bizcardx")
cur = conn.cursor() 

st.set_page_config(page_title='Business Card',
                   page_icon = "▶️", 
                   layout="wide")
st.header("Modify and Delete Business card's details")
with st.sidebar:
            mention(
            label="Business card",
            icon="Streamlit",  
            url="https://github.com/Vengatesan-K/BizCardX-Extracting-Business-Card",)
            selected = option_menu(
                menu_title=None,
                options=["Edit", "Delete"],
                icons=["pencil-square","trash"],
                default_index=0,
                orientation="horizontal"
            )
if selected == "Edit":
 cur.execute("SELECT  id,name FROM business_card")
 result = cur.fetchall()
 business_cards = {}
 for row in result:
    business_cards[row[1]] = row[0]
 selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))
    
    # Get the current information for the selected business card
 cur.execute("SELECT * FROM business_card WHERE name=%s", (selected_card_name,))
 result = cur.fetchone()

 col1,col2 = st.columns([5,5])
 with col1:
  add_vertical_space(2)
  st.write("Name:", result[1])
  add_vertical_space(2)
  st.write("Designation:", result[2])
  add_vertical_space(2)
  st.write("Company_name:", result[3])
  add_vertical_space(2)
  st.write("Contact:", result[4])
  add_vertical_space(2)
  st.write("Alternative:", result[5])
  add_vertical_space(2)
  st.write("Email:", result[6])
  add_vertical_space(2)
  st.write("Website:", result[7])
  add_vertical_space(2)
  st.write("Street:", result[8])
  add_vertical_space(2)
  st.write("City:", result[9])
  add_vertical_space(2)
  st.write("State:", result[10])
  add_vertical_space(2)
  st.write("Pincode:", result[11])
  add_vertical_space(2)

 with col2:
  name = st.text_input("Name", result[1])
  designation = st.text_input("Designation", result[2])
  company_name = st.text_input("Company_name", result[3])
  contact = st.text_input("Contact", result[4])
  alternative = st.text_input("Alternative", result[5])
  email = st.text_input("Email", result[6])
  website = st.text_input("Website", result[7])
  street = st.text_input("Street", result[8])
  city = st.text_input("City", result[9])
  state = st.text_input("State", result[10])
  pincode = st.text_input("Pincode", result[11])

    
 if st.button("Update Business Card"):
        
  cur.execute("UPDATE business_card SET name=%s, designation=%s, company_name=%s, contact=%s, alternate=%s, email=%s, website=%s,address=%s,city=%s,state=%s,pincode=%s WHERE name=%s", 
                             (name, designation, company_name, contact, alternative, email,website, street, city,state,pincode, selected_card_name))
  conn.commit()
  st.success("Business card information updated in database.")
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
  
else:
    # Create a dropdown menu to select a business card to delete
    cur.execute("SELECT id,name FROM business_card")
    result = cur.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[0]] = row[1]
    selected_card_id = st.selectbox("Select a business card to delete", list(business_cards.keys()), format_func=lambda x: business_cards[x])

    # Get the name of the selected business card
    cur.execute("SELECT name FROM business_card WHERE id=%s", (selected_card_id,))
    result = cur.fetchone()
    selected_card_name = result[0]

    # Display the current information for the selected business card
    st.write("Name:", selected_card_name)

    # Create a button to confirm the deletion of the selected business card
    if st.button("Delete Business Card"):
        cur.execute("DELETE FROM business_card WHERE name=%s", (selected_card_name,))
        conn.commit()
        st.success("Business card information deleted from database.")
        query =("SELECT name, designation,company_name ,contact, alternate, email, website, address, city,state,pincode FROM business_card")
        cur.execute(query)
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=['name', 'designation','company_name' ,'contact', 'alternate', 'email', 'website', 'address', 'city','state','pincode'])
        table_data = go.Table(
        header=dict(values=df.columns,fill_color='lightblue',font=dict(color='black', size=15)),
        cells=dict(values=[df.name, df.designation, df.company_name, df.contact, df.alternate, df.email, df.website,df.address,df.city,df.state,df.pincode]))
        layout = dict(width=800, height=600)
        fig3 = go.Figure(data=[table_data], layout=layout)
        st.plotly_chart(fig3,use_container_width=True)
         




    
