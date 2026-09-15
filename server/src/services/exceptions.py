class ServiceError(Exception):
    status_code: int = 400
    reason: str = "service_error"

    def __init__(self, reason: str | None = None) -> None:
        if reason is not None:
            self.reason = reason
        super().__init__(self.reason)


class ConflictError(ServiceError):
    status_code = 409
    reason = "conflict"


class UnauthorizedError(ServiceError):
    status_code = 401
    reason = "unauthorized"
