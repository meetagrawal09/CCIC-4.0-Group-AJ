import requests
from bs4 import BeautifulSoup
import datetime
import zipfile 
import pandas as pd
import os
import glob
from transformers import pipeline

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
    date = datetime.datetime.now().strftime("%d%m%Y")
    date = str(int(date[:2])-file_no)+date[2:]
    print('date ',date)
    return date

def get_date_xls(file_no):
    date = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%B")
    year = datetime.datetime.now().strftime("%Y")
    dat = str(int(date)-file_no)+'-'+month[:3]+'-'+year
    print(str(int(date)-file_no)+'-'+month[:3]+'-'+year)
    return dat

def get_csv(url_name, file_name,file_no):
    url = url_name+get_date_csv(file_no)+'.csv'
    response = requests.get(url)
    url_content = response.content
    csv_file = open(file_name, 'wb')
    csv_file.write(url_content)
    csv_file.close()
    
def get_zip(url_name):
    url = url_name+get_date_csv(1)+'.zip'
    response = requests.get(url)
    with open("file.zip", "wb") as f:
        f.write(response.content)
    zip_ref = zipfile.ZipFile("file.zip", "r")
    zip_ref.extractall("")
    zip_ref.close()

def get_xls(url_name, file_name,file_no):
    url = url_name+get_date_xls(file_no)+'.xls'
    response = requests.get(url)
    url_content = response.content
    xls_file = open(file_name, 'wb')
    xls_file.write(url_content)
    xls_file.close()

def market_to():
        #Stock Futures
        list_market_turnover = []
        path = os.getcwd()
        # print(path)
        csv_file = glob.glob(os.path.join(path, "./data/fo_27122022.csv"))#list of files
        # print(csv_file)
        data_stkfut = pd.read_csv(csv_file[0])
        data_arr = data_stkfut.to_numpy()
        # print('Stock Futures in USD Billion ',float(data_arr[2])/8280)
        list_market_turnover.append(float(data_arr[2])/8280)
        # print(data)

        # Nifty
        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "./data/ind_close*.csv"))#list of files
        data_nifty = pd.read_csv(csv_file[0])
        data_arr = data_nifty.to_numpy()
        # print(data_arr[0][9])
        # print('Nifty Truenover in USD Billions ',float(data_arr[0][9])/8280)
        list_market_turnover.append(float(data_arr[0][9])/8280)
        #Bank Nifty 
        # print('Nifty Truenover in USD Billions ',float(data_arr[10][9])/8280)
        list_market_turnover.append(float(data_arr[10][9])/8280)

        date = datetime.datetime.now().strftime("%d")
        month = datetime.datetime.now().strftime("%B")
        dat = str(int(date)-1)+'-'+month[:3]
        # print(dat)
        list_market_turnover.append(dat)
        
        return list_market_turnover

def insti_flow():
    list_insti_flow = []#fpi_cash , fpi_index_futures , fpi_stock_futures , dii_sto
    path = os.getcwd()
    for i in range(1,3):
        name = 'fii_stats_'+str(i)+'.xls'
        get_xls('https://www1.nseindia.com/content/fo/fii_stats_',name,i)
        string = "fii*"+str(i)+".xls"
        csv_file = glob.glob(os.path.join(path, string))#list of files
        # print(path)
        # print(csv_file)
        data_fii = pd.read_excel(csv_file[0],)
        # print(data_fii)
        data_arr_fii = data_fii.to_numpy()

        fpi_cash = 0
        for j in range(2,6):
            fpi_cash = fpi_cash + float(data_arr_fii[j][2]) - float(data_arr_fii[j][4])
        if(fpi_cash < 0):
            # print('fpi_cash ',str(fpi_cash*10/82.80))
            list_insti_flow.append(fpi_cash*10/82.80)
        else:
            # print('fpi_cash ','+'+str(fpi_cash*10/82.80))
            list_insti_flow.append(fpi_cash*10/82.80)

        FPI_index_futures = float(data_arr_fii[2][2]) - float(data_arr_fii[2][4])
        if(FPI_index_futures < 0 ):
            # print('FPI index futures value : ',str(FPI_index_futures*10/82.80))
            list_insti_flow.append(FPI_index_futures*10/82.80)
        else:
            # print('FPI index futures value : ','+'+str(FPI_index_futures*10/82.80))
            list_insti_flow.append(FPI_index_futures*10/82.80)
        
        # print('FII stats ',data_arr_fii)

        FPI_stock_futures = float(data_arr_fii[4][2]) - float(data_arr_fii[4][4])
        if(FPI_stock_futures < 0):
            # print('FPI stock futures value : ',str(FPI_stock_futures*10/82.80))
            list_insti_flow.append(FPI_stock_futures*10/82.80)
        else:
            # print('FPI stock futures value : ','+'+str(FPI_stock_futures*10/82.80))
            list_insti_flow.append(FPI_stock_futures*10/82.80)

        #DII data
        dii_idx_fut_buy_val = float(data_arr_fii[2][2])/ float(data_arr_fii[2][1])
        dii_idx_fut_sell_val = float(data_arr_fii[2][4])/ float(data_arr_fii[2][3])
        dii_stk_fut_buy_val = float(data_arr_fii[4][2])/ float(data_arr_fii[4][1])
        dii_stk_fut_sell_val = float(data_arr_fii[4][4])/ float(data_arr_fii[4][3])    

        path = os.getcwd()
        name = 'fao_participant_vol_'+str(i)+'.csv'
        get_csv('https://www1.nseindia.com/content/nsccl/fao_participant_vol_',name,i)
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
        else:
            # print('DII Stock Future',dii_stk_fut*10/82.80)
            list_insti_flow.append(dii_stk_fut*10/82.80)

        dii_idx_fut = float(data_arr_dii[2][1])*dii_idx_fut_buy_val - float(data_arr_dii[2][2])*dii_idx_fut_sell_val
        if(dii_idx_fut < 0):
            # print('DII index Future',dii_idx_fut*10/82.80)
            list_insti_flow.append(dii_idx_fut*10/82.80)
        else:
            # print('DII index Future',dii_idx_fut*10/82.80)
            list_insti_flow.append(dii_idx_fut*10/82.80)


        # dii_cash = 0
        # for j in range(2,6):
        #     dii_cash = dii_cash + float(data_arr_dii[j][2]) - float(data_arr_dii[j][4])

        #Cal OI_pCR from fao_participant_oi.csv
        path = os.getcwd()
        name = 'fao_participant_oi_'+str(i)+'.csv'#############################
        get_csv('https://www1.nseindia.com/content/nsccl/fao_participant_oi_',name,i)
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
        # print('#################')
    for i in range(1,3):
        date = get_date_xls(i)
        date = date[:6]
        # print(date,'   ',len(list_insti_flow))
        list_insti_flow.append(date)
    return list_insti_flow

