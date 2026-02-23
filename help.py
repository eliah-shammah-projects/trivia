# no futuro permitir mudanca de nivel durante o jogo 
# fazer funcao ask play


import json
import random
import argparse


class Question:
    def __init__(self, question, answer, options, difficulty, category):
        self.question = question
        self.answer = answer
        self.options = options
        self.difficulty = difficulty
        self.category = category
        
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

        print("Chose the difficulty level:")
        print("1. 1\n2. 2\n3. 3\n4. 2-\n5. 2+\n6. All")
        opcoes = {"1": 1, "2": 2, "3": 3, "4": "2-", "5": "2+", "6": "all"}
        while True:
            escolha = input("Enter the number of the desired difficulty: ").strip()
            if escolha in opcoes:
                nivel = opcoes[escolha]
                if nivel == "all":
                    perguntas_filtradas = self.questions.copy()
                elif nivel == "2-":
                    perguntas_filtradas = [q for q in self.questions if q.difficulty == 1 or q.difficulty == 2]
                elif nivel == "2+":
                    perguntas_filtradas = [q for q in self.questions if q.difficulty == 2 or q.difficulty == 3]
                else:
                    perguntas_filtradas = [q for q in self.questions if q.difficulty == nivel]
                if not perguntas_filtradas:
                    print("No questions available for this difficulty level.")
                    continue
                if len(perguntas_filtradas) < len(self.players):
                    print("Not enough questions for the number of players. Choose another difficulty.")
                    continue
                break
            else:
                print("Invalid option. Please try again.")
        

        first_player = random.randrange(len(self.players))
        current_player = first_player
        new = True
        rounds = (len(perguntas_filtradas) // len(self.players)) * len(self.players)
        self.flow_questions = perguntas_filtradas.copy()

        for i in range(rounds):
            if new:
                categories = sorted(set(q.category for q in self.flow_questions))
                print("Available categories:")
                for j, category in enumerate(categories):
                    print(f"{j + 1}. {category}")   
                while True:
                    try:
                        category_choice = int(input("Choose a category by entering its number: "))
                        if 1 <= category_choice <= len(categories):
                            chosen_category = categories[category_choice - 1]
                            break
                        else:
                            raise ValueError("Invalid input. Please enter a valid category number.")
                    except ValueError:
                        print("Invalid input. Please enter a valid category number.")

                question = random.choice([q for q in self.flow_questions if q.category == chosen_category])
                self.flow_questions.remove(question)
            print(f"{self.players[current_player].name}, it's your turn!")
            print(question.question)
            for i, j in enumerate(question.options):
                print(f"{i + 1}. {j}")

            while True:
                try:
                    answer = int(input("Your answer (1-4): "))
                    if answer > 0 and answer < 5:
                        break
                    else:
                        raise ValueError("Invalid input. Please enter a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a *number* between 1 and 4.")

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
            print("Starting tie-breaker round...")
            winners = [p for p in self.players if p.name in winners]
            self.tie_breaker(winners, perguntas_filtradas)


    def tie_breaker(self, winners, perguntas_filtradas):
        for i in winners:
            i.score = 0
        for i in range(3):
            self.flow_questions = perguntas_filtradas.copy()
            if len(self.flow_questions) < len(winners):
                print("There are not enough questions for the tie-breaker round. The game will end without a clear winner.")
                return
            first_player = random.randrange(len(winners))
            current_player = first_player
            new = True
            for p in range(len(winners)):
                if new:
                    categories = sorted(set(q.category for q in self.flow_questions))
                    print("Available categories:")
                    for j, category in enumerate(categories):
                        print(f"{j + 1}. {category}")   
                    while True:
                        try:
                            category_choice = int(input("Choose a category by entering its number: "))
                            if 1 <= category_choice <= len(categories):
                                chosen_category = categories[category_choice - 1]
                                break
                            else:
                                raise ValueError("Invalid input. Please enter a valid category number.")
                        except ValueError:
                            print("Invalid input. Please enter a valid category number.")

                    question = random.choice([q for q in self.flow_questions if q.category == chosen_category])
                    self.flow_questions.remove(question)
                print(f"{winners[current_player].name}, it's your turn!")
                print(question.question)
                for i, j in enumerate(question.options):
                    print(f"{i + 1}. {j}")
                while True:
                    try:
                        answer = int(input("Your answer (1-4): "))
                        if answer > 0 and answer < 5:
                            break
                        else:
                            raise ValueError("Invalid input. Please enter a number between 1 and 4.")
                    except ValueError:
                        print("Invalid input. Please enter a *number* between 1 and 4.")
               
                if answer == question.answer:
                    print("Correct!")
                    winners[current_player].score += 1
                    new = True
                else:
                    print("Wrong!")
                    new = False
                print(f"The correct answer was: {question.options[question.answer - 1]}")
                current_player = (current_player + 1) % len(winners)
                
            

            winners = [p for p in winners if p.score == 1]
            if not winners:
                print("Ninguém acertou! O jogo terminou sem vencedor.")
                return
            elif len(winners) == 1:
                print(f"The winner is {winners[0].name}!")
                break           
            else:
                print(f"The winners are {', '.join(p.name for p in winners)}! Starting tie-breaker round...")
                for i in winners:
                   i.score = 0
        print ("Game over!", "We dont have an alone winner!")

def read_json(file):
    try:
       with open (file, 'r') as f:
        data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{file}' is not a valid JSON file.")
        exit(1) 
   
    questions = []
    for i in data:
        question = i['question']
        answer = i['answer']
        options = i['options']
        difficulty = i['difficulty']
        category = i['category']    
        questions.append(Question(question, answer, options, difficulty, category))
    
    return questions


def main():
        parser = argparse.ArgumentParser(description="trivia game")
        parser.add_argument('--file', required = True, help='the path of the json file with the questions')
        parser.add_argument('--num_of_players', type = int, required = True,  help='the number of players')
        args = parser.parse_args()   

        if args.num_of_players < 2 or args.num_of_players > 10:
            print("Error: The number of players must be between 2 and 10.")
            exit(1)


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


if __name__ == "__main__":    main()

