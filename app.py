import xlsxwriter
import json
import re


def get_message(line):
    l = re.findall(r"\{[^{}]+\}", line.strip())
    output_str = None
    if len(l) > 0:
        response_dict = json.loads(l[0])
        output_str = (
            f"{response_dict['RESPONSECODE']}: {response_dict['RESPONSECONTENT']}"
        )
    return output_str


request_str = "createRecharge Req"
response_str = "createRecharge Resp"
power_gateway = "power-gateway provider"

workbook = xlsxwriter.Workbook("demo.xlsx")
worksheet = workbook.add_worksheet()

ids = []
with open("files/ids.txt") as f_n:
    for line in f_n.readlines():
        ids.append(line.strip())

i = 1
j = 1

for msg_id in ids:
    with open("files/catalina.2020-04-13.out", "r") as f:
        for line in f:
            if msg_id in line and request_str in line:
                exec_str = line.split()[3]
                demand_str = exec_str.replace("[", "").replace("]", "")
                id_c = "A" + str(i)
                d_c = "E" + str(j)
                worksheet.write(id_c, msg_id)
                worksheet.write(d_c, line)
                for line_2 in f:
                    if demand_str in line_2 and response_str in line_2:
                        j = j + 1
                        d_c = "E" + str(j)
                        worksheet.write(d_c, line_2)
                        worksheet.write("B" + str(j), get_message(line_2))
                        break
                    elif demand_str in line_2 and power_gateway in line_2:
                        j = j + 1
                        d_c = "E" + str(j)
                        worksheet.write(d_c, line_2)
                        worksheet.write("B" + str(j), get_message(line_2))
                        break
                i = i + 2
                j = j + 1
workbook.close()
