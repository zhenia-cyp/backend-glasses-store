class CustomTokenExceptionBase(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class CredentialsException(CustomTokenExceptionBase):
    pass

class TokenExpiredException(CustomTokenExceptionBase):
    pass