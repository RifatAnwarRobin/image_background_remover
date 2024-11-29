from rembg import remove
from PIL import Image
import streamlit as st
import io
from timeit import default_timer as timer
import zipfile36 as zipfile

import ui

def remove_img_background(processed_image, alpha_matting=False,
                          alpha_matting_foreground_threshold=None, 
                          alpha_matting_background_threshold=None,
                          alpha_matting_erode_size=None,
                          only_mask=False,
                          post_process_mask=False,
                          bgcolor=None):
    bg_color_val = hex_to_rgba(bgcolor) if bgcolor else None
    output_image = remove(processed_image,
                          alpha_matting=alpha_matting,
                          alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                          alpha_matting_background_threshold=alpha_matting_background_threshold,
                          alpha_matting_erode_size=alpha_matting_erode_size,
                          only_mask=only_mask,
                          post_process_mask=post_process_mask,
                          bgcolor=bg_color_val)
    
    return output_image

def custom_image_resizer(width_input,
                         height_input,
                         selected_filter,
                         original_w,
                         original_h):
    if height_input>50 and width_input>50:
        height_input = height_input
        width_input = width_input
    elif width_input and height_input==50:
        aspect_ratio = original_h / original_w
        height_input = int(width_input * aspect_ratio) 
    elif height_input and width_input==50:
        aspect_ratio = original_w / original_h
        width_input = int(height_input * aspect_ratio)
    else:
        width_input=original_w
        height_input=original_h

    resized_image=before_resized_image.resize((int(width_input), int(height_input)),resample=selected_filter)
    if resized_image.mode == 'CMYK':
        resized_image = resized_image.convert('RGB')

    resizer_value={
        'width_input':width_input,
        'height_input':height_input,
        'resized_image':resized_image
    }
    return resizer_value

def custom_image_position_switcher(image,selected_transpose):
    if selected_transpose:
        flipped_image=image.transpose(selected_transpose)
        if flipped_image.mode == 'CMYK':
            flipped_image = flipped_image.convert('RGB')

        flipped_data={
            'selected_transpose':selected_transpose,
            'flipped_image':flipped_image
        }
        return flipped_data
    


def download_zip(images_dict,selected_option=False,file_name=False):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image in images_dict.items():
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            zip_file.writestr(f"{filename}_removed.png", img_byte_arr.getvalue())
    zip_buffer.seek(0)
    print(f"{file_name}")
    st.download_button(
        label="Download as PNG ZIP",
        data=zip_buffer,
        file_name=f"{file_name}.zip" if file_name!=False else f"bg_removed_by_removebg-by-rifat.streamlit.app.zip",
        mime="application/zip"
    )

def download_as_jpeg_zip(images_dict,selected_option=False,file_name=False):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image in images_dict.items():
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            zip_file.writestr(f"{filename}_removed.jpeg", img_byte_arr.getvalue())
    zip_buffer.seek(0)
    print(f"{file_name}")
    st.download_button(
        label="Download as JPEG ZIP",
        data=zip_buffer,
        file_name=f"{file_name}.zip" if file_name!=False else f"bg_removed_by_removebg-by-rifat.streamlit.app.zip",
        mime="application/zip"
    )

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b, 255)

st.title("Image Processor [Python + Streamlit + Pillow]")
ui.show_sidebar()

#Container for Image Upload & Preview
with st.container():
    st.subheader("Upload Images")
    inp_images = st.file_uploader(label="Upload image files in JPG format", type=['jpeg', 'jpg', 'png','avif','webp'], accept_multiple_files=True)
    
    # Display input images in a grid
    if inp_images is not None:
        st.write("### Uploaded Images:")
        cols = st.columns(3)  # 3 columns for grid

        for idx, inp_image in enumerate(inp_images):
            before_resized_image = Image.open(inp_image)
            w, h = before_resized_image.size
            with cols[idx % 3]:
                st.image(before_resized_image, caption=f"Original Image ({w}x{h} px)", use_column_width=True)

operation_mode = st.radio(
    "Choose A Mode Please:",
    ('Want to Remove Background (default)', 'Resize Images','Flip Images'),
    index=0  # Default selection: Want to Remove Background
)
# Control Panel for Advanced Options
if inp_images is not None and operation_mode not in ['Resize Images','Flip Images']:
    with st.container():
        st.subheader("Background Removal Options")

        alpha_matting = st.checkbox("Use Alpha Matting", value=False)
        only_mask = st.checkbox("Only Mask", value=False)
        post_process_mask = st.checkbox("Post Process Mask", value=False)

        use_bgcolor = st.checkbox("Use background color instead of transparency", value=False)
        if use_bgcolor:
            bgcolor = st.color_picker("Pick a Background Color (Optional)", "#ffffff")
        else:
            bgcolor = None

        if alpha_matting:
            alpha_matting_foreground_threshold = st.slider(
                "Alpha Matting Foreground Threshold", 0, 255, 240
            )
            alpha_matting_background_threshold = st.slider(
                "Alpha Matting Background Threshold", 0, 255, 10
            )
            alpha_matting_erode_size = st.slider(
                "Alpha Matting Erode Size", 0, 30, 10
            )
        else:
            alpha_matting_foreground_threshold = None
            alpha_matting_background_threshold = None
            alpha_matting_erode_size = None

