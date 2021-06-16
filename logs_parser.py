import sys
from pathlib import Path
import glob

from parser import parse_log_line

if len(sys.argv) != 2:
    print("Usage:\n python logs_parser.py logs_directory\n or\n python logs_parser.py path_to_log.log")
    exit(1)

files_list = []
path = Path(sys.argv[1])
if path.is_file():
    files_list.append(sys.argv[1])
elif path.is_dir():
    files_list = glob.glob(sys.argv[1] + "/*.log")
else:
    print(f"Error: {sys.argv[1]} is not valid file or directory")
    exit(1)


requests_counter = 0
request_methods_counter = {}
requests_by_ip_counter = {}
slowest_requests = []

for file_name in files_list:
    print(file_name)
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


            if len(slowest_requests) < 3:
                slowest_requests.append(log_record)
                slowest_requests = sorted(slowest_requests, reverse=True, key=lambda record: record["response_time"])
            else:
                for slow_request in slowest_requests:
                    if log_record["response_time"] > slow_request["response_time"]:
                        slowest_requests.append(log_record)
                        slowest_requests = sorted(slowest_requests, reverse=True, key=lambda record: record["response_time"])[:3]
                        break




top_ip_list = sorted(requests_by_ip_counter, key=requests_by_ip_counter.get, reverse=True)[:3]


print("Result:")
print("Total requests: " + str(requests_counter))
print("")
print("Requests by methods:")
for method in request_methods_counter:
    print(method + ": " + str(request_methods_counter[method]))
print("")
print("Top requests by IP:")
for ip in top_ip_list:
    print(ip + ": " + str(requests_by_ip_counter[ip]))
print("")
print("Top slowest requests:")
for slow_request in slowest_requests:
    print(
        "method: " + slow_request["request_method"] +
        " url: " + slow_request["request_url"] +
        " ip: " + slow_request["ip"] +
        " response time: " + str(slow_request["response_time"]))


# print(top_ip_list)
# print(requests_by_ip_counter)
# print(slowest_requests)