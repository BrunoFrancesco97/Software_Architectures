from flask import Flask, jsonify, request
import json
import exercise
import course_sub
import assignment
import solution
import os
import tests
import utils
import result
import shutil
import subprocess
import time 

app = Flask(__name__)
SIMILARITY_CONSTRAINT = 0.82


@app.get('/')
def works():
	return jsonify({"works": True}), 200


@app.get('/exercise/<id>/<user>')
def get_exercises(id, user):
	assignment_got = assignment.get_assignments_by_id(id)
	if len(assignment_got) == 1:
		sub = course_sub.select_course_subs(user, assignment_got[0].course)
		if len(sub) == 1:  # I'm subscribed to that course thus I must be able to see the exercises of an assignment
			exercises = exercise.get_exercises_by_assignment(id)
			exercises_new = [exercise.obj_to_dict(item) for item in exercises]
			return jsonify({'exercises': exercises_new}), 200
		else:
			return jsonify({'exercises': []}), 401
	return jsonify({'exercises': []}), 400


@app.post('/exercise')
def create_exercise():
	data = request.get('data')
	quest = data.get('quest')
	correct = data.get('correct')
	assignment_el = data.get('assignment')
	type_el = data.get('type')
	if type_el == 'multiple' or type_el == 'open' or type_el == 'develop' or type_el == 'quiz':
		if 'wrong1' in data.keys() and 'wrong2' in data.keys() and 'wrong3' in data.keys():
			exercise.add_exercise_complete(
				quest, correct, data['wrong1'], data['wrong2'], data['wrong3'], assignment_el, type_el)
		else:
			resp = exercise.add_exercise_uncomplete(
				quest, correct, assignment_el, type_el)
			if resp[0] == True:
				return jsonify({'added': exercise.obj_to_dict(resp[1])}), 200
			else:
				return jsonify({'added': False}), 400
	else:
		return jsonify({'added': False}), 400


@app.put('/exercise')
def send_exercise_develop():
	x = json.loads(request.form['data'])
	if x.get('type').lower() == "develop":
		exercise_id = x.get('exercise')
		correct = exercise.get_exercise_by_id(exercise_id)
		if x.get('language').lower() == 'python':
			response = __python(x.get('program'), x.get(
				'user')['user'], exercise_id, correct[0])
		elif x.get('language').lower() == 'c':
			response = __c(x.get('program'), x.get(
				'user')['user'], exercise_id, correct[0])
		elif x.get('language').lower() == 'c++':
			response = __cpp(x.get('program'), x.get(
				'user')['user'], exercise_id, correct[0])
		elif x.get('language').lower() == 'java':
			response = __java(x.get('program'), x.get(
				'user')['user'], exercise_id, correct[0])
		else:
			return jsonify({"added": False}), 400
	elif x.get('type').lower() == "quiz":
		response = __quiz(x.get('text'), x.get(
			'exercise'), x.get('user')['user'], correct[0])
	elif x.get('type').lower() == "open":
		response = __open_question(x.get('text'), x.get(
			'exercise'), x.get('user')['user'])
	else:
		return jsonify({"added": False}), 400
	return response[0], response[1]


def __quiz(answer, exe, user, correct):
	exe_db = exercise.get_exercise_by_id(exe)
	if exe_db is not None and len(exe_db) == 1:
		if answer == exe_db[0].correct:
			solution.add_solution(
				exe, answer, user, True, True)
		else:
			solution.add_solution(
				exe, answer, user, False, True)
		n_exe = exercise.get_exercises_by_assignment(exe_db[0].assignment)
		count_sol = 0
		count_correct = 0
		for item in n_exe:
			db_sol = solution.get_solutions_by_name_and_exercise(
				user, item.id, True)
			if len(db_sol) == 1:
				count_sol += 1
				if db_sol[0].correct is True:
					count_correct += 1
		if len(n_exe) == count_sol:
			if count_correct == 0:
				result.add_result_without_comment(
					exe_db[0].assignment, user, 0)
				result_list = __get_result_assignment(
					user, correct.assignment)
				result_json = [result.obj_to_dict(
					item) for item in result_list]
			else:
				result.add_result_without_comment(exe_db[0].assignment, user,int((count_correct / len(n_exe)) * 100))
				result_list = __get_result_assignment(
					user, correct.assignment)
				result_json = [result.obj_to_dict(
					item) for item in result_list]
		response = jsonify({"results": result_json, "given": answer, "expected": exe_db[0].correct}), 200
	else:
		response = jsonify({}), 401
	return response 


