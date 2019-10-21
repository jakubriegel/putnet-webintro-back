from flask.json import JSONEncoder


class Student:
    next_id = 1

    def __init__(self, name: str, year: int) -> None:
        self.name: str = name
        self.year: int = year

        self.id: int = Student.next_id
        Student.next_id += 1


class StudentJSONEncoder(JSONEncoder):
    def default(self, obj) -> dict:
        if isinstance(obj, Student):
            return {
                "id": obj.id,
                "name": obj.name,
                "year": obj.year
            }
        return super(StudentJSONEncoder, self).default(obj)
