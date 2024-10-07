from rembg import remove
from PIL import Image
import streamlit as st
import io
from timeit import default_timer as timer

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile
    
import ui

def remove_img_background(processed_image, alpha_matting=False, alpha_matting_foreground_threshold=None, 
                          alpha_matting_background_threshold=None, alpha_matting_erode_size=None, only_mask=False, post_process_mask=False, bgcolor=None):
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

def download_zip(images_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, image in images_dict.items():
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            zip_file.writestr(f"{filename}_removed.png", img_byte_arr.getvalue())
    zip_buffer.seek(0)
    st.download_button(
        label="Download as ZIP",
        data=zip_buffer,
        file_name="background_removed_images.zip",
        mime="application/zip"
    )

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b, 255)

st.title("Image Background Remover [Python + Streamlit + Pillow]")
ui.show_sidebar()
#Container for Image Upload & Preview
with st.container():
    st.subheader("Upload Images")
    inp_images = st.file_uploader(label="Upload image files in JPG format", type=['jpeg', 'jpg'], accept_multiple_files=True)
    
    # Display input images in a grid
    if inp_images is not None:
        st.write("### Uploaded Images:")
        cols = st.columns(3)  # 3 columns for grid

        for idx, inp_image in enumerate(inp_images):
            before_resized_image = Image.open(inp_image)
            w, h = before_resized_image.size
            with cols[idx % 3]:
                st.image(before_resized_image, caption=f"Original Image ({w}x{h}px)", use_column_width=True)

# Control Panel for Advanced Options
if inp_images is not None:
    with st.container():
        st.subheader("Background Removal Options")

        # resize_by = st.slider("Resize Width and Height By:", 1, 50, 1, 1)
        # 1: This is the minimum value of the slider, which is set to 1.
        # 50: This is the maximum value of the slider, which is set to 50.
        # 1: This is the initial value of the slider, which is set to 1.
        # 1: This is the step size, which determines the increments/decrements of the slider value. In this case, it's set to 1, meaning the slider will move in increments of 1.
        # With this code, the slider will have a range from 1 to 50, and the user can select any value within that range.

        alpha_matting = st.checkbox("Use Alpha Matting", value=False)
        only_mask = st.checkbox("Only Mask", value=False)
        post_process_mask = st.checkbox("Post Process Mask", value=False)

        use_bgcolor = st.checkbox("Use selected background color instead of transparency", value=False)
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

# Process & Display Output Images
if inp_images is not None and st.button("Remove Background"):
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
        download_zip(images_dict)


