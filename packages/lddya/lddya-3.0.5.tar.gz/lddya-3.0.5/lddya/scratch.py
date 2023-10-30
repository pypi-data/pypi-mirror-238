from lddya.Algorithm import ACO
from lddya.Draw import ShanGeTu,IterationGraph
from lddya.Map import Map

map = Map()    
map.load_map_file('map.txt')
aco = ACO(map_data=map.data,start=[0,0],end=[19,19])
aco.run()
sfig = ShanGeTu(map_data= map.data)
sfig.draw_way(aco.way_data_best)
sfig.save()
dfig = IterationGraph([aco.generation_aver,aco.generation_best],
                    style_list=['--r','-.g'],
                    legend_list=['每代平均','每代最优'],
                    xlabel='迭代次数',
                    ylabel= '路径长度'
                    )
dfig.save()



