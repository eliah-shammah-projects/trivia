
import json
import random
import argparse


class Question:
    def __init__(self, question, answer, options):
        self.question = question
        self.answer = answer
        self.options = options
        self.shuffle_answers()
    
    def shuffle_answers(self):
        correct_text = self.options[self.answer - 1]
        random.shuffle(self.options)
        self.answer = self.options.index(correct_text) + 1

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
        rounds = (len(self.questions) // len(self.players)) * len(self.players)


        for i in range (rounds):
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
            print(f"The correct answer was: {question.options[question.answer - 1]}")
            current_player = (current_player + 1) % len(self.players)
        
        maxi = max(p.score for p in self.players)
        winners = []
        for p in self.players:
            print(f"{p.name} scored {p.score} points.")
            if maxi == p.score:
                winners.append(p.name)
        if len(winners) == 1:
            print(f"The winner is {winners[0]}!")
        else:
            print(f"The winners are {', '.join(winners)}!")
                




def read_json(file):
    with open (file, 'r') as f:
        data = json.load(f)
   
    questions = []
    for i in data:
        question = i['question']
        answer = i['answer']
        options = i['options']
        
        questions.append(Question(question, answer, options))
    
    return questions


def main():
        parser = argparse.ArgumentParser(description="trivia game")
        parser.add_argument('--file', required = True, help='the path of the json file with the questions')
        parser.add_argument('--num_of_players', type = int, required = True,  help='the number of players')
       
        args = parser.parse_args()   

        names_list = []
        for i in range(args.num_of_players):
           name = input(f"Enter the name of player {i + 1}: ")
           names_list.append(name)
           print (f"Welcome {name}!")

        players = []
        for name in names_list:
            player = Player(name)
            players.append(player)

        questions = read_json(args.file)

        game = Game(questions, players)
        game.play()


        
