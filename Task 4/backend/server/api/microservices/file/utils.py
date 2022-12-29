import re
import app
import solution
import result
from difflib import SequenceMatcher

def whitespaces_remover(text: str):
    return re.sub(' +', '', text)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.ALLOWED_EXTENSIONS


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check_integrity_solution(exercise_id,user):
    solutions_got = solution.get_solutions_by_name_and_exercise(user, exercise_id,True)
    if len(solutions_got) == 1:
        hash_generated = solutions_got[0].hash
        similar_solutions = solution.get_solutions_by_hash(hash_generated, exercise_id)
        if len(similar_solutions) > 1:
            return True 
        else:
            return False 
    return None  

def get_result_assignment(user : str,assigment : int):
    results = result.get_results_by_assignment_user(assigment,user)
    return results