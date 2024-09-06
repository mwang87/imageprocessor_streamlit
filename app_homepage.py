import streamlit as st
from streamlit.components.v1 import html

import streamlit as st
from PIL import Image
import piexif
import base64
import io

# Add a tracking token
html('<script async defer data-website-id="<your_website_id>" src="https://analytics.gnps2.org/umami.js"></script>', width=0, height=0)

def get_image_download_link(img, img_format, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format=img_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/{img_format.lower()};base64,{img_str}" download="{filename}">{text}</a>'
    return href


def page_config():
    st.set_page_config(
        page_title="Image Metadata Remover",
        page_icon="📷",
        layout="wide"
    )

    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def sidebar():
    st.sidebar.markdown(
    """ 
    <a href="https://twitter.com/cameronjoejones" target="_blank" style="text-decoration: none;">
        <div style="display: flex; align-items: center;">
            <img src="https://abs.twimg.com/icons/apple-touch-icon-192x192.png" width="30" height="30">
            <span style="font-size: 16px; margin-left: 5px;">Follow me on Twitter</span>
        </div>
    </a>
    """, unsafe_allow_html=True
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """This is a simple web app to remove metadata from images.""")
    st.sidebar.title("How to use it?")
    st.sidebar.info(
        """1. Upload an JPG image
2. Click on the button to remove metadata.
3. The metadata and image will be displayed.
4. Download the image without metadata""")
    st.sidebar.title('Credits')
    st.sidebar.info('''
        This app was built by Cameron Jones''')


def app():
    st.title('📷 Image Metadata Remover')

    example_image = st.checkbox('Use Example Image')

    if example_image == False:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg"])

    elif example_image == True:
        uploaded_file = 'input/streamlit-picture.jpeg'

    button = st.button('Remove Metadata')

    if button:
        if uploaded_file is None:
            st.warning('Please upload an image first!')

        elif uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            exif_dict = None

            if "exif" in image.info:
                exif_dict = piexif.load(image.info["exif"])
                with col1:
                    st.write("Original Metadata:")
                    st.json(exif_dict)

            else:
                with col1:
                    st.write("No Metadata Found!")

            data = image.getdata()
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)

            with col2:
                st.image(image_without_exif, caption='Image without metadata', use_column_width=True)

            if exif_dict is not None:
                st.success('Metadata has been removed successfully!')
            else:
                st.info('The image did not contain metadata.')

            st.markdown(get_image_download_link(image_without_exif, image.format, 'image_without_metadata.' + image.format.lower(), 'Download image without metadata'), unsafe_allow_html=True)



def main():
    page_config()
    sidebar()
    app()


if __name__ == "__main__":
    main()