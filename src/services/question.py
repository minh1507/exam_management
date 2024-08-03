from .base import BaseService
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QBuffer, QIODevice
import io

class QuestionService(BaseService):
    def fetch_questions(self):
        response = self.get(self.wrap_url("question/"))
        return response.json()["data"]
    
    def create_question(self, new_data):
        image_pixmap = new_data.get('image')
        if isinstance(image_pixmap, QPixmap):
            image_buffer = QBuffer()
            image_buffer.open(QIODevice.ReadWrite) 

            format = 'PNG'  
            image_pixmap.save(image_buffer, format=format)
            image_buffer.seek(0)

            mime_type = f'image/{format.lower()}'
        else:
            raise ValueError("Provided image is not a QPixmap object")
        
        files = {
            'file': ('image.png', image_buffer.data(), mime_type)
        }

        image_response = self.post(self.wrap_url("image/"), files=files)
        response = self.post(self.wrap_url("question/"), json={
            "lecturer": new_data.get('lecturer'),
            "content": new_data.get('content'),
            "mark": new_data.get('mark'),
            "unit": new_data.get('unit'),
            "subject": new_data.get('subject'),
            "mixChoices": new_data.get('mixChoices'),
            "image": image_response.json()["data"]["id"]
        })

        return response.json()

    def update_question(self, question_id, new_data, file):
        payload = {
            "lecturer": new_data.get('lecturer'),
            "content": new_data.get('content'),
            "mark": new_data.get('mark'),
            "unit": new_data.get('unit'),
            "subject": new_data.get('subject'),
            "mixChoices": new_data.get('mixChoices'),
            "image": file
        }
        response = self.put(self.wrap_url(f"question/{question_id}/"), json=payload)
        return response.json()

    def delete_question(self, question_id):
        response = self.delete(self.wrap_url(f"question/{question_id}"))
        return response.json()
