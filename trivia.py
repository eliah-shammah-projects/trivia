#TODO:
# There are still some things in Portuguese that need to be fixed
# In the future, allow changing the difficulty level during the game
# Add an option for how long the game will last
# Add a maximum time to answer
# Limit questions  


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
    def ask_category_and_question(self, flow_questions):
        categories = sorted(set(q.category for q in flow_questions if any(q2.category == q.category for q2 in flow_questions)))
        while True:
            print("Available categories:")
            for j, category in enumerate(categories):
                print(f"{j + 1}. {category}")
            try:
                category_choice = int(input("Choose a category by entering its number: "))
                if 1 <= category_choice <= len(categories):
                    chosen_category = categories[category_choice - 1]
                    questions_in_category = [q for q in flow_questions if q.category == chosen_category]
                    if questions_in_category:
                        question = random.choice(questions_in_category)
                        return question
                    else:
                        print("No more questions in this category. Please choose another category.")
                        categories.pop(category_choice - 1)
                        if not categories:
                            print("No more categories with questions available.")
                            return None
                else:
                    raise ValueError("Invalid input. Please enter a valid category number.")
            except ValueError:
                print("Invalid input. Please enter a valid category number.")

    def __init__(self, questions, players):
        self.questions = questions
        self.players = players

    def play(self):

        print("Chose the difficulty level:")
        print("1. 1\n2. 2\n3. 3\n4. 2-\n5. 2+\n6. All")
        options = {"1": 1, "2": 2, "3": 3, "4": "2-", "5": "2+", "6": "all"}
        while True:
            choice = input("Enter the number of the desired difficulty: ").strip()
            if choice in options:
                level = options[choice]
                if level == "all":
                    filtered_questions = self.questions.copy()
                elif level == "2-":
                    filtered_questions = [q for q in self.questions if q.difficulty == 1 or q.difficulty == 2]
                elif level == "2+":
                    filtered_questions = [q for q in self.questions if q.difficulty == 2 or q.difficulty == 3]
                else:
                    filtered_questions = [q for q in self.questions if q.difficulty == level]
                if not filtered_questions:
                    print("No questions available for this difficulty level.")
                    continue
                if len(filtered_questions) < len(self.players):
                    print("Not enough questions for the number of players. Choose another difficulty.")
                    continue
                break
            else:
                print("Invalid option. Please try again.")
        


        first_player = random.randrange(len(self.players))
        current_player = first_player
        new = True
        attemps = 0
        rounds = (len(filtered_questions) // len(self.players)) * len(self.players)
        self.flow_questions = filtered_questions.copy()

        for i in range(rounds):
            if new or attemps >= 2:
                question = self.ask_category_and_question(self.flow_questions)
                self.flow_questions.remove(question)
                attemps = 0


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
                attemps += 1
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
            self.tie_breaker(winners, filtered_questions)


    def tie_breaker(self, winners, filtered_questions):
        for i in winners:
            i.score = 0
        for i in range(3):
            self.flow_questions = filtered_questions.copy()
            if len(self.flow_questions) < len(winners):
                print("There are not enough questions for the tie-breaker round. The game will end without a clear winner.")
                return
            first_player = random.randrange(len(winners))
            current_player = first_player
            new = True
            attemps = 0
            for p in range(len(winners)):
                if new or attemps >= 2:
                    question = self.ask_category_and_question(self.flow_questions)
                    self.flow_questions.remove(question)
                    attemps = 0
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
                    attemps += 1    
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

