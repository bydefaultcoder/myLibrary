def format_time(hour):
    if hour < 0 or hour > 23:
        return "Invalid hour. Please provide a number between 0 and 23."

    # Determine AM/PM and corresponding time period
    if hour == 0:
        period = "12 AM"
        time_of_day = "midnight"
    elif hour < 12:
        period = f"{hour} AM"
        if 4 <= hour < 12:
            time_of_day = "morning"
        else:
            time_of_day = "night"
    elif hour == 12:
        period = "12 PM"
        time_of_day = "noon"
    else:
        period = f"{hour - 12} PM"
        if 12 < hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 20:
            time_of_day = "evening"
        else:
            time_of_day = "night"

    return f"{period} {time_of_day}"