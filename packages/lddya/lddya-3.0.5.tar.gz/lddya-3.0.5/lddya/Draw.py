import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np

class ShanGeTu():
    def __init__(self,map_data) -> None:
        self.map_size = len(map_data)
        self.fig = plt.figure(figsize=(7,7))
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.set_xbound(0,len(map_data))
        self.ax1.set_ybound(0,len(map_data))
        rect_pat = []
        for ki,i in enumerate(map_data):
            for kj,j in enumerate(i):
                if j == 1:
                    rect_pat.append(pat.Rectangle((kj,ki),1,1,color = 'k'))
                else:
                    rect_pat.append(pat.Rectangle((kj,ki),1,1,fill = False,edgecolor = 'k',linewidth = 1))
        for i in rect_pat:
            self.ax1.add_patch(i)
        x = np.array([i for i in range(len(map_data))])
        self.ax1.set_xticks(x+0.5,x+1)
        self.ax1.set_yticks(x+0.5,x+1)

    def draw_way(self,way_data,style = None):
        '''
        绘制一条路线，way_data为路径经过的节点坐标。坐标格式为[y,x],这是为了对接现有的算法标准，style同plt.plot中的style
        '''
        way_data = np.array(way_data)
        if style == None:
            self.ax1.plot(way_data[:,1]+0.5,way_data[:,0]+0.5)
        else:
            self.ax1.plot(way_data[:,1]+0.5,way_data[:,0]+0.5,style)

    
    def show(self):
        plt.show()
    
    def save(self,filename = 'figure.jpg'):
        plt.savefig(filename)
    

class IterationGraph():
    def __init__(self,data_list,style_list,legend_list,xlabel='x',ylabel='y') -> None:
        self.fig,self.ax = plt.subplots()
        for i in range(len(data_list)):
            if style_list[i][0] != '#':
                self.ax.plot(range(len(data_list[i])),data_list[i],style_list[i])
            else:
                self.ax.plot(range(len(data_list[i])),data_list[i],color=style_list[i][:7], marker=style_list[i][7] if len(style_list[i])>7 else ',', linestyle=style_list[i][8:]if len(style_list[i])>8 else '-')
        if type(legend_list) == list:
            self.ax.legend(legend_list)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def show(self):
        plt.show()
    def save(self,figname = 'figure.jpg'):
        self.fig.savefig(figname)