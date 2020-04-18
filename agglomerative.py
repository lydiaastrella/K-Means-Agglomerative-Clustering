import pandas
import math

# RUN function ini aja, affinity = "single" ato "complete", iteration jumlah mau sampe kapan clusterinnya

def Clustering(df, affinity, jml_cluster):
    jml_cluster = len(df) - jml_cluster

    if (affinity == "single"):
        return SingleLinkage(df, InitializeCluster(df), jml_cluster)
    elif (affinity == "complete"):
        return CompleteLinkage(df, InitializeCluster(df), jml_cluster)
    elif(affinity == "average"):
        return AverageLinkage(df, InitializeCluster(df), jml_cluster)
    elif(affinity == "average group"):
        return AverageGroup(df, InitializeCluster(df), jml_cluster)

# Di bawah ini ga dipanggil, tapi kalo mau dibaca boleh

def SingleLinkage(df, clusters, jml_cluster):
    if (jml_cluster == 0):
        return clusters
    else:
        new_clusters = MergeNodes(clusters, GetMinDistance(df, clusters, "single"))
        # print(new_clusters)
        # print("++++++++++++++++")
        return(CompleteLinkage(df, new_clusters, jml_cluster-1))

def CompleteLinkage(df, clusters, jml_cluster):
    if (jml_cluster == 0):
        return clusters
    else:
        new_clusters = MergeNodes(clusters, GetMinDistance(df, clusters, "complete"))
        return(SingleLinkage(df, new_clusters, jml_cluster-1))

def AverageLinkage(df, clusters, jml_cluster):
    #print("jumlah cluster yg hrs dimerge" , jml_cluster)
    if (jml_cluster == 0):
        return clusters
    else:
        new_clusters = MergeNodes(clusters, GetMinDistance(df, clusters, "average"))
        return(AverageLinkage(df, new_clusters, jml_cluster-1))

def AverageGroup(df, clusters, jml_cluster):
    #print("jumlah cluster yg hrs dimerge" , jml_cluster)
    if (jml_cluster == 0):
        return clusters
    else:
        new_clusters = MergeNodes(clusters, GetMinDistance(df, clusters, "average group"))
        return(AverageGroup(df, new_clusters, jml_cluster-1))

def CountJarak(arr1, arr2):
    jarak = 0
    
    for idx in range (len(arr1)):
        jarak = jarak + abs(arr1[idx] - arr2[idx])

    return jarak

def GetMinDistance(df, clusters, affinity):
    min_distance = 9999
    min_distance_idx = [-1,-1]

    for i in range (len(clusters)):
        for j in range (i, len(clusters)):
            if (i == j):
                pass
            else:
                if (affinity == "single"):
                    temp_min_distance = GetMinClusterDistance(df, clusters, i, j)
                elif (affinity == "complete"):
                    temp_min_distance = GetMaxClusterDistance(df, clusters, i, j)
                elif (affinity == "average"):
                    temp_min_distance = GetAvgAllPairDistance(df, clusters, i, j)
                elif (affinity == "average group"):
                    temp_min_distance = GetClusterMeanDistance(df, clusters, i, j)
                if (temp_min_distance < min_distance):
                    min_distance = temp_min_distance
                    min_distance_idx = [i,j]
    
    # print(min_distance, ":", min_distance_idx)
    return min_distance_idx

def GetMinClusterDistance(df, clusters, i, j):
    temp_min_distance = 9999
    for k in (clusters[i]):
        for l in (clusters[j]):
            curr_distance = CountJarak(GetAttributes(df, k), GetAttributes(df, l))
            if (curr_distance < temp_min_distance):
                temp_min_distance = curr_distance
            # print(">", "[", i, ",", j, "] =>", GetAttributes(df, k), "-", GetAttributes(df, l), "=", curr_distance)
    # print(">>", temp_min_distance)
    return temp_min_distance

def GetMaxClusterDistance(df, clusters, i, j):
    temp_max_distance = -9999
    for k in (clusters[i]):
        for l in (clusters[j]):
            curr_distance = CountJarak(GetAttributes(df, k), GetAttributes(df, l))
            if (curr_distance > temp_max_distance):
                temp_max_distance = curr_distance
    return temp_max_distance

def GetAvgAllPairDistance(df, clusters, i, j):
    count_pair = 0
    sum_pair = 0
    for k in (clusters[i]):
        for l in (clusters[j]):
            sum_pair += CountJarak(GetAttributes(df, k), GetAttributes(df, l))
            count_pair += 1
    return sum_pair / count_pair

def GetClusterMeanDistance(df, clusters, i, j):
    count = 0
    sum = []
    mean_cluster_1 =[]
    mean_cluster_2 =[]
    #print("masuk")
    for k in range (len(df.columns)-1):
        sum.append(0)
    for k in (clusters[i]):
        attributes_k = GetAttributes(df, k)
        for l in range (len(sum)):
            sum[l] += attributes_k[l]
        count += 1
    for k in range (len(sum)):
        mean_cluster_1.append(sum[k] / count)
    count = 0
    for k in range (len(df.columns)-1):
        sum[k] = 0
    for k in (clusters[j]):
        attributes_k = GetAttributes(df, k)
        for l in range (len(sum)):
            sum[l] += attributes_k[l]
        count += 1
    for k in range (len(sum)):
        mean_cluster_2.append(sum[k] / count)
    return CountJarak(mean_cluster_1, mean_cluster_2)

def InitializeCluster(df):
    arr = []
    for idx in range (len(df)):
        arr.append([idx])
    return arr

def GetAttributes(df, idx):
    atr1 = df.loc[idx]['sepal length (cm)']
    atr2 = df.loc[idx]['sepal width (cm)']
    atr3 = df.loc[idx]['petal length (cm)']
    atr4 = df.loc[idx]['petal width (cm)']

    hasil = [atr1, atr2, atr3, atr4]
    
    return hasil

def MergeNodes(clusters, nodes):
    for i in range (len(clusters[nodes[1]])):
        clusters[nodes[0]].append(clusters[nodes[1]][i])
    del clusters[nodes[1]]

    return clusters

def Convert(result_cluster, jml_data):
    list_cluster_num = [None] * jml_data
    cluster_num = 1
    for i in result_cluster:
        for j in i:
            list_cluster_num[j] = cluster_num
        cluster_num += 1
    return list_cluster_num

# TESTING
# df = pandas.read_csv('iris.csv')
# separator_iris = round((8/10)*len(df.index))
# test_iris = df.iloc[separator_iris:, :].reset_index(drop = True)

# affinity = input("affinity       : ")
# jml_cluster =  int(input("jumlah cluster : "))
# result_cluster = Clustering(test_iris, affinity, jml_cluster)
# list_cluster_num = Convert(result_cluster,len(test_iris.index))
# print(list_cluster_num)