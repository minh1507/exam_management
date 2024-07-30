from .base import BaseService

class SubjectService(BaseService):
    def fetch_subjects(self):
        response = self.get(self.wrap_url("subject/"))
        return response.json()["data"]
    
    def create_subject(self, new_data):
        response = self.post(self.wrap_url("subject/"), json={
            "order": new_data.get('order'),
            "code": new_data.get('code'),
            "name": new_data.get('name')
        })
        return response.json()

    def update_subject(self, subject_id, new_data):
        payload = {
            "order": new_data.get('order'),
            "code": new_data.get('code'),
            "name": new_data.get('name')
        }
        response = self.put(self.wrap_url(f"subject/{subject_id}/"), json=payload)
        return response.json()

    def delete_subject(self, subject_id):
        response = self.delete(self.wrap_url(f"subject/{subject_id}"))
        return response.json()
