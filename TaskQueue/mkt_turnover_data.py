import pandas as pd
import os
import glob
class mkt_to(object):
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    def market_to():
        #Stock Futures
        path = os.getcwd()
        print(path)
        csv_file = glob.glob(os.path.join(path, "fo_27122022.csv"))#list of files
        print(csv_file)
        data_stkfut = pd.read_csv(csv_file[0])
        data_arr = data_stkfut.to_numpy()
        print('Stock Futures in USD Billion - ',float(data_arr[2])/8280)
        # print(data)

        # Nifty
        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "ind_close*.csv"))#list of files
        data_nifty = pd.read_csv(csv_file[0])
        data_arr = data_nifty.to_numpy()
        # print(data_arr[0][9])
        print('Nifty Truenover in USD Billions ',float(data_arr[0][9])/8280)


        #Bank Nifty 
        print('Nifty Truenover in USD Billions ',float(data_arr[10][9])/8280)

    def insti_flow():
        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "fii*.xls"))#list of files
        data_fii = pd.read_excel(csv_file[0])
        data_arr_fii = data_fii.to_numpy()
        FPI_index_futures = float(data_arr_fii[2][2]) - float(data_arr_fii[2][4])
        print('FPI index futures value : ','+'+str(FPI_index_futures*10/82.80))
        # print('FII stats ',data_arr_fii)

        FPI_stock_futures = float(data_arr_fii[4][2]) - float(data_arr_fii[4][4])
        if(FPI_index_futures < 0):
            print('FPI stock futures value : ','-'+str(FPI_stock_futures*10/82.80))
        else:
            print('FPI stock futures value : ','+'+str(FPI_stock_futures*10/82.80))

        fpi_cash = 0
        for i in range(2,6):
            fpi_cash = fpi_cash + float(data_arr_fii[i][2]) - float(data_arr_fii[i][4])
        if(fpi_cash < 0):
            print('fpi_cash ','-'+str(fpi_cash*10/82.80))
        else:
            print('fpi_cash ','+'+str(fpi_cash*10/82.80))

        #DII data
        dii_idx_fut_buy_val = float(data_arr_fii[2][2])/ float(data_arr_fii[2][1])
        dii_idx_fut_sell_val = float(data_arr_fii[2][4])/ float(data_arr_fii[2][3])
        dii_stk_fut_buy_val = float(data_arr_fii[4][2])/ float(data_arr_fii[4][1])
        dii_stk_fut_sell_val = float(data_arr_fii[4][4])/ float(data_arr_fii[4][3])    

        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "fao*vol*.csv"))#list of files
        # print(csv_file[0])#check which files are fetched
        data_fao_vol = pd.read_csv(csv_file[0])
        data_arr_dii = data_fao_vol.to_numpy()

        dii_stk_fut = float(data_arr_dii[2][3])*dii_stk_fut_buy_val - float(data_arr_dii[2][4])*dii_stk_fut_sell_val
        print('DII Stock Future',dii_stk_fut*10/82.80)

        dii_idx_fut = float(data_arr_dii[2][1])*dii_idx_fut_buy_val - float(data_arr_dii[2][2])*dii_idx_fut_sell_val
        print('DII stock Future',dii_idx_fut*10/82.80)

        dii_cash = 0
        for i in range(2,6):
            dii_cash = dii_cash + float(data_arr_dii[2][2]) - float(data_arr_dii[2][4])

        #Cal OI_pCR from fao_participant_oi.csv
        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "fao*oi*.csv"))#list of files
        # print(csv_file[0])#check which files are fetched
        data_fao_oi = pd.read_csv(csv_file[0])
        data_arr_oi = data_fao_oi.to_numpy()
        put,call = 0,0
        for i in range(5,13):
            if(i % 2 == 1):
                call = call + int(data_arr_oi[5][i])
            else:
                put = put + int(data_arr_oi[5][i])
        print('OI PCR ',put/call)
        
    def opt_flow():
        # refer to the fao_participant_vol.csv file
        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "fii*.xls"))#list of files
        data_fii = pd.read_excel(csv_file[0])
        data_arr_fii = data_fii.to_numpy()

        #below values are per contract in crores
        idx_opt_buy_val = float(data_arr_fii[3][2])/ float(data_arr_fii[3][1])
        idx_opt_sell_val = float(data_arr_fii[3][4])/ float(data_arr_fii[3][3])
        stk_opt_buy_val = float(data_arr_fii[5][2])/ float(data_arr_fii[5][1])
        stk_opt_sell_val = float(data_arr_fii[5][4])/ float(data_arr_fii[5][3])  

        # print(idx_opt_buy_val,' --- ',idx_opt_sell_val)
        # print(stk_opt_buy_val,' ',stk_opt_sell_val)

        path = os.getcwd()
        csv_file = glob.glob(os.path.join(path, "fao*vol*.csv"))#list of files
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

        print('fpi index call option',fpi_ce/8280)
        print('fpi index put option',fpi_pe/8280)

        dii_ce,dii_pe = 0,0
        dii_ce = dii_ce+float(data_arr_fao[2][5])*idx_opt_buy_val
        dii_ce = dii_ce+float(data_arr_fao[2][7])*idx_opt_sell_val
        dii_ce = dii_ce+float(data_arr_fao[2][9])*stk_opt_buy_val
        dii_ce = dii_ce+float(data_arr_fao[2][11])*stk_opt_sell_val

        dii_pe = dii_pe+float(data_arr_fao[2][6])*idx_opt_buy_val
        dii_pe = dii_pe+float(data_arr_fao[2][8])*idx_opt_sell_val
        dii_pe = dii_pe+float(data_arr_fao[2][10])*stk_opt_buy_val
        dii_pe = dii_pe+float(data_arr_fao[2][12])*stk_opt_sell_val

        print('dii index call option',dii_ce/8280)
        print('dii index put option',dii_pe/8280)



if __name__ == "__main__":
    mkt_to.market_to()
    print("-----------------------")
    mkt_to.insti_flow()
    print("-----------------------")
    mkt_to.opt_flow()
    