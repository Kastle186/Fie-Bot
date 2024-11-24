# File: fiecommands.py

from datetime import datetime, timedelta, UTC
from fieutils import emote, help_msg, sylphid_greeting

import math
import statistics

# ********************************************************************************* #
# FIE UTILITIES FUNCTIONS:                                                          #
#                                                                                   #
# These are the helper functions for the non-game fie-commands (e.g. 'fie time').   #
# Try to name them after the commands they represent, if said commands are short    #
# enough. Like for 'fie time', the function's name would be fie_time(). Just to     #
# make it easier to navigate the code for debugging, extending, etc.                #
#                                                                                   #
# The exception to this rule is 'fie_response()', as that one handles Fie's replies #
# when someone says specific phrases in the server, rather than there being a       #
# command named 'fie response'.                                                     #
# ********************************************************************************* #

def fie_response(user_input: str) -> str:
    if user_input == "best girl":
        return "Yeah that's me!"

    if user_input == "fie":
        return sylphid_greeting()

    if user_input == "fie help":
        return help_msg()

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

    if emote("GRINV") in user_input:
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


def fie_time(dest_channel_id: int) -> str:
    # This is okay for now. If we want to add more timezones in the future, then
    # there are better approaches to take. And I'm getting a very cool idea but
    # need to cook it more :)
    utc = datetime.now(UTC)
    azores = utc - timedelta(hours=1)

    if dest_channel_id == 420709830622183434 or dest_channel_id == 420706417721475082:
        costa_rica = utc - timedelta(hours=6)
        egypt = utc + timedelta(hours=2)
        kuwait = utc + timedelta(hours=3)

        return (f"Costa Rica (UTC-6): {datetime_to_casual(costa_rica)}\n"
                f"Azores (UTC-1): {datetime_to_casual(azores)}\n"
                f"Egypt (UTC+2): {datetime_to_casual(egypt)}\n"
                f"Kuwait (UTC+3): {datetime_to_casual(kuwait)}")

    us_west = utc - timedelta(hours=8)
    us_east = utc - timedelta(hours=5)
    aus_west = utc + timedelta(hours=8)

    return (f"US West Coast (UTC-8): {datetime_to_casual(us_west)}\n"
            f"US East Coast (UTC-5): {datetime_to_casual(us_east)}\n"
            f"Azores (UTC-1): {datetime_to_casual(azores)}\n"
            f"UK (UTC+0): {datetime_to_casual(utc)}\n"
            f"Western Australia (UTC+8): {datetime_to_casual(aus_west)}")


def fie_solve(operation: str) -> str:
    # TODO: Handle incorrect data types. Right now, this function is unprotected
    #       against cases like 'fie solve 5 * lol'. So, we need to make sure all
    #       input operands are valid numbers.

    result = None
    tokens = operation.split()[2:]
    print(tokens)

    # If we have less than two tokens then we're either missing an operator or
    # the operands.
    if len(tokens) < 2:
        return f"Hey dummy, your operation '{" ".join(tokens)}' is malformed."

    # Cases starting with the operator or math function name.
    match tokens[0]:
        case "sqrt": result = math.sqrt(int(tokens[1]))
        case "mean" | "average": result = statistics.fmean(list(map(float, tokens[1:])))
        case _ if tokens[1] == "!": result = math.factorial(int(tokens[0]))

    # At this point, if we didn't match any of the above cases, then we only have
    # bi-operand operations left available. So, if we have less than 3 operands,
    # then the operation is incomplete, and if we have more than 3 operands, then
    # Fie won't like it :)

    if result == None:
        if len(tokens) < 3:
            return f"Hey dummy, your operation '{" ".join(tokens)}' is malformed."

        if len(tokens) > 3:
            return "Hey, my brain can only do so much at once! Give me a break :slight_frown:"

        # Cases starting with an operand.
        match tokens[1]:
            case "+": result = float(tokens[0]) + float(tokens[2])
            case "-": result = float(tokens[0]) - float(tokens[2])
            case "*": result = float(tokens[0]) * float(tokens[2])
            case "/": result = float(tokens[0]) / float(tokens[2])
            case "^": result = float(tokens[0]) ** float(tokens[2])
            case _: return f"Hey dummy, what is that '{tokens[1]}' operator?"

    return f"The result is {result}!"


def fie_days_until(target_day_msg: str) -> str:
    today = datetime.now()
    tokens = target_day_msg.split()[5:]
    days_until_msg = ""

    # A specific date was given, so calculate how long until or how long has passed
    # since said date.
    if len(tokens) > 0:
        target = datetime.strptime(tokens[0], "%d-%m-%Y")
        delta = target - today

        days_until_msg = \
            ({True: f"There are {delta.days + 1} days until {target}",
              False: f"{delta.days * (-1) + 1} days have passed since {target}"}) \
              [delta.days >= 0]

    # No specific date given, so Fie will show the days until or after some
    # important dates.
    else:
        christmas = datetime(today.year, 12, 25)
        christmas_msg = "Days until Christmas"

        # If Christmas has already passed this year, then Fie will tell how many
        # days left until next year's Christmas.
        until_christmas = \
            ({True: (christmas - today).days,
              False: (datetime(today.year + 1, 12, 25) - today).days}) \
              [christmas > today]

        daybreak2 = datetime(2025, 2, 14)
        until_daybreak2 = (daybreak2 - today).days

        daybreak2_msg = ({True: "Days until Daybreak II",
                          False: "Days since Daybreak II's launch"}) \
                          [daybreak2 > today]

        days_until_msg = (f"{christmas_msg}: {until_christmas}\n"
                          f"{daybreak2_msg}: {until_daybreak2}\n"
                          f"Days until Rean stops being dense: ∞")
    return days_until_msg


def fie_what_is(question_msg: str) -> str:
    tokens = question_msg.split()[2:]
    fun_fact = ""

    if len(tokens) == 0:
        return "What's what?"

    match tokens[0]:
        case "zemuria":
            fun_fact = ("Zemuria is the continent made up of 37 regions on which the"
                        " series takes place. It's the only known continent so far.")

        case "zemurian" if (len(tokens) > 1 and tokens[1] == "ore"):
            fun_fact = ("Zemurian Ore is an extremely rare material found in Zemuria."
                        " It's usually used in the series to craft very strong weapons!")

        case "zemurian":
            fun_fact = ("Zemurian is how the inhabitants and otherwise belonging beings"
                        " to the continent of Zemuria are known as.")

        case _:
            fun_fact = "Mmm... I will have to research that and get back to you later."

    return fun_fact

# **************************************************** #
# OTHER COMMAND UTILITIES:                             #
# Any other helper functions for the commands go here! #
# **************************************************** #

def datetime_to_casual(input_dt: datetime) -> str:
    return input_dt.strftime("%H:%M:%S")

