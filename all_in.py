import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import camelot
from datetime import datetime
import os
import csv
import tabula
import numpy as np





def santex():
#Находим ссылку на прайс
    url = 'https://www.santech.ru/main/how_to_buy/'
    path = 'data456531\\santex_new.xlsx'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find_all('a')

    for r in result:
        url = r.get('href')
        if 'list.xlsx' in url:
            url_price = url

#Подставляем ссылку на прайс
    price = requests.get('https://www.santech.ru' + url_price)

#Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

#Обрабатываем скаченный файл
    df = pd.read_excel('data456531\\santex_new.xlsx')
    df_new = df.iloc[3:, [2, 8]]
    df_new = df_new.dropna()
    df_new.rename(columns = {'Unnamed: 2':'Артикул', 'Unnamed: 8':str(datetime.now().date())}, inplace=True)

#Соеденяем актуальный прайс с нашим прайсам за все время
    df = pd.read_excel('data456531\\santex.xlsx')
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

#Сохраняем файл и удаляем не нужные
    df_new2.to_excel('data456531\\santex.xlsx')
    os.remove('data456531\\santex_new.xlsx')





def teremopt():

# Получаем курс евра
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    eur = data['Valute']['EUR']['Value']

# Находим ссылку на прайс
    url = 'https://teremopt.ru/products/pricelist/'
    path = 'data456531\\teremopt.xlsx'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find_all('a')

    for r in result:
        url = r.get('href')
        if url:
            if '.xlsx' in url:
                url_price = url

# Подаставляем ссылку на прайс
    price = requests.get('https://teremopt.ru' + url_price)

# Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

#Бугати
# Открываем файл Теремка
    bugatti = pd.read_excel('data456531\\teremopt.xlsx', sheet_name = 'Bugatti')

# Обрабатываем файл
    bugatti = bugatti[['Краны шаровые фирмы BUGATTI (Италия)', 'Unnamed: 3']]
    bugatti.rename(columns={'Краны шаровые фирмы BUGATTI (Италия)': 'Артикул', 'Unnamed: 3': str(datetime.now().date())}, inplace=True)
    bugatti.dropna(inplace=True)
    df_new = bugatti.iloc[1:, :]

# Открываем оригинал
    df = pd.read_excel('data456531\\bugatti.xlsx')

# Соеденяем наши два файла
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

# Перемножаем на курс евра
    for n, price in enumerate(df_new2[str(datetime.now().date())]):
        try:
            df_new2[str(datetime.now().date())][n] = int(price) * eur
        except Exception as exc:
            pass

# Сохраняеи файл
    df_new2.to_excel('data456531\\bugatti.xlsx')


#ITAP
# Открываем скаченый файл
    itap = pd.read_excel('data456531\\teremopt.xlsx', sheet_name = 'ITAP')

# Обрабатываем его
    df_new = itap[['Unnamed: 1', 'Unnamed: 7']]
    df_new.rename(columns={'Unnamed: 1': 'Артикул', 'Unnamed: 7': str(datetime.now().date())}, inplace=True)
    df_new.dropna(inplace=True)
    df_new = df_new.iloc[1:, :]

# Открываем файл с бд
    df = pd.read_excel('data456531\\itap.xlsx')

# Соеденяем актуальный прайс с нашим прайсам за все время
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

# Сохраняем файл и удаляем не нужные
    df_new2.to_excel('data456531\\itap.xlsx')
    os.remove('data456531\\teremopt.xlsx')






def stout():
# Курс доллора
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    eur = data['Valute']['EUR']['Value']

# Находим ссылку на прайс
    url = 'https://www.stout.ru/price_lists/'
    path = 'data456531\\stout_new.xlsx'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find_all('a')

    for r in result:
        url = r.get('href')
        if url:
            if '.xlsx' in url:
                url_price = url

# Подаставляем ссылку на прайс
    price = requests.get('https://www.stout.ru' + url_price)

# Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

# Обрабатываем скаченный файл
    stout = pd.read_excel('data456531\\stout_new.xlsx', sheet_name = 'STOUT Ассортимент')
    stout_new = stout[['Unnamed: 0', 'Unnamed: 2']]
    stout_new.dropna(inplace=True)
    stout_new.rename(columns={'Unnamed: 0':'Артикул', 'Unnamed: 2':str(datetime.now().date())}, inplace=True)
    stout_new.reset_index(inplace=True)

# Если евро, умножаем на курс евра если нет, то оставляем как есть
    for n, price in enumerate(stout_new[str(datetime.now().date())]):
        if price == 'Цена с НДС, eur':
            eur = data['Valute']['EUR']['Value']
        if price == 'Цена с НДС, Руб.':
            eur = 1
        try:
            stout_new[str(datetime.now().date())][n] = int(price) * eur
        except Exception as exc:
            pass
    df_new = stout_new

# Соеденяем актуальный прайс с нашим прайсам за все время
    df = pd.read_excel('data456531\\stout.xlsx')
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

# Сохраняем файл и удаляем не нужные
    df_new2.to_excel('data456531\\stout.xlsx')
    os.remove('data456531\\stout_new.xlsx')





