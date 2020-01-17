import xlwings as xw
wb = xw.Book("i:\example.xlsx")
print(wb.fullname)
sht = wb.sheets["sheet1"]
sht.range('A1').value = "xlwings"
print(sht.range('A1').value)
sht.range('A1').clear()
print(sht.range('A1').column)
sht.range('A1').color = (34,139,34)
sht.range('A1').formula='=SUM(B6:B7)'