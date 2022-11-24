import os
import pandas as pd

path = "Data\output" #文件夹目录
output_path=r'Data\result.csv'
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
        file_path=os.path.join(path, file)
        print(file_path)
        temp_df=pd.read_csv(file_path).iloc[:,1:]
        s.append(temp_df)

result=pd.concat(s, axis=0)
result=result.sort_values(by=['id'], ascending=True, axis=0)
# result=result.reset_index(drop=True)
result.to_csv(output_path, index=False)