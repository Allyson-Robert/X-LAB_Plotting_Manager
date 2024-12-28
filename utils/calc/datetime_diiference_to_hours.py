def datetime_difference_to_hours(datetime_difference):
    time_in_seconds = datetime_difference.total_seconds()
    division = divmod(time_in_seconds, 3600)
    return division[0] + division[1]/3600
