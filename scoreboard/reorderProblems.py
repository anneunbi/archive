import json

with open("scoreboard.json", "r") as f:
    data = json.load(f)

all_problem_ids = set()
for row in data["rows"]:
    for problem in row.get("problems", []):
        all_problem_ids.add(problem["problem_id"])

problem_order = sorted(list(all_problem_ids))

for i, pid in enumerate(problem_order):
    print(f"{i+1}. {pid}")

for row in data["rows"]:
    prob_dict = {p["problem_id"]: p for p in row.get("problems", [])}
    row["problems"] = [prob_dict[pid] for pid in problem_order if pid in prob_dict]

with open("scoreboard.json", "w") as f:
    json.dump(data, f, indent=2)

print("Problems reordered alphabetically")