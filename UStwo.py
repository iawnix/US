#!/home/hang/.conda/envs/py37/bin/python
#############################################################################
##python UStwo.py -Xmove 1 -Xfix 2 -XF 10 -Xname X -Xmin 1.0 -Xmax 10.0 -Xfoot 1 -Ymove 3 -Yfix 4 -YF 10 -Yname Y -Ymin 3.0 -Ymax 10.0 -Yfoot 1##
##Linux python3.7
##iawnix HENU
#############################################################################

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
        return out1

def cmdout2list(string : str) -> list:
    var = []
    for i in string.split("\n"):
        if i != "":
            var.append(i)
    return var

class US2Init():  
    def __init__(self,Xmove,Xfix,Ymove,Yfix,XF,YF,OUT_str) -> None:
        self.Xmove = Xmove
        self.Xfix = Xfix
        self.Ymove = Ymove
        self.Yfix = Yfix
        self.out = OUT_str #CharNum_NumCharNum_Num
        self.XF = XF
        self.YF = YF

    def USIn(self):
        line = [
            "md1-NVT"                                                                      #0
            ,"Model: 12 angstrom cut off, 5ns MD with restraints"                           #1
            ," &cntrl"                                                                      #2
            ," imin   = 0,"                                                              #3
            ," irest  = 1,"                                                              #4
            ," ntx    = 5,"                                                              #5
            ," ntb    = 1,"                                                                   #6
            ," ntr    = 1,"                                                                   #7
            ," restraint_wt=6000.0,"                                                                                    #8
            ," restraintmask=':426@CA|:368@CA',"                                                        #9
            ," iwrap  = 1,"                                                              #10
            ," cut    = 12.0,"                                                           #11
            ," ntc    = 2,"                                                                  #12
            ," ntf    = 2,"                                                                  #13
            ," tempi  = 300.0,"                                                      #14
            ," temp0  = 300.0,"                                                      #15
            ," nmropt=1,"                                                                   #16
            ," ntt    = 3,"                                                                         #17
            ," gamma_ln = 1.0,"                                                             #18
            ," nstlim = 500000, dt = 0.002"                                                  #19
            ," ntpr = 1000, ntwx = 1000, ntwr = 1000"                                                       #20
            ," /"                                                                          #21
            ," &wt type='DUMPFREQ', istep1=100/"                                                        #22
            ," &wt type='END'/"                                                     #23
            ," DISANG=chi.rst"                                                      #24
            ,"DUMPAVE=o23_5t25_5.dat"                                                     #25
            ," END"                                                                      #26
            ," END"                                                                      #27
        ]
        echo1 = lambda l,out : "echo \"{}\" > {}.in".format(l,out)     # 解决in文件中出现的单引号     
        echo2 = lambda l,out : "echo \"{}\" >> {}.in".format(l,out)

        vardat = lambda str_ : " DUMPAVE={}.dat".format(str_) 
        line[25] = vardat(self.out)
        for i in range(len(line)):
            if i == 0:
                runCMD( echo1(line[i],self.out) )
            else:
                runCMD( echo2(line[i],self.out) )
    
    def out_str2XY(self):
        # CharNum_NumCharNum_Num
        replaceSS = ""
        for ch in self.out:
            if ch == "_" or ch.isalpha():
                replaceSS += " "
            else:
                replaceSS += ch
        purenum = replaceSS.split(" ")
        for i in purenum:
            if i == "":
                purenum.remove(i)
        x,y = ".".join(purenum[:2]),".".join(purenum[2:])
        return (x,y)

    def chi(self):
        lin1= lambda move,fix,xy,F : "&rst iat={},{}, r1=-600, r2={}, r3={}, r4=600, rk2 = {},rk3 = {},".format(move,fix,xy,xy,F,F)
        lin2 = "/"
        lin3 = " "
        echo1 = lambda line : "echo '{}' > chi.rst".format(line)
        echo2 = lambda line : "echo '{}' >> chi.rst".format(line)
        X,Y = self.out_str2XY()
        runCMD( echo1(lin1(self.Xmove,self.Xfix,X,self.XF)) )
        runCMD( echo2(lin2) )
        runCMD( echo2(lin1(self.Ymove,self.Yfix,Y,self.YF)) )
        runCMD( echo2(lin2) )
        runCMD( echo2(lin3) )

    def run(self):
        self.chi()
        self.USIn()

