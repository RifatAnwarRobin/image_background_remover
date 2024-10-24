
__version__ = "009"
app_name = "Simple Image Processor (All in One)"

import streamlit as st

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

def ui_spacer(n=2, line=False, next_n=0):
	for _ in range(n):
		st.write('')
	if line:
		st.tabs([' '])
	for _ in range(next_n):
		st.write('')

def ui_info():
	st.markdown(f"""
	# Simple Image Processor (All in One) Using Python
	version {__version__}
	""")
	ui_spacer(1)
	st.markdown("""
		Feature List will be visible in future.
		""")
	ui_spacer(1)
	st.write("Made by [Rifat Anwar Robin](https://www.linkedin.com/in/rifat-anwar-robin/).", unsafe_allow_html=True)
	ui_spacer(1)
	st.markdown("""
		Thank you for your interest in my application.
		Please be aware that this is only a Proof of Concept system
		and may contain bugs or unfinished features.
		If you like this app you can ❤️ [follow me](https://www.linkedin.com/in/rifat-anwar-robin/)
		on Linkedin for news and updates.
	    You can also check other apps made by me on [Streamlit](https://share.streamlit.io/user/rifatanwarrobin).
		""")
	ui_spacer(1)
	st.markdown('Source code can be found [here](https://github.com/RifatAnwarRobin/image_background_remover).')
	
def show_sidebar():
    with st.sidebar:
        ui_info()