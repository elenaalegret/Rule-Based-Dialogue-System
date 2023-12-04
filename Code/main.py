
"""
Títol: Sistema de Diàleg basat en Regles
Descripción: Assistent de compra d'habitatges on el sistema identifica i mostra les
             cases que coincideixin amb les preferències del usuari.
Autor: Elena Alegret i Júlia Orteu
Data: 20 de setembre 2023
"""
from funcions import *
user_preferences, available_options = {}, {}
initialize_available_options(data, available_options)

while True:
    print("Assistant: ", data['start_message'])
    for question in data['questions']:

        answer_key = question['answer_key']
        possible_options = list(available_options.get(answer_key))

        # Preguntes numèriques
        if question['type'] == 'numerical':
            min_max = [int(house[answer_key]) for house in data['houses']]
            question['prompt']  = question['prompt'].format(minim=min(min_max), maxim=max(min_max))
            answer = process_numerical_question(question)
        
        # Preguntes multiple choise
        else:
            answer = process_multichoice_question(question, possible_options)

        # Gestió de les respostes
        if answer:
            if answer_key in ['terrace', 'elevator', 'commercial_use'] and answer != 'No':
                user_preferences[answer_key] = answer
            
            elif answer_key == 'floor':
                user_preferences[answer_key] = set(range(int(answer), max(min_max) + 1))
            
            # Si l'usuari només està interessat en un lloguer de l'habitatge
            elif answer_key == 'type' and answer == 'rent':
                user_preferences[answer_key] = answer
                prompt = input("Assistant: As you've opted for renting, could you please provide your monthly household income? \nUser:       ")
                
                # Bucle que continua fins que l'usuari introdueix un valor numèric vàlid
                while True:
                    try:
                        house_hold_income = int(prompt) * 0.35
                        break  # Sortim del bucle si l'usuari introdueix un valor vàlid
                    except ValueError:
                        prompt = input("Assistant: Please provide a valid numerical value. Try again: \nUser:       ")
                
                # Establim l'interval de lloguer basat en l'ingrés proporcionat
                user_preferences['rent'] = set(range(0, int(house_hold_income)))
                print(f"Assistant: Thank you for sharing your household income.\nWe will now display rental options that fit within your recommended maximum monthly rent of {house_hold_income} €")
                break
            
            else:
                user_preferences[answer_key] = answer
        
        # L'usuari no ha seleccionat cap opció de 'type'
        elif answer_key == 'type':
            print("Assistant: You're welcome to browse through our listings, which include houses available for both sale and rent.")

    # Mostrar cases adequades
    suitable_houses = find_suitable_houses(data, user_preferences)
    print_suitable_houses(suitable_houses)

    repeat = input("Assistant: Would you like to search for something different? \nUser:       ")
    
    if 'yes' not in repeat.lower() :
        break

print("Assistant: ", data['end_message'])



