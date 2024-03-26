import os


class Environment:
    @staticmethod
    def is_development() -> bool:
        return os.getenv("ENVIRONMENT") == "development"

    @staticmethod
    def is_production() -> bool:
        return os.getenv("ENVIRONMENT") == "production"