def __open_question(answer, exe, user):
	exe_db = exercise.get_exercise_by_id(exe)
	if exe_db is not None and len(exe_db) == 1:
		solution.add_solution_open(exe, answer, user, False)
		n_exe = exercise.get_exercises_by_assignment(exe_db[0].assignment)
		count_sol = 0
		for item in n_exe:
			db_sol = solution.get_solutions_by_name_and_exercise(
				user, item.id, True)
			if len(db_sol) == 1:
				count_sol += 1
		response = jsonify({"added": True}), 200
	else:
		response = jsonify({"added": False}), 400
	return response


def __python(program, user, exercise_id, correct):
	path: str = 'dockerdata/dockerfiles/python/' + user
	res = ""
	res_list = []
	tests_to_perform = []
	error = ""
	flag = False
	try:
		if not os.path.exists(path):
			flag = True
			os.mkdir(path)
			f = open(path + "/app.py", "w")
			f.write(program)
			f.close()
			tests_to_perform = tests.get_tests_by_exercise(exercise_id)
			if len(tests_to_perform) == 0:
				res = subprocess.check_output(
					"python " + path + "/app.py", stderr=subprocess.STDOUT, shell=True).decode('UTF-8')  # TODO: Cambiarei n Python3
			else:
				for test in tests_to_perform:
					resu = subprocess.check_output("python " + path + "/app.py "+test.given_value, stderr=subprocess.STDOUT,  # TODO: Cambiarei n Python3
												   shell=True).decode('UTF-8')

					if utils.similar(resu.replace('\r', '').strip(), test.expected) > SIMILARITY_CONSTRAINT:
						res_list.append(
							(True, resu.replace('\r', '').strip(), test.expected, test.name))
					else:
						res_list.append((False, resu.replace(
							'\r', '').strip(), test.expected, test.name))
	except subprocess.CalledProcessError as e:
		error = e.output.decode(
			'UTF-8')[e.output.decode('UTF-8').find('app.py'):]
		' '.join(error.split())
	finally:
		if flag == True:
			shutil.rmtree(path)
			res = res.replace('\r', '').strip()
			if len(tests_to_perform) == 0:
				if utils.similar(res, correct.correct) > SIMILARITY_CONSTRAINT:
					solution.add_solution(
						exercise_id, program, user, True, True)
				else:
					solution.add_solution(
						exercise_id, program, user, False, True) 
			else:
				if error == "":
					flag_passed = True
					for element in res_list:
						if element[0] == False:
							flag_passed = False
				else:
					flag_passed = False
				solution.add_solution(
					exercise_id, program, user, flag_passed, True)
			time.sleep(10) 
			similar = __check_integrity_solution(
				exercise_id, user)
			n_exe = exercise.get_exercises_by_assignment(correct.assignment)
			count_sol = 0
			count_correct = 0
			for item in n_exe:
				db_sol = solution.get_solutions_by_name_and_exercise(
					user, item.id, True)
				if len(db_sol) == 1:
					count_sol += 1
					if db_sol[0].correct == True:
						count_correct += 1
			result_json = []
			if len(n_exe) == count_sol: #I've completed all the exercises
				if count_correct == 0:
					result.add_result_without_comment(
						correct.assignment, user, 0)
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct.assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
				else:
					result.add_result_without_comment(correct.assignment, user,
													  int((count_correct / len(n_exe)) * 100))
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct.assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
			if len(tests_to_perform) == 0:
				response = jsonify({"results": result_json, "given": res,
									"expected": correct.correct, "correct": db_sol[0].correct, "similar_responses": similar, "error": error}), 200
			else:
				response = jsonify({"results": result_json, "tests": res_list,
									"similar_responses": similar, "error": error}), 200
		else:
			response = jsonify({"results": {}}), 500
		return response


