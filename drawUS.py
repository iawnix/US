#!/home/hang/.conda/envs/py37/bin/python
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
import os

def GetDAT(path):
    out = []
    for file in os.listdir(path):
                if ".dat" in file:
                    out.append(file.split(".")[0])
    return out
        
def draw(var : dict):
    plt.figure(figsize=(7,5),dpi=300)
    key = list(var.keys())
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    for i in range(len(key)):
        plt.plot(var[key[i]]["fra"],var[key[i]]["F"],color[i], linestyle='-',marker = 'o',markersize = 0.01, linewidth = 1, label = key[i],alpha=0.6)

    plt.legend(markerscale= 200)
    plt.savefig("./all.jpg")
    plt.savefig("./all.tiff")

def main():

    path = "./"
    global color 
    color = ["r","b","y","g","m","gold","k","c","steelblue","pink"]
    
    dat = GetDAT(path)
    var_dict = {}
    for i in dat:
        var_dict["{}".format(i)] = pd.read_csv("{}.dat".format(i),header=None,names=["fra","F"],sep=",")

    draw(var_dict)
if __name__ == "__main__":
    main()