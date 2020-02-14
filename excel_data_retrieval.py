import xlrd
def get_labels_from_excel(file_path,sheet_no,starting_row,row_amount):
    labels = []
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(sheet_no)
    for i in range(row_amount):
        labels.append(sheet.row_slice(starting_row+i,0,sheet.row_len(starting_row+i)))
    return labels