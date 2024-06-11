import math
import numpy as np 
g=9.81
e = 0.99

def read_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        numbers_str = file.read() 
    numbers = numbers_str.split()  
    numbers = [float(number) for number in numbers]  
    return numbers


def task1(Gv,m,rk,Bb,hg,V):
    spravka = read_numbers_from_file("t1s.txt")
    T1,D1,d1,e1,T2,D2,d2,e2,kk,km,kb,X,Y1,Y2,a1,b1 = spravka

    a=(a1 + (T1/2 + (d1+D1)*e1/6))/1000
    b=(b1 + (T2/2 + (d2+D2)*e2/6))/1000
    Zkv = 0.5*Gv - m*g
    Pb = 0.07*Gv/2
    Pr1p= (Zkv*b - Pb*rk)/(a+b)
    S1 = 0.83*e1*Pr1p
    Pr2p = (Zkv*a + Pb*rk)/(a+b)
    S2 = 0.83*e2*Pr2p
    if(S1<S2):
        Po1p = S2 - Pb
        Po2p = S2
    else:
        Po1p = S1 - Pb
        Po2p = S1
    if(Po1p/(kk*Pr1p)<e):
        Pe1p = kk*Pr1p*kb*km
    else:
        Pe1p = (kk*X*Pr1p + Y1*Po1p)*kb*km
    if(Po2p/(kk*Pr2p)<e):
        Pe2p = kk*Pr2p*kb*km
    else:
        Pe2p = (kk*X*Pr2p + Y1*Po2p)*kb*km
    

    Pr1o= (Zkv*b + Pb*rk)/(a+b)
    S1 = 0.83*e1*Pr1o
    Pr2o = (Zkv*a - Pb*rk)/(a+b)
    S2 = 0.83*e2*Pr2o
    if(S2<S1):
        Po1o = S1
        Po2o = S1 - Pb
    else:
        Po1o = S1 - Pb
        Po2o = S1
    if(Po1o/(kk*Pr1o)<e):
        Pe1o = kk*Pr1o*kb*km
    else:
        Pe1o = (kk*X*Pr1o + Y2*Po1o)*kb*km
    if(Po2o/(kk*Pr2o)<e):
        Pe2o = kk*Pr2o*kb*km
    else:
        Pe2o = (kk*X*Pr2o + Y2*Po2o)*kb*km

    Vn= 40
    Rn = 50
    aj = (Vn*Vn/(3.6*3.6*Rn))
    mm = aj*hg/(g*Bb)
    Gnk = 0.5*Gv*(1+mm)
    Znk = Gnk - m*g
    Pnb = aj/g*Gnk
    Pnr1 = (Znk*b-Pnb*rk)/(a+b)
    Pnr1 = abs(Pnr1)
    Sn1 = 0.83*e1*Pnr1
    Pnr2 = (Znk*a+Pnb*rk)/(a+b)
    Sn2 = 0.83*e2*Pnr2
    Pno1 = Sn2 - Pnb
    Pno2 = Sn2
    if(Pno1/(kk*Pnr1)<e):
        Pne1 = kk*Pnr1*kb*km
    else:
        Pne1 = (kk*X*Pnr1 + Y1*Pno1)*kb*km
    if(Pno2/(kk*Pnr2)<e):
        Pne2 = kk*Pnr2*kb*km
    else:
        Pne2 = (kk*X*Pnr2 + Y2*Pno2)*kb*km
    Gvk = 0.5*Gv*(1-mm)
    Zvk = Gvk - m*g
    Pvb = aj/g*Gvk
    Pvr1 = (Zvk*b+Pvb*rk)/(a+b)
    Sv1 = 0.83*e1*Pvr1
    Pvr2 = (Zvk*a-Pvb*rk)/(a+b)
    Pvr2 = abs(Pvr2)
    Sv2 = 0.83*e2*Pvr2
    Pvo1 = Sv1 
    Pvo2 = Sv1 + Pvb
    if(Pvo1/(kk*Pvr1)<e):
        Pve1 = kk*Pvr1*kb*km
    else:
        Pve1 = (kk*X*Pvr1 + Y1*Pvo1)*kb*km
    if(Pvo2/(kk*Pvr2)<e):
        Pve2 = kk*Pvr2*kb*km
    else:
        Pve2 = (kk*X*Pvr2 + Y2*Pvo2)*kb*km
    Pc1 = np.cbrt(0.45*(Pe1p**3 + Pe1o**3)+0.05*(Pne1**3 + Pve1**3))/1000
    Pc2 = np.cbrt(0.45*(Pe2p**3 + Pe2o**3)+0.05*(Pne2**3 + Pve2**3))/1000
    V = V*0.7
    ncp = 2.65*V/(rk)
    C = 26
    Lh1 = (1000000)*((C/Pc1)**(10.0/3.0))/((60*ncp))
    Sh1 = 6289.3*rk*((C/Pc1)**(10.0/3.0))/1000
    C = 29.6
    Lh2 = (1000000)*((C/Pc2)**(10.0/3.0))/((60*ncp))
    Sh2 = 6289.3*rk*((C/Pc2)**(10.0/3.0))/1000
    return Lh1

