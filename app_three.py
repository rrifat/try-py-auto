import xlsxwriter
import uuid

request_str = "createRecharge Req"
response_str = "createRecharge Resp"
power_gateway = "power-gateway provider"
power_purchase = "powerPurchase"

log_file = "files/catalina.2020-07-18.out"
id_file = "files/ids.txt"
output_file = f"{uuid.uuid1()}.xlsx"

# Helpers
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
visited_ids = []

for msg_id in ids:
    with open(log_file, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if msg_id in lines[i] and "response info" in lines[i + 1]:
                if msg_id not in visited_ids:
                    visited_ids.append(msg_id)
                    worksheet.write(f"A{id_row}", msg_id)
                worksheet.write(f"B{id_row}", lines[i + 1])
                id_row += 1

workbook.close()
