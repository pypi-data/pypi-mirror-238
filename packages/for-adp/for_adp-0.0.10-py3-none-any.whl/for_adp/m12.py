def m12():
    """
    12  Clustering
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    #import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from sklearn.preprocessing import StandardScaler

    군집분석은 데이터 전처리 과정의 일부로 나오는 경우 혹은 군집분석 단독으로 나오는 경우 두 가지가 있음
    군집분석 순서를 이해하고 적용하는 것이 필요함
    데이터가 클 경우 패키지별로 시간이 오래걸리는 경우가 있으므로 주의 필요
    데이터가 클 경우 대안 알고리즘 이용
    12.1 Data preprocessing
    12.1.1 표준화
    군집분석을 진행하기 전에 표준화를 진행해줍니다. 표준화를 진행해주는 이유는 군집 알고리즘 특성상 변수의 스케일에 민감하기 때문입니다. 변수 스케일의 영향으로 거리 기준이 왜곡되는 것을 막기 위해서 표준화를 진행해줍니다.

    df = pd.read_csv('./data/clustering/USArrests.csv')
    df.head()

       Murder  Assault  UrbanPop  Rape
    0    13.2      236        58  21.2
    1    10.0      263        48  44.5
    2     8.1      294        80  31.0
    3     8.8      190        50  19.5
    4     9.0      276        91  40.6
    numeric_data = df.select_dtypes('number')
    stdscaler = StandardScaler()
    df = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)
    df.head(2)

         Murder   Assault  UrbanPop      Rape
    0  1.255179  0.790787 -0.526195 -0.003451
    1  0.513019  1.118060 -1.224067  2.509424
    12.1.2 이상치 제거
    대부분 군집 알고리즘은 이상치에 민감합니다. 따라서 이상치 탐지 방법을 통해 이상치 확인 후 제거해도 무방할 경우 이상치를 제거하고 진행하는 것이 바람직합니다(데이터 전처리 파트 참고). 이상치를 제거할 수 없는 경우 이상치에 비교적 강건한 대안 알고리즘을 선택합니다.

    12.2 k means
    Note
    개 중심점을 사전에 선택
    관측치에 
     군집 번호를 임의로 할당
    각 군집별로 중심점(평균)을 계산
    각 관측치를 군집의 중심점에 가까운 군집에 할당
    군집 내 중심점(평균) 업데이트
    3-5번 과정을 변화가 없을 때까지 반복(혹은 사전에 지정한 최대 반복 횟수까지 반복)


    데이터가 주어졌을 때, step 1을 보면 사전에 지정한 
    에 대해 각 관측치별로 임의의 군집이 할당된 것을 볼 수 있습니다. step 2a에서는 임의로 할당된 각 군집에 대해 중심점(평균)을 계산합니다. step 2b에서는 군집별 중심점과 각 관측치 사이에 거리(유클리디안 거리)를 계산하여, 각 관측치를 가까운 군집에 할당합니다. step 2a에서는 다시 군집의 중심점을 계산하고, final result에서는 군집별 중심점과 각 관측치 사이에 거리(유클리디안 거리)를 계산하여, 각 관측치를 가까운 군집에 할당합니다. 변화가 없을 때까지 혹은 사전에 지정한 최대 반복 횟수만큼 업데이트를 진행합니다.

    장점

    구현이 비교적 간단하고, 계산 속도가 빠름

    알고리즘 특성상 수렴 보장

    단점

    사전에 
     값을 지정해줘야 함

    초기 중심점을 무작위로 선택함에 따라 성능의 변동이 있을 수 있음

    이상치에 민감

    복잡한 기하학적 특성이 있는 경우 성능이 떨어짐

    밀도가 다양한 데이터의 경우 성능이 떨어짐

    kmeans clustering을 진행하기 위해서 USArrests 데이터를 불러오겠습니다. kmeans clustering을 수행하기 전에 데이터 표준화를 먼저 진행해주겠습니다.

    k-means clustering을 진행하기 전에 적절한 
     를 지정하는 방법에 대해 알아보겠습니다. k-means clustering 알고리즘을 보면 사전에 
     값을 지정해주었습니다. 도메인 지식에 따라 임의로 
     를 지정해줄 수도 있지만, 도메인 지식이 없을 경우 적절한 
     값을 구하는 기준이 필요합니다. 적절한 
     를 구하는 방법은 다음과 같습니다.

    Note
    Average sillouette method
    ellbow method
    Gap statistic method
    Gap statistic은 공식 지원 패키지 목록에 없으므로, 답안 작성시 참고 개념으로 활용

    12.2.1 optimal cluster k
    Average silhouette method
    Average silhouette method는 각 
    별 평균 silhouette coefficient를 계산하고, 평균 silhouette coefficient값이 가장 큰 
    를 선택하는 방법입니다. 평균 silhouette coefficient는 각 
    별 개별 관측치의 silhouette coefficient를 평균낸 값입니다. 개별 관측치의 silhouette coefficient는 seperation, compactness를 동시에 고려하여 정의됩니다.

    추가 설명 링크 : https://dondonkim.netlify.app/posts/2022-10-08-sillouette/silhouette.html

    기준

    가장 큰 average silhouette coefficient 선택
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    scores = []

    for i in range(2,10):
        fit_kmeans = KMeans(n_clusters=i, init='random', n_init = 10, random_state=0).fit(df)
        score = silhouette_score(df, fit_kmeans.labels_)
        scores.append(score)
        print("For n_clusters={0}, the silhouette score is {1}".format(i, score))

    For n_clusters=2, the silhouette score is 0.4084890326217641
    For n_clusters=3, the silhouette score is 0.3081362264894561
    For n_clusters=4, the silhouette score is 0.34410807182093506
    For n_clusters=5, the silhouette score is 0.32271671265620105
    For n_clusters=6, the silhouette score is 0.28470556238973493
    For n_clusters=7, the silhouette score is 0.26160590685186647
    For n_clusters=8, the silhouette score is 0.2501550401248423
    For n_clusters=9, the silhouette score is 0.23754742149920813
    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    Elbow method
    Elbow method는 각 
    별 wss(total within-cluster sum of square)를 계산하고, elbow point를 찾는 방법입니다.

    wss가 작을수록 좋음
    단순히 wss로만 계산되므로, 
     값에 따라 wss는 감소하는 특성이 있습니다. 따라서 elbow point가 없을 경우 적절한 
    값을 찾는 것이 모호할 수 있습니다. 이 경우 Average silhouette method과 비교하여 적절한 
    값을 선택하면 됩니다.

    wss = []

    for i in range(2, 10):
        fit_kmeans = KMeans(n_clusters=i, init='random', n_init=5, random_state=109).fit(df)
        wss.append(fit_kmeans.inertia_)


    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), wss, 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method showing the optimal $k$')
    plt.show()



    12.2.2 Compute k-means
    kmeans = KMeans(n_clusters = 4)
    kmeans.fit(df)

    KMeans(n_clusters=4)
    label = kmeans.labels_
    #df['cluster'] = label
    df.head()

         Murder   Assault  UrbanPop      Rape
    0  1.255179  0.790787 -0.526195 -0.003451
    1  0.513019  1.118060 -1.224067  2.509424
    2  0.072361  1.493817  1.009122  1.053466
    3  0.234708  0.233212 -1.084492 -0.186794
    4  0.281093  1.275635  1.776781  2.088814
    Visualization

    from sklearn.decomposition import PCA
    pca = PCA(2)
    #Transform the data
    pca_df = pca.fit_transform(df)

    unique_labels = np.unique(kmeans.labels_)
    centroids = kmeans.cluster_centers_

    for i in unique_labels:
        plt.scatter(pca_df[label == i , 0] , pca_df[label == i , 1] , label = i)
    plt.legend()
    plt.show()



    세부적으로 KMeans 결과를 알아보겠습니다. k-means 함수 안에는 compactness와 seperation 관점에서의 지표가 정의되어 있습니다. 각 지표가 무엇을 의미하는지 알아보겠습니다. 먼저 compactness 관점에서의 지표인 total-within-cluster variation을 보겠습니다. 먼저 within-cluster variation은 아래와 같이 정의됩니다.


    군집번호
    에속하는관찰값
    에속하는관찰값들의평균


    즉, within-cluster variation은 각 
    별로 군집 내에 밀집도(잘 뭉쳐있는지)를 의미합니다. 이제 within-cluster variation을 더하면 total-within-cluster variation가 정의됩니다.




    군집번호
    에속하는관찰값
    에속하는관찰값들의평균




    그림을 보면 오른쪽으로 갈수록, 군집 내 변동이 작은 것을 알 수 있고, 이는 total-within-cluster variation이 가장 작다는 것을 의미하고, compactness 관점에서 좋은 군집을 의미합니다.

    total-within-cluster variation는 .inertia_를 통해 구할 수 있습니다.

    kmeans.inertia_

    57.55425863091106
    시험에서는 근거 제시만 하면 되기 때문에 적절한 지표를 선택하고, 해당 지표를 기준으로 적절한 
    값을 구해주면 됩니다(wss plot 참고).

    Note
    PAM, CLARA는 scikit-learn-extra 패키지에서 지원하며, 해당 패키지는 공식 지원 패키지 리스트에 없습니다. scikit-learn-extra 패키지를 사용하기 위해서는 scikit-learn > 0.24 로 업데이트해야 합니다.

    참고 : https://scikit-learn-extra.readthedocs.io/en/stable/install.html#dependencies

    12.2.3 pipeline 활용 참고
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline

    df = pd.read_csv('./data/clustering/USArrests.csv')
    df.head()

       Murder  Assault  UrbanPop  Rape
    0    13.2      236        58  21.2
    1    10.0      263        48  44.5
    2     8.1      294        80  31.0
    3     8.8      190        50  19.5
    4     9.0      276        91  40.6
    numeric_data = df.select_dtypes('number')
    stdscaler = StandardScaler()
    df = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)
    df.head(2)

         Murder   Assault  UrbanPop      Rape
    0  1.255179  0.790787 -0.526195 -0.003451
    1  0.513019  1.118060 -1.224067  2.509424
    num_columns = df.select_dtypes('number').columns.tolist()

    num_preprocess = make_pipeline(
        StandardScaler()
    )

    preprocess = ColumnTransformer(
        [("num", num_preprocess, num_columns)], 
        #remainder='passthrough'
    )

    k_range = range(2, 10)
    sse = []
    for i in k_range:
        Kmeans = KMeans(n_clusters=i, random_state=0)
        pipe = make_pipeline(preprocess, Kmeans)
        pipe.fit_predict(df)
        sse.append(pipe[1].inertia_)

    array([1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1,
           0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0,
           0, 0, 0, 0, 0, 0], dtype=int32)
    array([1, 1, 1, 2, 1, 1, 0, 0, 1, 1, 0, 2, 1, 0, 2, 0, 2, 1, 2, 1, 0, 1,
           2, 1, 1, 2, 2, 1, 2, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0,
           2, 0, 0, 2, 2, 0], dtype=int32)
    array([0, 1, 1, 0, 1, 1, 2, 2, 1, 0, 2, 3, 1, 2, 3, 2, 3, 0, 3, 1, 2, 1,
           3, 0, 1, 3, 3, 1, 3, 2, 1, 1, 0, 3, 2, 2, 2, 2, 2, 0, 3, 0, 1, 2,
           3, 2, 2, 3, 3, 2], dtype=int32)
    array([3, 1, 1, 2, 1, 1, 0, 0, 1, 3, 0, 4, 1, 2, 4, 2, 2, 3, 4, 1, 0, 1,
           4, 3, 1, 2, 2, 1, 4, 0, 1, 1, 3, 4, 0, 2, 0, 0, 0, 3, 4, 3, 1, 0,
           4, 2, 0, 4, 4, 2], dtype=int32)
    array([5, 4, 1, 0, 1, 1, 2, 0, 1, 5, 2, 3, 1, 0, 3, 0, 0, 5, 3, 1, 2, 1,
           3, 5, 0, 3, 3, 1, 3, 2, 1, 1, 5, 3, 2, 0, 0, 2, 2, 5, 3, 5, 1, 2,
           3, 0, 2, 3, 3, 0], dtype=int32)
    array([5, 4, 1, 0, 1, 1, 2, 0, 1, 5, 2, 3, 1, 0, 3, 0, 0, 5, 3, 1, 2, 1,
           3, 5, 0, 0, 3, 1, 3, 2, 1, 1, 5, 6, 2, 0, 0, 2, 2, 5, 6, 5, 1, 2,
           6, 0, 2, 6, 3, 0], dtype=int32)
    array([4, 7, 0, 3, 6, 6, 2, 3, 0, 4, 2, 1, 0, 3, 1, 3, 3, 4, 5, 0, 2, 0,
           1, 4, 3, 1, 1, 6, 1, 2, 0, 0, 4, 5, 3, 3, 3, 2, 2, 4, 5, 4, 0, 2,
           5, 3, 2, 5, 1, 3], dtype=int32)
    array([0, 8, 5, 4, 2, 2, 7, 4, 5, 0, 7, 1, 5, 4, 1, 4, 4, 0, 3, 5, 7, 5,
           1, 6, 4, 1, 1, 2, 1, 7, 5, 5, 6, 3, 4, 4, 4, 4, 7, 6, 3, 0, 5, 7,
           3, 4, 4, 3, 1, 4], dtype=int32)
    sse

    [104.96163315756873, 80.08569526137278, 57.55425863091107, 50.33327385184908, 44.200843606869185, 39.68379510054723, 34.69690734673087, 30.87662061527529]
    plt.plot(k_range, sse)
    #plt.plot(range(1,10), sse, linewidth=4, markersize=12,marker='o')
    plt.xlabel('Number of K')
    plt.ylabel('SSE')
    plt.show()



    from sklearn import set_config
    set_config(display='diagram')

    Kmeans = KMeans(n_clusters=4, random_state = 0)
    pipe = make_pipeline(preprocess, Kmeans)
    pipe

    Pipeline
    columntransformer: ColumnTransformer
    num

    StandardScaler

    KMeans
    12.3 hierarchical clustering
    Note
    개의 관측치와 
    개의 모든 쌍별 비유사성 측도를 가지고 시작. 각 관측치 자체를 군집으로 취급

     에 대해

    개 군집들 사이에서 모든 쌍별 군집 간 비유사성을 조사하여 비유사성이 가장 낮은 군집들의 쌍을 식별

    남아있는 
    개의 군집들 사이에서 새로운 쌍별 군집 간 비유사성 거리 계산



    정해야하는 것

    어떤 비유사성 측도를 사용해야 하는가?
    Euclidian distance

    Manhattan distance

    pearson correlation distance : 유전 데이터 분석에 주로 사용됨

    spearman correlation distance : 기하학에서 주로 사용

    기타 등등

    데이터의 특성에 따라 거리 측도 선택 기준은 달라집니다. 시험에서는 다양한 경우의 수가 있으므로, 유클리디안 거리로 통일하는 것을 추천드립니다.

    어떤 연결 측도를 사용해야 하는가?
    연결 측도

    완전연결(complete) : 군집 A와 군집 B 내의 관측치 사이에 모든 쌍별 비유사성(ex. 유클리디안 거리)을 계산하여 비유사성이 가장 큰 것을 기록


    단일연결(single) : 군집 A와 군집 B 내의 관측치 사이에 모든 쌍별 비유사성(ex. 유클리디안 거리)을 계산하여 비유사성이 가장 작은 것을 기록


    평균연결(average) : 군집 A와 군집 B 내의 관측치 사이에 모든 쌍별 비유사성(ex. 유클리디안 거리)을 계산하여 비유사성의 평균을 기록


    무게중심연결(centroid) : 군집 A의 무게중심과 군집 B의 무게중심 사이의 비유사성을 계산


    ward 연결 : 군집 A와 군집 B의 각 무게중심과 관측치 사이의 SSE(sum of squared error)를 계산 후, 군집 A와 군집 B를 병합한 후의 전체 군집에서 무게중심과 관측치 사이의 SSE를 계산하고, 병합 전과 병합 후 SSE의 차이를 계산


    정답 없음

    평균, 완전 연결의 경우 다른 연결법에 비해서 비교적 균형잡힌 덴드로그램을 형성하는 경향이 있음



    연결방법별 덴드로그램 차이
    어디에서 덴드로그램을 절단해야하는가?
    임의로 잘라도 되고, k-means처럼 “silhouette”, “wss” 이용
    임의로 자를 경우 해석에 유의


    덴드로그램을 수평으로 보면 2와 9는 유사하지만 실제로는 먼 것을 볼 수 있음

    수직축의 높이를 기준으로 해석

    수직으로 보면 9와 2,8,5,7이 같은 높이에서 함께 묶인 것을 볼 수 있음

    장점

    사전에 군집 수를 지정하지 않아도 됨(덴드로그램으로 주관적으로 결정)
    단점

    작은 군집은 잘 식별하지만 상대적으로 큰 군집은 잘 식별하지 못함
    optimal cluster k

    from sklearn.cluster import AgglomerativeClustering

    scores = []

    for i in range(2,10):
        fit_hk = AgglomerativeClustering(n_clusters=i, linkage = 'ward').fit(df)
        score = silhouette_score(df, fit_hk.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    hk = AgglomerativeClustering(n_clusters = 4, linkage = 'ward')
    hk.fit(df)


    AgglomerativeClustering
    AgglomerativeClustering(n_clusters=4)
    label = hk.labels_

    df2 = df.copy()
    df2['cluster'] = label
    df2.head()

         Murder   Assault  UrbanPop      Rape  cluster
    0  1.255179  0.790787 -0.526195 -0.003451        3
    1  0.513019  1.118060 -1.224067  2.509424        1
    2  0.072361  1.493817  1.009122  1.053466        1
    3  0.234708  0.233212 -1.084492 -0.186794        0
    4  0.281093  1.275635  1.776781  2.088814        1
    from scipy.cluster.hierarchy import dendrogram, linkage

    Z = linkage(df, method="ward")
    fig = plt.figure(figsize=(10, 6))
    dendrogram(Z)

    {'icoord': [[5.0, 5.0, 15.0, 15.0], [25.0, 25.0, 35.0, 35.0], [10.0, 10.0, 30.0, 30.0], [55.0, 55.0, 65.0, 65.0], [45.0, 45.0, 60.0, 60.0], [20.0, 20.0, 52.5, 52.5], [85.0, 85.0, 95.0, 95.0], [75.0, 75.0, 90.0, 90.0], [135.0, 135.0, 145.0, 145.0], [125.0, 125.0, 140.0, 140.0], [115.0, 115.0, 132.5, 132.5], [105.0, 105.0, 123.75, 123.75], [82.5, 82.5, 114.375, 114.375], [175.0, 175.0, 185.0, 185.0], [165.0, 165.0, 180.0, 180.0], [155.0, 155.0, 172.5, 172.5], [98.4375, 98.4375, 163.75, 163.75], [36.25, 36.25, 131.09375, 131.09375], [195.0, 195.0, 205.0, 205.0], [215.0, 215.0, 225.0, 225.0], [200.0, 200.0, 220.0, 220.0], [245.0, 245.0, 255.0, 255.0], [235.0, 235.0, 250.0, 250.0], [265.0, 265.0, 275.0, 275.0], [295.0, 295.0, 305.0, 305.0], [285.0, 285.0, 300.0, 300.0], [270.0, 270.0, 292.5, 292.5], [242.5, 242.5, 281.25, 281.25], [210.0, 210.0, 261.875, 261.875], [315.0, 315.0, 325.0, 325.0], [335.0, 335.0, 345.0, 345.0], [320.0, 320.0, 340.0, 340.0], [365.0, 365.0, 375.0, 375.0], [385.0, 385.0, 395.0, 395.0], [370.0, 370.0, 390.0, 390.0], [355.0, 355.0, 380.0, 380.0], [415.0, 415.0, 425.0, 425.0], [405.0, 405.0, 420.0, 420.0], [445.0, 445.0, 455.0, 455.0], [435.0, 435.0, 450.0, 450.0], [465.0, 465.0, 475.0, 475.0], [442.5, 442.5, 470.0, 470.0], [485.0, 485.0, 495.0, 495.0], [456.25, 456.25, 490.0, 490.0], [412.5, 412.5, 473.125, 473.125], [367.5, 367.5, 442.8125, 442.8125], [330.0, 330.0, 405.15625, 405.15625], [235.9375, 235.9375, 367.578125, 367.578125], [83.671875, 83.671875, 301.7578125, 301.7578125]], 'dcoord': [[0.0, 0.7800624726117171, 0.7800624726117171, 0.0], [0.0, 1.0225018692038894, 1.0225018692038894, 0.0], [0.7800624726117171, 1.1021694044411907, 1.1021694044411907, 1.0225018692038894], [0.0, 0.7945530103578827, 0.7945530103578827, 0.0], [0.0, 1.2197191288489164, 1.2197191288489164, 0.7945530103578827], [1.1021694044411907, 2.7421139544450304, 2.7421139544450304, 1.2197191288489164], [0.0, 0.3537743681310408, 0.3537743681310408, 0.0], [0.0, 0.952332839989021, 0.952332839989021, 0.3537743681310408], [0.0, 0.5408248189680332, 0.5408248189680332, 0.0], [0.0, 0.9610307025238368, 0.9610307025238368, 0.5408248189680332], [0.0, 1.3122402649731468, 1.3122402649731468, 0.9610307025238368], [0.0, 1.7079251328916916, 1.7079251328916916, 1.3122402649731468], [0.952332839989021, 2.2649420381778995, 2.2649420381778995, 1.7079251328916916], [0.0, 1.2089769072372043, 1.2089769072372043, 0.0], [0.0, 1.404214498699647, 1.404214498699647, 1.2089769072372043], [0.0, 3.055735303919404, 3.055735303919404, 1.404214498699647], [2.2649420381778995, 3.531541898650026, 3.531541898650026, 3.055735303919404], [2.7421139544450304, 6.527470828535695, 6.527470828535695, 3.531541898650026], [0.0, 0.7180984285039761, 0.7180984285039761, 0.0], [0.0, 0.9924604112760993, 0.9924604112760993, 0.0], [0.7180984285039761, 1.3303363086847781, 1.3303363086847781, 0.9924604112760993], [0.0, 0.7464962542035871, 0.7464962542035871, 0.0], [0.0, 0.815842993431543, 0.815842993431543, 0.7464962542035871], [0.0, 0.4990993894073977, 0.4990993894073977, 0.0], [0.0, 0.2079437976133826, 0.2079437976133826, 0.0], [0.0, 0.6625852157172658, 0.6625852157172658, 0.2079437976133826], [0.4990993894073977, 1.3585660787207545, 1.3585660787207545, 0.6625852157172658], [0.815842993431543, 1.7661673389439376, 1.7661673389439376, 1.3585660787207545], [1.3303363086847781, 3.023678727416965, 3.023678727416965, 1.7661673389439376], [0.0, 0.7109765828248565, 0.7109765828248565, 0.0], [0.0, 1.0705701702968808, 1.0705701702968808, 0.0], [0.7109765828248565, 1.1724104281482475, 1.1724104281482475, 1.0705701702968808], [0.0, 0.8058634904273213, 0.8058634904273213, 0.0], [0.0, 1.0865316609298954, 1.0865316609298954, 0.0], [0.8058634904273213, 1.55526892227882, 1.55526892227882, 1.0865316609298954], [0.0, 1.8302005688424474, 1.8302005688424474, 1.55526892227882], [0.0, 0.59956022650398, 0.59956022650398, 0.0], [0.0, 1.2729224911920178, 1.2729224911920178, 0.59956022650398], [0.0, 0.43312429085085896, 0.43312429085085896, 0.0], [0.0, 0.5591483670409593, 0.5591483670409593, 0.43312429085085896], [0.0, 0.7860298248284557, 0.7860298248284557, 0.0], [0.5591483670409593, 0.8558054806051812, 0.8558054806051812, 0.7860298248284557], [0.0, 1.0818450636699195, 1.0818450636699195, 0.0], [0.8558054806051812, 1.95573383070349, 1.95573383070349, 1.0818450636699195], [1.2729224911920178, 2.225708599114937, 2.225708599114937, 1.95573383070349], [1.8302005688424474, 3.2433103740861906, 3.2433103740861906, 2.225708599114937], [1.1724104281482475, 3.772026252105819, 3.772026252105819, 3.2433103740861906], [3.023678727416965, 7.261167758993684, 7.261167758993684, 3.772026252105819], [6.527470828535695, 13.653466603337856, 13.653466603337856, 7.261167758993684]], 'ivl': ['0', '17', '9', '41', '32', '23', '39', '42', '12', '31', '8', '2', '21', '19', '30', '1', '5', '4', '27', '40', '47', '33', '44', '11', '25', '26', '22', '48', '18', '14', '28', '45', '49', '3', '16', '7', '20', '29', '6', '38', '24', '36', '46', '35', '13', '15', '34', '37', '10', '43'], 'leaves': [0, 17, 9, 41, 32, 23, 39, 42, 12, 31, 8, 2, 21, 19, 30, 1, 5, 4, 27, 40, 47, 33, 44, 11, 25, 26, 22, 48, 18, 14, 28, 45, 49, 3, 16, 7, 20, 29, 6, 38, 24, 36, 46, 35, 13, 15, 34, 37, 10, 43], 'color_list': ['C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C0'], 'leaves_color_list': ['C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2']}
    plt.show()



    12.4 PAM
    k-means는 중심점을 결정할 때 평균을 이용하므로 이상치에 민감한 문제가 있습니다. 이 문제를 해결하기 위해서 PAM에서는 중심점을 결정할 때, 평균 대신 중앙값을 이용합니다. 알고리즘의 순서는 k-means와 거의 동일합니다.

    Note
    관측치 중 
    개 중심점을 랜덤하게 선택
    각 관측치를 군집의 중심점(중앙값)에 가까운 군집에 할당
    군집 내 중심점(중앙값) 업데이트
    2-3번 과정을 변화가 없을 때까지 반복(혹은 사전에 지정한 최대 반복 횟수까지 반복)


    간단하게 다시 그림을 보면 데이터가 주어졌을 때, 
    에 대해 각 관측치에서 임의로 중심점을 선택합니다(
    ). 중심점과 각 관측치 사이에 거리(ex. 유클리디안 거리)를 계산하여, 각 관측치를 가까운 군집에 할당합니다. 다음으로 묶인 군집에 대해서 중심점(중앙값)을 계산하고, 군집별 중심점과 각 관측치 사이에 거리를 계산하여, 각 관측치를 가까운 군집에 할당합니다. 변화가 없을 때까지 혹은 사전에 지정한 최대 반복 횟수만큼 업데이트를 진행합니다.

    장점

    k-means에 비해 이상치에 덜 민감함
    단점

    k-means와 마찬가지로 사전에 k 값을 지정해줘야 함

    알고리즘 계산이 오래걸림

    중앙값을 찾는데 많은 시간 소요
    from sklearn_extra.cluster import KMedoids

    scores = []

    for i in range(2,10):
        fit_km = KMedoids(n_clusters=i, random_state=0, method = 'pam').fit(df)
        score = silhouette_score(df, fit_km.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    km = KMedoids(n_clusters = 4, random_state=0, method = 'pam')
    km.fit(df)


    KMedoids
    KMedoids(method='pam', n_clusters=4, random_state=0)
    label = km.labels_

    df2 = df.copy()
    df2['cluster'] = label
    df2.head()

         Murder   Assault  UrbanPop      Rape  cluster
    0  1.255179  0.790787 -0.526195 -0.003451        1
    1  0.513019  1.118060 -1.224067  2.509424        2
    2  0.072361  1.493817  1.009122  1.053466        2
    3  0.234708  0.233212 -1.084492 -0.186794        1
    4  0.281093  1.275635  1.776781  2.088814        2
    12.5 CLARA
    CLARA의 경우 PAM의 대안입니다. PAM의 경우 데이터가 클 때, medoids를 계산하는데 시간이 오래걸리는 단점이 있습니다. 이를 보완하기 위해 CLARA의 경우 전체 데이터셋을 이용하지 않고 샘플링을 통해 연산 속도를 개선합니다.

    Note
    표본 데이터에 PAM 알고리즘을 적용
    각 표본에서 뽑힌 
    개 중심점을 전체 데이터셋에 적용 후 성능 평가
    군집 내 중심점(중앙값) 업데이트
    2-3번 과정을 변화가 없을 때까지 반복(혹은 사전에 지정한 최대 반복 횟수까지 반복)


    장점

    대용량 데이터셋을 다룰 수 있음
    단점

    표본 크기에 모델 성능이 민감함

    표본이 편향되어 있을 경우 표본으로 뽑은 데이터의 일부에서 좋은 군집이더라도, 전체 데이터에서 좋은 군집이라는 보장은 없음

    from sklearn_extra.cluster import CLARA

    scores = []

    for i in range(2,10):
        fit_cl = CLARA(n_clusters=i, random_state=0).fit(df)
        score = silhouette_score(df, fit_cl.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    cl = CLARA(n_clusters = 4)
    cl.fit(df)


    CLARA
    CLARA(n_clusters=4)
    label = km.labels_

    df2 = df.copy()
    df2['cluster'] = label
    df2.head()

         Murder   Assault  UrbanPop      Rape  cluster
    0  1.255179  0.790787 -0.526195 -0.003451        1
    1  0.513019  1.118060 -1.224067  2.509424        2
    2  0.072361  1.493817  1.009122  1.053466        2
    3  0.234708  0.233212 -1.084492 -0.186794        1
    4  0.281093  1.275635  1.776781  2.088814        2
    12.6 Gaussian Mixture Model(GMM)
    모델기반 군집방법 중 대표적으로 Gaussian Mixture Model(GMM)이 있습니다. GMM은 정규분포의 선형결합을 이용해서 만든 혼합분포를 이용해서 모델링하는 방법입니다. 실제 데이터는 정규분포를 따르지 않기 때문에 혼합 분포를 이용해서 모델링합니다. 혼합 분포의 각 모수는 EM 알고리즘을 이용해서 구할 수 있습니다.



    https://towardsdatascience.com/gaussian-mixture-models-explained-6986aaf5a95
    각 관측치는 각 정규분포에 해당하는 확률을 갖고, 가장 큰 확률을 갖는 군집으로 분류됩니다. 각 군집의 분포형태는 공분산의 형태에 의존합니다. 따라서 공분산의 형태를 사전에 지정해줘야 합니다. 공분산의 형태에 대한 매개변수가 존재하며, 사전 지식이 없는 경우 특정 지표를 기준으로 전부다 돌려보고 적절한 매개변수를 선택합니다.

    장점

    k-means와 같이 초기 중심점 선택 등 임의성에서 오는 성능 변화가 없음

    각 관측치가 특정 군집에 속할 확률을 구할 수 있음

    단점

    local optimum으로 수렴할 수 있음

    수렴속도가 느릴 수 있음

    df2 = pd.read_csv('./data/clustering/diabetes.csv')

    numeric_data = df2.select_dtypes('number')
    stdscaler = StandardScaler()
    df2 = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)
    df2.head(2)

        glucose   insulin      sspg
    0 -0.659025 -0.580247 -0.515421
    1 -0.392189 -0.790634 -0.573504
    from sklearn.mixture import GaussianMixture
    from sklearn.model_selection import GridSearchCV

    bic를 기준으로 모델을 선택할 수 있습니다. bic는 작을수록 좋지만, grid search시에 bic를 최대화하는 모형을 찾기 위해 -를 붙여주었습니다.

    def gmm_bic_score(estimator, X):
        return -estimator.bic(X)

    공분산의 형태를 지정해줍니다. R과 달리 총 4가지 케이스를 선택할 수 있습니다.

    param_grid = {
        "n_components": range(2, 10),
        "covariance_type": ["spherical", "tied", "diag", "full"],
    }

    GridSearchCV를 이용해서 -bic를 최대화하는 공분산의 형태와 군집의 수를 탐색해주었습니다.

    grid_search = GridSearchCV(
        GaussianMixture(random_state = 0), param_grid=param_grid, scoring=gmm_bic_score
    )
    grid_search.fit(df2)

    GridSearchCV

    GaussianMixture
    df = pd.DataFrame(grid_search.cv_results_)[
        ["param_n_components", "param_covariance_type", "mean_test_score"]]

    df.head()

      param_n_components param_covariance_type  mean_test_score
    0                  2             spherical      -364.290182
    1                  3             spherical      -358.564120
    2                  4             spherical      -412.999027
    3                  5             spherical      -407.371986
    4                  6             spherical      -426.495154
    bic에 다시 음수를 취해서 기준을 바꿔주었습니다.

    df["mean_test_score"] = -df["mean_test_score"]
    df = df.rename(
        columns={
            "param_n_components": "Number of components",
            "param_covariance_type": "Type of covariance",
            "mean_test_score": "BIC score",
        }
    )
    df.sort_values(by="BIC score").head()

       Number of components Type of covariance   BIC score
    16                    2               diag  248.258649
    8                     2               tied  298.713862
    1                     3          spherical  358.564120
    0                     2          spherical  364.290182
    3                     5          spherical  407.371986
    최종 결과는 공분산의 형태는 diag이고, 군집의 수는 2인 것을 확인할 수 있습니다. 간단하게 막대 그래프를 그려서 확인해볼 수 있습니다.

    sns.catplot(
        data=df,
        kind="bar",
        x="Number of components",
        y="BIC score",
        hue="Type of covariance",
    )



    plt.show();



    label = grid_search.predict(df2)
    prob = grid_search.predict_proba(df2)

    prob = pd.DataFrame(prob, columns = ['cluster1', 'cluster2'])
    label = pd.DataFrame({'cluster' : label})
    uncertainty = pd.concat([label, prob], axis = 1)
    uncertainty.head()

       cluster  cluster1  cluster2
    0        0  0.999605  0.000395
    1        0  0.999743  0.000257
    2        0  0.999709  0.000291
    3        0  0.999973  0.000027
    4        0  0.999995  0.000005
    참고 : https://scikit-learn.org/stable/auto_examples/mixture/plot_gmm_selection.html

    12.7 DBSCAN
    밀도 기반 군집(density-based clustering) 중 가장 대표적인 방법으로 DBSCAN이 있습니다. DBSCAN은 단순하게, 하나의 관측치를 기준으로 반경 
     내에 관측치가 
    이상 있으면 하나의 군집으로 인식하는 알고리즘입니다.
    Note
    (start point)와 임의의 다른 관측치 사이의 거리를 계산
    의 eps 내에 이웃 관측치 찾기
    이웃 관측치가 
     이상 있으면 중심점(core point)로 인식
    다른 core point에는 속하지만 이웃 관측치가 
     미만일 경우 border point로 인식
    다른 core point에는 속하지않고, 이웃 관측치가 
     미만일 경우 noise point로 인식
    다른 관측치에 대해 동일한 방식으로 core point, border point, noise point인지 확인
    core point가 다른 core point에 속해 있을 경우 core point 간에는 하나의 군집으로 인식


    그림을 보면 
    일 때, 
    는 자기 자신 포함 총 6개의 관측치가 eps 내에 있으므로, core point입니다. 
    를 보면 
    는 자기 자신 포함 총 
    개의 이웃이 있으므로, 
     입니다. 하지만 core point 
    의 eps 내에 속하므로, border point 입니다. 마지막으로, 
    는 
    이고, core point에도 속하지 않으므로, noise point가 됩니다.

    장점

    군집의 수를 사전에 지정할 필요가 없음

    밀도 기반이므로 군집이 기하학적인 모양을 갖는 경우에도 잘 작동함

    이상치 식별 가능

    단점

    eps, MinPts에 따라 성능의 변동이 있음


    from sklearn.cluster import DBSCAN

    df_8 = pd.read_csv('data/clustering/df_8.csv')
    df_8.head()

              x         y
    0 -0.803739 -0.853053
    1  0.852851  0.367618
    2  0.927180 -0.274902
    3 -0.752626 -0.511565
    4  0.706846  0.810679
    eps를 결정하는 방법

    eps에 따라서 성능 변동이 있으므로, 적절한 eps를 선정하는 기준이 있어야 합니다. 이를 위해 k-nearest neighbor distance(euclidean distance 이용)를 이용합니다. 각 관측치에 대해서 k-nearest neighbor distance를 구합니다. 여기서 
    는 
    입니다. k-nearest neighbor distance를 오름차순으로 정렬합니다. k-nearest neighbor distance의 elbow point를 찾아서 최적의 
    로 지정합니다.

    from sklearn.neighbors import NearestNeighbors 

    neighbors = NearestNeighbors(n_neighbors=4)
    neighbors_fit = neighbors.fit(df_8)
    distances, indices = neighbors_fit.kneighbors(df_8)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=0.15, color='black', linestyle='--', linewidth=3)
    plt.show();



    그래프를 보면 
    가 선택된 것을 볼 수 있습니다. minPts(= min_samples)의 경우 구하는 기준이 따로 없습니다. 경험적으로 논문에서는 minPts = 2*칼럼의 수로 추천합니다.

    db = DBSCAN(eps=0.15, min_samples=4).fit(df_8)
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)

    Estimated number of clusters: 5
    print("Estimated number of noise points: %d" % n_noise_)

    Estimated number of noise points: 29
    label = pd.DataFrame({'cluster' : labels})
    df_8 = pd.concat([label, df_8], axis = 1)

    sns.scatterplot(data=df_8, x="x", y="y", style = 'cluster')
    plt.show();



    그래프를 보면 군집의 형태와 무관하게 비교적 잘 작동하는 것을 볼 수 있습니다.

    12.8 군집 유효성 측도
    군집 분석이 잘 수행되었는지 평가할 수 있는 기준이 필요합니다. 기준은 각 상황 및 특성에 맞게 내부 유효성 측도, 외부 유효성 측도, 안정성 측도 등 총 세 가지로 분류해볼 수 있습니다.

    12.8.1 내부 유효성 측도(Internal measures for cluster validation)
    원 데이터로 군집화된 결과만을 가지고 데이터 본래의 정보를 사용하여 군집화를 얼마나 잘 수행했는지 평가하는 측도

    정답이 없는 경우에 해당, silhouette index or Dunn index로 계산 가능

    compactness
    같은 군집 내에 객체가 얼마나 가까운지를 나타냄

    즉, 군집 내 분산이 작은 경우 좋은 군집이라고 볼 수 있음

    Seperation
    얼마나 군집이 다른 군집과 잘 분리되었는지를 나타냄

    군집간 거리 or 군집 내 객체들의 군집 간 최소 거리가 멀면 좋은 군집이라고 볼 수 있음

    connectivity
    어떤 객체가 가까운 거리에 있는 객체들과 얼마나 같은 군집에 포함되었는지를 나타냄
    다음과 같은 기준으로 대표적으로 두 가지 측도가 있음

    silhouette coefficient

    군집 내 객체 사이의 평균 거리와 다른 군집에서의 객체 사이의 평균 거리를 이용해서 계산

    1에 가까우면 군집이 잘된 것이고, -1에 가까우면 군집이 잘 안된 것

    추가 설명 링크 : https://dondonkim.netlify.app/posts/2022-10-08-sillouette/silhouette.html

    from yellowbrick.cluster import SilhouetteVisualizer
    from sklearn import datasets

    Caution
    yellowbrick 패키지는 adp 패키지 지원 리스트에 없으므로, 사전에 설치 여부를 체크해야 합니다.

    iris = datasets.load_iris()
    X = iris.data 
    y = iris.target

    scaler = StandardScaler()
    scaled_df = pd.DataFrame(data = scaler.fit_transform(X))
    scaled_df.head()

              0         1         2         3
    0 -0.900681  1.019004 -1.340227 -1.315444
    1 -1.143017 -0.131979 -1.340227 -1.315444
    2 -1.385353  0.328414 -1.397064 -1.315444
    3 -1.506521  0.098217 -1.283389 -1.315444
    4 -1.021849  1.249201 -1.340227 -1.315444
    kmeans = KMeans(n_clusters=3, random_state=0)
    #visualizer 생성
    visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
    #생성된 visualizer에 데이터 입력 
    visualizer.fit(scaled_df)      

    SilhouetteVisualizer

    KMeans
    visualizer.show()



    silhouette width가 음수일 경우 잘못된 군집에 속해있다는 의미
    result = pd.DataFrame(X)
    result['cluster'] = visualizer.predict(scaled_df)
    result['silhouette_coefficient'] = visualizer.silhouette_samples_
    result.head()

         0    1    2    3  cluster  silhouette_coefficient
    0  5.1  3.5  1.4  0.2        1                0.734195
    1  4.9  3.0  1.4  0.2        1                0.568274
    2  4.7  3.2  1.3  0.2        1                0.677547
    3  4.6  3.1  1.5  0.2        1                0.620502
    4  5.0  3.6  1.4  0.2        1                0.728474
    result.loc[result.silhouette_coefficient < 0]

           0    1    2    3  cluster  silhouette_coefficient
    111  6.4  2.7  5.3  1.9        0               -0.010584
    127  6.1  3.0  4.9  1.8        0               -0.024894
    dbscan

    from sklearn.neighbors import NearestNeighbors 

    neighbors = NearestNeighbors(n_neighbors=6)
    neighbors_fit = neighbors.fit(scaled_df)
    distances, indices = neighbors_fit.kneighbors(scaled_df)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=0.5, color='black', linestyle='--', linewidth=3)
    plt.show();



    db = DBSCAN(eps=0.5, min_samples=6).fit(scaled_df)
    labels = db.labels_

    visualizer는 n_clusters가 지정된 estimator만 작동하므로(ex. k-means), 수동으로 n_clusters를 넣어주어야 합니다.
    n_clusters = len(set(db.labels_))
    db.n_clusters = n_clusters
    db.predict = lambda x: db.labels_

    visualizer = SilhouetteVisualizer(db, colors='yellowbrick')
    #생성된 visualizer에 데이터 입력 
    visualizer.fit(scaled_df)      

    SilhouetteVisualizer

    DBSCAN
    visualizer.show()



    12.9 외부 유효성 측도( External clustering validation)
    정답이 있는 경우 rand index, vi index(variable of information)를 이용해서 각 군집 분석별로 성능을 비교할 수 있음
    실제 데이터를 분석할 때는 정답을 알 수 없으므로, 알고리즘 연구할 때 주로 활용됨
    rand index : 1에 가까울 수록 좋음
    rand index는 군집의 수가 커지면, rand index값도 커지기 때문에 adjusted rand index를 주로 이용
    adjusted rand index는 1에 가까울수록 좋음
    from sklearn.metrics import adjusted_rand_score
    adjusted_rand_score(result.cluster, y)

    0.6201351808870379
    km = KMedoids(n_clusters = 5, random_state=0, method = 'pam')
    km.fit(X)


    KMedoids
    KMedoids(method='pam', n_clusters=5, random_state=0)
    label = km.labels_
    adjusted_rand_score(label, y)

    0.6202309314293009
    hk = AgglomerativeClustering(n_clusters = 5, linkage = 'ward')
    hk.fit(X)


    AgglomerativeClustering
    AgglomerativeClustering(n_clusters=5)
    label = hk.labels_
    adjusted_rand_score(label, y)

    0.59502294387575
    PAM 알고리즘의 경우 adjusted rand index가 가장 높다. 따라서 해당 데이터에서는 PAM 알고리즘이 가장 성능이 우수한 것을 확인할 수 있다.

    12.10 안정성 측도(stability measure)
    하나의 열이 제거된 후 군집과 원 군집 결과를 비교해서 군집 결과의 일관성을 측정함

    The average proportion of non-overlap (APN)

    전체 데이터를 이용한 군집과 하나의 열을 제거한 후 군집을 했을 때 동일한 군집에 배치되지 않는 관측치의 평균 비율을 측정함

    0에 가까울수록 변수 제거 전후의 군집간 객체 이동성이 작다는 의미

    The average distance (AD)

    전체 데이터를 이용한 군집과 하나의 열을 제거한 후 군집을 했을 때 동일한 클러스터에 배치된 관측치 간의 평균 거리를 측정

    0에 가까울수록 군집화의 결과가 일관성이 있다고 판단

    The average distance between means (ADM)

    전체 데이터를 이용한 군집과 하나의 열을 제거한 후 군집을 했을 때 동일한 클러스터에 배치된 관측치에 대한 군집 중심 간 평균 거리를 측정

    0에 가까울 수록 군집화의 결과가 일관성이 있다고 판단

    The figure of merit (FOM)

    하나의 열을 제거한 후 군집한 결과와 제거된 열의 관측치 간 군집 내 분산을 계산

    0에 가까울수록 군집의 변동성이 적다고 판단

    Note
    안정성 측도는 파이썬에 따로 구현이 안되어있습니다. 답안 작성시 참고용으로 알고계시기 바랍니다.

    12.11 연속형변수와 범주형변수가 혼합되어 있는 경우
    지금까지는 연속형 변수만을 활용하여, 군집분석을 실시했습니다. 하지만 실제 데이터에는 연속형 변수와 범주형 변수가 혼합되어 있는 경우가 대부분입니다. 이 경우 가장 쉽게 처리하는 방법은 범주형 변수를 인코딩해서 수치형 변수로 바꿔준 후 군집분석을 하는 방법입니다. 먼저 이렇게 처리할 경우 발생할 수 있는 문제점에 대해 알아보겠습니다.

    문제점

    수치형 변수의 경우 유클리디안 거리 값은 순수한 거리의 의미임

    유클리디안 거리가 크면 멀리 떨어져있고, 작으면 가까움
    범주형 변수를 인코딩한 후 거리를 계산했을 때, 수치형 변수에서 거리를 구한 것처럼 해석이 불가능

    사과, 배, 바나나는 가깝다, 멀다의 의미를 갖고 있지 않기 때문
    인코딩을 할 경우 차원이 늘어나기 때문에 계산량이 증가함

    추가적으로 차원의 저주(참고 : <ttps://chulhongsung.github.io/ml/%EC%B0%A8%EC%9B%90%EC%9D%98%EC%A0%80%EC%A3%BC/>)

    실험결과예시 : https://medium.com/analytics-vidhya/clustering-on-mixed-data-types-in-python-7c22b3898086

    따라서 범주형 변수를 인코딩하여 수치형 변수로 변환 후 군집분석을 실시하는 것은 바람직하지 않습니다. 다른 대안을 알아보겠습니다.

    대안

    k-prototype clustering (패키지 목록에 없으므로 생략)

    gower distance

    PAM 주로 이용
    k-means는 이용 x
    import gower

    Caution
    gower 패키지는 adp 패키지 지원 리스트에 없으므로, 사전에 설치 여부를 체크해야 합니다.

    iris = datasets.load_iris()
    X = iris.data 
    y = iris.target
    X = pd.DataFrame(X, columns=['X1', 'X2', 'X3', 'X4'])
    X['X4'] = np.where(X['X4'] < 2, 'LOW', 'HIGH')

    num_feature = ['X1', 'X2', 'X3']
    cat_feature = ['X4']
    scaler = StandardScaler()
    X[num_feature] = scaler.fit_transform(X[num_feature])
    dist_matrix = gower.gower_matrix(X)

    # neighbors = NearestNeighbors(n_neighbors=8)
    # neighbors_fit = neighbors.fit(dist_matrix)
    # distances, indices = neighbors_fit.kneighbors(dist_matrix)
    # 
    # distances = np.sort(distances, axis=0)
    # distances = distances[:,1]
    # plt.plot(distances)
    # plt.axhline(y=0.3, color='black', linestyle='--', linewidth=3)
    # plt.show();
    # 
    # db = DBSCAN(eps = 0.2, min_samples = 4, metric = "precomputed").fit(dist_matrix)
    # labels = db.labels_

    # db = DBSCAN(eps = 0.4, min_samples = 4).fit(X)
    # aa = pd.DataFrame(db.labels_)
    # aa.value_counts()
    # labels = db.labels_

    neighbors = NearestNeighbors(n_neighbors=8)
    neighbors_fit = neighbors.fit(dist_matrix)
    distances, indices = neighbors_fit.kneighbors(dist_matrix)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=0.3, color='black', linestyle='--', linewidth=3)
    plt.show();



    사전에 정의한 metric을 이용하기 위해서는 metric = "precomputed"로 설정해야 합니다.

    db = DBSCAN(eps = 0.2, min_samples = 2, metric = "precomputed").fit(dist_matrix)

    labels = db.labels_

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    # from sklearn.datasets import make_blobs
    # X, y = make_blobs(n_samples=50, centers=3, n_features=3, random_state=1234)
    # X = pd.DataFrame(X, columns=['X1', 'X2', 'X3'])
    # X['X3'] = np.where(X['X3'] < 0, 'LOW', 'HIGH')
    # con_feats = ['X1', 'X2'] 
    # cat_feats = ['X3']
    # scale = StandardScaler()
    # X[con_feats] = scale.fit_transform(X[con_feats])
    # X.head()
    # 
    # dist_matrix = gower.gower_matrix(X)
    # 
    # neighbors = NearestNeighbors(n_neighbors=8)
    # neighbors_fit = neighbors.fit(dist_matrix)
    # distances, indices = neighbors_fit.kneighbors(dist_matrix)
    # 
    # distances = np.sort(distances, axis=0)
    # distances = distances[:,1]
    # plt.plot(distances)
    # plt.axhline(y=0.3, color='black', linestyle='--', linewidth=3)
    # plt.show();
    # 
    # db = DBSCAN(eps = 0.15, min_samples = 6, metric = "precomputed").fit(dist_matrix)
    # 
    # labels = db.labels_

    12.12 데이터가 클 경우
    데이터가 
    개인 경우를 예로 들어보겠습니다.

    dat_num = pd.read_csv('data/clustering/large_data.csv')

    k-means

    scores = []
    start_time = time.time()
    for i in range(2,10):
        fit_kmeans = KMeans(n_clusters=i, init='random', n_init = 10, random_state=0).fit(dat_num)
        score = silhouette_score(dat_num, fit_kmeans.labels_)
        scores.append(score)
        print("For n_clusters={0}, the silhouette score is {1}".format(i, score))

    For n_clusters=2, the silhouette score is 0.524283962023498
    For n_clusters=3, the silhouette score is 0.559195433493867
    For n_clusters=4, the silhouette score is 0.524391135903275
    For n_clusters=5, the silhouette score is 0.5088340030567556
    For n_clusters=6, the silhouette score is 0.5026856412617199
    For n_clusters=7, the silhouette score is 0.49661780704261105
    For n_clusters=8, the silhouette score is 0.4913607037381164
    For n_clusters=9, the silhouette score is 0.3666265535061289
    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    print("{}s".format(time.time()-start_time))

    198.9404420852661s
    clara

    scores = []
    start_time = time.time()
    for i in range(2,10):
        fit_cl = CLARA(n_clusters=i, random_state=0, n_sampling=600).fit(dat_num)
        score = silhouette_score(dat_num, fit_cl.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    print("{}s".format(time.time()-start_time))

    197.18347311019897s
    PAM

    scores = []
    start_time = time.time()
    for i in range(2,10):
        fit_km = KMedoids(n_clusters=i, random_state=0, method = 'pam').fit(dat_num)
        score = silhouette_score(dat_num, fit_km.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()
    print("{}s".format(time.time()-start_time))

    GMM

    def gmm_bic_score(estimator, X):
        return -estimator.bic(X)

    param_grid = {
        "n_components": range(2, 10),
        "covariance_type": ["spherical", "tied", "diag", "full"],
    }
    start_time = time.time()
    grid_search = GridSearchCV(
        GaussianMixture(random_state = 0), param_grid=param_grid, scoring=gmm_bic_score
    )
    grid_search.fit(dat_num)

    GridSearchCV

    GaussianMixture
    print("{}s".format(time.time()-start_time))

    21.11660599708557s
    df = pd.DataFrame(grid_search.cv_results_)[
        ["param_n_components", "param_covariance_type", "mean_test_score"]]

    df.head()

      param_n_components param_covariance_type  mean_test_score
    0                  2             spherical   -280901.258019
    1                  3             spherical   -135649.693924
    2                  4             spherical   -133828.935607
    3                  5             spherical   -130062.719645
    4                  6             spherical   -129620.171232
    DBSCAN

    from sklearn.neighbors import NearestNeighbors 

    neighbors = NearestNeighbors(n_neighbors=16)
    neighbors_fit = neighbors.fit(dat_num)
    distances, indices = neighbors_fit.kneighbors(dat_num)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=0.75, color='black', linestyle='--', linewidth=3)
    plt.show();



    start_time = time.time()
    db = DBSCAN(eps=0.75, min_samples=16).fit(dat_num)
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)

    Estimated number of clusters: 3
    print("Estimated number of noise points: %d" % n_noise_)

    Estimated number of noise points: 2416
    print("{}s".format(time.time()-start_time))

    9.334905862808228s
    Warning
    average silhouette coefficient가 적절한 군집 알고리즘을 선택하기 위한 측도로 활용되지만, DBSCAN의 경우 적절하지 않을 수 있음





    시험에서는 근거만 제시하면 되기 때문에, 그냥 silhouette coefficient를 이용해도 무방하고, 해당 내용은 참고로 알고 있기 바람!

    12.13 PCA
    PCA의 경우 데이터 전처리 파트에서 활용되므로, 이론은 제외하고 어떻게 효율적으로 수행할 수 있는지를 중심으로 설명드리겠습니다(이론은 통계반 참고).

    Example

    df_5 = pd.read_csv('data/clustering/df_5.csv')
    df_5.columns = ['index', 'X100m', 'Long.jump', 'Shot.put', 'High.jump', 'X400m',
           'X110m.hurdle', 'Discus', 'Pole.vault', 'Javeline', 'X1500m']
    df_5.set_index('index', inplace = True)

    from sklearn.decomposition import PCA
    from sklearn.pipeline import Pipeline

    pca_pipe = Pipeline([("scaler", StandardScaler()), 
                         ("pca", PCA(n_components= 0.8, svd_solver='full'))
                         ])

    pca_data = pd.DataFrame(pca_pipe.fit_transform(df_5))                     
    pca_data.head()

              0         1         2         3
    0 -0.195505  1.589057  0.642491 -0.083897
    1 -0.807879  2.474814 -1.387383 -1.298382
    2  1.359134  1.648095  0.200558  1.964094
    3  0.888953 -0.442607  2.529584 -0.712908
    4  0.108122 -2.068838 -1.334259  0.101528
    scree plot

    pca_pipe.named_steps['pca'].n_components_

    4
    PC_values = np.arange(pca_pipe.named_steps['pca'].n_components_) + 1
    plt.plot(PC_values, pca_pipe.named_steps['pca'].explained_variance_ratio_, 'ro-', linewidth=2)
    plt.title('Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Proportion of Variance Explained')
    plt.show()



    out_sum = np.cumsum(pca_pipe.named_steps['pca'].explained_variance_ratio_)  
    print ("Cumulative Prop. Variance Explained: ", out_sum)

    Cumulative Prop. Variance Explained:  [0.41242133 0.59627443 0.72018845 0.80213247]
    12.13.1 pca 패키지 이용
    참고 : https://erdogant.github.io/pca/pages/html/Algorithm.html#loadings

    Caution
    pca 패키지는 adp 패키지 지원 리스트에 없으므로, 사전에 설치 여부를 체크해야 합니다.

    from pca import pca
    model = pca(normalize=True) 
    col_labels = df_5.columns
    results = model.fit_transform(df_5, col_labels=col_labels)

    [pca] >Extracting row labels from dataframe.
    [pca] >Normalizing input data per feature (zero mean and unit variance)..
    [pca] >The PCA reduction is performed to capture [95.0%] explained variance using the [10] columns of the input data.
    [pca] >Fit using PCA.
    [pca] >Compute loadings and PCs.
    [pca] >Compute explained variance.
    [pca] >Number of components is [8] that covers the [95.00%] explained variance.
    [pca] >The PCA reduction is performed on the [10] columns of the input dataframe.
    [pca] >Fit using PCA.
    [pca] >Compute loadings and PCs.
    [pca] >Outlier detection using Hotelling T2 test with alpha=[0.05] and n_components=[8]
    [pca] >Multiple test correction applied for Hotelling T2 test: [fdr_bh]
    [pca] >Outlier detection using SPE/DmodX with n_std=[3]
    model.biplot(cmap=None, legend=False)

    [pca] >Plot PC1 vs PC2 with loadings.
    (<Figure size 5000x3000 with 1 Axes>, <Axes: title={'center': '8 Principal Components explain [98.78%] of the variance'}, xlabel='PC1 (41.2% expl.var)', ylabel='PC2 (18.3% expl.var)'>)
    plt.show();



    results['loadings']['Pole.vault']

    PC1    0.106986
    PC2    0.595499
    PC3    0.084496
    PC4    0.374474
    PC5    0.264671
    PC6    0.503564
    PC7    0.018894
    PC8   -0.062827
    Name: Pole.vault, dtype: float64
    주성분 별로 계수의 효과를 파악하기 어렵기 때문에 plot을 그려서 확인

    화살표가 찍히는 꼭지점의 좌표는 각 주성분에서 특정 변수의 가중치 값이 됨

    예를 들어 Pole.vault의 경우 PC1의 가중치는 0.106, PC2의 가중치는 0.595이므로 해당 좌표(0.106, 0.595)에 점이 찍힘

    즉 주성분 축에 평행할수록 해당 변수는 주성분에 크게 기여했다고 볼 수 있음

    같은 각도로 뻗어나가는 경우 서로 비슷한 변수라고 볼 수 있음

    12.14 PCA and modeling tutorial
    https://www.kaggle.com/uciml/breast-cancer-wisconsin-data

    UCI machine learning 데이터가 시험에 나오는 경우가 많은 것 같아서 kaggle tutorial 중에 pca 후 모델링 관련 괜찮은 데이터를 골랐습니다.

    12.14.1 데이터 불러오기
    cancer = pd.read_csv("./data/clustering/cancer.csv")

    import janitor

    cancer.head()

      diagnosis  radius_mean  ...  symmetry_worst  fractal_dimension_worst
    0         M        17.99  ...          0.4601                  0.11890
    1         M        20.57  ...          0.2750                  0.08902
    2         M        19.69  ...          0.3613                  0.08758
    3         M        11.42  ...          0.6638                  0.17300
    4         M        20.29  ...          0.2364                  0.07678

    [5 rows x 31 columns]
    12.14.2 EDA
    변수 간 상관관계가 뚜렷함
    corr = cancer.select_dtypes(['int', 'float']).corr()
    sns.heatmap(corr)
    plt.show()



    12.14.3 데이터 전처리
    결측치 확인
    cancer.isna().sum()

    diagnosis                  0
    radius_mean                0
    texture_mean               0
    perimeter_mean             0
    area_mean                  0
    smoothness_mean            0
    compactness_mean           0
    concavity_mean             0
    concave_points_mean        0
    symmetry_mean              0
    fractal_dimension_mean     0
    radius_se                  0
    texture_se                 0
    perimeter_se               0
    area_se                    0
    smoothness_se              0
    compactness_se             0
    concavity_se               0
    concave_points_se          0
    symmetry_se                0
    fractal_dimension_se       0
    radius_worst               0
    texture_worst              0
    perimeter_worst            0
    area_worst                 0
    smoothness_worst           0
    compactness_worst          0
    concavity_worst            0
    concave_points_worst       0
    symmetry_worst             0
    fractal_dimension_worst    0
    dtype: int64
    12.14.4 Pipeline를 이용한 방법
    y = cancer.diagnosis
    X = cancer.drop(['diagnosis'], axis = 1)

    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.3, random_state = 0)

    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import set_config

    pipe_rf = Pipeline([("scaler", StandardScaler()), 
                         ("pca", PCA(n_components= 0.8, svd_solver='full')),
                         ("classifier", RandomForestClassifier())
                         ])

    RandomForest_param = {'classifier__max_features': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    start_time = time.time()
    RandomForest_search = GridSearchCV(estimator = pipe_rf, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'balanced_accuracy') # roc_auc, average_precision
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV

    StandardScaler

    PCA

    RandomForestClassifier
    pred = RandomForest_search.predict(test_X)
    print(classification_report(test_y, pred))

                  precision    recall  f1-score   support

               B       0.95      0.93      0.94       108
               M       0.88      0.92      0.90        63

        accuracy                           0.92       171
       macro avg       0.92      0.92      0.92       171
    weighted avg       0.93      0.92      0.92       171
    """