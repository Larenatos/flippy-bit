import json

with open("highscore.json", "x") as file:
  highest_score = {"highscore": 0}
  json.dump(highest_score, file)