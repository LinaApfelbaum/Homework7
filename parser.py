
QUOTE_REPLACE = "==**=="

def parse_log_line(line):
    line = line.replace('\\"', QUOTE_REPLACE)

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
    line = line.lstrip()

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

    request_url = request_url.replace(QUOTE_REPLACE, '\\"')
    user_agent = user_agent.replace(QUOTE_REPLACE, '\\"')
    referrer = referrer.replace(QUOTE_REPLACE, '\\"')

    if response_length == '-':
        response_length = '0'

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
