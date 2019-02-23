class JsonBuilder:

    def build(self, success, message):
        json_resp = {
            'success': success,
            'message': message
        }

        return json_resp