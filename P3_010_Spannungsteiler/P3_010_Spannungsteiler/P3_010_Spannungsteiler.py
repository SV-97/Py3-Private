
import math
import decimal
import bisect

def roundup(f,n): # round a float f to the n-th decimal place
    return math.ceil(f * 10**n) / 10**n

def widerstandsreihe(e): # Standart series E3 would be e=3
    k = 10**(1/e)
    unrounded = [1.0]
    for i in range(e-1):
        unrounded.append(unrounded[i]*k)
    rounded = [i for i in range(e)]
    for i in range(e):
        rounded[i] = round(decimal.Decimal(roundup(unrounded[i],1)),1)
    series = []
    for i in range(e):
        series = series + [rounded[i]*j for j in [10**l for l in range(6)]]
    series.sort()
    return tuple(series)

yn = input("Widerstandsreihen verwenden? J/n: ").lower()
if yn == "":
    yn = "j"
if  yn == "j":
    standart_series = int(input("Widerstandsreihe E"))
else:
    standart_series = ()
    
if input("Eingabe als Pegel(dB) oder Spannung(V): ") == "dB":
    mode = 1
else:
    mode = 0

Ub = decimal.Decimal(input("Betriebsspannung in V: "))
modes = {0:"V", 1:"dB"}

Uref = decimal.Decimal(input("Referenzspannungsbezug in V: "))
n = int(input("Anzahl an Stufen(Anzahl an Widerständen ohne Vorwiderstand): "))
modeR = decimal.Decimal(input("Festlegen des kleinsten Widerstandes(0), Gesamtwiderstandes(1): "))
if modeR == "":
    modeR = 0
if modeR == 0:
    Rmin = decimal.Decimal(input("Kleinster Widerstand in Ohm: "))
elif modeR == 1:
    Rg = decimal.Decimal(input("Gesamtwiderstand in Ohm: "))

steps = [] # voltages of the voltage divider in V
for i in range(n):
    val = decimal.Decimal(input("Stufe {} in {}: ".format(i,modes[mode])))
    if modes[mode] == "V":
        val = val
    elif modes[mode] == "dB":
        val = Uref * decimal.Decimal(10) ** (val/decimal.Decimal(20)) # dB to V
    steps.append( val )
steps.sort()

vp = [] # voltages in % of Uref
vp.append((Ub-steps[-1])/Ub) # voltage to drop on first resistor from total voltage down to Uref voltage
v = [] # voltages in V
for i in range(len(steps)):
    if i > 0:
        vp.append((steps[i]-steps[i-1])/Ub)
    else:
        vp.append(steps[i]/Ub)
        6
r = []
if modeR == 0:
    Rg = Rmin/vp[1]
    for i in range(len(vp)):
        r.append(vp[i]*Rg)    
elif modeR == 1:
    for i in range(len(vp)):
        r.append(vp[i]*Rg)        

print("{:-^60}".format(" Optimalwerte "))
print("Rv = {:>6.2g} Ohm".format(r[0]))
for i in range(1,len(r)):
    print("R{} = {:>6.2g} Ohm".format(i, r[i]))
print("RG = {:>6.2g} Ohm".format(sum(r)))
print("I = {:>6.2g} A".format(Ub/(sum(r))))

if standart_series != ():
    print("{:-^60}".format(" Werte aus Reihe E{} ".format(standart_series)))
    used_series = widerstandsreihe(standart_series)
    rstan = []
    for R in r: # select value that's closest to optimal value
        relative = bisect.bisect_left(used_series, R)
        if relative != 0:
            if abs(used_series[relative]-decimal.Decimal(R)) <= abs(used_series[relative-1]-decimal.Decimal(R)):
                pos = relative
            else:
                pos = relative-1
        rstan.append(used_series[pos])

    print("Rv = {:>6.2g} Ohm".format(rstan[0]))
    for i in range(1,len(rstan)):
        print("R{} = {:>6.2g} Ohm".format(i, rstan[i]))
    print("RG = {:>6.2g} Ohm".format(sum(rstan)))
    Istan = decimal.Decimal(Ub)/(sum(rstan))
    print("I = {:>6.2g} A".format(Istan))

    print("{:-^60}".format(" Abweichung der Werte aus E{} ".format(standart_series)))
    rstandev = [] # devation of percentage on Rg of standart series values from optimal values
    for i in range(len(rstan)):
        rstandev.append(rstan[i]/sum(rstan) - decimal.Decimal(vp[i]))  

    ustan = [] # voltage across resistor from standart series
    for i in range(len(rstan)):
        ustan.append(decimal.Decimal(Istan*rstan[i]))

    js = [] # potential on resistor from standart series
    jsdB = [] # potential on resistor in reference to Uref
    ustanw = ustan[1:]
    for i in range(len(ustanw)):
        js.append(sum(ustanw[:i+1]))
        a = math.log10(js[i]/decimal.Decimal(Uref))
        jsdB.append(decimal.Decimal(20)*decimal.Decimal(a))
    js.insert(0,sum(js))
    jsdB.insert(0,decimal.Decimal(20)*decimal.Decimal(math.log10(js[0]/decimal.Decimal(Uref))))
    
    print("delta Rv = {:>4.2f} %".format(rstandev[0]*100))
    for i in range(1,len(rstan)):
        print("delta R{} = {:>4.2f} % das Potential gegen Masse beträgt {:>6.2g} V bzw. {:>6.2g} dB der Referenzspannung".format(i, rstandev[i]*100,js[i],jsdB[i]))
