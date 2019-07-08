import json
import os


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
        new_json = json.dumps(self.questions)
        f = open(self.file_path, "w+")
        f.write(new_json)
        f.close()

    def ask_question(self, question):
        print("{} \noptions: {}".format(question['question_text'], question['options']))
        answer = input(":")
        if any(question['options']):
            if answer not in question['options']:
                print("Invalid response: must be an option")
                return self.ask_question(question)
        return answer

    def start_questionare(self):
        answers = dict()
        for question in self.questions:
            answers[question['question_text']] = self.ask_question(question)
        return answers


def main():
    dirpath = os.getcwd()
    questionare = Questionare(dirpath + "/questions.txt")
    print(questionare.questions)
    questionare.add_question("Hello?", ["no", "yes"])
    print(questionare.start_questionare())

# User functions

main()