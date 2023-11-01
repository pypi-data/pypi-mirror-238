from pydataconn import Gsheets

if __name__ == '__main__':
    gsheets = Gsheets('GOOGLE_SHEETS_STOCKS')
    df = gsheets.query('data')
    print(df)
