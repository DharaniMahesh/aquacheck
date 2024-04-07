import stqdm
import pickle
import pandas as pd
from PIL import Image
from time import sleep
import streamlit as st
from stqdm import stqdm
from streamlit_option_menu import option_menu

from flask import Flask, request
import numpy as np
import cv2
import os
#custom
from custom.credentials import token, account
from custom.essentials import stringToRGB, get_model
from custom.whatsapp import whatsapp_message
from validation import input_validation
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url


# Replace with your Cloudinary credentials
config = cloudinary.config(secure=True)

CLOUD_NAME=os.environ.get("cloud_name")
API_KEY=os.environ.get("api")
API_SECRET=os.environ.get("api_sec")



cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)


@st.cache_resource
def load_model():
    with open('assets/model.pkl', 'rb') as f:
        model = pickle.load(f)
        # print(model.__dict__)
        return model
    


def upload_image(image_path):
  # Upload the image
  print(image_path)
  upload_result = cloudinary.uploader.upload(image_path)

    # Extract the public URL from the upload result
  public_url, options = cloudinary_url(upload_result['public_id'], format=upload_result['format'])
  print(public_url)
  return public_url

 



st.set_page_config(page_title="AquaCheck", page_icon="💧", initial_sidebar_state="expanded")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
css_style = {
    "icon": {"color": "white"},
    "nav-link": {"--hover-color": "grey"},
    "nav-link-selected": {"background-color": "#FF4C1B"},
}

# Loading assets
img_banner = Image.open("assets/images/aqua2.jpg")
# img_banner2 = Image.open("assets/images/banner2.png")
img_rwanda = Image.open("assets/images/vvitlogo.png")


def home_page():
    st.write(f"""# Water Inspection System""", unsafe_allow_html=True)
    st.image(img_banner)

    st.write(f"""<h2>The Problem</h2>   
    <p>Access to clean water is a major challenge in Uppalapadu and similar regions globally, with dire consequences for health, including skin diseases due to contaminated water use. Ensuring water quality is vital for safe drinking, farming, and other activities. Traditional methods for water quality assessment are often costly, slow, and may not provide timely, accurate results. To combat this, our team has started working on a project to use machine learning to create an automated system for predicting water quality to address this problem.
</p> """, unsafe_allow_html=True)

    st.write(f"""<h2>Project goal</h2> <p>The principal objective of this project is to create a precise and effective machine learning model that can forecast water quality by considering various factors like turbidity, amount of organic carbon in ppm, amount of trihalomethanes in μg/L, and electrical conductivity of the water. The model is intended to generate water quality predictions and will be trained on a sizable dataset of historical data on water quality.
</p> """, unsafe_allow_html=True)




