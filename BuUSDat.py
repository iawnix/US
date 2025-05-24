#!/home/hang/.conda/envs/py37/bin/python
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


def GetName():
    out = []
    dat = cmdout2list(runCMD("ls | grep \.dat"))
    # 去除dat
    for i in dat:
        out.append(i.split(".")[0])
    return out

def GroupFIle(f_lis):
    old = []
    Bu = []
    out = []
    for f in f_lis:
        if "Bu" in f:
            Bu.append(f)
        else:
            old.append(f)
    for id,it in enumerate(Bu):
        if it[:-2] in old:
            out.append(it[:-2])
        else:
            print("Error: {} can not find {}".format(it, it[:-2]))
    return out

def CatFile(f_lis):
    func = lambda f1: "cat {}.dat {}Bu.dat >> {}all.dist".format(f1,f1,f1)
    for i in f_lis:
        runCMD(func(i))

def main():
    f_lis = GetName()
    f_lis = GroupFIle(f_lis)
    CatFile(f_lis)

if __name__ == "__main__":
    main()
