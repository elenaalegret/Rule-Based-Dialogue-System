# Libraries importation
from nltk.tokenize.treebank import TreebankWordTokenizer
import nltk

"""
# Requeriments
nltk.data.path.append("http://nltk.github.com/nltk_data/")
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
"""
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import json
import sys

# Open the json file and download the data
with open('./house_data.json') as f:
    data = json.load(f)

# Library Functions:

def print_question(prompt, possible_options = []):
    """
    Prints a question prompt and, if provided, the possible options.
    :param prompt: The question prompt to be printed.
    :param possible_options: (Optional) A list of possible options for the question.
    """
    print(prompt)
    if not len(possible_options) == 0:
        print("Assistant:  Options:", ", ".join(possible_options))

def initialize_available_options(house_data, available_options):
    """
    Initializes available options for each key in the house data.
        :param house_data: The house data containing information about available options.
        :param available_options: A dictionary to store available options for each key.
    """
    for house in house_data['houses']:
        for key, value in house.items():
            available_options.setdefault(key, set()).add(value)

def preprocess_answer(answer):
    """
    Tokenizes and preprocesses an answer.
        :param answer: The answer to preprocess.
        :return: A preprocessed answer as a list of tokens.
    """
    answer = nltk.word_tokenize(answer)
    return answer

def get_numerical_value(tok_answer):
    """
    Extracts the first numerical value from a list of tokens.
        :param tok_answer: A list of tokens.
        :return: The first numerical value found in the list, or an empty string if none is found.
    """
    for token in tok_answer:
        if token.isnumeric() or token[:-1].isnumeric():
            return token
    return ''

def process_numerical_question(question):
    """
    Processes a numerical question, prompting the user for an answer and returning a valid numerical value.
        :param question: A numerical question dictionary containing 'question' and 'prompt' keys.
        :return: The numerical value obtained from the user's answer.
    """
    print_question("Assistant:  " + question['question'])
    while True:
      answer = input('Assistant:  ' + question['prompt'] + '\nUser:       ')
      tok_answer = preprocess_answer(answer)
      value = get_numerical_value(tok_answer)
      if not value == '':
        return value
      elif answer.lower() == 'quit':
        print('Assistant:  ' + data['end_message'])
        sys.exit()
      else:
        return None

def process_multichoice_question(question, options):
    """
    Processes a multiple-choice question, prompting the user for an answer and returning a valid choice.
        :param question: A multiple-choice question dictionary containing 'question' and 'prompt' keys.
        :param options: A list of possible choices for the question.
        :return: The user's selected choice from the available options.
    """
    print_question("Assistant:  " + question['question'], options)
    while True:
      answer = input("Assistant:  " + question['prompt'] + '\nUser:       ' )
      if answer in options:
       return answer
      elif answer.lower() == 'quit':
        print('Assistant:  ' + data['end_message'])
        sys.exit()
      else:
        print("Assistant:  I'm sorry, but the answer is not among the available options.")
        return None


def find_suitable_houses(data, user_preferences):
    """
    Finds suitable houses in the given data based on user preferences.
        :param data: A dictionary containing information about available houses.
        :param user_preferences: A dictionary representing the user's preferences.
        :return: A list of suitable houses that match the user's preferences.
    """
    suitable_houses = []  # Suitable houses for the user
    keys =  user_preferences.keys()

    for house in data["houses"]:  # For each house
        is_suitable = True

        for key in keys:
            if  (key in house and house[key] == user_preferences[key])  or \
                (key not in house) or \
                (key in ['floor', 'rent'] and int(house[key]) in user_preferences[key]):
                pass
            
            else:
                is_suitable = False
                break
        
        if is_suitable:
            suitable_houses.append(house)  # Suitable answer

    return suitable_houses


def print_suitable_houses(suitable_houses):
    """
    Prints information about suitable houses based on user preferences.
        :param suitable_houses: A list of suitable houses to be printed.
    """
    if suitable_houses:
        print("\nAssistant:  Based on your preferences, the most suitable houses are:")
        
        for house in suitable_houses:

            print(f"    House ID: {house['id']}")
            print(f"    Type: {house['type']}")
            print("     Bedrooms:", house['bedrooms'])
            print("     Bathrooms:", house['bathrooms'])
            
            if 'rent' in house:
                print("     Price:", house['rent'], "€")
            else:
                print("     Price:", house['price'], "€")

            print("     Square Meters:", house['square_meters'], "m^2")
            print("     Location:", house['location'])
            print("     Elevator:", house['elevator'])
            print("     Terrace:", house['terrace'])
            print("     Floor:", house['floor'])
            print()
    else:
        print("\nAssistant:  Sorry, no suitable houses match your preferences. \n")
