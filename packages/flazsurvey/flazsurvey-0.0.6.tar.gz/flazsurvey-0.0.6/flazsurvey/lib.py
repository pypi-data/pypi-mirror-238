from dataclasses import dataclass
import requests
from io import StringIO
import json

@dataclass
class ABQuestion:
  id: int
  question: str
  a: str = "a"
  b: str = "b"

@dataclass
class TextInputQuestion:
  id: int
  question: str
  pattern: str = ""

@dataclass
class Form:
  id: str
  token: str
  server: str = "http://localhost:8080"

  def csv(self) -> str:
    resp = requests.get(f"{self.server}/data?id={self.id}&csv", headers={"Authorization": f"Bearer {self.token}"})
    csv = resp.content.decode("utf-8")
    return StringIO(csv)
  
  def questions(self) -> list[ABQuestion]:
    resp = requests.get(f"{self.server}/form?id={self.id}", headers={"Authorization": f"Bearer {self.token}"})
    raw = resp.content.decode("utf-8")
    data = json.loads(raw)

    questions = []

    for q in data["questions"]:
      match q["type"]:
        case "ab-question":
          config = q["config"]
          questions.append(ABQuestion(q["id"], config["question"], config["a"], config["b"]))
        case _:
          pass
    return questions