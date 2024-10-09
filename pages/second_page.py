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

    st.title('📷 Image Stitcher')
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    button = st.button('stitch together')

    if button:
        if uploaded_file is None:
            st.warning('Please upload an image first!')

        # iterate through all the image files, figuring out the dimensions
        elif uploaded_file is not None:
            # we want to find the smallest height
            min_height = 10000000000
            all_images = []
            for image in uploaded_file:
                image = Image.open(image)
                
                min_height = min(min_height, image.size[1])

                all_images.append(image)

            # Let's resize each image to the min_height while maintaining the aspect ratio
            resized_images = []

            for image in all_images:
                width, height = image.size
                aspect_ratio = width / height
                new_width = int(min_height * aspect_ratio)
                
                # Resize the image
                resized_image = image.resize((new_width, min_height))
                resized_images.append(resized_image)

            # Stitch images together side by side
            total_width = sum(image.size[0] for image in resized_images)
            stitched_image = Image.new('RGB', (total_width, min_height))

            x_offset = 0
            for image in resized_images:
                stitched_image.paste(image, (x_offset, 0))
                x_offset += image.size[0]

            # output filename
            output_filename = 'stitched.jpg'

            st.markdown(get_image_download_link(stitched_image, "JPEG", output_filename, 'Download Stitched'), unsafe_allow_html=True)


def main():
    page_config()
    sidebar()
    app()


if __name__ == "__main__":
    main()