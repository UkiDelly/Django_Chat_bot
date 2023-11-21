from dataclasses import dataclass


@dataclass
class Token:
    access_token: str
    refresh_token: str


if __name__ == '__main__':
    token = Token("access_token", "refresh_token")

    print(token.__dict__)
