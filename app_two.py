from openpyxl import load_workbook

file = "files/token_import.xlsx"
workbook = load_workbook(file)

meters = []
sheet = workbook.active

for i in range(1, len(sheet["A"])):
    meter_no = sheet["A"][i]
    if meter_no.value in meters:
        ptr += 1
        sheet[f"C{i + 1}"].value = ptr
    else:
        ptr = 1
        sheet[f"C{i + 1}"].value = ptr
        meters.append(meter_no.value)

workbook.save(file)
