from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def make_excel(invoice, output_path="invoice.xlsx"):
    """
    invoice = your Pydantic Invoice model
    - invoice.supplier: str
    - invoice.date: str
    - invoice.items: list[LineItem] -> description, quantity, price, total
    - invoice.total_amount: float
    Returns path to the Excel file
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"

    header_fill = PatternFill("solid", fgColor="1A3A5C")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    title_font = Font(bold=True, size=14)
    total_font = Font(bold=True, size=12)
    total_fill = PatternFill("solid", fgColor="EEEEEE")
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    # 1. Title
    ws["A1"] = f"Invoice - {invoice.supplier} - {invoice.date}"
    ws["A1"].font = title_font
    ws.merge_cells("A1:D1")
    ws.row_dimensions[1].height = 25

    # 2. Headers - ENGLISH
    headers = ["Description", "Qty", "Price", "Total"]
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    ws.row_dimensions[3].height = 22

    # 3. Items
    row = 4
    for item in invoice.items:
        c1 = ws.cell(row=row, column=1, value=item.description)
        c2 = ws.cell(row=row, column=2, value=item.quantity)
        c3 = ws.cell(row=row, column=3, value=item.price)
        c4 = ws.cell(row=row, column=4, value=item.total)

        c3.number_format = '#,##0.00 "EUR"'
        c4.number_format = '#,##0.00 "EUR"'

        c2.alignment = Alignment(horizontal="center")
        c3.alignment = Alignment(horizontal="right")
        c4.alignment = Alignment(horizontal="right")

        for c in [c1, c2, c3, c4]:
            c.border = thin_border

        if row % 2 == 0:
            for c in [c1, c2, c3, c4]:
                c.fill = PatternFill("solid", fgColor="F2F2F2")

        row += 1

    # 4. Total row
    ws.cell(row=row, column=1, value="")
    ws.cell(row=row, column=2, value="")
    label = ws.cell(row=row, column=3, value="TOTAL")
    label.font = total_font
    label.alignment = Alignment(horizontal="right")
    label.fill = total_fill
    label.border = thin_border

    total_cell = ws.cell(row=row, column=4, value=invoice.total_amount)
    total_cell.font = total_font
    total_cell.number_format = '#,##0.00 "EUR"'
    total_cell.alignment = Alignment(horizontal="right")
    total_cell.fill = total_fill
    total_cell.border = thin_border

    # 5. Pretty - widths, filter, freeze
    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 15
    ws.auto_filter.ref = f"A3:D{row-1}"
    ws.freeze_panes = "A4"
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    wb.save(output_path)
    return output_path
