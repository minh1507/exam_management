class StringHelper:
    def parse_question_mark(mark):
        try:
            float_value = float(mark)
            if float_value.is_integer():
                return int(float_value) 
            else:
                return float_value 
        except ValueError:
            raise ValueError("Input cannot be converted to a number.")