#!/home/hang/.conda/envs/py37/bin/python
#############################################################################
##python UStwo.py -Xmove 1 -Xfix 2 -XF 10 -Xname X -Xmin 1.0 -Xmax 10.0 -Xfoot 1 -Ymove 3 -Yfix 4 -YF 10 -Yname Y -Ymin 3.0 -Ymax 10.0 -Yfoot 1##
##Linux python3.7
##iawnix HENU
##要求当前工作目录下只存在需要补作业的目录
#############################################################################
import sys
import subprocess
import argparse
from decimal import Decimal
import os

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
        return out1

def cmdout2list(string : str) -> list:
    var = []
    for i in string.split("\n"):
        if i != "":
            var.append(i)
    return var

# 此函数用于读取当前目录下需要Bu时间的文件夹
def GetWorkPATH():
    Now = os.getcwd()
    dir = []
    for root, dirs,files in os.walk(Now):
        for d in dirs:
            dir.append(d)
        return dir
    
# 此函数用于在Bu目录下初始化所需要的文件
## 需要model.prmtop start.rst .in chi.rst
## 注意in文件需要修改
## 因此可以读取cdf的文件名
## model.prmtop 默认在../../中
class InitUSBu():
    def __init__(self,dp,ntpr,ntwx,ntwr,nstlim,dt) -> None:
        
        self.ntpr = ntpr                                  #这些参数是固定的                
        self.ntwx = ntwx                                #这些参数是固定的
        self.ntwr = ntwr                                #这些参数是固定的 
        self.nstlim = eval(nstlim)               #这些参数是固定的      
        self.dt = Decimal(dt)                       #这些参数是固定的
        self.in_out = []
        os.chdir(dp)
        self._init()
        
    def alterIn(self):
        cmd_1 = "sed -i '20c  nstlim = {}, dt = {},' {}.in".format(self.nstlim,self.dt,self.in_out[1])
        cmd_2= "sed -i '21c  ntpr = {}, ntwx = {}, ntwr = {},' {}.in".format(self.ntpr,self.ntwx,self.ntwr,self.in_out[1])
        cmd_3 = "sed -i '26c DUMPAVE={}.dat' {}.in".format(self.in_out[1],self.in_out[1])
        runCMD(cmd_1)
        runCMD(cmd_2)
        runCMD(cmd_3)
    def _init(self):

        Now = os.getcwd()
        for root,dirs,files in os.walk(Now):
            for f in files:
                if f.split(".")[-1] == "in":
                        var = f.split(".")[0]
        
        os.mkdir("Bu")
        os.system("cp -r {}.rst ./Bu".format(var))
        os.system("cp -r ./chi.rst ./Bu")
        os.system("cp -r ../model.prmtop ./Bu/")
        os.system("cp -r ./{}.in ./Bu/{}Bu.in".format(var,var))
        # 修改
        os.chdir("Bu")
        self.in_out.append(var)
        self.in_out.append(var+"Bu")
        self.alterIn()
        

def Parm():
        parser = argparse.ArgumentParser(description='伞形采样补时间')
        parser.add_argument('-ntpr', type=str, nargs=1,help='num]')
        parser.add_argument('-ntwx', type=str, nargs=1,help='num]')
        parser.add_argument('-ntwr', type=str, nargs=1,help='num]')
        parser.add_argument('-nstlim', type=str, nargs=1,help='num]')
        parser.add_argument('-dt', type=str, nargs=1,help='num.num]')
        return parser.parse_args()

def main():
    myp = Parm()

    Now = os.getcwd()
    work_list = GetWorkPATH()

    pmemdcuda = lambda in_,out :"pmemd.cuda -O -i {}.in -p model.prmtop -c {}.rst -ref {}.rst -r {}.rst -o {}.out -x {}.cdf".format(out,in_,in_,out,out,out)
    for i in work_list:
        # 需要注意初始化之后位于Bu的目录下
        Bu = InitUSBu(i,myp.ntpr[0],myp.ntwx[0],myp.ntwr[0],myp.nstlim[0],myp.dt[0])
        #print(pmemdcuda(Bu.in_out[0],Bu.in_out[1]))
        runCMD(pmemdcuda(Bu.in_out[0],Bu.in_out[1]))
        os.chdir(Now)

if __name__ == "__main__":
    main()
