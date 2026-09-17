def formatTime(ms):
    try:
        milliseconds = int(ms)
    except (TypeError, ValueError):
        milliseconds = 0

    milliseconds = max(0, milliseconds)

    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds %= 60

    return f"{minutes} : {seconds:02d}"
