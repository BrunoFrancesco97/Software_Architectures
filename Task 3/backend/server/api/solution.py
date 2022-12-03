import sqlalchemy
import database
import crypto
from exercise import Exercise


class Solution(database.Base):
    __tablename__ = 'solution'
    exercise = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("exercises.id"), primary_key=True)
    answer = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("user.email"), primary_key=True)
    correct = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
    hash = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    review = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False)


def obj_to_dict(obj: Solution):  # for build json format
    return {
        "exercise": obj.exercise,
        "answer": obj.answer,
        "user": obj.user,
        "correct": obj.correct,
        "hash": obj.hash,
        "review": obj.review,
    }


def obj_to_dict_quest(obj: Solution, quest):  # for build json format
    return {
        "exercise": obj.exercise,
        "answer": obj.answer,
        "user": obj.user,
        "correct": obj.correct,
        "hash": obj.hash,
        "review": obj.review,
        "quest": quest,
    }


def compute_hash(answer: str):
    answer = answer.strip()
    while '  ' in answer:
        answer = answer.replace('  ', ' ')
    answer = crypto.sha256_basic(answer)
    return answer


def add_solution(exercise: int, answer: str, user: str, correct, review):
    session = database.Session()
    try:
        new_solution = Solution(exercise=exercise, answer=answer, user=user, correct=correct, hash=compute_hash(answer),
                                review=review)
        session.add(new_solution)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def add_solution_open(exercise: int, answer: str, user: str, review):
    session = database.Session()
    try:
        new_solution = Solution(exercise=exercise, answer=answer, user=user, hash=compute_hash(answer),
                                review=review)
        session.add(new_solution)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def get_solutions_by_name(user: str):
    session = database.Session()
    solutions = session.query(Solution).filter_by(user=user).all()
    session.close()
    return solutions


def get_solutions_by_exercise(exercise: str):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise).all()
    session.close()
    return solutions


def get_solutions_by_name_and_exercise(user: str, exercise, review):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise, user=user, review=review).all()
    session.close()
    return solutions


def get_solutions_by_hash(hash: str, exercise: int):
    session = database.Session()
    solutions = session.query(Solution).filter_by(hash=hash, exercise=exercise).all()
    session.close()
    return solutions


def get_unreviewed_solution(exercise):
    session = database.Session()
    solutions = session.query(Solution).filter_by(exercise=exercise, review=False).all()
    session.close()
    return solutions


def check_solution(exercise, user, correct):
    session = database.Session()
    session.query(Solution).filter(Solution.exercise == exercise, Solution.review == False,
                                   Solution.user == user).update({Solution.correct: correct, Solution.review: True},
                                                                 synchronize_session="evaluate")
    session.commit()
