leituras=int(input("Quantas leituras de pressão serão lidas? "))
num_media=0
media=0
Mn=0
PB=0
verde=0
amarelo=0
vermelho=0
PV=0
TS=True
while leituras<0:
    leituras=int(input("Não são permitidas leituras negativas, coloque um valor valido:. "))
for i in range(1,leituras+1):
    Upc=float(input("Quantidade de UPCs: "))
    while Upc<0:
        Upc=int(input("Não são permitidas leituras negativas, coloque um valor valido:. "))
    if Upc >150:
        Upc=Upc*1.08
    else:
        Upc=Upc*0.96
    num_media+=Upc
    media=num_media/i
    print (f"\n{Upc:.2f}")
    if Upc<=120:
        print(f"\n Alerta!!! Pressão Baixa, Risco de Entupimento!")
        PB+=1
    elif 120<=Upc<=180:
        verde+=1
    elif 180<Upc<250:
        amarelo+=1
    else:
        vermelho+=1  
    if Mn==0 or Upc<Mn:
        Mn=Upc
    PV=verde*100/i
    if TS==False and Upc>=250:
        porcentagem=(i*100)/(leituras)
        print(f"\n SISTEMA INTERROMPIDO! Foram feitas {i} leituras, tendo um aproveitamento de: {porcentagem:.2f}%")
        break
    if Upc>=250:
        TS=False
    else:
        TS=True
print(f"\n A porcentagem de Leituras Verdes foram: {PV}%")
print(f"\n A media das pressões após o ajuste é de: {media:.2f}")
print(f"\n A menor pressão após reajuste foi de:{Mn:.2f}")
print(f"\n Verde: {verde} | Amarelo: {amarelo} | Vermelho: {vermelho} | Pressão Baixa: {PB}")