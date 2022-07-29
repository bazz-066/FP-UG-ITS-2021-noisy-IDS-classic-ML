import csv


list_atk_source=[]
list_atk_sourceport=[]
list_atk_destinationip=[]
list_atk_destinationport=[]
list_atk_name=[]

with open('NUSW-NB15_GT.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        sourceport=row[8]
        if(sourceport=='80'):
            list_atk_source.append(row[5])
            list_atk_sourceport.append(row[6])
            list_atk_destinationip.append(row[7])
            list_atk_destinationport.append(row[8])
            list_atk_name.append(row[9])
            
#print(list_atk_source)
data_source=[]
data_sourceport=[]
data_destinationip=[]
data_destinationport=[]
data_prediksi=[]        
with open('Isoforest_result.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        data_source.append(row[0])
        data_sourceport.append(row[1])
        data_destinationip.append(row[2])
        data_destinationport.append(row[3])
        data_prediksi.append(row[4])
        
#print(data_prediksi)
total_data=0
tp=0
tn=0
fp=0
fn=0
for data in data_source:
    if (data in list_atk_source):
        if(data_prediksi[total_data]=='-1'):
            tp=tp+1
        else:
            fn=fn+1
    else:
        if(data_prediksi[total_data]=='-1'):
            fp=fp+1
        else:
            tn=tn+1
    total_data=total_data+1

print("Total Data= ",total_data)
print("True Positive= ",tp)
print("True Negative= ",tn)
print("False Positive= ",fp)
print("False Negative= ",fn)