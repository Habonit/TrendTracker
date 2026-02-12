class AppError(Exception):
    """
    애플리케이션 전용 예외 클래스
    """
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)
