import json
import os
import datetime


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
        answer = input(":")

        # check it's valid, given the options
        if any(question['options']):
            if is_number(answer):
                # check if it's in the range
                minimum, maximum = get_range(question['options'])
                number = float(answer)
                if number < minimum or number > maximum:
                    print("Invalid response: must be an option")
                    return self.ask_question(question)
            elif answer not in question['options']:
                print("Invalid response: must be an option")
                return self.ask_question(question)
        return answer

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
    d = datetime.datetime.today()
    dirpath = '/Users/narush/data-driven'
    questionare = Questionare(dirpath + "/questions.txt")
    questionare.record_questonare(dirpath + "/answers/" + str(d) + ".txt")

# User functions

main()