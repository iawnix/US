#!/home/hang/.conda/envs/py37/bin/python
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math
from scipy import interpolate
from scipy.interpolate import RBFInterpolator
from scipy.interpolate import Rbf
from matplotlib.colors import TwoSlopeNorm 
from matplotlib.colors import LogNorm
from matplotlib.colors import ListedColormap

def ReadXYZ(fp):
    data = pd.read_csv(fp,sep =",",header=None)
    return data

def reShapeXYZ(data):
    z = data[2].to_list()
    # 生成z的坐标点
    z_xy = []
    for i in range(len(z)):
        z_xy.append((data[0][i],data[1][i]))

    X,Y = np.meshgrid(np.array(list(data.groupby(0).groups.keys())),np.array(list(data.groupby(1).groups.keys())))
    line,column = X.shape
    Z = np.zeros([line,column])
    count1 = 0
    count2 = 0
    checkZ = []
    for i in range(line):
        for j in range(column):
            try:
                ind = z_xy.index((X[i][j],Y[i][j]))
                Z[i][j] = z[ind]
                #if z[ind] == np.inf:
                #    Z[i][j] = 0
                #else:
                if Z[i][j] == 0:
                    print(i,j,"ymt",X[i][j],Y[i][j])
                count1 += 1
                checkZ.append(ind)
            except:
                Z[i][j] = 0
                print(i,j,"zjh")
                count2 += 1
    print("")
    print("Z not Null = {}".format(count1))
    print("Z Null = {}".format(count2))
    print("Save Z_origin_2.csv")
    pd.DataFrame(Z).to_csv("Z_origin_1.csv")
    print("Strat  to Replace inf of Z By zjh 's Ten-Cross-Average")
    print("---"*20)
    a, b = X.shape
    fZ = []
    for i in range(a):
        for j in range(b):
            if Z[i][j] == np.inf:
                sum = 0
                flag = 0
                if i - 1 >= 0:
                    # 上面有数
                    # 判断是否为inf
                    if Z[i-1][j] != np.inf and (i-1,j) not in fZ:
                        sum += Z[i-1][j]
                        flag += 1
                if i - 2 >= 0:
                    # 上面有数
                    # 判断是否为inf
                    if Z[i-2][j] != np.inf and (i-2,j) not in fZ:
                        sum += Z[i-2][j]
                        flag += 1
                       
                if i+1 <= a-1:
                    # 下面有数
                    # 判断是否为inf
                    if Z[i+1][j] != np.inf and (i+1,j) not in fZ:
                        sum += Z[i+1][j]
                        flag += 1
                if i+2 <= a-1:
                    # 下面有数
                    # 判断是否为inf
                    if Z[i+2][j] != np.inf and (i+2,j) not in fZ:
                        sum += Z[i+2][j]
                        flag += 1
                  
                if j - 1 >= 0:
                    # 左边有数
                    # 判断是否为inf
                    if Z[i][j-1] != np.inf and (i,j-1) not in fZ:
                        sum += Z[i][j-1]
                        flag += 1 
                if j - 2 >= 0:
                    # 左边有数
                    # 判断是否为inf
                    if Z[i][j-2] != np.inf and (i,j-2) not in fZ:
                        sum += Z[i][j-2]
                        flag += 1 
                     
                if j + 1 <= b-1:
                    # 右边有数
                    # 判断是否为inf
                    if Z[i][j+1] != np.inf and (i,j+1) not in fZ:
                        sum += Z[i][j+1]
                        flag += 1
                if j + 2 <= b-1:
                    # 右边有数
                    # 判断是否为inf
                    if Z[i][j+2] != np.inf and (i,j+2) not in fZ:
                        sum += Z[i][j+2]
                        flag += 1
                    
                if  flag:
                    Z[i][j] = sum/flag
                    print("({},{}): {} plots, sum is {:.2f}, Ave is {:.2f}".format(i,j,flag,sum,Z[i][j]))
                    fZ.append((i,j))
    print("---"*20)

    var = Z.flatten()
    var = var[np.isfinite(var)]                                         # 选取非Nan与非Inf
    print("Zmax={:.4f},Zmin={:.4f}".format(var.max(),var.min()))
    print("Save Z_origin_2.csv")
    pd.DataFrame(Z).to_csv("Z_origin_2.csv")
    return [X,Y,Z]

