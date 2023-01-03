import sqlalchemy
import database
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class Result(database.Base):
    __tablename__ = 'results'
    assignment = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("assignments.id"), nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), nullable=False)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

def obj_to_dict(obj: Result):  # for build json format
    return {
        "assignment": obj.assignment,
        "user": obj.user,
        "subscription":obj.subscription,
        "result":obj.result,
        "comment":obj.comment,
        "id":obj.id
    }


def add_result_without_comment(assignment_el: int, user_el: str, result_el: int):
    session = database.Session()
    try:
        new_result = Result(assignment=assignment_el, user=user_el, result=result_el)
        session.add(new_result)
    except:
        session.rollback()
    else:
        session.commit()


def add_result_with_comment(assignment_el: int, user_el: str, result_el: int, comment_el: str):
    session = database.Session()
    try:
        new_result = Result(assignment=assignment_el, user=user_el, result=result_el, comment=comment_el)
        session.add(new_result)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def add_result_without_vote(assignment_el: int, user_el: str, comment_el: str):
    session = database.Session()
    try:
        new_result = Result(assignment=assignment_el, user=user_el, comment=comment_el)
        session.add(new_result)
    except Exception as e:
        print(e)
        session.rollback()
    else:
        session.commit()


def remove_result(id_el):
    session = database.Session()
    session.query(Result).filter_by(id=id_el).delete(synchronize_session="evaluate")
    session.commit()


def selectAll():
    session = database.Session()
    results = session.query(Result).all()
    session.close()
    return results


def get_result_by_id(id_el):
    session = database.Session()
    results = session.query(Result).filter_by(id=id_el).all()
    session.close()
    return results


def get_results_by_user(user : str):
    session = database.Session()
    results = session.query(Result).filter_by(user=user).all()
    session.close()
    return results


def get_results_by_assignment(assignment: int):
    session = database.Session()
    results = session.query(Result).filter_by(assignment=assignment).all()
    session.close()
    return results

def get_results_by_assignment_user(assignment: int, user : str):
    session = database.Session()
    results = session.query(Result).filter_by(assignment=assignment,user=user).all()
    session.close()
    return results
