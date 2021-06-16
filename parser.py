
def parse_log_line(line):
    cut_index = line.find(' ')
    ip = line[0:cut_index]
    line = line[cut_index+1:]

    cut_index = line.find('[')
    line = line[cut_index+1:]
    cut_index = line.find(']')
    date_time = line[0:cut_index]
    line = line[cut_index+3:]

    cut_index = line.find(' ')
    request_method = line[0:cut_index]
    line = line[cut_index+1:]

    cut_index = line.find(' ')
    request_url = line[0:cut_index]
    line = line[cut_index+1:]

    cut_index = line.find(' ')
    line = line[cut_index+1:]

    cut_index = line.find(' ')
    response_code = line[0:cut_index]
    line = line[cut_index+1:]

    cut_index = line.find(' ')
    response_length = line[0:cut_index]
    line = line[cut_index+1:]

    cut_index = line.find('"')
    line = line[cut_index+1:]

    cut_index = line.find('"')
    referrer = line[0:cut_index]
    line = line[cut_index+3:]

    cut_index = line.find('"')
    user_agent = line[0:cut_index]
    line = line[cut_index+2:]

    response_time = line

    return {
        "ip": ip,
        "date": date_time,
        "request_method": request_method,
        "request_url": request_url,
        "response_code": int(response_code),
        "response_length": int(response_length),
        "referrer": referrer,
        "user_agent": user_agent,
        "response_time": int(response_time)
    }
