import os
matriz=[[],[]]
alfabeto=[]
errores=False


def hacerAutomata(expresion):
    for x in range(2):
        for y in range(len(alfabeto)+1):
             matriz[x].append("00")

def newState():
    global matriz
    matriz.append([])
    for x in matriz[0]:
        matriz[-1].append("00")
    return len(matriz)-1

def hacerAlfabeto(expresion): # crea array alfabeto
    global alfabeto
    letras="*+()"
    for x in expresion:
        if x not in letras:
            if x not in alfabeto:
                alfabeto+=x
    hacerAutomata(expresion)
    spliter(expresion,0,1)

def spliter(expresion,qinicial,qfinal):
    global errores
    #string,array,int,int
    arrayExpresion=[]
    letrainicial=0
    openParentesis=0
    #print("recibi",expresion)
    for x in range(len(expresion)):
        if expresion[x] not in alfabeto:
            if expresion[x] =="+":
                if openParentesis==0:
                    arrayExpresion.append(expresion[letrainicial:x])
                    letrainicial=x+1
            elif expresion[x] =="(":
                openParentesis+=1
            elif expresion[x] ==")":
                openParentesis-=1
                if openParentesis<0:
                    print("error, parentesis no cerrado")
                    errores=True
                    return -1
    arrayExpresion.append(expresion[letrainicial:])
    #print(arrayExpresion)
    splitunion(arrayExpresion,qinicial,qfinal)

def splitunion(expresion,qinicial,qfinal):
    #print("empezando splitunion",qinicial,qfinal)
    global errores
    for x in expresion:
        if len(x)==1:
            if(x) not in alfabeto:
                print("error, operacion repetida")
                errores=True
                return -1
            for z in range(len(alfabeto)):
                if alfabeto[z] == x:
                    matriz[qinicial][z]=qfinal
                    break
                    #c encontro un path
        elif x[0]=="(" and x[-1]==")":
            if(len(x)>2):
                parentesisa=0
                c=1
                while c<len(x)-1:
                    if x[c]=="(":
                        parentesisa+=1
                    elif x[c]==")":
                        parentesisa-=1
                        if parentesisa<0:
                            parentesisa=20
                            break
                    c+=1
                if parentesisa==0:
                    #print("tencontre")
                    spliter(x[1:-1],qinicial,qfinal)
                else:
                    cspliter(x,qinicial,qfinal)
            else:
                print("error, nada entre parentesis")
                errores=True
                return -1
        else:
            cspliter(x,qinicial,qfinal)

def cspliter(expresion,qinicial,qfinal):
    #print("cspliter recibi",expresion)
    arrayExpresion=[]
    openParentesis=0
    lastopen=-1
    for x in range(len(expresion)):
        if expresion[x]==")":
            openParentesis-=1
        if x+1<len(expresion):
            if expresion[x+1] == "*":
                if openParentesis==0:
                    if expresion[x] in alfabeto:
                        arrayExpresion.append(expresion[x:x+2])
                    elif expresion[x] ==")":
                        arrayExpresion.append(expresion[lastopen:x+2])
            else:
                if openParentesis==0:
                    if expresion[x] in alfabeto:
                        arrayExpresion.append(expresion[x])
                    elif expresion[x] ==")":
                        arrayExpresion.append(expresion[lastopen:x+1])
                    elif expresion[x] =="(":
                        lastopen=x
                        openParentesis+=1
        else:
            if openParentesis==0:
                if expresion[x] in alfabeto:
                    arrayExpresion.append(expresion[x])
                elif expresion[x] ==")":
                    arrayExpresion.append(expresion[lastopen:x+1])
                elif expresion[x] =="(":
                    lastopen=x
                    openParentesis+=1

    csplit(arrayExpresion,qinicial,qfinal)

