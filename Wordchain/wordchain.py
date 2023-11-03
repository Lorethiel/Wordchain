import requests
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

with open('Oxford 5000.txt','r+') as file:
    word_list = [line.strip() for line in file]

used_words = []
user_score = 0
opponent_score = 0

def Game():
    rounds = get_rounds()
    difficulty_level = input('Choose the game difficulty: Easy, Medium, or Hard (default: Easy). \n\n').lower()
    while rounds > 0:
        user_input = input('\nEnter your word: ')
        validated_input = validate_input(user_input)
        if validated_input is not None:
            if validated_input in used_words:
                print('You already used this word. ')
            else:
                checked_word = check_word(validated_input)
                if checked_word:
                    used_words.append(validated_input)   
                    opponent_answer = opponent(checked_word,difficulty_level)                           
                    rounds = rounds - 1
                    calculate_score(validated_input,opponent_answer)
                    print(f"\nYour score is: {user_score} and Opponent's score is: {opponent_score}, Remaining Rounds: {rounds}\n")       
                else:
                    print('Failed')
                    if len(used_words) == 0:
                        random_letter = random.choice(letters)
                        used_words.append(random_letter)
                        opponent_answer = random_letter
                    rounds = rounds - 1
                    opponent(used_words[-1],difficulty_level)
                    calculate_score(validated_input,opponent_answer)
                    print(f"Your score is: {user_score} and Opponent's score is: {opponent_score}, Remaining Rounds: {rounds}")
        else:
            print("Failed")
            if len(used_words) == 0:
                random_letter = random.choice(letters)
                used_words.append(random_letter)
                opponent_answer = random_letter
            rounds = rounds - 1
            opponent(used_words[-1],difficulty_level)
            calculate_score(validated_input,opponent_answer)
            print(f"Your score is: {user_score} and Opponent's score is: {opponent_score}, Remaining Rounds: {rounds}")
        if rounds == 0 and user_score == opponent_score:
            print(f'Tiebreaker!, Current Last Word: ({used_words[-1][-1]})')
            rounds = rounds + 1    
    print(f'\nRESULTS: You:{user_score}, Opponent {opponent_score}\n')

def validate_input(user_word):
    if len(user_word) > 1 and user_word.isalpha():
        if len(used_words) == 0:
            return user_word
        elif user_word[0] == used_words[-1][-1]:
            return user_word
    else:
        return None

def check_word(user_word):
    
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{user_word}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return user_word
        elif response.status_code == 404:
            return False           
        else:
            print(f"API request failed with status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
def opponent(user_word, difficulty):
    if check_word(user_word):
        last_letter = user_word[-1]
        filtered_words = [word for word in word_list if word.startswith(last_letter)]
        if filtered_words:
            random_word = random.choice(filtered_words)
            error_chance = random.randint(1, 100)
            
            if difficulty == 'hard':
                max_error_chance = 5
            elif difficulty == 'medium':
                max_error_chance = 15
            elif difficulty == 'easy':
                max_error_chance = 25
            else:
                max_error_chance = 25 

            if error_chance > max_error_chance:
                print(f"\nOpponent's Answer is {random_word.title()}.")
                used_words.append(random_word)
                word_list.remove(random_word)
                return random_word
                
            else:
                print(f"\nOpponent couldn't find a valid word, Current Last Letter: ({used_words[-1][-1]})\n")
                
def get_rounds():
    while True:
        try:
            user_input = int(input('How many rounds do you want to play? \n'))           
        except:
            print('\nEnter a valid number of rounds ')
            continue
        return user_input
    
def calculate_score(user_word,opponent_word):
    global user_score, opponent_score
    if not user_word == None:
        user_score = user_score + 1

    if not opponent_word == None:
        opponent_score = opponent_score + 1
    
    if user_word is None and opponent_word is None:
        if user_score > 0:
            user_score = user_score - 1
        if opponent_score > 0:
            opponent_score = opponent_score - 1
    
def main():
    Game()

if __name__ == '__main__':
    main()