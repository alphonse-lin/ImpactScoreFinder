import pandas as pd

path=r'Data\result.csv'
df=pd.read_csv(path)
dic={}
for index, row in df.iterrows():
    type=df.iloc[index].loc["Subject Area, Categories, Scope"]
    type_list=type.split(';')
    for item in type_list:
        item=item.split('(')[0].strip()
        if item in dic:
            temp=dic.get(item)+1
            dic.update({item:temp})
        else:
            dic.update({item:1})
result_df=pd.DataFrame(list(dic.items()))
result_df.columns=['title','count']
final=result_df.sort_values(by=['count'], ascending=False, axis=0)
final.to_csv(r'Data\sortJounralType.csv')

