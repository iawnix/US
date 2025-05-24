import os
import sys
import subprocess
from decimal import Decimal



##########################################################
## Author:iawnix, HENU                                  ##
## Date: 20220405                                       ##
## python3.8                                            ##
## RUNFORMAT: python TouchMetaDataFile.py xf yf         ##
## FILEFORMAT: (alpha)(num)_(num)(alpha)(num)_(num).dat ##
##########################################################
def Pipe(cmd1 : str, cmd2 : str) -> str:
    ret = subprocess.Popen(cmd1,bufsize=-1,shell=True,encoding="utf-8",stdout = subprocess.PIPE)
    out = ret.communicate(input=None)
    out1,error1 = out[0],out[1]
    if error1 != None:
        print("ERROR: {} ".format(cmd1))
        print(error1)
        sys.exit(1)
    else:
        ret_ = subprocess.Popen(cmd2,bufsize=-1,shell=True,encoding="utf-8",stdout = subprocess.PIPE,stdin = subprocess.PIPE)
        out_ = ret_.communicate(input=out1)
        out2,error2 = out_[0],out_[1]
        if error2 != None:
            print("ERROR: {} ".format(cmd2))
            print(error2)
            sys.exit(1)
        else:
            return out2


class MetaDataFile():

    def __init__(self):
        self.workpath = os.getcwd()
        self.spring_x = str(2*Decimal(sys.argv[1]))     #XF
        self.spring_y = str(2*Decimal(sys.argv[2]))     #YF
        self.dat = []
    def CMDout(self,cmd1 : str, cmd2 : str) -> list:
        ret = []
        
        out = Pipe(cmd1,cmd2).split("\n")
        # checknull
        for s in out:
            if s != "":
                ret.append(s)
            else:
                pass

        return ret

    def devideXY(self, datfilename : str) -> list:
        #o1000_2000g2000_4000000.dat
        x,y = [],[]

        nosuffix = datfilename[:-4]
        replacess = ""
        for ch in nosuffix:
            if ch == "_" or ch.isalpha():
                replacess += " "
            else:
                replacess += ch
        # 1000 2000 2000 4000000
        purenum = replacess.split(" ")
        for i in purenum:
            if i == "":
                purenum.remove(i)
            else:
                pass
        x,y = purenum[:2],purenum[2:]
        return [x,y]
    def line2MetaDataFile(self,cont: str) -> int:
        return os.system("echo {} >> metadatafile".format(cont))


    def run(self):
        self.dat = [i for i in self.CMDout("ls","grep '.dat' ")]
        
        if not os.system("echo '#' >> metadatafile"):
            
            line = lambda path,f,xz,xx,yz,yx,xf,yf:"{}/{} {}.{} {}.{} {} {} ".format(path,f,xz,xx,yz,yx,xf,yf)

            for da in self.dat:
                f = da[:-4] + ".dist"
                xy = self.devideXY(da)
                if not self.line2MetaDataFile(line(self.workpath,f,xy[0][0],xy[0][1],xy[1][0],xy[1][1],self.spring_x,self.spring_y)):
                    pass
                else:
                    print("ERROR write {} to metadatafile".format(da))
        else:
            print("ERROR write # to metadatafile")


        if not os.system("echo '\n' >> metadatafile"):
            pass
        else:
            print("ERROR write NULL LINE to metadatafile")
            

def main():
    myclass = MetaDataFile()
    myclass.run()

if __name__ == "__main__":
    main()



