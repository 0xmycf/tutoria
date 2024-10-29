
from collections import defaultdict
import  os, sys,  json
import os.path as path
import shutil
from dataclasses import dataclass
from pathlib import Path

def get_data_home():
    """
    Gets the xdg data home directory.
    """
    if value := os.getenv("XDG_DATA_HOME"):
        return Path(value)
    return Path.home() / ".local" / "share"

@dataclass
class Person:
    name: str

@dataclass
class Task:
    task_name: str
    score: int

class Sheet:
    def __init__(self) -> None:
        self.data = {
                # dict of str (person's name) dict of str (task_name) and int (score)
                "name": defaultdict(dict),
                }

    def add_task(self, person: Person, task: Task):
        self.data["name"][person.name][task.task_name] = task.score

    def person(self, name: str):
        return self.data["name"][name] # TODO make pretty

    def from_file(self, file: Path):
        if not file.exists():
            return self

        with open(file, "r") as io:
            self.data = json.load(io)
        return self

def main():
    data = get_data_home() / "tutoria"
    if not path.exists(data):
        os.makedirs(data)
    
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == "delete":
        confirm = input("Are you sure you want to delete the sheet? [type anything to confirm]: ")
        if confirm:
            os.remove(data / "sheet.json")
        else:
            print("Sheet not deleted")
        return

    if not args:
        print("Please provide a command")
        sys.exit(1)

    sheet = Sheet().from_file(data / "sheet.json")

    if args[0] == "keys":
        for i, key in enumerate(sheet.data["name"].keys()):
            print(f"{i+1}: ", key)
        return

    if args[0] == "read":
        if len(args) == 2:
            data = sheet.person(args[1])
            max_len = max(len(k) for k in data.keys())
            for k,v in data.items():
                print(f"{k:<{max_len}}: {v}")
        else:
            print(sheet.data)
        return

    topic, score = args[1].split(":")
    sheet.add_task(Person(args[0]), Task(topic, int(score)))

    if path.exists(data / "sheet.json"):
        shutil.copy(data / "sheet.json", data / "sheet.json.bak")

    with open(data / "sheet.json", "w") as io:
        json.dump(sheet.data, io)

if __name__ == '__main__':
    main() 

