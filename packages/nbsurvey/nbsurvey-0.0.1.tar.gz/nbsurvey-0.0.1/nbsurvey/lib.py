from dataclasses import dataclass
import requests
from io import StringIO

@dataclass
class Form:
  id: int
  server: str = "http://localhost:8080"

  def csv(self) -> str:
    resp = requests.get(f"{self.server}/data?id={self.id}&csv")
    csv = resp.content.decode("utf-8")
    return StringIO(csv)