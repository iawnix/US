#!/home/hang/.conda/envs/py37/bin/python
#############################################################################
##python USone.py -Xmove 12190 -Xfix 12100 -XF 10 -Xmin 22 -Xmax 50 -foot 1##
##Linux python3.7
##iawnix HENU
#############################################################################



import sys
import subprocess
import argparse
from decimal import Decimal

import sys
import subprocess
import argparse
from decimal import Decimal

def runCMD(cmd:str) -> str:
    ret1 = subprocess.Popen(cmd,bufsize=-1,shell=True,encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret1_ = ret1.communicate(input=None)
    out1,error1 = ret1_[0],ret1_[1]
    code = ret1.returncode
    if error1 != "":
        if not code:								# 解决UBUNTU上浮点数的Note导致程序跳出
            print("Sucessful: {},But: {}".format(cmd,error1))
            return(out1)
        else:
            print("Error: {}".format(error1))
            sys.exit(1)
    else:
        print("Sucessful: {}".format(cmd))
        return(out1)

def cmdout2list(string : str) -> list:
    var = []
    for i in string.split("\n"):
        if i != "":
            var.append(i)
    return var

def num2two(num : str) -> list:
    if "." in num:
        var = num.split(".")
        num1,num2 = var[0],var[1]
    else:
        num1,num2 = num,"0"

    return [num1,num2]

class USInit():
    def __init__(self,Xmove,Xfix,X,XF) -> None:
        self.Xmove = Xmove
        self.Xfix = Xfix
        self.X = X
        self.XF = XF
    def chi(self):
        lin1= lambda Xmove,Xfix,X,XF : "&rst iat={},{}, r1=-600, r2={}, r3={}, r4=600, rk2 = {},rk3 = {},".format(Xmove,Xfix,X,X,XF,XF)
        lin2 = "/"
        lin3 = " "
        echo1 = lambda line : "echo '{}' > chi.rst".format(line)
        echo2 = lambda line : "echo '{}' >> chi.rst".format(line)
        runCMD( echo1(lin1(self.Xmove,self.Xfix,self.X,self.XF)) )
        runCMD( echo2(lin2) )
        runCMD( echo2(lin3) )

    def USIn(self):
        line = [
            "md-NVT"                                                                    # 0
            ,"Model: 12 angstrom cut off, 2ns MD with restraints"                       # 1
            ," &cntrl"                                                                  # 2
            ," imin   = 0,"                                                             # 3
            ," irest  = 1,"                                                             # 4
            ," ntx    = 5,"                                                             # 5
            ," ntb    = 1,"                                                             # 6
            ," ntr    = 1,"                                                             # 7
            ," restraint_wt=6000.0,"                                                    # 8
            ," restraintmask=':656@CA',"                                          # 9 Only Xfix
            ," iwrap  = 1,"                                                             # 10
            ," cut    = 12.0,"                                                          # 11
            ," ntc    = 2,"                                                             # 12
            ," ntf    = 2,"                                                             # 13
            ," tempi  = 300.0,"                                                         # 14
            ," temp0  = 300.0,"                                                         # 15
            ," nmropt = 1,"                                                             # 16
            ," ntt    = 3,"                                                             # 17
            ," gamma_ln = 1.0,"                                                         # 18
            ," nstlim = 1000000, dt = 0.002,"                                           # 19
            ," ntpr = 2000, ntwx = 2000, ntwr = 2000,"									# 20
            ," /"                                                                       # 21
            ," &wt type='DUMPFREQ', istep1=100/"                                        # 22
            ," &wt type='END'/"                                                         # 23
            ," DISANG=chi.rst"                                                          # 24
            ," DUMPAVE=10.5_20.dat"                                                     # 25
            ," END"                                                                     # 26
            ," END"                                                                     # 27
]
        vardat = lambda num1,num2,Xf : " DUMPAVE={}-{}_{}.dat".format(num1,num2,Xf) 
        

        var = num2two(self.X)
        num1,num2 = var[0],var[1]
        
        echo1 = lambda l,num1,num2,Xf : "echo \"{}\" > {}-{}_{}.in".format(l,num1,num2,Xf)     # 解决in文件中出现的单引号     
        echo2 = lambda l,num1,num2,Xf : "echo \"{}\" >> {}-{}_{}.in".format(l,num1,num2,Xf)

        line[25] = vardat(num1,num2,self.XF)
        for i in range(len(line)):
            if i == 0:
                runCMD( echo1(line[i],num1,num2,self.XF) )
            else:
                runCMD( echo2(line[i],num1,num2,self.XF) )

    def run(self):
        self.chi()
        self.USIn()

class Parm():
    
    def __init__(self) -> None:
        self.Xmove = []
        self.Xfix = []
        self.XF = []
        self._range = []

    def get(self):
        parser = argparse.ArgumentParser(description='执行一维伞形采样')
        parser.add_argument('-Xmove', type=str, nargs=1,help='num]')
        parser.add_argument('-Xfix', type=str, nargs=1,help='num]')
        parser.add_argument('-XF', type=str, nargs=1,help='num]')
        parser.add_argument('-Xmin', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Xmax', type=str, nargs=1,help='num.num]')
        parser.add_argument('-foot', type=str, nargs=1,help='num.num]')
        
        return parser.parse_args()

    def run(self):
        
        my = self.get()
        
        var = Decimal(my.Xmin[0])
        
        # 修复无法将移动原子拉进至固定原子的参数生成问题
        if var < Decimal(my.Xmax[0]):
            while var <= Decimal(my.Xmax[0]):
                self._range.append(var)
                var += Decimal(my.foot[0])
        elif var > Decimal(my.Xmax[0]):
            while var >= Decimal(my.Xmax[0]):
                self._range.append(var)
                var -= Decimal(my.foot[0])
        
        self.Xmove = my.Xmove[0]
        self.Xfix = my.Xfix[0]
        self.XF = my.XF[0]
        
def out2dir(in_,out):
    f = ["{}.rst".format(in_),"{}.in".format(out),"chi.rst","{}.cdf".format(out),"{}.dat".format(out),"{}.out".format(out),"mdinfo"]
    #f = ["{}.in".format(out),"chi.rst"]
    ss = " ".join(f)
    # 修复bug,分割格式错误导致文件目录创建异常
    var = out.split("_")[0]
    runCMD("mkdir {}".format(var))
    runCMD("mv {} ./{}".format(ss,var))
    runCMD("cp -r {} ./{}".format("{}.rst".format(out),var))

def main():

    my = Parm()
    my.run()
    print(my._range) 
    pmemdcuda = lambda in_,out :"pmemd.cuda -O -i {}.in -p model.prmtop -c {}.rst -ref {}.rst -r {}.rst -o {}.out -x {}.cdf".format(out,in_,in_,out,out,out)
    var = lambda num1,num2,Xf : "{}-{}_{}".format(num1,num2,Xf) 
    
    for i in range(len(my._range)):
        USInit(my.Xmove,my.Xfix,str(my._range[i]),my.XF).run()
        
        var1 = num2two(str(my._range[i]))
        num1,num2 = var1[0],var1[1]
        out = var(num1,num2,my.XF)
        
        if i == 0:
            in_ = "first"
        else:
            var2 = num2two(str(my._range[i-1]))
            num3,num4 = var2[0],var2[1]
            in_ = var(num3,num4,my.XF)
        #print(in_) 
        runCMD(pmemdcuda(in_,out))
        #print(pmemdcuda(in_,out))
        out2dir(in_,out)


if __name__ == "__main__":
    main()
