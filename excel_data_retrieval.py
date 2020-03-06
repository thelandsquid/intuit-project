import xlrd
def get_labels_from_excel(file_path,sheet_no,starting_row,row_amount):
    labels = []
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(sheet_no)
    for i in range(row_amount):
        labels.append(remove_label_and_marks(str(sheet.row_slice(starting_row+i,0,sheet.row_len(starting_row+i))[1:])))
    return labels

# Removed labels added by excel document and removed decimals from integers (some numbers with .0 at end are integers in the W-2)
def remove_label_and_marks(str):
    builtString = ''
    insideString = False
    for c in range(len(str)):
        if (str[c] == '\''):
            builtString += ' '*insideString
            insideString = not insideString
        elif insideString:
            builtString+=str[c]
    return builtString