def task2(Ga,m,rk,Ba,hg,V):
    spravka = read_numbers_from_file("t2s.txt")
    kk,km,kb,Vn = spravka
    Pb = 0.07*Ga/2
    Zk = 0.5*Ga - m*g
    f = 0.01+0.05
    Xk = Ga*0.5*f
    Zk=Zk/1000
    Xk=Xk/1000
    Pr = math.sqrt(Zk*Zk+Xk*Xk)
    Po=Pb/1000
    if(Po/(kk*Pr)<0.99):
        Pe=(kk*Pr+0.63*Po)*kb*km
    else:
        Pe=(0.59*kk*Pr+1.04*Po)*kb*km
    R= 50
    aj=Vn*Vn/(3.6*3.6*R)
    mc = aj*hg/(g*Ba)
    Gnk = 0.5*Ga*(1+mc)
    Znk=Gnk-m*g
    Znk=Znk/1000
    Prn = math.sqrt(Znk*Znk+Xk*Xk)
    Pnb = aj/g*Gnk
    Pno=Pnb/1000
    if(Pno/(kk*Pr)<0.99):
        Pne=(kk*Prn+0.63*Pno)*kb*km
    else:
        Pne=(0.59*kk*Prn+1.04*Pno)*kb*km
    Gvk = 0.5*Ga*(1-mc)
    Zvk = Gvk-m*g
    Zvk=Zvk/1000
    Prv = math.sqrt(Zvk*Zvk+Xk*Xk)
    Pvb = aj/g*Gvk
    Pvo=Pvb/1000
    if(Pvo/(kk*Pr)<0.99):
        Pve=(kk*Prv+0.63*Pvo)*kb*km
    else:
        Pve=(0.59*kk*Prv+1.04*Pvo)*kb*km
    Pc = np.cbrt(0.9*Pe*Pe*Pe + 0.05*(Pve*Pve*Pve + Pne*Pne*Pne))
    V = V*0.7

    ncp = 2.65*V/(rk)
    C = 29
    Lh = (1000000)*(C/Pc)*(C/Pc)*(C/Pc)/((60*ncp))
    Sh = 6289.3*rk*(C/Pc)*(C/Pc)*(C/Pc)
    return(Lh)



def task3(Ga,m,L,rk,Ba,hg,V):
    spravka = read_numbers_from_file("t3s.txt")
    a,b,am,bm,X1,X2,Y1,Y2,km,rcp,kd,phi1,phi2,e1,e2 = spravka


    Gk = 0.5*Ga*km
    Zk = Gk - m*g
    Pt = phi1*Gk
    Tm = Pt*rk
    Pm = Tm/rcp
    Pzr1 = Zk*b/(a+b)
    Ptr1 = Pt*b/(a+b)
    Pmr1 = Pm*bm/(a+b)
    Pr1 = np.sqrt((Pzr1+Pmr1)**2 + Ptr1**2)/1000
    Pzr2 = Zk*a/(a+b)
    Ptr2 = Pt*a/(a+b)
    Pmr2 = Pm*am/(a+b)
    Pr2 = np.sqrt((Pzr2+Pmr2)**2 + Ptr2**2)/1000
    Zn = Gk*(1+phi2*hg/Ba) - m*g
    Pn = Gk*(1+phi2*hg/Ba)*phi2
    Zv = Gk*(1-phi2*hg/Ba) -  m*g
    Pv = Gk*(1-phi2*hg/Ba)*phi2
    Prn1 = (Zn*b-Pn*rk)/(a+b)/1000
    Prn2 = (Zn*a+Pn*rk)/(a+b)/1000
    Prv1 = (Zv*b+Pv*rk)/(a+b)/1000
    Prv2 = (Zv*a-Pv*rk)/(a+b)/1000

    Zd = kd*Gk
    Prd1 = (Zd*b)/(a+b)/1000
    Prd2 = (Zd*a)/(a+b)/1000
    P1 = max(Pr1,Prn1,Prv1,Prd1)
    P2 = max(Pr2,Prn2,Prv2,Prd2)

    Po1 = 0.83*e1*P1
    Po2 = 0.83*e2*P2
    Pc1 = max(X1*Pr1 +Y1*Po1,Pr1)
    Pc2 = max(X2*Pr2 +Y2*Po2,Pr2)
    C1 = 73
    C2 = 113
    k = min(C1/Pc1,C2/Pc2)
    return k





def task1To():
    file_path = "task1.txt" 
    numbers = read_numbers_from_file(file_path)
    return task1(*numbers)

def task2To():
    file_path = "task2.txt" 
    numbers = read_numbers_from_file(file_path)
    return task2(*numbers)

def task3To():
    file_path = "task3.txt" 
    numbers = read_numbers_from_file(file_path)
    return task3(*numbers)
s1 = 'Определить долговечность конических роликовых подшипников ступицы колеса задней ведомой оси переднеприводного легкового автомобиля'
s2 = 'Определить долговечность двухрядного шарикового радиально-упорного подшипника ступицы колеса передней ведущей оси  легкового автомобиля'
s3 = 'Определить максимальные значения нагрузок на подшипники ступицы  колеса переднего моста грузового  автомобиля и сравнить их со  статической грузоподъемностью'

ss = [s1,s2,s3]

s11 = 'Параметры Gv m Bb hg  V соответсвенно равны \n' + str(read_numbers_from_file("task1.txt"))
s22 = 'Ga m rk Ba hg V \n' + str(read_numbers_from_file("task2.txt"))
s33 = 'Ga m L rk Ba hg V \n' + str(read_numbers_from_file("task3.txt"))

ss1 = [s11,s22,s33]


# 3914.2 15.2 0.252 1.29 0.555 140
# 5405.3 15.2 0.252 1.314 0.555 140
# 23500 50 4250 0.351 1.82 1.0 90