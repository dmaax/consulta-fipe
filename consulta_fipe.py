import cloudscraper
import lxml.html as lh
import requests
import pandas as pd

try:
    placa = input('Digite a placa do veículo: ')
except KeyboardInterrupt:
    print('\nFechando o prgrama (CTRL+C)')
    exit()

scraper = cloudscraper.create_scraper()
response = scraper.get(f"https://www.keplaca.com/placa/{placa}").text

doc = lh.fromstring(response)
tr_elements = doc.xpath('//table[@class="fipe-desktop"]//tr')

col=[]
i=0

try:
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))
except IndexError as ex:
    print('Placa não encontrada.')
    exit()

for j in range(1,len(tr_elements)):
    T=tr_elements[j]
    
    #Se nao for de tamanho 3 nao é dado do site.
    if len(T)!=3:
        break
    
    #index
    i=0
    
    #Iterando
    for t in T.iterchildren():
        data=t.text_content() 
        #Se nao for vazio
        if i>0:
        #Converte tudo para string
            try:
                data=str(data)
            except:
                pass
        #Append
        col[i][1].append(data)
        #Increment
        i+=1

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
print(df)

writer = pd.ExcelWriter(f'veiculo_{placa}.xlsx')
df.to_excel(writer, index=False)

writer.book.save(f'veiculo_{placa}.xlsx')
writer.close()
