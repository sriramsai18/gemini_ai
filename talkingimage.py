import google.generativeai as genai
import os
from dotenv import load_dotenv,find_dotenv
import streamlit as st


def ask_and_get_answer(prompt,img):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([prompt,img])
    return response.text
def st_image_to_pil(st_img):
    import io
    from PIL import Image
    image_data=st_img.read()
    pil_image=Image.open(io.BytesIO(image_data))
    return pil_image

if __name__=='__main__':
    load_dotenv(find_dotenv(),override=True)
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    st.image('gemini.png')
    st.subheader('Talking with an Image')
    img=st.file_uploader("select an image:",type=["jpg","jpeg","png","gif"])
    if img:
        st.image(img,caption="talk with this image")
        prompt=st.text_area("ask a question about the image")
        if prompt:
            pil_image=st_image_to_pil(img)
            with st.spinner("Running:"):
                answer=ask_and_get_answer(prompt,pil_image)
                st.text_area("Gemini Answer:",value=answer)
            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history=''
            value=f'Q:{prompt} \n\n answer:{answer}'
            st.session_state.history=f'{value}\n\n  {"-"*100}  \n\n {st.session_state.history}'
            h=st.session_state.history
            st.text_area(label='chat_history',value=h,height=400,key="history")






