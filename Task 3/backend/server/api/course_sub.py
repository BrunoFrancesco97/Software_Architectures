import sqlalchemy
import database
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Course_Sub(database.Base):
    __tablename__ = 'course_subscriptions'
    course = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("courses.name"), primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=40), sqlalchemy.ForeignKey("user.email"), primary_key=True)
    subscription = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def obj_to_dict(obj: Course_Sub):  # for build json format
    return {
        "user": obj.user,
        "course": obj.course,
        "subscription": obj.subscription,
    }


def add_subscription(course: str, user: str):
    session = database.Session()
    try:
        sub = select_course_subs(user, course)
        if sub is not None and len(sub) == 0:
            new_course_sub = Course_Sub(course=course, user=user)
            session.add(new_course_sub)
    except:
        session.rollback()
    else:
        session.commit()


def remove_subscription(name: str, course: str):
    session = database.Session()
    session.query(Course_Sub).filter_by(user=name, course=course).delete(synchronize_session="evaluate")
    session.flush()
    session.commit()


def select_all():
    session = database.Session()
    courses = session.query(Course_Sub).all()
    session.flush()
    return courses


def select_course_subs_by_courses(course: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(course=course).all()
    session.flush()
    return sub


def select_course_subs_by_user(name: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(user=name).all()
    session.flush()
    return sub


def select_course_subs(name: str, course: str):
    session = database.Session()
    sub = session.query(Course_Sub).filter_by(user=name, course=course).all()
    session.flush()
    return sub
