

from hashers import hashpw, chk_password

class HashingUltil:
    def hash(password):
        return hashpw(password, "bcrypt")
    def compare(hash_password, input_password):
        return chk_password(input_password, hash_password)