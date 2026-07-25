from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    password: str


STANDARD_USER = User("standard_user", "secret_sauce")
LOCKED_OUT_USER = User("locked_out_user", "secret_sauce")
PROBLEM_USER = User("problem_user", "secret_sauce")
PERFORMANCE_GLITCH_USER = User("performance_glitch_user", "secret_sauce")
ERROR_USER = User("error_user", "secret_sauce")
VISUAL_USER = User("visual_user", "secret_sauce")

INVALID_PASSWORD_USER = User("standard_user", "wrong_password")
UNKNOWN_USER = User("no_such_user", "secret_sauce")
