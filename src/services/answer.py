from .base import BaseService

class AnswerService(BaseService):
    def fetch_answers(self, question_id):
        response = self.get(self.wrap_url(f"answer/?question_id={question_id}"))
        return response.json()["data"]
    
    def create_answer(self, new_data, question_id):
        response = self.post(self.wrap_url("answer/"), json={
            "content": new_data.get('content'),
            "isResult": new_data.get('isResult'),
            "question": question_id
        })
        return response.json()

    def update_answer(self, answer_id, new_data, question_id):
        payload = {
            "content": new_data.get('content'),
            "isResult": new_data.get('isResult'),
            "question": question_id
        }
        response = self.put(self.wrap_url(f"answer/{answer_id}/"), json=payload)
        return response.json()

    def delete_answer(self, answer_id):
        response = self.delete(self.wrap_url(f"answer/{answer_id}"))
        return response.json()
