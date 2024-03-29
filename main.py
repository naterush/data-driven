import json
import os
from datetime import datetime, timedelta
import sys


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_range(options):
    minimum = float(options[0].split("-")[0])
    maximum = float(options[0].split("-")[1])
    return minimum, maximum

def valid_answer(answer, question):
    if any(question['options']):
            if is_number(answer):
                # check if it's in the range
                try:
                    minimum, maximum = get_range(question['options'])
                except:
                    return False
                number = float(answer)
                if number < minimum or number > maximum:
                    return False
            elif answer not in question['options']:
                return False
    return True

class Questionare():

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            self.questions = []
        else:
            self.questions = self.read_questions(file_path)

    def read_questions(self, file):
        """
        JSON File. Array of JSON objects. Each is a question:
        contains a permanent ID, and question_text, and options
        """
        f = open(file, "r")
        txt = f.read()
        if len(txt) == 0:
            return []
        questions = json.loads(txt)
        return questions

    def add_question(self, question_text, options):
        for question in self.questions:
            if question['question_text'] == question_text:
                print("Cannot question that already exists")
                return
        self.questions.append({'question_text' : question_text, 'options': options})
        new_json = json.dumps(self.questions, indent=4)
        f = open(self.file_path, "w+")
        f.write(new_json)
        f.close()

    def ask_question(self, question):
        print("{} \noptions: {}".format(question['question_text'], question['options']))
        answers = input(":").split(";")

        # check it's valid, given the options
        for answer in answers:
            answer = answer.strip()
            if not valid_answer(answer, question):
                print("Invalid answer: must be from {}".format(question['options']))
                return self.ask_question(question)
        return "{}".format(answers)

    def start_questionare(self):
        answers = dict()
        for question in self.questions:
            answers[question['question_text']] = self.ask_question(question)
        return answers

    def record_questonare(self, save_as):
        answers = self.start_questionare()
        new_json = json.dumps(answers, indent=4)
        f = open(save_as, "w+")
        f.write(new_json)
        f.close()

def main():
    dirpath = '/Users/narush/data-driven'
    questionare = Questionare(dirpath + "/questions.txt")

    if len(sys.argv) == 1:
        # be default, do it for today
        date = (datetime.now()).strftime('%Y-%m-%d')
        questionare.record_questonare("{}/answers/{}.txt".format(dirpath, date))
    elif sys.argv[1] == 'add':
        # add a new question
        while True:
            new_question = input("New question: ")
            options = input("Options (; delimited): ").split(";")
            for i in range(len(options)):
                options[i] = options[i].strip()
            questionare.add_question(new_question, options)
    else:
        if not is_number(sys.argv[1]) or float(sys.argv[1]) > 0:
            raise Exception("Usage: must be a non-positive number (default 0)")
        date = (datetime.now() + timedelta(float(sys.argv[1]))).strftime('%Y-%m-%d')
        questionare.record_questonare("{}/answers/{}.txt".format(dirpath, date))

main()