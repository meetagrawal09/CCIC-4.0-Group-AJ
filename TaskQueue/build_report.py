from fpdf import FPDF
from tasks import collect_news_data

def build_table_section(data, pdf):
    page_width = pdf.w
    cell_width = page_width / 3
    html = '<table style="border-collapse: collapse; width: 100%;">'
    for row in data:
        html += '<tr>'
        for cell in row:
            html += f'<td style="border: 1px solid black; width: {cell_width}px;">{cell}</td>'
        html += '</tr>'
    html += '</table>'
    pdf.set_xy(10, 10)
    pdf.write_html(html, ln=True)

def build_news_section(pdf, data):

    pdf.write_html("""
        <font color="#0000ff"><p>***Market Commentary - Intended for Institutional Clients Only***</p></font>
        <h5><b>NEWS</b></h5>
    """)
    pdf.set_font('helvetica','',10)
    for element in data:
        pdf.multi_cell(0, 5, element)
        pdf.ln()

def build_reports(report_name):
    pdf = FPDF()
    pdf.add_page()
    data = collect_news_data()
    data[2] = data[2].replace('’','\'')
    build_news_section(pdf, [data[0], data[1], data[2]])
    
    pdf.output(report_name)

build_reports('report.pdf')
