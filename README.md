🧠 Trivia Game

🎮 A fun multiplayer trivia game in Python where players compete by answering questions from different categories and difficulty levels. Perfect for testing your knowledge with friends!

✨ Features

🗂️ Multiple categories: History, Science, Sports, Geography, Math, and more

🎯 Adjustable difficulty: 1, 2, 3, 2-, 2+, or All

👥 Multiplayer support: 2 to 10 players

🔀 Randomized questions and shuffled answer options

🏆 Tie-breaker rounds in case of a draw

✅ Input validation to prevent invalid answers

🚀 How to Play

Run the game in your terminal:

python game.py --file questions.json --num_of_players 3

--file : Path to your JSON file with the questions

--num_of_players : Number of players (2–10)

Steps in the game

Enter player names

Choose a difficulty level

Answer questions in turns

View scores after each round

💡 Tip: Tie-breakers are handled automatically if there's a draw!

📄 JSON Question Format

Example of how a question should look in your JSON file:

{
  "question": "Who was the first president of the United States?",
  "answer": 1,
  "options": ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"],
  "difficulty": 1,
  "category": "history"
}

question : The question text

answer : Index (1–4) of the correct option

options : List of four possible answers

difficulty : 1–3 (or use 2- / 2+ in game selection)

category : Question category

🔧 Future Improvements

Change difficulty during the game

Limit game duration or number of questions

Add time limit per question

Expand database with more categories and questions