def XYZreshape(data):
    x = data.groupby(0).groups.keys()
    y = data.groupby(1).groups.keys()
    X,Y = np.meshgrid(np.array(list(x)),np.array(list(y)))

    Z = data[2].to_numpy().reshape(X.shape)
    # 对Z进行inf替换
                        
    return [X,Y,Z]

def InterNUM2(data,n):

    X,Y,Z = data[0].to_numpy(),data[1].to_numpy(),data[2].to_numpy()
    xmin = X.min()
    xmax = X.max()
    ymin = Y.min()
    ymax = Y.max()
    x = np.linspace(xmin,xmax,num = n,endpoint=True)
    y = np.linspace(ymin,ymax,num = n,endpoint=True)
    xx,yy = np.meshgrid(x,y)
    z = interpolate.griddata((X,Y),Z,(xx,yy), method='linear',rescale=1)
    pd.DataFrame(z).to_csv("z2.csv")
    return [xx,yy,z]

def InterNUM1(data,n):

    X,Y,Z = data
    xmin = X.min()
    xmax = X.max()
    ymin = Y.min()
    ymax = Y.max()
    x = np.linspace(xmin,xmax,num = n,endpoint=True)
    y = np.linspace(ymin,ymax,num = n,endpoint=True)
    xx,yy = np.meshgrid(x,y)
    z = interpolate.griddata((X.flatten(),Y.flatten()),Z.flatten(),(xx,yy), method='linear',rescale=1)
    pd.DataFrame(z).to_csv("z2.csv")
    return [xx,yy,z]

# 此函数用于插值之后的处理，此函数将数据中的inf替换为nan
def Finternum1(XYZ):
    X,Y,Z = XYZ
    if np.isnan(Z).any():
        var = Z.flatten()
        var = var[np.isfinite(var)]
        b = var.min()-1
        print("Inf in Zmatrix replace to np.nan")
        Z[np.isinf(Z)] = np.nan
    else:
        print("Inf not in Zmatrix")

    pd.DataFrame(Z).to_csv("Z-draw-withNan.csv",index=0)
    pd.DataFrame(Y).to_csv("Y-draw-withNan.csv",index=0)
    pd.DataFrame(X).to_csv("X-draw-withNan.csv",index=0)

    return (X,Y,Z)


def Finternum2(XYZ):
    X,Y,Z = XYZ
    if np.isnan(Z).any():
        var = Z.flatten()
        var = var[np.isfinite(var)]
        b = var.min()-1
        print("Nan and Inf in Zmatrix replace to {:.2f}".format(b))
        Z[np.isnan(Z)] = b
        Z[np.isinf(Z)] = b
        Z[np.isinf(Z)] = np.nan
    else:
        print("Nan and Inf not in Zmatrix")

    pd.DataFrame(Z).to_csv("Z-draw-noNan.csv",index=0)
    pd.DataFrame(Y).to_csv("Y-draw-noNan.csv",index=0)
    pd.DataFrame(X).to_csv("X-draw-noNan.csv",index=0)

    return (X,Y,Z)



