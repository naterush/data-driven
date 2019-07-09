# data-driven
A program built for keeping track of your life. Each day, answer questions about your life that matter to you. Then, use the included tools to figure out what makes you happy. 

# How to Use

First, create a file named `questions.txt` in the same folder as the program. Make sure it fits the JSON format: 

~~~~
[
    {
        "question_text": "How happy were you today?",
        "options": [
            "1-5"
        ]
    },
    ...
]
~~~~

Then, run the program, and it will ask you all of the questions. It will also, optionally, keep track of data like your internet history and usage patterns.