def __java(program, user, exercise_id, correct):
	path: str = 'dockerdata/dockerfiles/java/' + user
	res = ""
	res_list = []
	tests_to_perform = []
	error = ""
	flag = False
	try:
		if not os.path.exists(path):
			flag = True
			os.mkdir(path)
			f = open(path + "/app.java", "w")
			f.write(program.replace('\"', '"'))
			f.close()
			tests_to_perform = tests.get_tests_by_exercise(exercise_id)
			if len(tests_to_perform) == 0:
				res = subprocess.check_output("java " + path + "/app.java", stderr=subprocess.STDOUT,
											  shell=True).decode('UTF-8')
			else:
				for test in tests_to_perform:
					resu = subprocess.check_output(
						"java " + path + "/app.java "+test.given_value, stderr=subprocess.STDOUT, shell=True).decode('UTF-8')
					if utils.similar(resu.replace('\r', '').strip(), test.expected) > SIMILARITY_CONSTRAINT:
						res_list.append(
							(True, resu.replace('\r', '').strip(), test.expected, test.name))
					else:
						res_list.append((False, resu.replace(
							'\r', '').strip(), test.expected, test.name))
	except subprocess.CalledProcessError as e:
		print(e.output)
		error = str(e.output.decode('UTF-8'))
	finally:
		if flag == True:
			shutil.rmtree(path)
			res = res.replace('\r', '').strip()
			if len(tests_to_perform) == 0:
				if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
					solution.add_solution(
						exercise_id, program, user, True, True)
				else:
					solution.add_solution(
						exercise_id, program, user, False, True)
			else:
				if error == "":
					flag_passed = True
					for element in res_list:
						if element[0] == False:
							flag_passed = False
				else:
					flag_passed = False
				solution.add_solution(
					exercise_id, program, user, flag_passed, True)
			time.sleep(10)
			similar = __check_integrity_solution(exercise_id, user)
			n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
			count_sol = 0
			count_correct = 0
			for item in n_exe:
				db_sol = solution.get_solutions_by_name_and_exercise(
					user, item.id, True)
				if len(db_sol) == 1:
					count_sol += 1
					if db_sol[0].correct is True:
						count_correct += 1
			if len(n_exe) == count_sol:
				if count_correct == 0:
					result.add_result_without_comment(
						correct[0].assignment, user, 0)
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
				else:
					result.add_result_without_comment(correct[0].assignment, user,
													  int((count_correct / len(n_exe)) * 100))
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
			if len(tests_to_perform) == 0:
				response = jsonify({"results": result_json, "given": res,
									"expected": correct[0].correct, "correct": db_sol[0].correct, "similar_responses": similar, "error": error}), 200
				' '.join(response.split())
			else:
				response = jsonify({"results": result_json, "tests": res_list,
									"similar_responses": similar, "error": error}), 200
		else:
			response = jsonify({"results": {}}), 500
	return response


def __c(program, user, exercise_id, correct):
	path: str = 'dockerdata/dockerfiles/c/' + user
	res = ""
	res_list = []
	tests_to_perform = []
	error = ""
	flag = False
	try:
		if not os.path.exists(path):
			flag = True
			os.mkdir(path)
			f = open(path + "/app.c", "w")
			f.write(program.replace('>', '>\n'))
			f.close()
			subprocess.check_output("gcc -lstdc++ " + path + "/app.c -o " + path + "/app",
									stderr=subprocess.STDOUT, shell=True)
			tests_to_perform = tests.get_tests_by_exercise(exercise_id)
			if len(tests_to_perform) == 0:
				res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
											  shell=True).decode('UTF-8')
			else:
				for test in tests_to_perform:
					resu = subprocess.check_output("./ " + path + "/app "+test.given_value, stderr=subprocess.STDOUT,
												   shell=True).decode('UTF-8')
					if utils.similar(resu.replace('\r', '').strip(), test.expected) > SIMILARITY_CONSTRAINT:
						res_list.append(
							(True, resu.replace('\r', '').strip(), test.expected, test.name))
					else:
						res_list.append((False, resu.replace(
							'\r', '').strip(), test.expected, test.name))
	except subprocess.CalledProcessError as e:
		#response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
		error = str(e.output)
	finally:
		if flag == True:
			shutil.rmtree(path)
			res = res.replace('\r', '').strip()
			if len(tests_to_perform) == 0:
				if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
					solution.add_solution(
						exercise_id, program, user, True, True)
				else:
					solution.add_solution(
						exercise_id, program, user, False, True)
			else:
				if error == "":
					flag_passed = True
					for element in res_list:
						if element[0] == False:
							flag_passed = False
				else:
					flag_passed = False
				solution.add_solution(
					exercise_id, program, user, flag_passed, True)
			time.sleep(10)
			similar = __check_integrity_solution(
				exercise_id, user)
			n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
			count_sol = 0
			count_correct = 0
			for item in n_exe:
				db_sol = solution.get_solutions_by_name_and_exercise(
					user, item.id, True)
				if len(db_sol) == 1:
					count_sol += 1
					if db_sol[0].correct is True:
						count_correct += 1
			if len(n_exe) == count_sol:
				if count_correct == 0:
					result.add_result_without_comment(
						correct[0].assignment, user, 0)
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
				else:
					result.add_result_without_comment(correct[0].assignment, user,
													  int((count_correct / len(n_exe)) * 100))
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
			if len(tests_to_perform) == 0:
				response = jsonify({"results": result_json, "given": res,
									"expected": correct[0].correct, "correct": db_sol[0].correct, "similar_responses": similar, "error": error}), 200
			else:
				response = jsonify({"results": result_json, "tests": res_list,
									"similar_responses": similar, "error": error}), 200
		else:
			response = jsonify({"results": {}}), 500
	return response


