import stqdm
import pickle
import pandas as pd
from PIL import Image
from time import sleep
import streamlit as st
from stqdm import stqdm
from streamlit_option_menu import option_menu


@st.cache_resource
def load_model():
    with open('assets/model.pkl', 'rb') as f:
        model = pickle.load(f)
        # print(model.__dict__)
        return model


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
    <p>One of the biggest problems facing, Uppalapadu and many other places in the world is access to clean water. Predicting the quality of water is crucial to guaranteeing that there is clean, safe water available for drinking, farming, and other uses. However, conventional techniques for predicting the quality of water are frequently expensive and time-consuming, and they might not deliver correct information quickly. Our team has started working on a project to use machine learning to create an automated system for predicting water quality in order to address this problem.
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
        TurbidityNTU = st.number_input(label="Turbidity (NTU)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                       key="test_slider1")
        pH = st.number_input(label="pH", min_value=0.0, max_value=1000.0, step=50.0, format="%f", key="test_slider2")
        ConductivityuS = st.number_input(label="Conductivity (uS/cm)", min_value=0.0, max_value=1000.0, step=50.0,
                                         format="%f", key="test_slider3")
        TotalDissolvedSolids = st.number_input(label="Total Dissolved Solids (mg/l)", min_value=0.0, max_value=1000.0,
                                               step=50.0, format="%f", key="test_slider4")
        TotalHardness = st.number_input(label="Total Hardness (mg/l as CaCO3)", min_value=0.0, max_value=1000.0,
                                        step=50.0, format="%f", key="test_slider5")

    with col2:
        Aluminium = st.number_input(label="Aluminium (mg/l)", min_value=0.0, max_value=1000.5, step=50.1, format="%f",
                                    key="test_slider6")
        Chloride = st.number_input(label="Chloride (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                   key="test_slider7")
        Iron = st.number_input(label="Iron (mg/l)", min_value=0.0, max_value=1000.5, step=50.1, format="%f",
                               key="test_slider8")
        Sodium = st.number_input(label="Sodium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                 key="test_slider9")
        Sulphate = st.number_input(label="Sulphate (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                   key="test_slider10")
        Zinc = st.number_input(label="Zinc (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                               key="test_slider11")

    with col3:
        Magnesium = st.number_input(label="Magnesium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                    key="test_slider12")
        Calcium = st.number_input(label="Calcium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                  key="test_slider13")
        Potassium = st.number_input(label="Potassium (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                    key="test_slider14")
        Nitrate = st.number_input(label="Nitrate (mg/l)", min_value=0.0, max_value=1000.0, step=50.0, format="%f",
                                  key="test_slider15")
        Phosphate = st.number_input(label="Phosphate (mg/l)", min_value=0.0, max_value=1000.2, step=50.1, format="%f",
                                    key="test_slider16")
        st.write("<br>", unsafe_allow_html=True)
        predict_button = st.button('  Predict Water Quality  ')

    dataframe = pd.DataFrame({'Colour (TCU)': [ColourTCU], 'Turbidity (NTU)': [TurbidityNTU], 'pH': [pH],
                              'Conductivity (uS/cm)': [ConductivityuS],
                              'Total Dissolved Solids (mg/l)': [TotalDissolvedSolids],
                              'Total Hardness (mg/l as CaCO3)': [TotalHardness], 'Aluminium (mg/l)': [Aluminium],
                              'Chloride (mg/l)': [Chloride], 'Total Iron (mg/l)': [Iron],
                              'Sodium (mg/l)': [Sodium], 'Sulphate (mg/l)': [Sulphate], 'Zinc (mg/l)': [Zinc],
                              'Magnesium (mg/l)': [Magnesium], 'Calcium (mg/l)': [Calcium],
                              'Potassium (mg/l)': [Potassium], 'Nitrate (mg/l)': [Nitrate],
                              'Phosphate (mg/l)': [Phosphate]})

    if predict_button:
        model = load_model()
        result = model.predict(dataframe)
        for _ in stqdm(range(50)):
            sleep(0.015)
        if result[0] == 1.0:
            st.error("This Water Quality Bad")
        else:
            st.success('This Water Quality is Good')


def contributors_page():
    st.write("""
                <h1 style="text-align: center; color:#FFF6F4;">Our Team</h1><hr>
                <div style="text-align:center;">
                <br>
                <table>
                    <tbody>
                        <tr>
                            <th width="20%" style="font-size: 140%;" colspan="2">Contributors</th>
                        </tr>
                        <tr>
                            <td width="20%"> Dharani Mahesh Dadi</td>
                            <td width="20%"> 20BQ1A4213</td>
                        </tr>
                        <tr>
                            <td>Hrudayesh Yaddala</td>
                            <td>20BQ1A4264</td>
                        </tr>
                        <tr>
                            <td>Jashwanth Panitapu</td>
                            <td>20BQ1A4242</td>
                        </tr>
                        <tr>
                            <td>Mokshitha Kakarla</td>
                            <td>20BQ1A4225</td>
                        </tr>
                    </tbody>
                </table>
                </div>
                <hr>
            """, unsafe_allow_html=True)


with st.sidebar:
    st.image(img_rwanda)
    selected = option_menu(
        menu_title=None,
        options=["Home", "Check Water Quality","Contributors"],
        icons=["house", "droplet", "people"],
        styles=css_style
    )

if selected == "Home":
    home_page()

elif selected == "Check Water Quality":
    model_section()

elif selected == "Contributors":
    contributors_page()

