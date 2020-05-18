import xlsxwriter
import json
import re

request_str = "createRecharge Req"
response_str = "createRecharge Resp"
power_gateway = "power-gateway provider"

log_file = "files/catalina.2020-04-13.out"
id_file = "files/ids.txt"
output_file = "demo.xlsx"

# Helpers
def get_message(line):
    l = re.findall(r"\{[^{}]+\}", line.strip())
    output_str = None
    if len(l) > 0:
        response_dict = json.loads(l[0])
        if "RESPONSECODE" in response_dict and "RESPONSECONTENT" in response_dict:
            output_str = (
                f"{response_dict['RESPONSECODE']}: {response_dict['RESPONSECONTENT']}"
            )
    return output_str


def get_responses(exec_str, file):
    for line in file:
        if exec_str in line and response_str in line:
            return [line, get_message(line)]
        if exec_str in line and power_gateway in line:
            return [line, get_message(line)]


def get_ids():
    ids = []
    with open(id_file, "r") as f:
        for line in f:
            ids.append(line.strip())
    return ids


# Main
ids = get_ids()

workbook = xlsxwriter.Workbook(output_file)
worksheet = workbook.add_worksheet()

id_row = 1

for msg_id in ids:
    with open(log_file, "r") as f:
        for line in f:
            if msg_id in line and request_str in line:
                exec_str = line.split()[3]

                worksheet.write("A" + str(id_row), msg_id)
                worksheet.write("E" + str(id_row), line)

                responses = get_responses(exec_str, f)
                response_line = responses[0]
                response_message = responses[1]

                response_row = id_row + 1

                worksheet.write("E" + str(response_row), response_line)
                worksheet.write("B" + str(response_row), response_message)

                id_row += 2

workbook.close()
