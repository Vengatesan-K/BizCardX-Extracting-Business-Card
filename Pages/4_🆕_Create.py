import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import streamlit as st
import qrcode
from streamlit_extras.mention import mention
# Streamlit app title
from streamlit_option_menu import option_menu
st.set_page_config(page_title='Business Card',
                   page_icon = "▶️", 
                   layout="wide")

with st.sidebar:
            mention(
            label="Business card",
            icon="Streamlit",  # Some icons are available... like Streamlit!
            url="https://github.com/Vengatesan-K/BizCardX-Extracting-Business-Card",)

            selected = option_menu(
                menu_title=None,
                options=["Biz card", "With QR"],
                icons=["person-vcard","qr-code"],
                default_index=0,
                orientation="horizontal"
            )

if selected == "Biz card":
 def create_business_card(name, title, email, phone, logo):
    card_width = 1004
    card_height = 591

    image_path = "C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/gen.png"
    business_card = Image.open(image_path)

    # Add the logo to the card
    logo = logo.resize((150,150))  # Resize the logo to fit
    logo_position = ((card_width - logo.width) // 5, 120)
    business_card.paste(logo, logo_position)
    
    # Add text details to the card
    draw = ImageDraw.Draw(business_card)
    text_color = (0,0,0)  # Black

    font = ImageFont.truetype("C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/OpenSans-ExtraBold.ttf",25)
    font2 = ImageFont.truetype("C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/OpenSans-ExtraBoldItalic.ttf",50)
    text_y = logo_position[1] + logo.height + 30
    draw.text((520, text_y-250), name, font=font2, fill='green')
    draw.text((530, text_y-180), designation, font=font, fill='green')
    draw.text((30, text_y + 5), title, font=font2, fill='green')
    draw.text((550, text_y - 100), address, font=font, fill=text_color)
    draw.text((550, text_y -70), city, font=font, fill=text_color)
    draw.text((550,text_y-30),phone,font=font, fill=text_color)
    draw.text((550,text_y+20),email,font=font, fill=text_color)
    draw.text((550,text_y+70),website,font=font, fill=text_color)

    return business_card

# Streamlit app
 st.header("Business Card Generator")

 name = st.text_input("Name")
 designation = st.text_input("Designation")
 title = st.text_input("Title")
 email = st.text_input("Email")
 phone = st.text_input("Phone")
 address = st.text_input("Address")
 city = st.text_input("City")
 website = st.text_input("Website")
 logo = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
 if st.button("Generate Business Card") and logo is not None:
    logo_image = Image.open(logo)
    business_card = create_business_card(name, title, email, phone, logo_image)
    st.image(business_card, caption="Generated Business Card", use_column_width=True)
    
    download_buffer = io.BytesIO()
    business_card.save(download_buffer, format="PNG")
    st.download_button(label="Download Business Card", data=download_buffer.getvalue(), file_name="business_card.png")
    
#----------------------------------------------------------------------------------------------#-------------------------------------------------------------------------------#

if selected == "With QR":

 st.title("Business Card Generator")

# Input fields
 FName = st.text_input("Enter first name")
 Sname = st.text_input("Enter last name")
 Designation = st.text_input("Enter designation")
 Email = st.text_input("Enter email")
 Mobile = st.text_input("Enter mobile number")
 Address = st.text_input("Enter address")
 City = st.text_input("Enter city")
 Company1 = st.text_input("Enter company")
 Company2 = st.text_input("Enter company2")
# Button to generate business card
 if st.button("Generate Business Card with QR"):
    if Mobile != '0':
        # Generate QR code image and save
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(f"BEGIN:VCARD\nVERSION:3.0\nFN;CHARSET=UTF-8:{FName} {Sname}\nN;CHARSET=UTF-8:{Sname};{FName};;;\nEMAIL;CHARSET=UTF-8;type=WORK,INTERNET:{Email}\nTEL;TYPE=WORK,VOICE:{Mobile}\nADR;CHARSET=UTF-8;TYPE=WORK:{Address}\nTITLE;CHARSET=UTF-8:{Designation}\nORG;CHARSET=UTF-8:{Company1}\nREV:2021-10-25T08:06:20.364Z\nEND:VCARD")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))

        qr_filename = f"C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project//{FName} {Sname} QRCODE.png"
        qr_img.save(qr_filename)

        # Create and display the business card template with added information
        template = Image.open("blu.png")
        pic = Image.open(qr_filename).resize((150, 156), Image.ANTIALIAS)

        template.paste(pic, (750, 200))
        draw = ImageDraw.Draw(template)

        fontNum = ImageFont.truetype("C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/arial.ttf", size=45)
        fontBig = ImageFont.truetype("C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/arial.ttf", size=32)
        fontDes = ImageFont.truetype("C:/Users/VENKA/Desktop/Data Science/Python Anaconda/Project/arial.ttf", size=28)
        draw.text((60, 70), f" {FName}", font=fontNum, fill='white')
        draw.text((320, 70), f" {Sname}", font=fontNum, fill='white')
        draw.text((150, 250), f"+91 {Mobile}", font=fontDes, fill='white')
        draw.text((150, 340), f"{Email}", font=fontDes, fill='white')
        draw.text((80, 130), f"{Designation}", font=fontBig, fill='white')
        draw.text((150, 470), f"{City}", font=fontDes, fill='white')
        draw.text((150, 420), f"{Address}", font=fontDes, fill='white')
        draw.text((810, 100), f"{Company1}", font=fontDes, fill='black')
        draw.text((750, 150), f"{Company2}", font=fontDes, fill='black')
        

        st.image(template, caption="Generated Business Card with QR", use_column_width=True)
        
        download_buffer = io.BytesIO()
        template.save(download_buffer, format="PNG")
        st.download_button(label="Download Business Card", data=download_buffer.getvalue(), file_name="business_card.png")

    else:
        st.warning("Mobile number is 0")
