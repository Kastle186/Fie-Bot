# File: fiecommands.py

from datetime import datetime, timedelta, UTC
from fieutils import datetime_to_casual

import math
import statistics

# ******************************************************************************* #
# FIE UTILITIES FUNCTIONS:                                                        #
# These are the helper functions for the non-game fie-commands (e.g. 'fie time'). #
# Try to name them after the commands they represent, if said commands are short  #
# enough. Like for 'fie time', the function's name would be fie_time(). Just to   #
# make it easier to navigate the code for debugging, extending, etc.              #
# ******************************************************************************* #

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

    return (f"US West Coast (UTC-8): {datetime_to_casual(us_west)}"
            f"US East Coast (UTC-5): {datetime_to_casual(us_east)}"
            f"Azores (UTC-1): {datetime_to_casual(azores)}"
            f"UK (UTC+0): {datetime_to_casual(utc)}"
            f"Western Australia (UTC+8): {datetime_to_casual(aus_west)}")


def fie_solve(operation: str) -> str:
    # TODO: Handle incorrect data types. Right now, this function is unprotected
    #       against cases like 'fie solve 5 * lol'. So, we need to make sure all
    #       input operands are valid numbers.

    result = 0
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

    # At this point, we only have bi-operand operations left available. So, if we
    # have less than 3 operands, then the operation is incomplete, and if we have
    # more than 3 operands, then Fie won't like it :)

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


def fie_days_until():
    pass


def fie_schedule():
    pass


def fie_what_is():
    pass

