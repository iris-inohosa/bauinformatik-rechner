#import
from tkinter import *
from tkinter import messagebox
import math as m

'''
Aufgabe:
Erstellen Sie einen Programmcode in der Programmiersprache - Python zur Berechnung des Druck-verlustes
in einer Rohrstrecke bei reibungsbehafteten, stationären und inkompressiblen Strömungen.
'''

#Berechnenfunktionen
#Berechnen der Reynoldszahl
def calcReNumber(volSt, d, visc):
    w = volSt*4/(m.pow(d, 2)*3.14159265359) #mittlere Geschwindichkeit in m/s
    re = w*d/visc
    return re


#rekursive Berechnung nach Prandtl und Karman Formel
def lambdaRekursivPK(l, re):
    x = 1 / m.sqrt(2 * m.log10(re*m.sqrt(l)-0.8))
    if l == x:
        lm = l
    else:
        lm = lambdaRekursivPK(x, re)
    return lm


#rekursive Berechnung nach Moody Formel
def lambdaRekursivM(l, re, y):
    x = 0.0055 + 0.15 * (2.51/(re * m.sqrt(l)) + y*0.269)
    if l == x:
        lm = l
    else:
        lm = lambdaRekursivM(x, re, y)
    return lm


#rekursive Berechnung nach Prandl-Colebrook Formel
def lambdaRekursivPC(l, re, y):
    x = 1 / m.sqrt(-2 * m.log10(2.51/(re * m.sqrt(l)) + y*0.269))
    if l == x:
        lm = l
    else:
        lm = lambdaRekursivPC(x, re, y)
    return lm


#Rohrreibungszahlberechnen
def calcLambda(re, k, d):
    x = re*k/d
    if re < 2320:
        lm = 64/re #wenn re < 2320
    else:
        if x < 65:
            if 2320 < re < 100000:
                #nutzen Blasiui Formel
                lm = 0.3164 * m.pow(re, -0.25)
                #print ("Blasius")
            elif 100000 <= re < 5000000:
                #nutzen Nikuradse Formel
                lm = 0.0032 + 0.221* m.pow(re, -0.237)
                #print ("Nikuradse")
            else:
                #falls re => 5*10^6 nutzen Prandl und v.Karman Formel
                lm = lambdaRekursivPK(0.02, re)
                #print ("Prandl und Karman")
        elif x > 1300:
            wahl = 1
            if wahl == 1:
                #nutzen Prandtl und Nikuradse Formel
                lm = 1 / m.pow((2*m.log10(3.71 * d / k)),2)
                #print ("Prandl und Nikuradse")
            else:
                #Moody Formel
                y = k/d
                lm = lambdaRekursivM(0.02, re, y)
                #print ("Moody") 
        else:
            #Uebergangsgebiet
            #Prandl-Colebrook Formel
            y = k/d
            lm = lambdaRekursivPC(0.02, re, y) #hier wieder rekursiv
            #print ("Prandl und Colebrook")
    return lm


def calcDruckverlust(lm, L, d, V, dichte):
    A = m.pi * m.pow(d, 2)/4
    w = V/A
    #w - mittlere Stroemungsgeschwindigkeit
    h = lm * L* m.pow(w, 2) / (2*9.8*d) #in [m]
    druckWert = dichte*9.8*h/100000 #convert to bar
    #1 bar = 100000 pascal
    #1 bar = 1*10^5 kg/m*s^2
    return druckWert
    

#Eingabe auslesen und ergebnisse aufschreiben
def getResult():
    try:
        dVal = float(diameter.get())/1000 #Durchmesser auslesen und in meter konvertieren
        rVal = float(rWert.get())/1000 #Rauhigkeitswertauslesen und in meter konvertieren
        vVal = float(visc.get()) #Vuskisitaet / Kin.Zaehigkeit auslesen
        lenVal = float(length.get())*1000 #km in meter
        volStVal = float(volStrom.get())/3600 #Vol.Strom auslesen und m2/h in m2/s konvertieren
        dichteVal = float(dichte.get()) # dichte
        
        #Raynolds Zahl berechnen
        re = calcReNumber(volStVal , dVal, vVal)
        lm = calcLambda(re, rVal, dVal)
        drVerlust = round(calcDruckverlust(lm, lenVal, dVal, volStVal, dichteVal), 2) 
        result = "Rohrreibungszahl: " + str(round(lm,3)) + "\n" + "Druckverlust: " + str(drVerlust) + " bar"
        label1.configure(text = result)

    except Exception as ex:
        messagebox.showwarning(title = 'Warning', message = 'Die Eingabe ist ungültig! ')

#set up value from dict by key
def fluidQn(event):
    key = var.get()
    #Dictionary fuer Dichte
    dichteDict = {
    "Wasser (15°)" : 1000,
    "Wasser (30°)" : 1000, 
    "Wasser (45°)" : 1000,
    "Wasser (60°)" : 1000,
    "Wasser (75°)" : 1000,
    "Wasser (90°)" : 1000,
    "Heizöl" : 900
    }

    #Dictionary fuer kinematische Viskositaet
    viscDict = {
    "Wasser (15°)" : 1.13e-6, 
    "Wasser (30°)" : 7.80e-7, 
    "Wasser (45°)" : 5.70e-7,
    "Wasser (60°)" : 4.5e-7,
    "Wasser (75°)" : 4.0e-7,
    "Wasser (90°)" : 3.20e-7,
    "Heizöl" : 40e-6
    }
    dichte.delete(0, 'end')
    visc.delete(0,'end')
    dichte.insert(0, dichteDict[key])
    visc.insert(0, viscDict[key])