def valtec():
# Находим ссылку на прайс
    url = 'https://valtec.ru/document/price.html'
    path = 'data456531\\valtec_new.xlsx'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find_all('a')

    for r in result:
        url = r.get('href')
        if url:
            if '.xlsx' in url:
                url_price = url

# Подставляем ссылку на прайс
    price = requests.get('https://valtec.ru' + url_price)

# Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

# Обрабатываем скаченный файл
    df = pd.read_excel('data456531\\valtec_new.xlsx', sheet_name=None)
    df = pd.concat(df, ignore_index=True)
    df_new = df.iloc[1:, [1, 4]]
    df_new = df_new.dropna()
    df_new = df_new[(df_new['Unnamed: 1'] != 'Артикул')]
    df_new.rename(columns = {'Unnamed: 1':'Артикул', 'Unnamed: 4':str(datetime.now().date())}, inplace=True)

# Соеденяем актуальный прайс с нашим прайсам за все время
    df = pd.read_excel('data456531\\valtec.xlsx')
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

# Сохраняем файл и удаляем не нужные
    df_new2.to_excel('data456531\\valtec.xlsx')
    os.remove('data456531\\valtec_new.xlsx')





def valfex():
# Находим ссылку на прайс
    url = 'https://valfex.ru/clients/price/'
    path = 'data456531\\valfex.pdf'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find('a', class_ = 'documents__item documents-item')
    url_price = result.get('href')

# Подставляем ссылку на прайс
    price = requests.get('https://valfex.ru' + url_price)

# Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

# Преобразовываем pfd в csv файл
    df = tabula.read_pdf('data456531\\valfex.pdf', pages='all')
    tabula.convert_into('data456531\\valfex.pdf', 'data456531\\valfex_new.csv', output_format='csv', pages='all')

    tables = camelot.read_pdf("data456531\\valfex.pdf", encoding='utf-8', pages='all')
    cominate_tables = pd.DataFrame()

    for table in tables:
        df = table.df
        cominate_tables = pd.concat([cominate_tables, df])

    cominate_tables.to_csv('data456531\\valfex_new.csv', index=False)

    df = pd.read_csv('data456531\\valfex_new.csv')
    data = df[['2', '9']]
    data = data.dropna()
    data['9'].replace(to_replace = ' RUB', value = '', regex = True, inplace=True)
    data.rename(columns = {'2':'Артикул', '9':str(datetime.now().date())}, inplace=True)

# Форматируем csv файл убираем лишние строчки

    df = tabula.read_pdf('data456531\\valfex.pdf', pages='all')
    tabula.convert_into('data456531\\valfex.pdf', 'data456531\\valfex_new.csv', output_format='csv', pages='all')

    list_data = []

    with open('data456531\\valfex_new.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in spamreader:
            row_new = ','.join(row)
            row_new = row_new.replace('"', '').replace("'", '').replace(' ', '')
            row_new = row_new.split(',')
            if '' in row_new:
                row_new.remove('')
            if len(row_new) > 5:
                list_data.append([row_new[1], str(row_new[-2]) + ',' + str(row_new[-1])])

    df = pd.DataFrame(list_data)
    for n, rub in enumerate(df[1]):
        if 'RUB' not in str(rub):
            df.drop(n, inplace=True)

# Обрабатываем csv файл убираю все лишнее из столбцов
    df_new = df[[0, 1]]
    df_new = df_new.dropna()
    df_new[1].replace(to_replace = 'RUB', value = '', regex = True, inplace=True)
    df_new.rename(columns = {0:'Артикул', 1:str(datetime.now().date())}, inplace=True)

# Соеденяем актуальный прайс с нашим прайсам за все время    
    df = pd.read_excel('data456531\\valfex.xlsx')
    df_new2 = pd.merge(df, data, how='outer')
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=[ 'Unnamed: 0'], axis=0, inplace=True)
    df_new2.drop_duplicates(inplace=True)

# Сохраняем файл и удаляем не нужные
    df_new2.to_excel('data456531\\valfex.xlsx')
    os.remove('data456531\\valfex_new.csv')
    os.remove('data456531\\valfex.pdf')





def gallop():
# Находим ссылку на прайс
    url = 'https://gallop.ru/'
    path = 'data456531\\gallop.xls'
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    result = soup.find_all('a')

    for r in result:
        url = r.get('href')
        if url:
            if '.xls' in url:
                url_price = url

# Подаставляем ссылку на прайс
    price = requests.get('https://gallop.ru' + url_price)

# Скачиваем прайс
    with open(path, 'wb') as f:
        f.write(price.content)

