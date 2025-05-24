#!/home/hang/.conda/envs/py37/bin/python
import subprocess
import sys
def GetFileName():
    ret = subprocess.Popen(args="ls",bufsize=-1,shell=True,encoding = "utf-8", stdout=subprocess.PIPE)
    ret.wait()
    sign = ret.returncode
    result = []
    if sign == 0:
        for i in ret.stdout.readlines():
            file = i.rstrip()
            if file.split(".")[1] == "dat":
                result.append(file)
        print("Success: read filename:{} \n".format(result))
    else:
        print("Error: read filename \n")

    return result


def CatToZ(filename,end,start):
    new = "".join((filename.split(".")[0],".z"))
    cmd_ = lambda filename,end,start,new:"cat {} | head -n {}| tail -n +{} >> {}".format(filename,end,start,new)
    cmd1 = lambda filename:"cat {}".format(filename)
    cmd2 = lambda end:"head -n {}".format(end)
    cmd3 = lambda start, new:"tail -n +{} >> {}".format(start,new)
    ret1 = subprocess.Popen(cmd1(filename),bufsize=-1,shell=True,encoding = "utf-8", stdout=subprocess.PIPE)
    ret2 = subprocess.Popen(cmd2(end),bufsize=-1,shell=True,encoding = "utf-8",stdin=ret1.stdout,stdout=subprocess.PIPE)
    ret3 = subprocess.Popen(cmd3(start,new),bufsize=-1,shell=True,encoding = "utf-8",stdin=ret2.stdout)
    ret3.communicate(input=None)
    if not ret3.returncode:
        print("Success: {}".format(cmd_(filename,end,start,new)))
    return 0

def main():
    start = sys.argv[1]
    end = sys.argv[2]

    file_list = GetFileName()

    tmp = []
    for file in file_list:
        tmp.append(CatToZ(file,end,start))
    
    if tmp.count(0) == len(file_list):
        print("OK")
    else:
        print("Error: please check stdout")

if __name__ == "__main__":
    main()