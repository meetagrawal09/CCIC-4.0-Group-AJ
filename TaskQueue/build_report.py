from fpdf import FPDF


def build_table(data, report_name):
    pdf = FPDF()
    pdf.set_font_size(10)
    pdf.add_page()
    pdf.write_html(
        f"""<table border="1"><thead><tr>
        <th width="40%">{data[0][0]}</th>
        <th width="20%">{data[0][1]}</th>
        <th width="20%">{data[0][2]}</th>
        <th width="20%">{data[0][3]}</th>
    </tr></thead><tbody><tr>
        <td style="font-weight: bold">{'</td><td>'.join(data[1])}</td>
    </tr><tr>
        <td>{'</td><td>'.join(data[2])}</td>
    </tr><tr>
        <td>{'</td><td>'.join(data[3])}</td>
    </tr><tr>
        <td>{'</td><td>'.join(data[4])}</td>
    </tr></tbody></table>""",
        table_line_separators=True,
    )
    pdf.output(report_name)



data = (
    ("MARKET TURNOVER (USD Billion)"," "," "," "),
    ("Product", "Volume", "30D Avg",  "Basis in Pts (Chg) vs Fair"),
    ("Cash Equity", " ", " ", " "),
    ("Stock Futures", " ", " ", " "),
    ("Nifty Index", "", " ", " "),
    ("BankNifty Index", " ", " ", " "),
)
build_table(data, 'report.pdf')
