from typing import Any, Dict, Optional, Sequence


class ISignFieldErrorInfo:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def error_code(self) -> int:
        return int(self.data["error_code"])

    @property
    def message(self) -> str:
        return str(self.data["message"])

    @property
    def field(self) -> str:
        return str(self.data["field"])

    def __str__(self) -> str:
        return f"{self.error_code}: {self.field}: {self.message}"


class ISignError(Exception):
    def __init__(self, method: str, url: str, status_code: int, response: Dict, request: Optional[Dict] = None) -> None:
        super(ISignError, self).__init__()
        self.method = method
        self.url = url
        self.status_code = status_code
        self.response = response
        self.request = request

    @property
    def status(self) -> str:
        return str(self.response["status"])

    @property
    def error_code(self) -> int:
        return int(self.response["error_code"])

    @property
    def message(self) -> str:
        return str(self.response["message"])

    @property
    def errors(self) -> Sequence[ISignFieldErrorInfo]:
        errors = self.response.get("errors", None)
        if not errors:
            return []
        return [ISignFieldErrorInfo(err) for err in errors]

    def __str__(self) -> str:
        result = f"ISignError: {self.method} {self.url}: {self.error_code}: {self.message}"
        errors = "\n".join([f"  {err}" for err in self.errors])
        if errors:
            result += f": [\n{errors}\n]"
        return result
