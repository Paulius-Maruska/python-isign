from .base import Base


class Response(Base):
    @property
    def status(self) -> str:
        return str(self.raw["status"])
