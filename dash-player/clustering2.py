import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster import hierarchy
import plotly.figure_factory as ff

import scipy.cluster.hierarchy as sch

# def get_dendogram():
#     overall_similarities = [['video1tovideo2','1','2', 0.5],
#             ['video1tovideo3','1','3', 0.85],
#             ['video1tovideo4','1','4', 0.9],
#             ['video1tovideo5','1','5', 0.3],
#             ['video1tovideo6','1','6', 0.45],
#             ['video2tovideo3','2','3', 0.45],
#             ['video2tovideo4','2','4', 0.3],
#             ['video2tovideo5','2','5', 0.8],
#             ['video2tovideo6','2','6', 0.9],
#             ['video3tovideo4','3','4', 0.87],
#             ['video3tovideo5','3','5', 0.33],
#             ['video3tovideo6','3','6', 0.20],
#             ['video4tovideo5','4','5', 0.1],
#             ['video4tovideo6','4','6', 0.36],
#             ['video5tovideo6','5','6', 0.9]]
#
#     df = pd.DataFrame(overall_similarities,
#                   columns=['Name','Video1','Video2', 'Similarity'])
#     data=df.values
#     labels=list(df.iloc[:,0].values)
#     data = df.iloc[:, 1:].values
#
#     fig = ff.create_dendrogram(data, orientation='left', labels=labels)
#     fig.update_layout(width=1100, height=800,title="Dance Poses Clustering")
#     # fig.show()
#     return fig

# plt.figure(figsize=(10, 7))
# plt.title("Dance Poses Clustering")
# Z = hierarchy.linkage(data, method='average')
# dendrogram = hierarchy.dendrogram(Z,labels=labels,orientation='right')
#
# from scipy.cluster.hierarchy import fcluster
# k=2
# fcluster(Z, k, criterion='maxclust')
# get_dendogram()

def get_dendogram():
    l=[1,2,3,4,5,6]

    M = [[0.00, 0.85, 0.3, 0.2, 0.95, 0.75],
         [0.85, 0.00, 0.65, 0.76, 0.24, 0.22],
         [0.3, 0.65, 0.00, 0.17, 0.73, 0.62],
         [0.2, 0.76, 0.17, 0.00, 0.91, 0.63],
         [0.95, 0.24, 0.73, 0.91, 0.00, 0.1],
         [0.75, 0.22, 0.62, 0.63, 0.1, 0.00]]
    Mnp = np.array(M)
    y = Mnp[np.triu_indices(6,1)]

    # the condensed matrix can then be fed into linkage
    Z = hierarchy.linkage(y, 'average')

    fig = ff.create_dendrogram(Mnp,linkagefun=lambda x: sch.linkage(x, "average"),labels=l)
    fig.update_layout(width=1100, height=800,title="Dance Poses Clustering")
    return fig