def opt_flow():
        # refer to the fao_participant_vol.csv file
    path = os.getcwd()
    list_of_opt_flow = []
    for i in range(1,3):
        string = "fii*"+str(i)+".xls"
        csv_file = glob.glob(os.path.join(path, string ))#list of files
        data_fii = pd.read_excel(csv_file[0])
        # data_fii = pd.read_csv(csv_file[0])
        data_arr_fii = data_fii.to_numpy()

        #below values are per contract in crores
        idx_opt_buy_val = float(data_arr_fii[3][2])/ float(data_arr_fii[3][1])
        idx_opt_sell_val = float(data_arr_fii[3][4])/ float(data_arr_fii[3][3])
        stk_opt_buy_val = float(data_arr_fii[5][2])/ float(data_arr_fii[5][1])
        stk_opt_sell_val = float(data_arr_fii[5][4])/ float(data_arr_fii[5][3])  

        # print(idx_opt_buy_val,' --- ',idx_opt_sell_val)
        # print(stk_opt_buy_val,' ',stk_opt_sell_val)
        string = "fao*vol*"+str(i)+".csv"
        csv_file = glob.glob(os.path.join(path, string))#list of files
        # print(csv_file[0])#check which files are fetched
        data_fao_vol = pd.read_csv(csv_file[0])
        data_arr_fao = data_fao_vol.to_numpy()
        
        fpi_ce,fpi_pe = 0,0
        fpi_ce = fpi_ce+float(data_arr_fao[3][5])*idx_opt_buy_val
        fpi_ce = fpi_ce+float(data_arr_fao[3][7])*idx_opt_sell_val
        fpi_ce = fpi_ce+float(data_arr_fao[3][9])*stk_opt_buy_val
        fpi_ce = fpi_ce+float(data_arr_fao[3][11])*stk_opt_sell_val

        fpi_pe = fpi_pe+float(data_arr_fao[3][6])*idx_opt_buy_val
        fpi_pe = fpi_pe+float(data_arr_fao[3][8])*idx_opt_sell_val
        fpi_pe = fpi_pe+float(data_arr_fao[3][10])*stk_opt_buy_val
        fpi_pe = fpi_pe+float(data_arr_fao[3][12])*stk_opt_sell_val

        # print('fpi index call option',fpi_ce/8280)
        # print('fpi index put option',fpi_pe/8280)
        list_of_opt_flow.append(fpi_ce/8280)
        list_of_opt_flow.append(fpi_pe/8280)
        

        dii_ce,dii_pe = 0,0
        dii_ce = dii_ce+float(data_arr_fao[2][5])*idx_opt_buy_val
        dii_ce = dii_ce+float(data_arr_fao[2][7])*idx_opt_sell_val
        dii_ce = dii_ce+float(data_arr_fao[2][9])*stk_opt_buy_val
        dii_ce = dii_ce+float(data_arr_fao[2][11])*stk_opt_sell_val

        dii_pe = dii_pe+float(data_arr_fao[2][6])*idx_opt_buy_val
        dii_pe = dii_pe+float(data_arr_fao[2][8])*idx_opt_sell_val
        dii_pe = dii_pe+float(data_arr_fao[2][10])*stk_opt_buy_val
        dii_pe = dii_pe+float(data_arr_fao[2][12])*stk_opt_sell_val

        # print('dii index call option',dii_ce/8280)
        # print('dii index put option',dii_pe/8280)

        list_of_opt_flow.append(dii_ce/8280)
        list_of_opt_flow.append(dii_pe/8280)
    for i in range(1,3):
        date = get_date_xls(i)
        date = date[:6]
        # print(date,'   ',len(list_of_opt_flow))
        list_of_opt_flow.append(date)
    return list_of_opt_flow
        