if inp_images and operation_mode not in ['Resize Images','Flip Images'] and st.button("Remove Background",type='primary'):
    with st.container():
        st.subheader("Output Images with Background Removed")
        cols = st.columns(3)
        images_dict = {}

        for idx, inp_image in enumerate(inp_images):
            before_resized_image = Image.open(inp_image)
            w, h = before_resized_image.size
            # resized_image = before_resized_image.resize((int(w / resize_by), int(h / resize_by)))
            
            output_image = remove_img_background(before_resized_image,
                                                alpha_matting=alpha_matting,
                                                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                                                alpha_matting_background_threshold=alpha_matting_background_threshold,
                                                alpha_matting_erode_size=alpha_matting_erode_size,
                                                only_mask=only_mask,
                                                post_process_mask=post_process_mask,
                                                bgcolor=bgcolor)

            if output_image:
                images_dict[inp_image.name] = output_image

            # Display output images in a grid
            rw, rh = before_resized_image.size
            with cols[idx % 3]:
                st.image(output_image, caption=f"Output Image ({rw}x{rh}px)", use_column_width=True)

    #Download option for processed images
    if images_dict:
        download_zip(images_dict,selected_option=False,file_name=False)
        download_as_jpeg_zip(images_dict,selected_option=False,file_name=False)
    

if inp_images is not None and operation_mode=='Resize Images':
    # resize_by = st.slider("Resize Width and Height By:", 1, 50, 1, 1)
    # 1: This is the minimum value of the slider, which is set to 1.
    # 50: This is the maximum value of the slider, which is set to 50.
    # 1: This is the initial value of the slider, which is set to 1.
    # 1: This is the step size, which determines the increments/decrements of the slider value. In this case, it's set to 1, meaning the slider will move in increments of 1.
    # With this code, the slider will have a range from 1 to 50, and the user can select any value within that range.

    # Input fields for width and height in pixels
    width_input = st.number_input("Width (px):", min_value=49, value=50)
    height_input = st.number_input("Height (px):", min_value=49, value=50)

    resampling_filters = {
        "Nearest": Image.NEAREST,
        "Box": Image.BOX,
        "Bilinear": Image.BILINEAR,
        "Hamming": Image.HAMMING,
        "Bicubic": Image.BICUBIC,
        "Lanczos": Image.LANCZOS,
    }
    selected_filter_name = st.selectbox("Select Resampling Filter:", list(resampling_filters.keys()))
    selected_filter = resampling_filters[selected_filter_name]
    
    custom_file_name=st.text_input("Enter Filename: ")

    if inp_images and st.button("Resize",type='primary'):
        with st.container():
            st.subheader("Resized Images")
            cols = st.columns(3)
            images_dict = {}
            for idx, inp_image in enumerate(inp_images):
                before_resized_image = Image.open(inp_image)
                original_w, original_h = before_resized_image.size

                resized_data=custom_image_resizer(width_input,height_input,selected_filter,original_w,original_h)
                print(f"{resized_data}")
                resized_output_image = resized_data['resized_image']

                if resized_output_image:
                    images_dict[inp_image.name] = resized_output_image

                with cols[idx % 3]:
                    st.image(resized_output_image, caption=f"Resized Image({resized_data['width_input']}x{resized_data['height_input']}px)", use_column_width=True)

        #Download option for processed images
        if images_dict:
            print(f"Main Filename: {custom_file_name}")
            if not custom_file_name:
                    custom_file_name = f"Resized_images-by-rifat.streamlit.app-[{selected_filter_name}]"
            download_zip(images_dict,selected_option=selected_filter_name,file_name=custom_file_name)
            download_as_jpeg_zip(images_dict,selected_option=selected_filter_name,file_name=custom_file_name)

if inp_images is not None and operation_mode=='Flip Images':
    transpose_filters = {
        "Horizontal": Image.FLIP_LEFT_RIGHT,
        "Virtical": Image.FLIP_TOP_BOTTOM,
        "Rotate 90 deg": Image.ROTATE_90,
        "Rotate 180 deg": Image.ROTATE_180,
        "Rotate 270 deg": Image.ROTATE_270,
    }
    selected_transpose_name = st.selectbox("Select Image Rotation:", list(transpose_filters.keys()))
    selected_transpose = transpose_filters[selected_transpose_name]
    
    custom_file_name=st.text_input("Enter Filename: ")

    if inp_images and st.button("Switch Position",type='primary'):
        with st.container():
            st.subheader("Flip Images")
            cols = st.columns(3)
            images_dict = {}
            for idx, inp_image in enumerate(inp_images):
                before_flipped_image = Image.open(inp_image)
                original_w, original_h = before_flipped_image.size

                # flipped_data=custom_image_position_switcher(before_flipped_image,selected_transpose)
                flipped_data=before_flipped_image.transpose(selected_transpose)
                print(f"{flipped_data}")
                flipped_output_image = flipped_data

                if flipped_output_image:
                    images_dict[inp_image.name] = flipped_output_image

                with cols[idx % 3]:
                    st.image(flipped_output_image, caption=f"Flipped Image based on {selected_transpose_name}", use_column_width=True)

        #Download option for processed images
        if images_dict:
            print(f"Main Filename: {custom_file_name}")
            if not custom_file_name:
                    custom_file_name = f"Flipped_images-by-rifat.streamlit.app-[{selected_transpose_name}]"
            download_zip(images_dict,selected_option=selected_transpose_name,file_name=custom_file_name)
            download_as_jpeg_zip(images_dict,selected_option=selected_transpose_name,file_name=custom_file_name)