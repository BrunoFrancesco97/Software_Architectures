from flask import Flask, jsonify,request
import json 
import exercise
import solution 
import result 

app = Flask(__name__)

@app.get('/')
def works():
    return jsonify({"works":True}), 200


@app.get('/solution/<id>')
def get_open_question(id):
    exe_list = exercise.get_exercise_by_type_and_assignment('open', id)
    open_q = []
    for item in exe_list:
        unreviewed = solution.get_unreviewed_solution(item.id)
        for elem in unreviewed:
            open_q.append(solution.obj_to_dict_quest(elem, item.quest))
    return jsonify({"solution": open_q}), 200

@app.post('/solution')
def check_open_question():
    data = json.loads(request.data.decode(encoding='UTF-8'))
    exercise_id = data.get('exercise')
    res = data.get('correct')
    msg = data.get('comment')
    user = data.get('username')
    current_ass = exercise.get_exercise_by_id(exercise_id)
    if current_ass is not None and len(current_ass) == 1:
        solution.check_solution(exercise_id, user, (res=='true'))
        n_exe = exercise.get_exercises_by_assignment(current_ass[0].assignment)
        count_sol = 0
        count_correct = 0
        result_json = []
        for item in n_exe:
            db_sol = solution.get_solutions_by_name_and_exercise(user, item.id, True)
            if len(db_sol) == 1:
                count_sol += 1
                if db_sol[0].correct is True:
                    count_correct += 1
        if len(n_exe) == count_sol:
            if count_correct == 0:
                result.add_result_with_comment(current_ass[0].assignment, user, 0, msg)
                result_list = __get_result_assignment(user,current_ass[0].assignment)
                result_json = [result.obj_to_dict(item) for item in result_list]
            else:
                result.add_result_with_comment(current_ass[0].assignment, user,int((count_correct / len(n_exe)) * 100), msg)
                result_list = __get_result_assignment(user,current_ass[0].assignment)
                result_json = [result.obj_to_dict(item) for item in result_list]
        return jsonify({"results": result_json}), 200

def __get_result_assignment(user : str,assigment : int):
    results = result.get_results_by_assignment_user(assigment,user)
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)