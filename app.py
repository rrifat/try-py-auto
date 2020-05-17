import xlsxwriter

request_str = "createRecharge Req"
response_str = "createRecharge Resp"
power_gateway = "power-gateway provider"

workbook = xlsxwriter.Workbook("demo.xlsx")
worksheet = workbook.add_worksheet()

lines = []
with open("files/ids.txt") as f_n:
    for line in f_n.readlines():
        lines.append(line.strip())

i = 1
j = 1

for msg_id in lines:
    with open("files/catalina.2020-04-13.out", "r") as f:
        for line in f:
            if msg_id in line and request_str in line:
                exec_str = line.split()[3]
                demand_str = exec_str.replace("[", "").replace("]", "")
                id_c = "A" + str(i)
                d_c = "B" + str(j)
                worksheet.write(id_c, msg_id)
                worksheet.write(d_c, line)
                for line_2 in f:
                    if demand_str in line_2 and response_str in line_2:
                        j = j + 1
                        d_c = "B" + str(j)
                        worksheet.write(d_c, line_2)
                        break
                    elif demand_str in line_2 and power_gateway in line_2:
                        j = j + 1
                        d_c = "B" + str(j)
                        worksheet.write(d_c, line_2)
                        break
                i = i + 2
                j = j + 1
workbook.close()
