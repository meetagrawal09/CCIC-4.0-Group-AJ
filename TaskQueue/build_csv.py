import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta
import zipfile 
import pandas as pd
import os
import glob
import csv
# from transformers import pipeline

def commentary_section_data():
    url = 'https://www.businesstoday.in/markets/market-commentary/'
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text, 'html.parser')

    divs = soup.find_all('div', class_='widget-listing-content-section')
    texts = []

    for div in divs:
        headlines = div.find('a')
        description = div.find('p')
        texts.append(headlines.contents[0]+' '+description.text)

    data = ' '.join(texts)
    new_split_data = data.split(' ')
    data_cleanup = [x for x in new_split_data if x]
    new_data = ' '.join(data_cleanup[0:650])

    model_name = 'sshleifer/distilbart-cnn-12-6'
    model_revision = 'a4f8f3e'
    summarizer = pipeline('summarization', model=model_name, revision=model_revision)
    summary = summarizer(new_data, max_length=200, min_length=100, do_sample=False)
    return summary[0]['summary_text']

def collect_news_data():
    url = 'https://economictimes.indiatimes.com/markets/indexsummary/indexid-13602,exchange-50.cms'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='syn')
    texts = [div.text for div in divs]

    model_name = 'sshleifer/distilbart-cnn-12-6'
    model_revision = 'a4f8f3e'
    summarizer = pipeline('summarization', model=model_name, revision=model_revision)
    for text in texts:
        if len(text) > 500:
            summary = summarizer(text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
            text = text.replace(summary, '')

    return texts

############################################################################################################
   
def get_date_csv(file_no):
    date1 = datetime.datetime.now().strftime("%d%m%Y")

    cur_day = date.today()
    check_date = cur_day - timedelta(days=file_no)

    # print('date used xls -> ',check_date)
    datetime_obj = datetime.datetime.strptime(str(check_date), '%Y-%m-%d')
    formatted_date = datetime_obj.strftime('%d%m%Y')
    # print('formated csv -> ',formatted_date)

    # if(int(date1[:2])-file_no < 10):
    #    date1 = '0'+str(int(date1[:2])-file_no)+date1[2:]
    # else:
    #     date1 = str(int(date1[:2])-file_no)+date1[2:]
    # print('date used csv->',date1)
    return formatted_date

def get_date_xls(file_no):
    date1 = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%B")
    year = datetime.datetime.now().strftime("%Y")

    cur_day = date.today()
    check_date = cur_day - timedelta(days=file_no)

    # print('date used xls -> ',check_date)
    datetime_obj = datetime.datetime.strptime(str(check_date), '%Y-%m-%d')
    formatted_date = datetime_obj.strftime('%d-%B-%Y')

    # print('formated xls -> ',formatted_date)
    dat = ''
    if(int(date1)-file_no < 10):
        # dat = '0'+str(int(date1)-file_no)+'-'+month[:3]+'-'+year
        mydat = str(formatted_date)[:6]+str(formatted_date)[len(str(formatted_date))-5:]
    else:
        # dat = str(int(date1)-file_no)+'-'+month[:3]+'-'+year
        mydat = str(formatted_date)[:6]+str(formatted_date)[len(str(formatted_date))-5:]
    # print(str(int(date)-file_no)+'-'+month[:3]+'-'+year)
    # print('date use xls -> ',mydat)
    return mydat

def get_csv(url_name, file_name,file_no):
    url = url_name+get_date_csv(file_no)+'.csv'
    try:
        response = requests.get(url,timeout=10)
    except TimeoutError:
        print('today is holiday')
    else:
        response = requests.get(url)
        url_content = response.content
        csv_file = open(file_name, 'wb')
        csv_file.write(url_content)
        csv_file.close()
    
def get_zip(url_name,start):
    url = url_name+get_date_csv(start)+'.zip'
    response = requests.get(url,timeout=10)
    with open("file.zip", "wb") as f:
        f.write(response.content)
    zip_ref = zipfile.ZipFile("file.zip", "r")
    zip_ref.extractall("")
    zip_ref.close()

def get_xls(url_name, file_name,file_no):
    url = url_name+get_date_xls(file_no)+'.xls'
    # print('generated url for : ',get_date_xls(file_no), ' is :',url)
    try:
        response = requests.get(url,timeout=10)
    except TimeoutError:
        print('today is holiday')
    
    else:
        response = requests.get(url,timeout=10)
        if response.status_code == 200:
            # print('response for the mrkt_to is: ')
            # print(response)
            url_content = response.content
            xls_file = open(file_name, 'wb')
            xls_file.write(url_content)
            xls_file.close()
        else: 
            print('file not found :')

def get_trading_holidays():
    url = 'https://www.moneycontrol.com/markets/NSEholidays.php'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', {'class': 'OtherArticals'})
    table = div.find('table')
    rows = table.find_all('td', {'class': 'det'})

    trading_holidays = []
    for i in range(2, len(rows), 4):
        trading_holidays.append(rows[i].text)
    lis_trading_holidays = []
    for date_str in trading_holidays:
        datetime_obj = datetime.datetime.strptime(date_str, '%b %d, %Y')
        formatted_date = datetime_obj.strftime('%Y-%m-%d')
        lis_trading_holidays.append(formatted_date)
        # print(formatted_date)
    
    return lis_trading_holidays

def holidays(days_of_data):
    i = 1
    cur_day = date.today()
    calling_2_prevvalid_date = 0
    lis_holidays = get_trading_holidays()
    lis = []
    while(calling_2_prevvalid_date < days_of_data):
        check_date = cur_day - timedelta(days=i)
        # Check if the date is a weekday
        # holiday = lis_holidays.count(check_date)
        holiday = 0
        for st in lis_holidays:
            if st == str(check_date):
                holiday = 1
        if check_date.weekday() > 4 or holiday > 0:
            i = i+1
            print('date excluded is :',check_date)
            continue
        print('date under consideration is : ',check_date)
        lis.append(i)
        i = i+1
        calling_2_prevvalid_date = calling_2_prevvalid_date+1
    return lis

def insti_flow_csv(days_of_data):
    list_insti_flow = []#fpi_cash , fpi_index_futures , fpi_stock_futures , dii_sto
    path = os.getcwd()
    lis = holidays(days_of_data)
    make_csv_forlstm = [['date','fpi cash','fpi index futures values','fpistock futures value','dii stock future','dii index future','OI PCR']]
    
    for i in lis:
        temp_list = []
        temp_list.append(get_date_xls(i))
        print(' ---------- ',get_date_csv(i),' --------- ')
        name = 'fii_stats_'+str(i)+'.xls'
        get_xls('https://archives.nseindia.com/content/fo/fii_stats_',name,i)
        string = "fii*"+str(i)+".xls"
        csv_file = glob.glob(os.path.join(path, string))#list of files
        
        data_fii = pd.read_excel(csv_file[0],)
        
        data_arr_fii = data_fii.to_numpy()

        fpi_cash = 0
        for j in range(3,7):
            fpi_cash = fpi_cash + float(data_arr_fii[j][2]) - float(data_arr_fii[j][4])
        if(fpi_cash < 0):
            # print('fpi_cash ',str(fpi_cash*10/82.80))
            list_insti_flow.append(fpi_cash*10/82.80)
            temp_list.append(fpi_cash*10/82.80)
        else:
            # print('fpi_cash ','+'+str(fpi_cash*10/82.80))
            list_insti_flow.append(fpi_cash*10/82.80)
            temp_list.append(fpi_cash*10/82.80)

        FPI_index_futures = float(data_arr_fii[2][2]) - float(data_arr_fii[2][4])
        if(FPI_index_futures < 0 ):
            # print('FPI index futures value : ',str(FPI_index_futures*10/82.80))
            list_insti_flow.append(FPI_index_futures*10/82.80)
            temp_list.append(FPI_index_futures*10/82.80)
        else:
            # print('FPI index futures value : ','+'+str(FPI_index_futures*10/82.80))
            list_insti_flow.append(FPI_index_futures*10/82.80)
            temp_list.append(FPI_index_futures*10/82.80)
        
        FPI_stock_futures = float(data_arr_fii[14][2]) - float(data_arr_fii[14][4])
        if(FPI_stock_futures < 0):
            # print('FPI stock futures value : ',str(FPI_stock_futures*10/82.80))
            list_insti_flow.append(FPI_stock_futures*10/82.80)
            temp_list.append(FPI_stock_futures*10/82.80)
        else:
            # print('FPI stock futures value : ','+'+str(FPI_stock_futures*10/82.80))
            list_insti_flow.append(FPI_stock_futures*10/82.80)
            temp_list.append(FPI_stock_futures*10/82.80)

        #DII data
        dii_idx_fut_buy_val = float(data_arr_fii[2][2])/ float(data_arr_fii[2][1])
        dii_idx_fut_sell_val = float(data_arr_fii[2][4])/ float(data_arr_fii[2][3])
        dii_stk_fut_buy_val = float(data_arr_fii[14][2])/ float(data_arr_fii[14][1])
        dii_stk_fut_sell_val = float(data_arr_fii[14][4])/ float(data_arr_fii[14][3])    

        path = os.getcwd()
        name = 'fao_participant_vol_'+str(i)+'.csv'
        get_csv('https://archives.nseindia.com/content/nsccl/fao_participant_vol_',name,i)
        # get_csv('https://www1.nseindia.com/content/nsccl/fao_participant_vol_',name,i)
        string = "fao*vol*"+str(i)+".csv"
        csv_file = glob.glob(os.path.join(path, string))#list of files
        # print(csv_file[0])#check which files are fetched
        data_fao_vol = pd.read_csv(csv_file[0])
        data_arr_dii = data_fao_vol.to_numpy()
        # print(data_arr_dii)

        dii_stk_fut = float(data_arr_dii[2][3])*dii_stk_fut_buy_val - float(data_arr_dii[2][4])*dii_stk_fut_sell_val
        if(dii_stk_fut < 0):
            # print('DII Stock Future',dii_stk_fut*10/82.80)
            list_insti_flow.append(dii_stk_fut*10/82.80)
            temp_list.append(dii_stk_fut*10/82.80)
        else:
            # print('DII Stock Future',dii_stk_fut*10/82.80)
            list_insti_flow.append(dii_stk_fut*10/82.80)
            temp_list.append(dii_stk_fut*10/82.80)

        dii_idx_fut = float(data_arr_dii[2][1])*dii_idx_fut_buy_val - float(data_arr_dii[2][2])*dii_idx_fut_sell_val
        if(dii_idx_fut < 0):
            # print('DII index Future',dii_idx_fut*10/82.80)
            list_insti_flow.append(dii_idx_fut*10/82.80)
            temp_list.append(dii_idx_fut*10/82.80)
        else:
            # print('DII index Future',dii_idx_fut*10/82.80)
            list_insti_flow.append(dii_idx_fut*10/82.80)
            temp_list.append(dii_idx_fut*10/82.80)

        # dii_cash = 0
        # for j in range(2,6):
        #     dii_cash = dii_cash + float(data_arr_dii[j][2]) - float(data_arr_dii[j][4])

        #Cal. OI_pCR from fao_participant_oi.csv
        path = os.getcwd()
        name = 'fao_participant_oi_'+str(i)+'.csv'#############################
        # According to new Changes made in NSE website
        get_csv('https://archives.nseindia.com/content/nsccl/fao_participant_oi_',name,i)
        # Based on previous NSE website
        # get_csv('https://www1.nseindia.com/content/nsccl/fao_participant_oi_',name,i)
        string = "fao*oi*"+str(i)+".csv"
        csv_file = glob.glob(os.path.join(path, string))#list of files
        # print(csv_file[0])#check which files are fetched
        data_fao_oi = pd.read_csv(csv_file[0])
        data_arr_oi = data_fao_oi.to_numpy()
        put,call = 0,0
        for j in range(5,13):
            if(j % 2 == 1):
                call = call + int(data_arr_oi[5][j])
            else:
                put = put + int(data_arr_oi[5][j])
        # print('OI PCR ',put/call)
        list_insti_flow.append(put/call)
        temp_list.append(put/call)
        make_csv_forlstm.append(temp_list)
    
    #################### creating csv file ###############
    print(make_csv_forlstm)
    filename = 'inputforlstm.csv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in make_csv_forlstm:
            writer.writerow(row)
    ################ make csv file code ends here ###############   
    for i in lis:
        list_insti_flow.append(get_date_xls(i))

    return list_insti_flow
