import base64
import requests
import google.generativeai as genai

class OpenAIAPI:
    """
    Kelas untuk berinteraksi dengan API OpenAI.
    """

    def __init__(self, api_key):
        """
        Inisialisasi kelas dengan kunci API.
        :param api_key: Kunci API OpenAI.
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.payload = None

    def encode_image(self, image_path):
        """
        Mengkodekan gambar menjadi string base64.
        :param image_path: Jalur ke gambar yang akan dikodekan.
        :return: String base64 dari gambar.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_payload(self, image_path, text_prompt, model="gpt-4o-mini", max_tokens=1000):
        """
        Menghasilkan payload untuk permintaan API OpenAI.
        :param image_path: Jalur ke gambar yang akan dikodekan.
        :param text_prompt: Teks permintaan dari pengguna.
        :param model: Model yang akan digunakan.
        :param max_tokens: Jumlah maksimum token dalam respons.
        """
        image_base64 = self.encode_image(image_path)
        self.payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": max_tokens
        }

    def get_response(self):
        """
        Mendapatkan respons dari API OpenAI.
        :return: Respons dari API OpenAI dalam format string.
        """
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=self.payload)
        result = response.json()
        return result["choices"][0]["message"]["content"]

class GeminiAPI:
    """
    Kelas untuk berinteraksi dengan API Google Gemini Vision.
    """

    def __init__(self, api_key):
        """
        Inisialisasi kelas dengan kunci API.
        :param api_key: Kunci API Google Gemini.
        """
        genai.configure(api_key=api_key)
        self.payload = None

    def upload_image(self, image_path, display_name):
        """
        Mengunggah gambar ke Google Gemini Vision.
        :param image_path: Jalur ke gambar yang akan diunggah.
        :param display_name: Nama yang akan ditampilkan untuk gambar yang diunggah.
        :return: Objek file yang diunggah.
        """
        return genai.upload_file(path=image_path, display_name=display_name)

    def generate_payload(self, image_path, text_prompt, model_name="gemini-1.5-pro"):
        """
        Menghasilkan payload untuk permintaan API Google Gemini Vision.
        :param image_path: Jalur ke gambar yang akan diunggah.
        :param text_prompt: Teks permintaan dari pengguna.
        :param model_name: Model yang akan digunakan.
        """
        uploaded_file = self.upload_image(image_path=image_path, display_name="Uploaded Image")
        model = genai.GenerativeModel(model_name=model_name)
        self.payload = model.generate_content([uploaded_file, text_prompt])

    def get_response(self):
        """
        Mendapatkan respons dari API Google Gemini Vision.
        :return: Respons dari API Google Gemini dalam format string.
        """
        return self.payload.text
