import random

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "best girl":
        return "yeah that's me"
    elif lowered == "fie":
        choice = random.randint(0,2)
        if choice == 0:
            return "Roger!"
        elif choice == 1:
            return "Ja!"
        elif choice == 2:
            return "Sylphid reporting in!"
    elif lowered == "fie help":
            return ("What a pain... here are the commands you can use\n"
                    "'fie rps' -> play rock paper scissors with yours truly\n"
                    "'fie time' -> I indicate the time of some of the members' timezones\n"
                    "'claussell' -> a random pic of me. Seriously you guys are obsessed\n"
                    "'fie' (with nothing added) -> Random greeting\n"
                    "'fie solve' -> I will solve some math problems... (+ - * / ! sqrt average)\n"
                    "'fie how many days until' -> relevant dates (feel free to ask for more)\n"
                    "'fie how many days until day-month-year' -> insert a date you want to calculate\n"
                    "'fie hangman' -> Come guess random trails words! ")

    elif "thank you fie" in lowered:
        return ("at your service :saluting_face:")
    elif "thanks fie" in lowered:
        return ("at your service :saluting_face:")
    elif "good night fie" in lowered:
        return "night night :sleeping:"
    elif "professorpd" in lowered:
        return ("ProfessorPd owns me :pensive:")
    elif "yuuyuu" in lowered:
        return ("He's a good boy :relaxed:")
    elif "hi fie" in lowered:
        return ("Hey what's up :wave:")
    elif "hey fie" in lowered:
        return ("Hey what's up :wave:")
    elif "good morning fie" in lowered:
        return ("morning :wave:")
    elif "good job fie" in lowered:
        return ("Thanks~ :blush::v:")
    elif "good work fie" in lowered:
        return ("Thanks~ ️:blush::v:")
    elif "nice job fie" in lowered:
        return ("Thanks~ ️:blush::v:")
    elif "nice work fie" in lowered:
        return ("Thanks~ :blush::v:️")
    elif ":grin: :v::️" in lowered:
        return(":grin::v:")
    elif "fie gsw" in lowered:
        return ("The Warriors are 9-2!")
    elif "fie bulls" in lowered:
        return ("The Bulls are 5-7! :(")
    elif "fie you're a meanie" in lowered:
        return("no u")