def model_section():
    st.write("""<h1>Predict Water Quality</h1>
    <p>Enter these values of the parameters to know if the water quality is suitable to drink or not.</p><hr>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        ColourTCU = st.number_input(label="Colour (TCU)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                    key="test_slider0")
        # TurbidityNTU = st.number_input(label="Turbidity (NTU)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
        #                                key="test_slider1")
        # pH = st.number_input(label="pH", min_value=0.0, max_value=1000.0, step=50.0, format="%f", key="test_slider2")
        ConductivityuS = st.number_input(label="Conductivity (uS/cm)", min_value=0.0, max_value=1000.0, step=50.0,
                                         format="%f", key="test_slider3")
        # TotalDissolvedSolids = st.number_input(label="Total Dissolved Solids (mg/l)", min_value=0.0, max_value=1000.0,
        #                                        step=50.0, format="%f", key="test_slider4")
        # TotalHardness = st.number_input(label="Total Hardness (mg/l as CaCO3)", min_value=0.0, max_value=1000.0,
                                        # step=50.0, format="%f", key="test_slider5")

    with col2:
        Aluminium = st.number_input(label="Aluminium (mg/l)", min_value=0.0, max_value=1000.5, step=50.1, format="%f",
                                    key="test_slider6")
        Chloride = st.number_input(label="Chloride (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                   key="test_slider7")
        # Iron = st.number_input(label="Iron (mg/l)", min_value=0.0, max_value=1000.5, step=50.1, format="%f",
        #                        key="test_slider8")
        # Sodium = st.number_input(label="Sodium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
        #                          key="test_slider9")
        # Sulphate = st.number_input(label="Sulphate (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
        #                            key="test_slider10")
        # Zinc = st.number_input(label="Zinc (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                            #    key="test_slider11")

    with col3:
        Magnesium = st.number_input(label="Magnesium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                    key="test_slider12")
        Calcium = st.number_input(label="Calcium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                  key="test_slider13")
        # Potassium = st.number_input(label="Potassium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
        #                             key="test_slider14")
        # Nitrate = st.number_input(label="Nitrate (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
        #                           key="test_slider15")
        # Phosphate = st.number_input(label="Phosphate (mg/l)", min_value=0.0, max_value=1000.2, step=50.1, format="%f",
        #                             key="test_slider16")
        st.write("<br>", unsafe_allow_html=True)
        predict_button = st.button('  Predict Water Quality  ')

    dataframe = pd.DataFrame({'Colour (TCU)': [ColourTCU], 'Turbidity (NTU)': [400], 'pH': [500],
                              'Conductivity (uS/cm)': [ConductivityuS],
                              'Total Dissolved Solids (mg/l)': [250],
                              'Total Hardness (mg/l as CaCO3)': [300], 'Aluminium (mg/l)': [Aluminium],
                              'Chloride (mg/l)': [Chloride], 'Total Iron (mg/l)': [200],
                              'Sodium (mg/l)': [550], 'Sulphate (mg/l)': [350], 'Zinc (mg/l)': [500],
                              'Magnesium (mg/l)': [Magnesium], 'Calcium (mg/l)': [Calcium],
                              'Potassium (mg/l)': [200], 'Nitrate (mg/l)': [300],
                              'Phosphate (mg/l)': [550]})

    if predict_button:
        model = load_model()
        result = model.predict(dataframe)
        for _ in stqdm(range(50)):
            sleep(0.015)
        if result[0] == 1.0:
            st.error("This Water Quality Bad")
        else:
            st.success('This Water Quality is Good')

def disease_detect(result_img, patient_name, patient_contact_number, doctor_name, doctor_contact_number, url):
  
  model_name = 'Model/best_model.h5'
  model = get_model()
  model.load_weights(model_name)
  classes = {4: ('nv', ' melanocytic nevi'), 6: ('mel', 'melanoma'), 2 :('bkl', 'benign keratosis-like lesions'), 1:('bcc' , ' basal cell carcinoma'), 5: ('vasc', ' pyogenic granulomas and hemorrhage'), 0: ('akiec', 'Actinic keratoses and intraepithelial carcinomae'),  3: ('df', 'dermatofibroma')}
  img = cv2.resize(result_img, (28, 28))
  result = model.predict(img.reshape(1, 28, 28, 3))
  result = result[0]
  max_prob = max(result)
  
  
  if max_prob>0.80:
    class_ind = list(result).index(max_prob)
    class_name = classes[class_ind]
    # short_name = class_name[0]
    full_name = class_name[1]
    print(full_name)
  else:
    full_name = 'No Disease' #if confidence is less than 80 percent then "No disease" 
  

  #whatsapp message
  message = '''
  Patient Name: {}
  Doctor Name: {}
  Disease Name : {}
  Confidence: {}

  '''.format(patient_name, doctor_name, full_name, max_prob)
  print(patient_contact_number)
  #send whatsapp mesage to patient
  print(url)
  whatsapp_message(token, account, patient_contact_number, message, url)
  print(doctor_contact_number)
  sleep(2)
  message = '''
  Patient Name: {}
  Paetient Contact Numbr: {}
  Doctor Name: {}
  Disease Name : {}
  Confidence: {}

  '''.format(patient_name, patient_contact_number,doctor_name, full_name, max_prob)
  whatsapp_message(token, account, doctor_contact_number, message, url)
  return 'Success'

  


def streamlit_form():
  st.write('<h1 style="margin-bottom: 25px">Skin Disease Detection</h1>', unsafe_allow_html=True)
  with st.form("boolq form"):
    label = 'choose a image file'
    uploaded_file = st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
    patient_name = st.text_input("Patient's Name")
    patient_contact_number = st.text_input("Patient's Contact Number")
    doctor_name = st.text_input("Doctor's Name")
    doctor_contact_number = st.text_input("Doctor's Contact Number")

    if st.form_submit_button("Get Answer"):
      input_validation(uploaded_file, patient_name, patient_contact_number, doctor_name, doctor_contact_number)


       
      file_name = uploaded_file.name
      file_extension = os.path.splitext(file_name)[1]

      if file_extension in ['.jpg', '.jpeg', '.png']:
        bytes_data = uploaded_file.getvalue()
        
        
        with open(f'test_images/temp{file_extension}', 'wb') as f:
          f.write(bytes_data)

        result_img = cv2.imread(f'test_images/temp{file_extension}')
        url = upload_image(f'test_images/temp{file_extension}')
        result = disease_detect(result_img, patient_name, patient_contact_number, doctor_name, doctor_contact_number, url)
        st.success(result)


        # st.write(type(base64_string))
        
      else:
        st.error('File must be one of .png, .jpg or .jpeg')
        st.stop()



def contributors_page():
    st.write("""
                <h1 style="text-align: center; color:#FFF6F4;">Our Team</h1><hr>
                <div style="text-align:center;">
                <br>
                <table>
                    <tbody>
                        <tr>
                            <th width="20%" style="font-size: 140%;" colspan="3">Contributors</th>
                        </tr>
                        <tr>
                            <td width="20%"> Dharani Mahesh Dadi</td>
                            <td width="20%"> 20BQ1A4213</td>
                            <td width="20%"> 9398241099</td>
                        </tr>
                        <tr>
                            <td>Hrudayesh Yaddala</td>
                            <td>20BQ1A4264</td>
                            <td>9381091871</td>
                        </tr>
                        <tr>
                            <td>Jashwanth Panitapu</td>
                            <td>20BQ1A4242</td>
                            <td> 8106501665</td>
                        </tr>
                        <tr>
                            <td>Mokshitha Kakarla</td>
                            <td>20BQ1A4225</td>
                            <td> 9014448207</td>
                        </tr>
                    </tbody>
                </table>
                </div>
            """, unsafe_allow_html=True)


with st.sidebar:
    st.image(img_rwanda)
    selected = option_menu(
        menu_title=None,
        options=["Home", "Check Water Quality", "Skin Diagnose","Contributors"],
        icons=["house", "droplet", "capsule","people"],
        styles=css_style
    )

if selected == "Home":
    home_page()

elif selected == "Check Water Quality":
    model_section()

elif selected == "Skin Diagnose":
   streamlit_form()

elif selected == "Contributors":
    contributors_page()

