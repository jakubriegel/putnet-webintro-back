from flask import Flask, jsonify, request, Response

from app.student import Student, StudentJSONEncoder

app = Flask(__name__)
app.json_encoder = StudentJSONEncoder
students = [Student("John", 1), Student("Jim", 1), Student("Jane", 3)]


def get_student_by_id(student_id: int) -> Student:
    return next(s for s in students if s.id == student_id)


@app.route('/students', methods=['GET'])
def get_students():
    if request.args.get('year') is not None:
        year = int(request.args.get('year'))
        return jsonify({
            "students": list(filter(lambda s: s.year == year, students))
        })
    else:
        return jsonify({
            "students": students
        })


@app.route('/student/<student_id>', methods=['GET', 'DELETE'])
def get_or_delete_student(student_id: int):
    student = get_student_by_id(int(student_id))
    if request.method == 'GET':
        return jsonify(student)
    elif request.method == 'DELETE':
        students.remove(student)
        return Response({}, status=204)


@app.route('/student', methods=['POST', 'PUT'])
def add_or_update_student():
    student_data = request.get_json()
    if request.method == 'POST':
        student = Student(student_data["name"], student_data["year"])
        students.append(student)
        return jsonify(student)
    elif request.method == 'PUT':
        student = get_student_by_id(int(student_data["id"]))
        student.name = student_data["name"]
        student.year = student_data["year"]
        return jsonify(student)