# 此函数用于生成颜色条与颜色分割比例
# 有一些参数需要自行修改
def MyColorNorm():

    import matplotlib.colors as colors
    #colors_undersea = plt.cm.binary(np.linspace(0, 0.001, 256))
    colors_undersea = plt.cm.coolwarm(np.linspace(0, 0.5, 128))
    #colors_land = plt.cm.coolwarm(np.linspace(0, 1, 256))
    #colors_land = plt.cm.viridis(np.linspace(0, 1, 256))
    #colors_land = plt.cm.seismic(np.linspace(0, 1, 256))
    #colors_land = plt.cm.gist_ncar(np.linspace(0, 1, 256))
    colors_land = plt.cm.jet(np.linspace(0.5, 1, 128))
    #colors_land = plt.cm.brg(np.linspace(0, 1, 256))
    #colors_land = plt.cm.tab20c(np.linspace(0, 1, 256))
    #colors_land = plt.cm.tab20b(np.linspace(0, 1, 256))
    #colors_land = plt.cm.winter(np.linspace(0, 1, 256))
    #colors_land = plt.cm.rainbow(np.linspace(0, 1, 256))
    #colors_land = plt.cm.gist_rainbow(np.linspace(0, 1, 256))
    all_colors = np.vstack((colors_undersea, colors_land))
    terrain_map = colors.LinearSegmentedColormap.from_list('terrain_map', all_colors)
    #divnorm = colors.TwoSlopeNorm(vmin=-0.1, vcenter=0.0, vmax=22)
    divnorm = colors.TwoSlopeNorm(vmin=-0.1, vcenter=0.0, vmax=15)
    return terrain_map,divnorm

# 用于绘制热图
def draw2(xyz,mycn):
    
    
    #plt.rcParams["font.family"]="Times New Roman"
    plt.rcParams["font.family"]="arial"
    plt.rcParams["font.weight"]="bold"
    plt.rcParams["font.size"]=10
    
    plt.rcParams["axes.labelweight"] ="bold"
    fig,ax = plt.subplots(dpi=300) 
    #plt.rcParams["axes.titlesize"] = 10
    #plt.rcParams['xtick.labelsize'] = 10
    #plt.rcParams['ytick.labelsize'] = 10

    X,Y,Z = xyz
    
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)

    #ax.set_xlabel(r"Reaction coordinates $\alpha$ [Å]")
    #ax.set_ylabel(r"Reaction coordinates $\beta$ [Å]")
    ax.set_ylabel(r"TC2 (Å)")
    ax.set_xlabel(r"TC4 (Å)")

    #C=plt.contour(X,Y,Z,6,colors='black')  #生成等值线图
    #plt.contourf(X,Y,Z,5)
    #plt.clabel(C,inline=1,fontsize=10)
    #Pcolor= ax.pcolor(X,Y, Z,shading='auto',cmap=mycn[0], norm=mycn[1])   
    import matplotlib.colors as colors     
    #Pcolor= ax.pcolor(X,Y, Z,shading='auto',cmap="jet", norm=colors.TwoSlopeNorm(vmin=0, vcenter=6.15, vmax=12.3021))
    Pcolor= ax.pcolor(X,Y, Z,shading='auto',cmap="jet", norm=colors.TwoSlopeNorm(vmin=0, vcenter=7.15, vmax=14.3))
    #ax.set_xticks([13.5,16.5,19.5,22.5,25.5])
    #ax.set_yticks([10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5])
    #ax.set_yticks([6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5])

    
    #ax.invert_xaxis()
    #ax.invert_yaxis()
    cb = ax.figure.colorbar(Pcolor,ax=ax)
   
    cb.set_label("Free Energy Profile (kcal/mol)")
    plt.savefig("ByGdd-Linear-2D.tiff")
    plt.savefig("ByGdd-Linear-2D.jpg")
    
    
