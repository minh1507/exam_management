from .base import BaseService
import io
from PIL import Image

class ImportService(BaseService):
    def import_question(self, new_data):
        for item in new_data:
            pil_image = item['image']
                
            if not isinstance(pil_image, Image.Image):
                print(f"Expected PIL.Image object but got {type(pil_image)}")
                continue
                
            image_buffer = io.BytesIO()
            pil_image.save(image_buffer, format='PNG')
            image_buffer.seek(0)
            files = {
                'file': ('image.png', image_buffer, 'image/png')
            }

            subjects = (self.get(self.wrap_url("subject/"))).json()['data']
            id_subject = next((subject['id'] for subject in subjects if subject['name'] == item["subject"]), None)
            image_response = self.post(self.wrap_url("image/"), files=files)
            image_data = image_response.json().get("data", {})
            image_id = image_data.get("id", None)
            if image_id is None:
                print("Failed to get image ID from response")
                continue

            result_question = self.post(self.wrap_url("question/"), json={
                "lecturer": item["lecturer"],
                "content": item["content"],
                "mark": item["mark"],
                "unit": item["unit"],
                "subject": id_subject,
                "mixChoices": item["mixChoice"],
                "image": image_id
            })            

            question_id = result_question.json()["data"]
            for answer in item['answers']:
                self.post(self.wrap_url("answer/"), json={
                    "content": answer.get('content'),
                    "isResult": answer.get('isResult'),
                    "question": question_id
                })

        return 1
