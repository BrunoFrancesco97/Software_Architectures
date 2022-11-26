
def dockerfile_python(name : str):
    return "FROM python:3.8-slim-buster\nWORKDIR /dockerdata/dockerfiles/python\nCOPY "+name+"/app.py .\nCMD [\"python\", \"app.py\"]"