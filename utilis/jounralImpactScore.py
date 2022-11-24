import urllib3
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import os

input_path=r'Data\test.csv'
output_dir=r'Data\output'
ori_df=pd.read_csv(input_path)

series=np.linspace(16, len(ori_df), 19, dtype = int)
for count in range(len(series)-1):
    start=series[count]
    end=series[count+1]
    output_path=os.path.join(output_dir, "data_{0}-{1}.csv".format(start, end))
    cut_df=ori_df.iloc[start:end, :]
    df=cut_df.reset_index(drop=True)

    dic={'Title': [], 'Abbreviation':[], 'Publication Type': [], 'Subject Area, Categories, Scope': [], 
'h-index': [], 'Overall Rank/Ranking': [], 'SCImago Journal Rank (SJR)': [], 'Impact Score': [], 
'Publisher': [], 'Country': [], 'ISSN': []}
    for index, row in df.iterrows():
        temp_title=str(row['Publication Title'])
        title=temp_title.replace(' ','+')

        url = 'https://www.resurchify.com/find/?query={0}#search_results'.format(title)

        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data.decode('utf-8'))
        flag= soup.findAll(text=re.compile('No search results were found'))
        if len(flag) == 0:
            # res2=soup.findAll('a')[36]
            res2=soup.findAll(text=re.compile('Impact Score:'))[0]
            website=res2.find_parent().find_parent().find_parent().find_next_sibling()['href']
            print(("{0}_{1}").format(index, website))

            url1 = website

            http1 = urllib3.PoolManager()
            response1 = http1.request('GET', url1)
            soup1 = BeautifulSoup(response1.data.decode('utf-8'))
            res3=soup1.select(".w3-right-align")
            name_list=soup1.select("td b.w3-text-black")

            for key in dic:
                dic.get(key).append('-1')
            for i in range(len(name_list)):
                item=res3[i]
                name=item.get_text().strip()
                data_value=item.find_next_sibling().text
                if name in dic:
                    dic.get(name)[index]=(data_value)
        else:
            for key in dic:
                dic.get(key).append("-1")
            
    dic_df=pd.DataFrame.from_dict(dic)
    df=pd.concat([df,dic_df],axis=1)
    df.to_csv(output_path)