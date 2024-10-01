from rembg import remove
from PIL import Image
import streamlit as st
import io
from timeit import default_timer as timer

def add_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>By Rifat Anwar Robin - © 2024</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

def remove_img_background(processed_image,alpha_matting=False, alpha_matting_foreground_threshold=None, 
                          alpha_matting_background_threshold=None, alpha_matting_erode_size=None,only_mask=False,post_process_mask=False,bgcolor=None):
    # Remove the background from the image
    st.write("Removing Background...")
    bg_color_val = hex_to_rgba(bgcolor) if use_bgcolor else None
    output_image=remove(processed_image,
                        alpha_matting=alpha_matting,
                        alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                        alpha_matting_background_threshold=alpha_matting_background_threshold,
                        alpha_matting_erode_size=alpha_matting_erode_size,
                        only_mask=only_mask,
                        post_process_mask=post_process_mask,
                        bgcolor=bg_color_val)
    
    st.image(output_image,output_format='png')
    return output_image

def download_bg_removed_image(output_image,input_image):
    output_image_buffer=io.BytesIO()
    output_image.save(output_image_buffer, format='png')
    output_image_buffer.seek(0)
    st.download_button(
        label="Download",
        data=output_image_buffer,
        file_name=f"{inp_image.name}_removed.png",
        mime=f"image/png",
    )

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b, 255)

st.title("Image Backgroud Remover using [PYTHON X Streamlit X Pillow]")

inp_image=st.file_uploader(label="Upload an image file with jpg formate.",type=['jpeg','jpg'])
if inp_image is not None:
    resize_by = st.slider("Resize Width and Height By:", 1, 50, 1, 1)
    # 1: This is the minimum value of the slider, which is set to 1.
    # 50: This is the maximum value of the slider, which is set to 50.
    # 1: This is the initial value of the slider, which is set to 1.
    # 1: This is the step size, which determines the increments/decrements of the slider value. In this case, it's set to 1, meaning the slider will move in increments of 1.
    # With this code, the slider will have a range from 1 to 50, and the user can select any value within that range.

    before_resized_image=Image.open(inp_image)
    w,h=before_resized_image.size

    resized_image=before_resized_image.resize((int(w/resize_by),int(h/resize_by)))
    rw,rh=resized_image.size

    st.write(f"Input Image Size Preview [width={w},height={h}].\nNow Previewing [width={rw},height={rh}]")
    st.image(resized_image,output_format='auto')

    # Additional options for background removal
    st.write("Advanced Options for Background Removal")
    alpha_matting = st.checkbox("Use Alpha Matting", value=False)
    only_mask = st.checkbox("Only Mask", value=False)
    post_process_mask = st.checkbox("Post Process Mask", value=False)

    use_bgcolor = st.checkbox("Use selected background color instead of transparency", value=False)
    if use_bgcolor:
        bgcolor = st.color_picker("Pick a Background Color (Optional)", "#ffffff")
    else:
        bgcolor = None
    
    # Show sliders only if alpha_matting is enabled
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

    if st.button("Remove Background"):
        start_time = timer()
        output_image=remove_img_background(before_resized_image,
                                        alpha_matting=alpha_matting,
                                        alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                                        alpha_matting_background_threshold=alpha_matting_background_threshold,
                                        alpha_matting_erode_size=alpha_matting_erode_size,
                                        only_mask=only_mask,
                                        post_process_mask=post_process_mask,
                                        bgcolor=bgcolor)
        end_time = timer()
        execution_time = end_time - start_time
        st.write(f"Background removal took: {execution_time:.4f} seconds")

        if output_image:
            download_bg_removed_image(output_image,inp_image)

add_footer()


