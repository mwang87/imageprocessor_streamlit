import os
import streamlit as st
from streamlit.components.v1 import html

import streamlit as st
from PIL import Image
import piexif
import base64
import io


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


def app():
    # Add a tracking token
    #html('<script async defer data-website-id="<your_website_id>" src="https://analytics.gnps2.org/umami.js"></script>', width=0, height=0)

    st.title('📷 Image Metadata Remover')
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg"])

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

            # We want to resize this as well for the web 1600 width and maintain aspect ratio
            st.write("size:", image.size)

            # Define the target width
            target_width = 1600

            # Get the original dimensions
            original_width, original_height = image_without_exif.size

            # Calculate the new height to maintain the aspect ratio
            aspect_ratio = original_height / original_width
            new_height = int(target_width * aspect_ratio)

            # Resize the image
            resized_image = image_without_exif.resize((target_width, new_height), Image.LANCZOS)
            
            with col2:
                st.image(resized_image, caption='Image without metadata and resized', use_column_width=True)

            if exif_dict is not None:
                st.success('Metadata has been removed successfully!')
            else:
                st.info('The image did not contain metadata.')

            # output filename
            output_filename = '{}_image_without_metadata.{}'.format(os.path.basename(uploaded_file.name), image.format.lower())

            st.markdown(get_image_download_link(resized_image, image.format, output_filename, 'Download image without metadata'), unsafe_allow_html=True)



def main():
    page_config()
    sidebar()
    app()


if __name__ == "__main__":
    main()