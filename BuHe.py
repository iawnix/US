import os

def GetFreq(lis):
    freq = {}
    result = []
    for i in lis:
        freq[i] = freq.get(i,0) + 1
    for j in freq.keys():
        if freq[j] == 2:
            result.append(j)
        elif freq[j] == 1:
            print("{} is only 1".format(j))
        else:
            print("please check {}".format(j))
    return [i for i in set(result)]

def GetFileName():
    os.system("ls >> dirname.txt")
    result = []
    with open("./dirname.txt",mode="r") as dir:
        for i in dir.readlines():
            file = i.rstrip("\n")
            if file.split(".")[1] not in ["py","txt"]:
                if "Bu.dat" in file:
                    result.append(file[:-6])
                else:
                    result.append(file[:-4])
    os.system("rm dirname.txt")
    return GetFreq(result)

def DivideName(name):
    start = 0               
    move = 0
    result = []
    for i in range(1,len(name)):
        move = i
        if name[i].isalpha():
            result.append("".join([j for j in name[start:move]]).replace("_","."))
            start = i
        if i == len(name) - 1:
            result.append("".join([j for j in name[start:move + 1]]).replace("_",".")) 
    return result

def SplitNum(var):
    tmp = []
    for i in var:
        tmp.append(i[0])
        tmp.append(i[1:])
    return tmp

def getmetadatafile(file,lis,spring_x,spring_y,n):
    loc_with_x = lis[0]
    loc_with_y = lis[1]
    line = "{} {} {} {} {}".format(os.path.abspath(file),loc_with_x,loc_with_y,spring_x*2,spring_y*2)
    with open("metadatafile",mode='a') as M:
        if n == 0:
            M.writelines('#'+"\n")
        M.writelines(line+"\n")

def main(spring_x,spring_y):
    cont1 = lambda a,b,c,d:"{}{}{}{}.dat".format(a,b,c,d)
    cont2 = lambda a,b,c,d:"{}{}{}{}Bu.dat".format(a,b,c,d)
    cont3 = lambda a,b,c,d:"{}{}{}{}all.dist".format(a,b,c,d)
    cmd_ = lambda a,b,c,d,e,f:"cat {} {} >> {}{}{}{}all.dist".format(a,b,c,d,e,f)
    file = GetFileName()
    for i in range(len(file)):
        char1,num1,char2,num2 = SplitNum(DivideName(file[i]))
        num1 = num1.replace(".","_")
        num2 = num2.replace(".","_")
        s=os.system(cmd_(cont1(char1,num1,char2,num2),cont2(char1,num1,char2,num2),char1,num1,char2,num2))
        getmetadatafile(cont3(char1,num1,char2,num2),[num1.replace("_","."),num2.replace("_",".")],spring_x,spring_y,i)


if __name__ == '__main__':
    print("starting")
    main(10,10)
    print("OK")








