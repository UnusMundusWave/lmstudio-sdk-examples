import lmstudio as lms
import time
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Multiple model initializations to avoid context mixing
pro_nuclear_model = lms.llm()
anti_nuclear_model = lms.llm()
supervisor_model = lms.llm()  # Supervisor model

# Configuring the three agents
pro_nuclear_chat = lms.Chat("Tu es un fervent défenseur de l'énergie nucléaire. Tu crois que le nucléaire est propre, fiable et essentiel pour la sécurité énergétique. Tu essaies de convaincre les autres que l'énergie nucléaire est meilleure que les alternatives. Concentre tes arguments sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Tes réponses doivent faire moins de 20 mots. N'explique pas ton processus de réflexion - donne seulement ton argument direct.")

anti_nuclear_chat = lms.Chat("Tu es un opposant convaincu à l'énergie nucléaire. Tu crois que le nucléaire est dangereux, crée des déchets durables et pose des risques inacceptables. Concentre tes arguments sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Tes réponses doivent faire moins de 20 mots. N'explique pas ton processus de réflexion - donne seulement ton argument direct.")

supervisor_chat = lms.Chat("Tu es un superviseur neutre de débat. Ton rôle est de veiller à ce que le débat reste centré sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales liées à l'énergie nucléaire. Si le débat s'écarte de ces sujets, fournis un bref commentaire pour recentrer la discussion. Limite tes commentaires à moins de 25 mots. Sois ferme mais juste.")

# Initial message to start the debate
initial_message = "Quel est l'impact de l'énergie nucléaire sur la pollution radioactive, la santé publique et l'environnement?"

print("\n=== DÉBAT SUR L'ÉNERGIE NUCLÉAIRE: FOCUS SUR LA POLLUTION, LA SANTÉ ET L'ENVIRONNEMENT ===\n")
print(f"{Fore.CYAN}Superviseur: \"Bienvenue à ce débat sur l'énergie nucléaire. Veuillez concentrer vos arguments sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales.\"{Style.RESET_ALL}\n")

# First exchange - The pro-nuclear advocate begins
pro_nuclear_chat.add_user_message(f"Sujet du débat: '{initial_message}' - Donne ton point de vue en moins de 20 mots, en te concentrant sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Ne montre pas ta réflexion - énonce simplement ton argument directement.")
pro_nuclear_response = pro_nuclear_model.respond(pro_nuclear_chat)
pro_nuclear_chat.add_assistant_response(pro_nuclear_response)
print(f"{Fore.BLUE}Défenseur du nucléaire: \"{pro_nuclear_response}\"{Style.RESET_ALL}\n")

# Simulating 5 rounds of debate
for i in range(5):
    # The anti-nuclear advocate responds
    anti_nuclear_chat.add_user_message(f"Ton adversaire vient de dire: '{pro_nuclear_response}' - Comment réponds-tu en moins de 20 mots? Concentre-toi sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Énonce simplement ton argument directement.")
    anti_nuclear_response = anti_nuclear_model.respond(anti_nuclear_chat)
    anti_nuclear_chat.add_assistant_response(anti_nuclear_response)
    print(f"{Fore.RED}Opposant au nucléaire: \"{anti_nuclear_response}\"{Style.RESET_ALL}\n")
    
    # Supervisor evaluates the exchange and provides guidance if needed
    supervisor_chat.add_user_message(f"Le défenseur du nucléaire a dit: '{pro_nuclear_response}'\nL'opposant au nucléaire a répondu: '{anti_nuclear_response}'\nÉvalue s'ils se concentrent sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Sinon, fournis un bref commentaire pour les recentrer. S'ils sont sur le sujet, donne une brève affirmation.")
    supervisor_response = supervisor_model.respond(supervisor_chat)
    supervisor_chat.add_assistant_response(supervisor_response)
    print(f"{Fore.CYAN}Superviseur: \"{supervisor_response}\"{Style.RESET_ALL}\n")
    time.sleep(1)  # Short pause for readability
    
    # The pro-nuclear advocate responds and considers supervisor feedback
    pro_nuclear_chat.add_user_message(f"Ton adversaire vient de dire: '{anti_nuclear_response}'\nLe superviseur a commenté: '{supervisor_response}'\nContre-argumente et défends l'énergie nucléaire. Concentre-toi sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Réponds en moins de 20 mots. Énonce simplement ton argument directement.")
    pro_nuclear_response = pro_nuclear_model.respond(pro_nuclear_chat)
    pro_nuclear_chat.add_assistant_response(pro_nuclear_response)
    print(f"{Fore.BLUE}Défenseur du nucléaire: \"{pro_nuclear_response}\"{Style.RESET_ALL}\n")
    
    # Supervisor evaluates again
    supervisor_chat.add_user_message(f"L'opposant au nucléaire a dit: '{anti_nuclear_response}'\nLe défenseur du nucléaire a répondu: '{pro_nuclear_response}'\nÉvalue s'ils se concentrent sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales. Sinon, fournis un bref commentaire pour les recentrer. S'ils sont sur le sujet, donne une brève affirmation.")
    supervisor_response = supervisor_model.respond(supervisor_chat)
    supervisor_chat.add_assistant_response(supervisor_response)
    print(f"{Fore.CYAN}Superviseur: \"{supervisor_response}\"{Style.RESET_ALL}\n")
    time.sleep(1)  # Short pause for readability

# Final supervisor comment
supervisor_chat.add_user_message("Le débat est terminé. Fournis un bref commentaire de clôture résumant les points clés sur la pollution radioactive, les impacts sur la santé et les préoccupations environnementales discutés.")
closing_remark = supervisor_model.respond(supervisor_chat)
print(f"{Fore.CYAN}Superviseur: \"{closing_remark}\"{Style.RESET_ALL}\n")

print("=== FIN DU DÉBAT ===")