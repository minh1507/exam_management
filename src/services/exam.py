from .base import BaseService

class ExamService(BaseService):
    def fetch_exams(self):
        response = self.get(self.wrap_url("exam/"))
        return response.json()["data"]
    
    def create_exam(self, new_data):
        response = self.post(self.wrap_url("exam/"), json={
            "supervisor": new_data.get('supervisor'),
            "code": new_data.get('code'),
            "start_time": new_data.get('start_time'),
            "expired_time": new_data.get('expired_time'),
            "total_question": new_data.get('total_question'),
            "subject": new_data.get('subject'),
        })
        return response.json()

    def delete_exam(self, exam_id):
        response = self.delete(self.wrap_url(f"exam/{exam_id}"))
        return response.json()