# Скаченный файл сохраняем в csv и кодируем в ISO-8859-1
    data_xls = pd.read_excel('data456531\\gallop.xls', index_col=None)

    df1 = data_xls[['Ïðàéñ-ëèñò', 'Unnamed: 2']]
    df2 = data_xls[['Unnamed: 4', 'Unnamed: 6']]
    df2.dropna(inplace=True)
    df1.dropna(inplace=True)
    df_new1 = df1.rename(columns = {'Ïðàéñ-ëèñò' : 'Артикул', 'Unnamed: 2' : str(datetime.now().date())})
    df_new2 = df2.rename(columns = {'Unnamed: 4' : 'Артикул', 'Unnamed: 6' : str(datetime.now().date())})
    df_new = pd.concat([df_new1, df_new2])
    df_new = df_new.reset_index()
    df_new = df_new.iloc[1: , 1:]
    df_new['Артикул'].replace(to_replace = 'Ê', value = 'К', regex = True, inplace=True)


    df_new.to_csv('data456531\\gallop.csv')

# Читаем закодированный csv файл
    data = pd.read_csv('data456531\\gallop.csv')
    df_new = data.iloc[: , 1:]
    df_new.dropna(inplace = True)

# Читаем наш БД галоп
    df = pd.read_excel('data456531\\gallop.xlsx')

# Объеденяем наши бд
    df_new2 = pd.merge(df, df_new, how='outer')
    df_new2.drop(columns=['Unnamed: 0'], axis=0, inplace=True)

# Сохраняем их 
    df_new2.to_excel('data456531\\gallop.xlsx')

# Удаляем лишнее
    os.remove('data456531\\gallop.csv')
    os.remove('data456531\\gallop.xls')





def articul_price(coefficient):

# Считываем базы данных
    df = pd.read_excel('data456531\\База сопоставления артикулов.xlsx')
    valtec = pd.read_excel('data456531\\valtec.xlsx')
    valfex = pd.read_excel('data456531\\valfex.xlsx')
    santech = pd.read_excel('data456531\\santex.xlsx')
    gallop = pd.read_excel('data456531\\gallop.xlsx')
    bugatti = pd.read_excel('data456531\\bugatti.xlsx')
    itap = pd.read_excel('data456531\\itap.xlsx') 
    stout = pd.read_excel('data456531\\stout.xlsx')
    bd_list = [
    valtec, valfex,santech, gallop
    ]

# Проходимся по названиям колонк в База сопоставления артикуловq
    for column in df.columns[3:]:

# По ключевым словам определяем бд где ищем
        if 'Valfex' in str(column):
            bd = valfex
            coff = coefficient['valfex']
        elif 'Valtec' in str(column):
            bd = valtec
            coff = coefficient['valtec']
        elif 'Aquasfera' in str(column):
            bd = santech
            coff = coefficient['aquasfera']
        elif 'GALLOP' in str(column):
            bd = gallop
            coff = coefficient['gallop']
        elif 'Itap' in str(column):
            bd = itap
            coff = coefficient['itap']
        elif 'Stout' in str(column):
            bd = stout
            coff = coefficient['stout']
        elif 'Bugatti' in str(column):
            bd = bugatti
            coff = coefficient['bugatti']

# Заходим в сами колонки и берем их артикул с индексом 
        for n, articul in enumerate(df[column]):

# Проходимся по базе и иещм артикул который взяли если находим то забираем прайс
            ind = bd[bd['Артикул'] == articul].index
            ind = ind.to_list()
            if ind != []:
                price = bd[str(datetime.now().date())][ind[0]]
                try:
                    df[column][n] = price * coff
                except Exception as exc:
                    pass
                price = None
            if all(bd['Артикул'] != articul) == True:
                df[column][n] = None

# Сохраняем База сопоставления артикулов, но уже с ценами за место артикулов
    df.to_excel('data456531\\База артикулов с ценами.xlsx')
    df = pd.read_excel('data456531\\База сопоставления артикулов.xlsx')

# Проходимся по названиям колонк в База сопоставления артикуловq
    for column in df.columns[3:]:

# По ключевым словам определяем бд где ищем
        if 'Valfex' in str(column):
            bd = valfex
        elif 'Valtec' in str(column):
            bd = valtec
        elif 'Aquasfera' in str(column):
            bd = santech
        elif 'GALLOP' in str(column):
            bd = gallop
        elif 'Itap' in str(column):
            bd = itap
        elif 'Stout' in str(column):
            bd = stout
        elif 'Bugatti' in str(column):
            bd = bugatti

# Заходим в сами колонки и берем их артикул с индексом 
        for n, articul in enumerate(df[column]):

# Проходимся по базе и иещм артикул который взяли если находим то забираем прайс
            ind = bd[bd['Артикул'] == articul].index
            ind = ind.to_list()
            if ind != []:
                price = bd[str(datetime.now().date())][ind[0]]
                try:
                    df[column][n] = price
                except Exception as exc:
                    pass
                price = None
            if all(bd['Артикул'] != articul) == True:
                df[column][n] = None

    df.to_excel('data456531\\База артикулов с ценами без кэф.xlsx')



def download_new_price():
    valfex()
    valtec()
    santex()
    gallop()
    teremopt()
    stout()

def main(coefficient):
    coefficient = coefficient
    download_new_price()
    articul_price(coefficient)

if __name__ == '__main__' :
    coefficient = {
        'valfex': 2,
        'valtec': 2,
        'aquasfera': 2,
        'gallop': 2,
        'itap': 2,
        'stout': 2,
        'bugatti': 2,
}

    main(coefficient)
