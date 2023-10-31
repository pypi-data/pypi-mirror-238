class ModelNotFoundException(Exception):
    def __init__(self, model_id):
        self.model_id = model_id
        super().__init__(f"Model with ID {model_id} not found")


class APIException(Exception):
    """Exception raised for API errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
