import json

#exception model
class InvalidModelException(Exception):
    "Raised when valuemodel is None"
    def __init__(self, missing_key=None, msg=None):
        if missing_key:
            super().__init__(f"Error Ocurrido, Mensaje: missing attr - {missing_key}")
        elif msg:
            super().__init__(f"Error Ocurrido, Mensaje: {msg}")
        else:
            super().__init__(f"Error Ocurrido, Mensaje: Invalid model configuration")

class InvalidTrainModelException(Exception):
    def __init__(self, group_model=None, class_model=None, msg=None):
        if group_model:
            super().__init__(f"Error Ocurrido - [Train], Mensaje: Clustering training model returned with the following error - {msg}")
        elif class_model:
            super().__init__(f"Error Ocurrido - [Train], Mensaje: Classification training model returned with the following error - {msg}")
        else:
            super().__init__(f"Error Ocurrido, Mensaje: Model cannot be trained; check the sent configuration")

#transfer signmodel intermediary
class SignModel:
    def validate_info_system(self, configuration=None):
        if configuration is not None:
            required_keys = ['label', 'hands_relation', 'face_relation', 'body_relation', 'move_relation']
            missing_keys = [key for key in required_keys if key not in configuration]

            if len(missing_keys)>0:
                raise InvalidModelException(missing_key=missing_keys)
        else:
            raise InvalidModelException()

    def validate_info_fromJson(self, json_data: str):
        try:
            json_object = json.loads(json_data)
            required_keys = ['data', 'configuration']
            if all(key in json_object for key in required_keys):
                config_keys = ['label', 'hands_relation', 'face_relation', 'body_relation', 'move_relation']
                missing_keys = [key for key in config_keys if key not in json_object['configuration']]
    
                if len(missing_keys)>0:
                    raise InvalidModelException(missing_key=missing_keys)
            else:
                raise InvalidModelException(required_keys)
        except Exception as e:
            raise InvalidModelException(msg=str(e))