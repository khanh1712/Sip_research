import time

def Tnm2(n, x, m):
    if n == 0:
        return 1
    elif n == 1:
        return x % m
    else:
        e = n - 1
        a11, a12, a21, a22 = 1, 0, 0, 1
        s11, s12, s21, s22 = 0, 1, -1, (2 * x)
        
        while e > 1:
            if e % 2 == 1:
                t1 = (a11 * s11 + a12 * s21) % m
                a12 = (a11 * s12 + a12 * s22) % m
                a11 = t1
                t2 = (a21 * s11 + a22 * s21) % m
                a22 = (a21 * s12 + a22 * s22) % m
                a21 = t2
            t1 = s11 + s22
            t2 = s12 * s21
            s11 = (s11 ** 2 + t2) % m
            s12 = (s12 * t1) % m
            s21 = (s21 * t1) % m
            s22 = (s22 ** 2 + t2) % m
            e //=2
        
        t1 = (a21 * s11 + a22 * s21) % m
        t2 = (a21 * s12 + a22 * s22) % m
        return (t1 + t2 * x) % m


#pr = number.getPrime(bit_length)
p = 4158882755129780466453818699659244206976052282911691362991364371845722940260164927026307811901826436765474434383134654873801624177970863368889322569133345001233378371904157803451068747013023512059017407227150501400554265645092083930324113198444872362084794895200080159333159950156181823553719805388323537288887860270134696096737073358440440148467841263546456645885502672133800949873418103907415386824196879694527432919058944280170759460598759861606458383208443911897097528569929097878874229366795435843604764922210889662975169529185019540997307331672463139366506846048939484978777005065729680557889411751635290920142959199579315693102184203556431821988461569952160787904883179011220660735858375194771012159838307051586537778258888547742252235101420705413701350845547613847276265583006721800742114423811830835005138183459870744768681341947266304754523251374523104382375916971813057774965086647971014360026939724572916809362023
#print("Generated Prime Number:", p)
x = 2**203
n = 2**3072 + 1
print(len(bin(n)[2:]))
#kg = Tnm2(n, x, p)
#print(kg, len(bin(kg)[2:]))

count = 100
avg = 0
for i in range(count):
        start_time = time.time()
        # Đoạn code cần đo thời gian thực thi
        kg = Tnm2(n, x, p)
        end_time = time.time()
        duration = end_time - start_time
        avg += duration

avg /= count
print(kg, len(bin(kg)[2:]))
print("Thời gian chạy cbs2: {:.20f} giây".format(avg))