#dictionary for formulas selection if x>1300
def formel(event):
    keyFl = var2.get()
    formelDict = {
    "Moody" : 0,
    "Prandtl-Nikuradse" : 1
    }
    wahl = formelDict[keyFl]


##################
#Start GUI und App
myFont = 'Arial'
fSize = 11
smallFont = 9
inputWidth = 5
mainColor = 'gray90'
textColor = 'black'
xStart = 1

#main window
root = Tk()
root.title("Berechnung des Druckverlustes")
root.rowconfigure((2, 3), weight = 3)
root.geometry('400x650+200+200')
root.resizable(False, False)
root.configure(bg = mainColor)

frame = Frame(root, bg = mainColor)
frame.grid()
header = Label(frame, text = 'EINGABE: ', font = (myFont, fSize), padx = 5, pady = 5, bg = mainColor, fg = textColor)
header.grid(row = 1, column = xStart)

#Input
#ROW 2
diameter = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize))
Label(frame, text = "Rohrdurchmesser, d: ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 2, column = xStart)
diameter.grid(row = 2, column = 2)
Label(frame, text = " mm", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 2, column = 3)

#ROW 3
rWert = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize))
rWert.insert(0, "0")
Label(frame, text = "Rauhigkeitswert, k* : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 3, column = xStart)
rWert.grid(row = 3, column = 2)
Label(frame, text = " mm", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 3, column = 3)

#ROW 4
length = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize))
Label(frame, text = "Länge : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 4, column = xStart)
length.grid(row = 4, column = 2)
Label(frame, text = " km", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 4, column = 3)

#ROW 5
#declare before dropdown menu
dichte = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize), state = 'normal', textvariable = "default")
visc = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize), state = 'normal')

Label(frame, text = "Medium : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 5, column = xStart)
fluidList = ["Wasser (15°)", 
"Wasser (30°)", 
"Wasser (45°)",
"Wasser (60°)",
"Wasser (75°)",
"Wasser (90°)",
"Heizöl"]

var = StringVar(root)
var.set(fluidList[0])
drop1 = OptionMenu(frame, var, *fluidList, command = fluidQn)
drop1.grid(row = 5, column = 2)
#ROW 7
rowDicht = 7
Label(frame, text = "Dichte : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowDicht, column = xStart)
dichte.grid(row = rowDicht, column = 2)
Label(frame, text = "kg/m³", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowDicht, column = 3)
#ROW 8
rowVisc = 8
Label(frame, text = "Kin. Zähigkeit : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowVisc, column = xStart)

visc.grid(row = rowVisc, column = 2)
Label(frame, text = "m²/s", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowVisc, column = 3)

#ROW 9
rowVol = 9
volStrom = Entry(frame, width = inputWidth, fg = 'black', font = (myFont, fSize))
Label(frame, text = "Vol. Strom : ", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowVol, column = xStart)
volStrom.grid(row = rowVol, column = 2)
Label(frame, text = " m³/h", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = rowVol, column = 3)

#ROW 10
rowFormel = 10
Label(frame, text = "Formel** :", font = (myFont, fSize), bg = mainColor, fg = textColor).grid(row = 10, column = xStart)
fList = ["Prandtl-Nikuradse", 
"Moody"]
var2 = StringVar(root)
var2.set(fList[1])
drop2 = OptionMenu(frame, var2, *fList, command = formel)
drop2.grid(row = rowFormel, column = 2)

#ROW 12
rowOut = 12
label1 = Label(frame,text = 'AUSGABE', bg = 'ghostWhite', width = 35, height = 10, font = (myFont, fSize)) 
label1.grid(row = rowOut, column = 0, columnspan = 7, rowspan = 2, stick = 'nsew', pady = 20, padx = 25)

#ROW 14 Hinweise
rowHin = 14
Label(frame, text = "Hinweise: \n * Rauhigkeitswert k wird mitberechnet nur  für turbulente \n Strömungen \n ** Formelauswahl gilt nur für RE*k/d > 1300 \n RE - Reynolds-Zahl ", font = (myFont, smallFont), bg = mainColor, fg = textColor, justify = LEFT).grid(row = rowHin, column = 0,columnspan = 7, rowspan = 2, pady = 20, padx = 25)


#Berechnen Button
rowBut = rowHin + 2
rowExit = rowBut + 1
Button(frame, text ='Berechnen', command = getResult, font = (myFont, fSize, 'bold')).grid(row = rowBut, column = 3)
#exit button
Button(frame, text = 'Schliessen', command = root.destroy,font = (myFont, fSize, 'bold')).grid(row = rowExit, column = 3)
root.mainloop()
