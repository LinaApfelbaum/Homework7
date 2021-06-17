import json
import sys
from pathlib import Path
import glob

from parser import LogsParser

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


parser = LogsParser()
results = parser.parse(files_list)

with open('results.txt', 'w') as outfile:
    json.dump(results, outfile, indent=2, sort_keys=True)


print("Result:")
print("Total requests: " + str(results["requests_counter"]))
print("")
print("Requests by methods:")
for method in results["request_methods_counter"]:
    print(method + ": " + str(results["request_methods_counter"][method]))
print("")
print("Top requests by IP:")
for ip in results["top_ip_list"]:
    print(ip + ": " + str(results["requests_by_ip_counter"][ip]))
print("")
print("Top slowest requests:")
for slow_request in results["slowest_requests"]:
    print(
        "method: " + slow_request["request_method"] +
        " url: " + slow_request["request_url"] +
        " ip: " + slow_request["ip"] +
        " response time: " + str(slow_request["response_time"]))
