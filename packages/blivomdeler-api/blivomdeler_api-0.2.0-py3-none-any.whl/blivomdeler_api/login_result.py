from dataclasses import dataclass


@dataclass(frozen=True)
class LoginResult:
    user: str
    password: str
    worker_type: str
