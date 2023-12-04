"""
Title: Functions for the Home Buying Assistant
Description: Set of functions for the rule-based dialogue system that identifies and displays homes based on user preferences.
Author: Elena Alegret and Júlia Orteu
Date: September 20, 2023
"""

# Requeriments
#nltk.data.path.append("http://nltk.github.com/nltk_data/")
#nltk.download('omw-1.4')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('punkt')


# Libraries importation
from nltk.tokenize.treebank import TreebankWordTokenizer
import nltk
from tkinter import *
from tkinter import simpledialog
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import json
import sys

class ChatbotManager:
    def __init__(self, txt, data):
        self.txt = txt
        self.data = data

    ## -- GUI Functions --
    def system_send(self, question, min = None, max = None):
        # Display the system's question and prompt
        self.txt.insert(END, "\n Assistant: "+ question['question'])
        self.txt.insert(END, "\n Assistant: "+ question['prompt'].format(minim=min, maxim=max))
        self.txt.see("end")
        
    def calculate_min_max(self, actual_question):
        # Calculate minimum and maximum values based on the current question
        answer_key = actual_question['answer_key']
        min_max = [int(house[answer_key]) for house in self.data['houses']]
        return min_max

    def user_send(self, user_message):
        # Display the user's message
        if user_message ==  None:
            pass
        else:
            self.txt.insert(END, "\n User: " + user_message)
            self.txt.see("end")
            return user_message

    # -- Library Functions --
    def send_available_options(self, possible_options=[]):
        """
        Sends a message with available options.
            :param possible_options: A list of possible options.
        """
        if possible_options:
            message = "Options: " + ", ".join(possible_options)
            self.txt.insert(END, "\n Assistant: " + message)
            self.txt.see("end")

    def initialize_available_options(self, available_options):
        """
        Initializes available options for each key in the house data.
            :param available_options: A dictionary to store available options for each key.
        """
        for house in self.data['houses']:
            for key, value in house.items():
                available_options.setdefault(key, set()).add(value)

    def preprocess_answer(self, answer):
        """
        Tokenizes and preprocesses an answer.
            :param answer: The answer to preprocess.
        :return: A preprocessed answer as a list of tokens.
        """
        answer = nltk.word_tokenize(answer)
        return answer

    def get_numerical_value(self, tok_answer):
        """
        Extracts the first numerical value from a list of tokens.
            :param tok_answer: A list of tokens.
        :return: The first numerical value found in the list, or an empty string if none is found.
        """
        for token in tok_answer:
            if token.isnumeric() or token[:-1].isnumeric():
                return token
        return ''

    def process_numerical_question(self, question):
        """
        Processes a numerical question, prompting the user for an answer and returning a valid numerical value.
            :param question: A numerical question dictionary containing 'question' and 'prompt' keys.
        :return: The numerical value obtained from the user's answer.
        """
        while True:
            answer = simpledialog.askstring("User entrance", "Insert your preference:")
            tok_answer = self.preprocess_answer(answer)
            value = self.get_numerical_value(tok_answer)
            
            if not value == '':
                return value
            elif answer.lower() == 'quit':
                self.txt.insert(END, "\n Assistant: " + self.data['end_message'])
                self.txt.see("end")
                sys.exit()
            else:
                return None

    def process_multichoice_question(self, question, options):
        """
        Processes a multiple-choice question, prompting the user for an answer and returning a valid choice.
            :param question: A multiple-choice question dictionary containing 'question' and 'prompt' keys.
            :param options: A list of possible choices for the question.
        :return: The user's selected choice from the available options.
        """
        self.send_available_options(options)
        
        while True:
            answer = simpledialog.askstring("User Input", "Insert your preference:")
            
            if answer in options:
                return answer
            elif answer.lower() == 'quit':
                self.txt.insert(END, "\n Assistant: " + self.data['end_message'])
                self.txt.see("end")
                sys.exit()
            else:
                self.txt.insert(END, "\n Assistant: I'm sorry, but the answer is not among the available options.")
                self.txt.see("end")
                return None

    def find_suitable_houses(self, user_preferences):
        """
        Finds suitable houses in the given data based on user preferences.
            :param user_preferences: A dictionary representing the user's preferences.
            :return: A list of suitable houses that match the user's preferences.
        """
        suitable_houses = []  # Suitable houses for the user
        keys =  user_preferences.keys()

        for house in self.data["houses"]:  # For each house
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


    def print_suitable_houses(self, suitable_houses):
        """
        Prints information about suitable houses based on user preferences.
            :param suitable_houses: A list of suitable houses to be printed.
        """
        if suitable_houses:

            self.txt.insert(END, "\n Assistant:  Based on your preferences, the most suitable houses are:")
            self.txt.see("end")
            
            for house in suitable_houses:
                
                self.txt.insert(END, "\n                                         ")
                self.txt.insert(END, "\n    House ID: " + str(house['id']) + "\n")
                self.txt.insert(END, "\n    Type: " + str(house['type']) + "\n")
                self.txt.insert(END, "\n    Bedrooms :" + str(house['bedrooms']) + "\n")
                self.txt.insert(END, "\n    Bathrooms :" + str(house['bathrooms']) + "\n")

                if 'rent' in house:
                    self.txt.insert(END, "\n    Price: " + str(house['rent'] + "€") + "\n")
                else:
                    self.txt.insert(END, "\n    Price: " + str(house['price'] + "€") + "\n")
                    self.txt.insert(END, "\n    Square Meters: " + str(house['square_meters']) + "m^2" + "\n")
                    self.txt.insert(END, "\n    Location: " + str(house['location']) + "\n")
                    self.txt.insert(END, "\n    Elevator: " + str(house['elevator']) + "\n")
                    self.txt.insert(END, "\n    Terrace: " + str(house['terrace']) + "\n")
                    self.txt.insert(END, "\n    Floor: " + str(house['floor']) + "\n")
                    self.txt.insert(END, "\n                                         ")
                    self.txt.insert(END, "\n ----------------------------------------")
                    self.txt.insert(END, "\n                                         ")
                    self.txt.see("end")

        else:
            self.txt.insert(END, "\n Assistant: Sorry, no suitable houses match your preferences. \n")
            self.txt.see("end")
