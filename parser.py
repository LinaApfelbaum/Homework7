class LogsParser:
    def parse(self, files):
        slowest_requests_rate = 3
        top_ip_rate = 3
        requests_counter = 0
        request_methods_counter = {}
        requests_by_ip_counter = {}
        slowest_requests = []

        for file_name in files:
            with open(file_name) as file:
                for line in file:
                    line = line.rstrip()
                    requests_counter += 1
                    log_record = parse_log_line(line)

                    if log_record["request_method"] not in request_methods_counter:
                        request_methods_counter[log_record["request_method"]] = 1
                    else:
                        request_methods_counter[log_record["request_method"]] += 1

                    if log_record["ip"] not in requests_by_ip_counter:
                        requests_by_ip_counter[log_record["ip"]] = 1
                    else:
                        requests_by_ip_counter[log_record["ip"]] += 1

                    if len(slowest_requests) < slowest_requests_rate:
                        slowest_requests.append(log_record)
                        slowest_requests = sorted(slowest_requests, reverse=True,
                                                  key=lambda record: record["response_time"])
                    else:
                        last_element = slowest_requests[len(
                            slowest_requests) - 1]
                        if log_record["response_time"] > last_element["response_time"]:
                            slowest_requests.append(log_record)
                            slowest_requests = sorted(slowest_requests, reverse=True,
                                                      key=lambda record: record["response_time"])[:slowest_requests_rate]

        top_ip_list = sorted(
            requests_by_ip_counter, key=requests_by_ip_counter.get, reverse=True)[:top_ip_rate]

        return {
            "requests_counter": requests_counter,
            "request_methods_counter": request_methods_counter,
            "requests_by_ip_counter": requests_by_ip_counter,
            "slowest_requests": slowest_requests,
            "top_ip_list": top_ip_list
        }


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