def draw3(xyz,mycn):
    fig = plt.figure(dpi = 300)
    plt.rcParams["axes.labelweight"] ="bold"
    #plt.rcParams["font.family"]="Times New Roman"
    plt.rcParams["font.family"]="arial"
    plt.rcParams["font.weight"]="bold"
    plt.rcParams["font.size"]=10

    X,Y,Z = xyz
    
    ax = fig.add_subplot(projection="3d")
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)

    ax.set_ylabel(r"RC2 (Å)")
    ax.set_xlabel(r"RC4 (Å)")
    ax.set_zlabel(r"Free Energy Profile (kcal/mol)")
    # 设置背景颜色
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))


    # 设置坐标轴
    #ax.zaxis.set_rotate_label(1)
    ax.set_xticks([-1,0,1,2,3])
    ax.set_yticks([-2,-1,0,1,2])
    ax.set_zticks([0, 5 , 10, 15, 20, 25])
    #ax.set_xticks([-0.5,0,0.5,1,1.5,2,2.5])
    #ax.set_yticks([-2.0,-1.5,-1,-0.5,0,0.5,1,1.5])
    #ax.set_zticks([0,2.5,5,7.5,10,12.5,15,17.5,20])

    ax.view_init(35,135)

    ax.plot_surface(X, Y, Z
                                    , rstride=1
                                    , cstride=1
                                    , cmap=mycn[0]
                                    ,linewidth=0
                                    , antialiased=False
                                    ,zorder=0
                                    ,alpha=1 
                                    ,norm = mycn[1])
    plt.savefig("ByGdd-Linear-3D.tiff")
    plt.savefig("ByGdd-Linear-3D.jpg")

def draw23(xyz,mycn):
    from mpl_toolkits.mplot3d import Axes3D  
    fig = plt.figure(dpi = 300)
    plt.rcParams["axes.labelweight"] ="bold"
    #plt.rcParams["font.family"]="Times New Roman"
    plt.rcParams["font.family"]="arial"
    plt.rcParams["font.weight"]="bold"
    plt.rcParams["font.size"]=10

    X,Y,Z = xyz
    
    ax = fig.add_subplot(projection="3d")
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)

    ax.set_ylabel(r"RC2 (Å)")
    ax.set_xlabel(r"RC4 (Å)")

    # 设置背景颜色
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    #ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([4, 4, 5, 4.4]))#前3个参数用来调整各坐标轴的缩放比例
    #ax.view_init(elev=35, azim=135)
    # 设置坐标
    #ax.set_xlim(X.min()-0.1, X.max()+0.1)
    #ax.set_zlim(Y.min()-0.1,Y.max()+0.1)
    #ax.set_zlim(Z.min()-20,Z.max()+20)
    ax.set_xlim(-0.7, 2.7)
    ax.set_ylim(-2.2,1.7)
    ax.set_zlim(-20,25)
    #ax.set_xlim(27.5, 7.5)
    #ax.set_ylim(35,10)
    #ax.set_zlim(-20,15)

    #ax.set_xticks([-0.5,0,0.5,1,1.5,2,2.5])
    #ax.set_yticks([-2.0,-1.5,-1,-0.5,0,0.5,1,1.5])
    #ax.set_zticks([0,2.5,5,7.5,10,12.5,15,17.5,20])
    
    # 用于控制坐标旋转,俯视角，旋转角
    ax.view_init(35,45)
    
    ax.grid(True)
    ax.contourf(X,Y,Z,6,cmap=mycn[0],norm = mycn[1],zdir='z', offset=-20)  #生成等值线图

    ax.plot_surface(X, Y, Z
                                    , rstride=1
                                    , cstride=1
                                    , cmap=mycn[0]
                                    ,linewidth=0
                                    , antialiased=False
                                    ,zorder=0
                                    ,alpha=1
                                    ,norm = mycn[1])

    plt.savefig("ByGdd-Linear-2_3D.tiff")
    plt.savefig("ByGdd-Linear-2_3D.jpg")
 

def main():
    fp = sys.argv[1]
    sign = eval(sys.argv[2])
    XYZ = ReadXYZ(fp)
    print("start to reShapeXYZ")
    my = reShapeXYZ(XYZ)
    mycn = MyColorNorm()
    if sign:
        #draw(InterNUM2(XYZ,n = sign))
        #After_Inter_xyz1 = Finternum1(InterNUM1(my,n = sign))
        After_Inter_xyz2 = Finternum2(InterNUM1(my,n = sign))

        draw2(After_Inter_xyz2,mycn)
        #draw3(After_Inter_xyz2,mycn)
        #draw23(After_Inter_xyz1,mycn)
    else:
        pass
        #draw2(my,mycn)
        #draw3(my,mycn)
        #draw23(my,mycn)


if __name__ == "__main__":
    main()
