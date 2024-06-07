import streamlit as st
from PIL import Image
import base64
import requests
import json
from utils.config import OPENAI_API_TOKEN


# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to use OpenAI API for image and text analysis
def analyze_image_with_openai(image_path):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_TOKEN}",
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "If the image is receipt please return the response in the following JSON format: {'items': [{'name': 'item1', 'quantity': 'qty1', 'price': 'price1'}, ...], 'total': 'total_amount'} if not return null",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    return response.json()


# Streamlit app setup
st.header("Deteksi Dan Kategorisasi Item Struk")
st.text("Masukkan Struk Dan AI Akan Mendeteksi Dan Kategorisasi Secara Otomatis!")

if img_file := st.sidebar.file_uploader(
    label="Upload Struk Belanja", type=["png", "jpg", "jpeg"]
):
    img = Image.open(img_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Save the uploaded image temporarily
    img_path = "temp_image.png"
    img.save(img_path)

    # Use OpenAI API to analyze the image
    analysis_result = analyze_image_with_openai(img_path)

    st.subheader("Hasil Pengkategorisasian:")
    st.text(analysis_result)

    if analysis_result is not None:
        try:
            result = analysis_result["choices"][0]["message"]["content"]
            
            if result != "null":
                items = result["items"]
                total = result["total"]

                st.subheader("Extracted Items:")
                for item in items:
                    st.text(
                        f"Item: {item['name']}, Quantity: {item['quantity']}, Price: {item['price']}"
                    )

                st.subheader("Total:")
                st.text(total or "Total Harga Tidak Ditemukan")
            else:
                st.error("Silahkan Memasukkan Foto Struk Yang Benar.")
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse the analysis result. Error: {str(e)}")
    else:
        st.error("Failed to receive a valid response from the OpenAI API.")
