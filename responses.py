# File: responses.py

from fieutils import emote

# Fie is constantly watching what everyone says in the server. When certain messages
# are sent or are included in other messages, she will participate in the conversation.
# This function is in charge of mapping her answers to said trigger messages.

def get_response(user_input: str) -> str:
    if user_input == "best girl":
        return "Yeah that's me!"

    if any(msg in user_input for msg in ["hi fie", "hey fie"]):
        return f"Hey what's up {emote("WAVE")}"

    if any(msg in user_input for msg in ["thank you fie", "thanks fie"]):
        return f"At your service {emote("SALUTE")}"

    if any(msg in user_input for msg in
           ["good job fie",
            "good work fie",
            "nice job fie",
            "nice work fie"]):
        return f"Thanks~ {emote("BLUSHV")}"

    if emote("GRINV")} in user_input:
        return emote("GRINV")

    if "good night fie" in user_input:
        return f"Night night {emote("SLEEP")}"

    if "professorpd" in user_input:
        return f"ProfessorPd owns me {emote("PENSIVE")}"

    if "yuuyuu" in user_input:
        return f"He's a good boy {emote("RELAXED")}"

    if "good morning fie" in user_input:
        return f"Morning {emote("WAVE")}"

    # IDEA: Would be cool to somehow use some sports news outlet's API to get
    #       actual results of games here.

    if "fie gsw" in user_input:
        return "The Warriors are 9-2!"

    if "fie bulls" in user_input:
        return "The Bulls are 5-7! :("

    # Fie ain't taking blame on being mean ever >:)
    if "fie you're a meanie" in user_input:
        return "No u!"

    return "<empty>"