def __cpp(program, user, exercise_id, correct):
	path: str = 'dockerdata/dockerfiles/cpp/' + user
	res = ""
	res_list = []
	tests_to_perform = []
	error = ""
	flag = False
	try:
		if not os.path.exists(path):
			flag = True
			os.mkdir(path)
			f = open(path + "/app.cpp", "w")
			f.write(program.replace('>', '>\n'))
			f.close()
			subprocess.check_output("g++ " + path + "/app.cpp -o " + path + "/app",
									stderr=subprocess.STDOUT, shell=True)
			tests_to_perform = tests.get_tests_by_exercise(exercise_id)
			if len(tests_to_perform) == 0:
				res = subprocess.check_output("./" + path + "/app", stderr=subprocess.STDOUT,
											  shell=True).decode('UTF-8')
			else:
				for test in tests_to_perform:
					resu = subprocess.check_output("./" + path + "/app "+test.given_value, stderr=subprocess.STDOUT,
												   shell=True).decode('UTF-8')
					if utils.similar(resu.replace('\r', '').strip(), test.expected) > SIMILARITY_CONSTRAINT:
						res_list.append(
							(True, resu.replace('\r', '').strip(), test.expected, test.name))
					else:
						res_list.append((False, resu.replace(
							'\r', '').strip(), test.expected, test.name))
	except subprocess.CalledProcessError as e:
		#response = jsonify({'return': e.output.decode('UTF-8'), 'correct': 'false'}), 200
		error = str(e.output)
	finally:
		if flag == True:
			shutil.rmtree(path)
			res = res.replace('\r', '').strip()
			if len(tests_to_perform) == 0:
				if utils.similar(res, correct[0].correct) > SIMILARITY_CONSTRAINT:
					solution.add_solution(
						exercise_id, program, user, True, True)
				else:
					solution.add_solution(
						exercise_id, program, user, False, True)
			else:
				if error == "":
					flag_passed = True
					for element in res_list:
						if element[0] == False:
							flag_passed = False
				else:
					flag_passed = False
				solution.add_solution(
					exercise_id, program, user, flag_passed, True)
			time.sleep(10)
			similar = __check_integrity_solution(
				exercise_id, user)
			n_exe = exercise.get_exercises_by_assignment(correct[0].assignment)
			count_sol = 0
			count_correct = 0
			for item in n_exe:
				db_sol = solution.get_solutions_by_name_and_exercise(
					user, item.id, True)
				if len(db_sol) == 1:
					count_sol += 1
					if db_sol[0].correct is True:
						count_correct += 1
			if len(n_exe) == count_sol:
				if count_correct == 0:
					result.add_result_without_comment(
						correct[0].assignment, user, 0)
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
				else:
					result.add_result_without_comment(correct[0].assignment, user,
													  int((count_correct / len(n_exe)) * 100))
					time.sleep(10)
					result_list = __get_result_assignment(
						user, correct[0].assignment)
					result_json = [result.obj_to_dict(
						item) for item in result_list]
			if len(tests_to_perform) == 0:
				response = jsonify({"results": result_json, "given": res,
									"expected": correct[0].correct, "correct": db_sol[0].correct, "similar_responses": similar, "error": error}), 200
				' '.join(response.split())
			else:
				response = jsonify({"results": result_json, "tests": res_list,
									"similar_responses": similar, "error": error}), 200
		else:
			response = jsonify({"results": {}}), 500
	return response

def __check_integrity_solution(exercise_id,user):
    solutions_got = solution.get_solutions_by_name_and_exercise(user, exercise_id,True)
    if len(solutions_got) == 1:
        hash_generated = solutions_got[0].hash
        similar_solutions = solution.get_solutions_by_hash(hash_generated, exercise_id)
        if len(similar_solutions) > 1:
            return True 
        else:
            return False 
    return None

def __get_result_assignment(user : str,assigment : int):
    results = result.get_results_by_assignment_user(assigment,user)
    return results

if __name__ == '__main__':
	if not os.path.exists('dockerdata'):
		os.mkdir('dockerdata')
		os.mkdir('dockerdata/dockerfiles')
		os.mkdir('dockerdata/dockerfiles/c')
		os.mkdir('dockerdata/dockerfiles/cpp')
		os.mkdir('dockerdata/dockerfiles/java')
		os.mkdir('dockerdata/dockerfiles/python')
	app.run(host='0.0.0.0', debug=True, port=5008)
