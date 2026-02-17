
import json
import random


class Question:
    def __init__(self, question, answer, options):
        self.question = question
        self.answer = answer
        self.options = options

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class Game:

    def __init__(self, questions, players):
        self.questions = questions
        self.players = players

    def play(self):
        first_player = random.randrange(len(self.players))
        current_player = first_player
        new = True

        while self.questions:
            if new:
              question = random.choice(self.questions)
              self.questions.remove(question)


            print(f"{self.players[current_player].name}, it's your turn!")
            print(question.question)
            for i, j in enumerate(question.options):
                print(f"{i + 1}. {j}")
            answer = int(input("Your answer (1-4): "))
            if answer == question.answer:
                print("Correct!")
                self.players[current_player].score += 1
                new = True
            else:
                print("Wrong!")
                new = False
            print(f"The correct answer was: {question.answer}")
           

            current_player = (current_player + 1) % len(self.players)

def shuffle (question_dict):
    correct = question_dict['options'][question_dict['answer'] - 1]
    opts = question_dict['options'].copy()
    random.shuffle(opts)
    new_ans = opts.index(correct) + 1
    return Question(question_dict['question'], new_ans, opts)

def read_json(file):
    with open (file, 'r') as f:
        data = json.load(f)
    questions = []
    for i in data:
        questions.append(shuffle(i))
    return questions


        
        