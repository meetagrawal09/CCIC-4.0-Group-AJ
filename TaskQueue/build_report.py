from fpdf import FPDF
from tasks import commentary_section_data, collect_news_data, opt_flow, insti_flow, market_to

def build_news_section(pdf, news_data):

    pdf.write_html("""
        <font color="#0000ff"><p>***Market Commentary - Intended for Institutional Clients Only***</p></font>
    """)
    
    commentary = commentary_section_data()

    pdf.set_font('helvetica','',10)
    pdf.multi_cell(0, 5, commentary)

    pdf.write_html("""
        <h5><b>NEWS</b></h5>
    """)

    for element in news_data:
        pdf.multi_cell(0, 5, element)
        pdf.ln()

    pdf.write_html("""
        <h5><b>MARKET TURNOVER</b></h5>
    """)

    market_turnover_data = market_to()

    pdf.write_html(
        f"""<table border="1">
                <thead>
                    <tr>
                        <th width="50%">Category</th>
                        <th width="50%">{market_turnover_data[3]}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Stock Future</td>
                        <td>{market_turnover_data[0]}</td>
                    </tr>
                    <tr>
                        <td>Nifty</td>
                        <td>{market_turnover_data[1]}</td>
                    </tr>
                    <tr>
                        <td>BankNifty</td>
                        <td>{market_turnover_data[2]}</td>
                    </tr>
                </tbody>
            </table>""",
        table_line_separators=True,
    )



    pdf.write_html("""
        <h5><b>INSTITUTIONAL FLOW</b></h5>
    """)

    i_flow_data = insti_flow()

    pdf.write_html(
        f"""<table border="1">
                <thead>
                    <tr>
                        <th width="33%">Category</th>
                        <th width="33%">{i_flow_data[12]}</th>
                        <th width="33%">{i_flow_data[13]}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>FPI Cash</td>
                        <td>{i_flow_data[0]}</td>
                        <td>{i_flow_data[6]}</td>
                    </tr>
                    <tr>
                        <td>FPI Index future value</td>
                        <td>{i_flow_data[1]}</td>
                        <td>{i_flow_data[7]}</td>
                    </tr>
                    <tr>
                        <td>FPI stock future value</td>
                        <td>{i_flow_data[2]}</td>
                        <td>{i_flow_data[8]}</td>
                    </tr>
                    <tr>
                        <td>DII stock future value</td>
                        <td>{i_flow_data[3]}</td>
                        <td>{i_flow_data[9]}</td>
                    </tr>
                    <tr>
                        <td>Dii index future value</td>
                        <td>{i_flow_data[4]}</td>
                        <td>{i_flow_data[10]}</td>
                    </tr>
                    <tr>
                        <td>OI PCR</td>
                        <td>{i_flow_data[5]}</td>
                        <td>{i_flow_data[11]}</td>
                    </tr>
                </tbody>
            </table>""",
        table_line_separators=True,
    )

    pdf.write_html("""
        <h5><b>OPTION FLOWS</b></h5>
    """)

    opt_flow_data = opt_flow()

    pdf.write_html(
        f"""<table border="1">
                <thead>
                    <tr>
                        <th width="25%">Category</th>
                        <th width="25%">{opt_flow_data[8]}</th>
                        <th width="25%">{opt_flow_data[9]}</th>
                        <th width="25%">1D Change</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>FPI call Option</td>
                        <td>{opt_flow_data[0]}</td>
                        <td>{opt_flow_data[4]}</td>
                        <td>{abs(opt_flow_data[0]-opt_flow_data[4])}</td>
                    </tr>
                    <tr>
                        <td>FPI put Option</td>
                        <td>{opt_flow_data[1]}</td>
                        <td>{opt_flow_data[5]}</td>
                        <td>{abs(opt_flow_data[1]-opt_flow_data[5])}</td>
                    </tr>
                    <tr>
                        <td>DII call Option</td>
                        <td>{opt_flow_data[2]}</td>
                        <td>{opt_flow_data[6]}</td>
                        <td>{abs(opt_flow_data[2]-opt_flow_data[6])}</td>
                    </tr>
                    <tr>
                        <td>DII put Option</td>
                        <td>{opt_flow_data[3]}</td>
                        <td>{opt_flow_data[7]}</td>
                        <td>{abs(opt_flow_data[3]-opt_flow_data[7])}</td>
                    </tr>
                </tbody>
            </table>""",
        table_line_separators=True,
    )

    pdf.write_html(f"""<table border="1">
                <tbody>
                    <tr>
                        <th colspan="2">Information</th>
                    </tr>
                    <tr>
                        <td width="25%"><font color="#0000FF">Source</font></td>
                        <td width="75%"><font color="#0000FF">Bloomberg & NSE for all data tables/data, Exchange data, CNBC and <br> other print media channels</font></td>
                    </tr>
                    <tr>
                        <td width="25%"><font color="#0000FF">Author(s)</font></td>
                        <td width="75%"><font color="#0000FF">XXX</font></td>
                    </tr>
                    <tr>
                        <td width="25%"><font color="#0000FF">Date</font></td>
                        <td width="75%"><font color="#0000FF">XXX</font></td>
                    </tr>
                </tbody>
            </table>""",
        table_line_separators=True,
    )

def build_reports(report_name):
    pdf = FPDF()
    pdf.add_page()
    data = collect_news_data()
    for i in range(len(data)):
        data[i] = data[i].replace('’','\'')
        data[i]= data[i].replace('“','\"')
        data[i]= data[i].replace('”','\"')
    build_news_section(pdf, [data[0], data[1], data[2]])
    
    pdf.output(report_name)

build_reports('report.pdf')
