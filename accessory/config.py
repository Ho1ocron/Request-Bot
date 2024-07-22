class Token:
    def __init__(self) -> None:
        with open("config.cfg", "r+") as cfg_file:
            self.TOKEN = cfg_file.read().split("=")[1]

    def get_token(self) -> str:
        return self.TOKEN


if __name__ == "__main__":
    TOKEN = Token()