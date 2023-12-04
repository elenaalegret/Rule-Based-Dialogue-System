
"""
Title: Rule-Based Dialogue System
Description: Home buying assistant where the system identifies and displays houses that match the user's preferences.
Authors: Elena Alegret and Júlia Orteu
Date: September 20, 2023

"""

from tkinter import *
from tkinter import simpledialog
from funcions_interface import *

if __name__ == "__main__":
    # Create a Tkinter window for the chatbot
    root = Tk()
    root.title("House Buying Assistant")

    # Select the stetic background
    BG_GRAY, BG_COLOR, TEXT_COLOR = "#ABB2B9", "#17202A", "#EAECEE"

    FONT, FONT_BOLD = "Helvetica 14", "Helvetica 13 bold"

    # Create GUI elements
    label1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="🏠 Buying Assistant", font=FONT_BOLD, pady=10, width=20, height=1)
    label1.grid(row=0, columnspan=2)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=100, height=50) # Conversation text
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(root, command=txt.yview) # Create a vertical scrollbar
    scrollbar.grid(row=1, column=2, sticky='ns')
    txt.config(yscrollcommand=scrollbar.set)

    # Open the json file and download the data
    with open('./house_data.json') as f:
            data = json.load(f)

    chatbot_manager = ChatbotManager(txt, data)
    user_preferences, available_options = {}, {}
    chatbot_manager.initialize_available_options(available_options)

    while True:
        txt.insert(END, "\n Assistant: " + data['start_message'])
        
        for question in data['questions']:
            answer_key = question['answer_key']
            possible_options = list(available_options.get(answer_key))

            # Numerical questions
            if question['type'] == 'numerical':
                min_max = chatbot_manager.calculate_min_max(question) # Calculate min_max
                
                # Start numerical question and prompt
                chatbot_manager.system_send(question, min(min_max), max(min_max))
                answer = chatbot_manager.process_numerical_question(question)
                chatbot_manager.user_send(answer)
                txt.see("end")

            # Multiple choise questions
            else:
                # Start multiple-choice question
                txt.insert(END,"\n Assistant: " + question['question'] + "\n Assistant: " + question['prompt'])
                answer = chatbot_manager.process_multichoice_question(question, possible_options)
                chatbot_manager.user_send(answer)
                txt.see("end")

            # Handling user responses
            if answer:
                if answer_key in ['terrace', 'elevator', 'commercial_use'] and answer != 'No':
                    user_preferences[answer_key] = answer
                
                elif answer_key == 'floor':
                    user_preferences[answer_key] = set(range(int(answer), max(min_max) + 1))
                
                # If the user is interested in renting
                elif answer_key == 'type' and answer == 'rent':
                    user_preferences[answer_key] = answer
                    txt.insert(END, "\n Assistant: As you've opted for renting, could you please provide your monthly household income?")
                    txt.see("end")
                    
                    # Loop until the user provides a valid numeric value
                    while True:
                        try:
                            house_hold_income = simpledialog.askinteger("User Input", "Insert your preference:")
                            chatbot_manager.user_send(str(house_hold_income))
                            house_hold_income *=  0.35
                            break
                        
                        except ValueError:
                            txt.insert(END, "\n Assistant: Please provide a valid numerical value. Try again: ")
                            txt.see("end")
                            
                    # Set the rental range based on the provided income
                    user_preferences['rent'] = set(range(0, int(house_hold_income)))
                    message = (f" Assistnant: Thank you for sharing your household income. We will now display rental options that fit within your recommended maximum monthly rent of {str(house_hold_income)} €")
                    txt.insert(END, "\n Assistant: " + str(message))
                    txt.see("end")
                    break
                
                else:
                    user_preferences[answer_key] = answer
            
            # If the user didn't select any 'type' option
            elif answer_key == 'type':
                txt.insert(END, "\n You're welcome to browse through our listings, which include houses available for both sale and rent.")
                txt.see("end")
                
        # Suitable houses
        suitable_houses = chatbot_manager.find_suitable_houses(user_preferences)
        chatbot_manager.print_suitable_houses(suitable_houses)
        txt.see("end")
        txt.insert(END, "\n Assistant: Would you like to search for something different? ")
        txt.see("end")
        
        repeat = simpledialog.askstring("User Input", "Insert your preference:")
        chatbot_manager.user_send(repeat)
        
        if 'yes' not in repeat.lower():
            break
    
    txt.insert(END, f"\n Assistant: {data['end_message']}")
    txt.see("end")
    root.mainloop()
