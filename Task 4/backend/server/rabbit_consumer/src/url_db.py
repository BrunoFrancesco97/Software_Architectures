import os
URL_USER = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_USER']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_SOLUTION = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_SOLUTION']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_CHANNEL = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_CHANNEL']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_COURSE = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_COURSE']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_CHANNEL_SUB = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_SUBSCRIPTION']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_COURSE_SUB = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_SUBSCRIPTION']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_MESSAGE = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_MESSAGE']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_ASSIGNMENT = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_ASSIGNMENT']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_EXERCISE = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_EXERCISE']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_TEST = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_TEST']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_RESULT = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_RESULT']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_LOGIN = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_LOGIN']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']
URL_FILE = "mysql+pymysql://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@"+os.environ['URL_DB_FILE']+":"+os.environ['DB_PORT']+"/"+os.environ['DB_NAME']