class Parm():
    def __init__(self) -> None:
        self.move = []          #x y
        self.fix = []           #x y
        self.F = []             #x y
        self.name = []          #x y
        
    def get(self):
        parser = argparse.ArgumentParser(description='执行二维伞形采样')
        parser.add_argument('-Xmove', type=str, nargs=1,help='num]')
        parser.add_argument('-Xfix', type=str, nargs=1,help='num]')
        parser.add_argument('-XF', type=str, nargs=1,help='num]')
        parser.add_argument('-Xname', type=str, nargs=1,help='char]')
        parser.add_argument('-Xmin', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Xmax', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Xfoot', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Ymove', type=str, nargs=1,help='num]')
        parser.add_argument('-Yfix', type=str, nargs=1,help='num]')
        parser.add_argument('-YF', type=str, nargs=1,help='num]')
        parser.add_argument('-Yname', type=str, nargs=1,help='char]')
        parser.add_argument('-Ymin', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Ymax', type=str, nargs=1,help='num.num]')
        parser.add_argument('-Yfoot', type=str, nargs=1,help='num.num]')
        return parser.parse_args()
# 用于生成任务串
    def run(self):
        my = self.get()
        out,rst,xy,x_list,y_list,x_y_rst_dif = [],[],[],[],[],[]
        X_num,Y_num = 0,0
        Xmin,Xmax,Ymin,Ymax,Xfoot,Yfoot = Decimal(my.Xmin[0]),Decimal(my.Xmax[0]),Decimal(my.Ymin[0]),Decimal(my.Ymax[0]),Decimal(my.Xfoot[0]),Decimal(my.Yfoot[0])
        self.move,self.fix,self.name,self.F = [my.Xmove[0],my.Ymove[0]],[my.Xfix[0],my.Yfix[0]],[my.Xname[0],my.Yname[0]],[my.XF[0],my.YF[0]]
        while Xmin <= Xmax:
            x_list.append(str(Xmin))
            Xmin += Xfoot
            X_num += 1
        while Ymin <= Ymax:
            y_list.append(str(Ymin))
            Ymin += Yfoot
            Y_num += 1
        for x in x_list:
            for y in y_list:
                content = "{}{}{}{}".format(my.Xname[0],x,my.Yname[0],y)
                out.append(content.replace('.','_'))
        for m in range(1,X_num+1):
            dif = (m-1)*Y_num+1-1
            x_y_rst_dif.append(dif)
        for out_index in range(len(out)):
            if out_index in x_y_rst_dif:
                if out_index == 0:
                    rst.append("first")
                else:
                    rst.append(out[out_index-Y_num])
            else:
                rst.append(out[out_index-1])
        return [rst,out]

def out2dir(in_,out):
    #f = ["{}.rst".format(in_),"{}.in".format(out),"chi.rst","{}.cdf".format(out),"{}.dat".format(out),"{}.out".format(out),"mdinfo"]
    f = ["{}.in".format(out),"chi.rst","{}.cdf".format(out),"{}.dat".format(out),"{}.out".format(out),"mdinfo"]
    #f = ["{}.in".format(out),"chi.rst"]
    ss = " ".join(f)
    runCMD("mkdir {}".format(out))
    runCMD("mv {} ./{}".format(ss,out))
    runCMD("cp -r {} ./{}".format("{}.rst".format(out),out))

def rst2dir(out_lis):
    for i in out_lis:
        runCMD("mv ./{}.rst ./{}".format(i,i))
    
def main():
    my = Parm()
    Parm_Out = my.run()

    pmemdcuda = lambda in_,out :"pmemd.cuda -O -i {}.in -p model.prmtop -c {}.rst -ref {}.rst -r {}.rst -o {}.out -x {}.cdf".format(out,in_,in_,out,out,out)
    if len(Parm_Out[0]) == len(Parm_Out[0]):
        for rst_index in range(len(Parm_Out[0])):
            rst = Parm_Out[0][rst_index]
            out = Parm_Out[1][rst_index]
            US2Init(my.move[0],my.fix[0],my.move[1],my.fix[1],my.F[0],my.F[1],out).run()
            runCMD(pmemdcuda(rst,out))
            #print(pmemdcuda(rst,out))
            out2dir(rst,out)
        rst2dir(Parm_Out[1])
if __name__ == "__main__":
    main()