def csplit(expresion,qinicial,qfinal):
    #print("empezando Cplit",qinicial,qfinal)
    global matriz
    global errores
    #print(matriz)
    qending=qfinal
    indexCounter=1
    for x in expresion:
        if len(x)==1:
            if(x) not in alfabeto:
                print("error, operacion repetida ")
                errores=True
                return -1
            for z in range(len(alfabeto)):
                if alfabeto[z] == x:
                    if indexCounter >= len(expresion):
                        #print("last de una letra")
                        #print("desde",qinicial,"hasta",qfinal)
                        matriz[qinicial][z]=qending
                        #print(matriz)
                        break
                    else:
                        qfinal=newState()
                        #print(len(matriz))
                        #print("desde",qinicial,"hasta",qfinal)
                        matriz[qinicial][z]=qfinal
                        qinicial=qfinal
                        qfinal=qending
                        #print("pathde 1 letra")
                        #print(matriz)
                        break
                    #c encontro un path
        elif x[0]=="(" and x[-1]==")":
            if(len(x)>2):
                if indexCounter >= len(expresion):
                    #print("last parentesis")
                    spliter(x[1:-1],qinicial,qending)
                    break
                else:
                    qfinal=newState()
                    #print("parentesis",qinicial,qfinal)
                    spliter(x[1:-1],qinicial,qfinal)
                    qinicial=qfinal
                    qfinal=qending
            else:
                print("invalid syntax, no hay nada entre parentesis")
                errores=True
                return -1
        else:
            if indexCounter >= len(expresion):
                #print("last bunch")
                asterisk(x,qinicial,qending)
                break
            else:
                #print("bunch")
                qfinal=newState()
                asterisk(x,qinicial,qfinal)
                qinicial=qfinal
                qfinal=qending
        indexCounter+=1

def asterisk(expresion,qinicial,qfinal):
    global errores
    if expresion[-1] == "*":
        if(expresion[-2]==")"):
            nueva=newState()
            matriz[qinicial][-1]=nueva
            matriz[nueva][-1]=qfinal
            spliter(expresion[1:-2],nueva,nueva)
        else:
            if len(expresion)==2:
                for z in range(len(alfabeto)):
                    if alfabeto[z] == expresion[0]:
                        nueva=newState()
                        matriz[qinicial][-1]=nueva
                        matriz[nueva][-1]=qfinal
                        matriz[nueva][z]=nueva
                        break
            else:
                print("error, fallo la creacion")
                errores=True
                return -1

def encontrar(character):
    for z in range(len(alfabeto)):
        if alfabeto[z] == character:
            return z

def evaluarCadena(cadena):
    resultado=[]
    resultado+=rec(0,cadena)
    if 1 in resultado:
        #print(cadena, "es valida")
        return True
    else:
        #print(cadena, "no es valida")
        return False

def rec(estado,cadena):#continue todos los e aun sin cadena
    resultado=[]
    #print("entraaa en",estado)
    #print(matriz[estado][-1])
    if len(cadena)>0:
        #print("caso de muchoss",cadena,"estado:",estado)
        nuevoEstado=rec(estado,cadena[:-1])#es un array de str
        #print("estados resultantes de",cadena,nuevoEstado)
        for x in nuevoEstado:
            if x != "00":
                #procesar estados
                agregar=matriz[x][encontrar(cadena[-1])]
                if agregar not in resultado and agregar!="00":
                    resultado.append(agregar)
                #son los resultados
                for y in resultado:
                    if y!="00":
                        if matriz[y][-1]!="00" and matriz[y][-1] not in resultado:
                            resultado.append(matriz[y][-1])
        #print("resultado de",cadena, resultado)

    else:
        if matriz[estado][-1]!="00":
            resultado.append(matriz[estado][-1])
        resultado.append(estado)#regresa lista
    if not resultado:
        return ["00"]
    return resultado

def buscarArchivos(path):
    cadenasAceptadas=[]
    for r,d,f in os.walk(path):
        mandar=""
        for archivo in f:
            for letra in archivo:
                if letra in alfabeto:
                    mandar+=letra
                    if(evaluarCadena(mandar)):
                        cadenasAceptadas.append(os.path.join(r, archivo))
                        break
                else:
                    mandar=""
            mandar=""
        if mandar:
            evaluarCadena(cadena)
    return cadenasAceptadas

def buscarPrueba(path):
    palabra=""
    for r,d,f in os.walk(path):
        for archivo in f:
            for letra in archivo:
                palabra+=letra
            print(palabra)
            palabra=""
            break


                #manda el mandar y continua
        #si f tiene alguna letra del alfabeto
input1=input("registra la expresion regular\n")
input1.strip()
currentPath='C:\\Users\\edgar\\Desktop\\pruebas'
hacerAlfabeto(input1)
print(alfabeto)
print(matriz)
if not errores:
    print("matriz exitosa")
    if input("current path es: "+currentPath+"\n desea cambiarla? y/n\n")=='y':
        currentPath=input("ingrese el path\n")
    print("buscando archivos\n")
    arcg=buscarArchivos(currentPath)
    for i in arcg:
        print(i)
else:
    print("ocurrio un error")
#evaluarCadena("abc")
