def m26():
    """
    26회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    24.1 머신러닝
    Data description

    Invoice_no : 송장번호

    Stock_code : 제품코드

    Stock_category : 제품 분류

    Quantity : 수량

    Invoice_date : 주문일자

    Unit_price : 단가

    Customer_id : 고객번호

    Country : 국가

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from sklearn.preprocessing import StandardScaler
    from datetime import datetime

    dat = pd.read_csv("data/retail3.csv")

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 44416 entries, 0 to 44415
    Data columns (total 8 columns):
     #   Column         Non-Null Count  Dtype  
    ---  ------         --------------  -----  
     0   InvoiceNo      44416 non-null  object 
     1   StockCode      44416 non-null  object 
     2   StockCategory  44416 non-null  object 
     3   Quantity       44400 non-null  float64
     4   InvoiceDate    44416 non-null  object 
     5   UnitPrice      44416 non-null  float64
     6   CustomerID     44416 non-null  int64  
     7   Country        44416 non-null  object 
    dtypes: float64(2), int64(1), object(5)
    memory usage: 2.7+ MB
    dat = dat.clean_names()

    dat = dat.astype({'invoicedate' : 'datetime64[ns]', 'customerid' : 'object'})

    dat['year'] = dat['invoicedate'].dt.year
    dat['month'] = dat['invoicedate'].dt.month
    dat['day'] = dat['invoicedate'].dt.day

    24.1.1 1. 결측치 처리하시오.
    결측치를 삭제하지 않고, 처리하는 방법과 수행 결과를 제시하시오.

    dat.isna().sum()

    invoiceno         0
    stockcode         0
    stockcategory     0
    quantity         16
    invoicedate       0
    unitprice         0
    customerid        0
    country           0
    year              0
    month             0
    day               0
    dtype: int64
    quantity 변수에 결측치 16개 존재
    mean_q = dat.groupby(['customerid', 'year', 'month', 'day']).agg(mean1 = ('quantity', 'mean')).round(0).reset_index()
    mean_q.head(2)

       customerid  year  month  day  mean1
    0       12347  2010     12    7   10.0
    1       12347  2011      1   26   11.0
    고객별 하루동안 구매한 quantity의 평균값을 산출함
    dat = pd.merge(dat, mean_q, left_on = ["customerid", "year", "month", "day"], right_on = ["customerid", "year", "month", "day"], how = 'left')

    dat['quantity'][dat['quantity'].isna()] = dat['mean1'][dat['quantity'].isna()]

    dat = dat.drop(['mean1', 'year', 'month', 'day'], axis = 1)
    dat.isna().sum()

    invoiceno        0
    stockcode        0
    stockcategory    0
    quantity         0
    invoicedate      0
    unitprice        0
    customerid       0
    country          0
    dtype: int64
    특정 고객이 해당 제품을 몇 개를 살지 유추하기 어려움

    따라서 특정 고객이 그 날에 구매한 제품 quantity의 평균으로 결측치 대치

    24.1.2 고객 데이터를 활용하여 군집분석을 수행하려고 한다. 군집분석 수행 전에 이상치를 제거하려고 한다. 이상치를 제거하는 방법을 설명하고, 이상치를 제거한 후 이상치가 모두 제거되었다는 통계 자료를 제시하시오.
    dat.describe()

               quantity                    invoicedate     unitprice
    count  44416.000000                          44416  44416.000000
    mean      20.158704  2011-07-07 15:45:49.833393408      5.135913
    min     -624.000000            2010-12-01 08:45:00      0.000000
    25%        4.000000            2011-04-04 11:18:00      1.250000
    50%       10.000000            2011-07-27 14:21:00      1.950000
    75%       16.000000            2011-10-12 10:20:00      3.750000
    max     2400.000000            2011-12-09 12:50:00   4161.060000
    std       48.147072                            NaN     57.720402
    quantity가 0 이하인 값 존재

    quantity가 음수의 값이 나올 수 없으므로 이상치로 판단하고 제거
    unit price가 0인 값 존재

    dat.loc[dat.unitprice == 0, ['stockcode', 'stockcategory']]

          stockcode                        stockcategory
    452       22619            SET OF 6 SOLDIER SKITTLES
    923       23234        BISCUIT TIN VINTAGE CHRISTMAS
    1188      22385            JUMBO BAG SPACEBOY DESIGN
    7612      22423             REGENCY CAKESTAND 3 TIER
    9938      23157           SET OF 6 NATIVITY MAGNETS 
    14182         M                               Manual
    27312         M                               Manual
    29220     22841         ROUND CAKE TIN VINTAGE GREEN
    35511     23270     SET OF 2 CERAMIC PAINTED HEARTS 
    35512     23268  SET OF 2 CERAMIC CHRISTMAS REINDEER
    35513     22955             36 FOIL STAR CAKE CASES 
    35514     21786                   POLKADOT RAIN HAT 
    37304     23407       SET OF 2 TRAYS HOME SWEET HOME
    39236         M                               Manual
    40319     22960             JAM MAKING SET WITH JARS
    43799     22636   CHILDS BREAKFAST SET CIRCUS PARADE
    dat.loc[dat.stockcode == '22619', ['stockcode', 'stockcategory', 'unitprice']]

          stockcode              stockcategory  unitprice
    111       22619  SET OF 6 SOLDIER SKITTLES       3.75
    150       22619  SET OF 6 SOLDIER SKITTLES       3.75
    200       22619  SET OF 6 SOLDIER SKITTLES       3.39
    365       22619  SET OF 6 SOLDIER SKITTLES       3.39
    440       22619  SET OF 6 SOLDIER SKITTLES       3.39
    452       22619  SET OF 6 SOLDIER SKITTLES       0.00
    796       22619  SET OF 6 SOLDIER SKITTLES       3.39
    2063      22619  SET OF 6 SOLDIER SKITTLES       3.75
    2899      22619  SET OF 6 SOLDIER SKITTLES       3.75
    3920      22619  SET OF 6 SOLDIER SKITTLES       3.75
    7622      22619  SET OF 6 SOLDIER SKITTLES       3.75
    8745      22619  SET OF 6 SOLDIER SKITTLES       3.75
    8902      22619  SET OF 6 SOLDIER SKITTLES       3.75
    12040     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14324     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14475     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14513     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14725     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14747     22619  SET OF 6 SOLDIER SKITTLES       3.75
    14851     22619  SET OF 6 SOLDIER SKITTLES       3.75
    15103     22619  SET OF 6 SOLDIER SKITTLES       3.75
    15682     22619  SET OF 6 SOLDIER SKITTLES       3.75
    17586     22619  SET OF 6 SOLDIER SKITTLES       3.75
    20688     22619  SET OF 6 SOLDIER SKITTLES       3.75
    20775     22619  SET OF 6 SOLDIER SKITTLES       3.75
    21159     22619  SET OF 6 SOLDIER SKITTLES       3.75
    24201     22619  SET OF 6 SOLDIER SKITTLES       3.75
    25137     22619  SET OF 6 SOLDIER SKITTLES       3.75
    25713     22619  SET OF 6 SOLDIER SKITTLES       3.75
    28398     22619  SET OF 6 SOLDIER SKITTLES       3.75
    29880     22619  SET OF 6 SOLDIER SKITTLES       3.75
    30975     22619  SET OF 6 SOLDIER SKITTLES       3.75
    31976     22619  SET OF 6 SOLDIER SKITTLES       3.75
    33266     22619  SET OF 6 SOLDIER SKITTLES       3.75
    33379     22619  SET OF 6 SOLDIER SKITTLES       3.75
    36512     22619  SET OF 6 SOLDIER SKITTLES       3.75
    38612     22619  SET OF 6 SOLDIER SKITTLES       3.75
    39121     22619  SET OF 6 SOLDIER SKITTLES       3.75
    39187     22619  SET OF 6 SOLDIER SKITTLES       3.75
    40624     22619  SET OF 6 SOLDIER SKITTLES       3.75
    40695     22619  SET OF 6 SOLDIER SKITTLES       3.75
    40900     22619  SET OF 6 SOLDIER SKITTLES       3.75
    42747     22619  SET OF 6 SOLDIER SKITTLES       3.75
    43545     22619  SET OF 6 SOLDIER SKITTLES       3.75
    43708     22619  SET OF 6 SOLDIER SKITTLES       3.75
    제품코드, 제품 분류가 같아도 단가가 다름

    unit price가 0인 경우는 사은품으로 증정해주는 경우를 생각해볼 수 있음

    이상치 제거 x

    dat.loc[:, ['quantity', 'unitprice']].plot(
        kind='box', 
        subplots=True, 
        sharey=False, 
        figsize=(10, 6)
    )

    quantity        Axes(0.125,0.11;0.352273x0.77)
    unitprice    Axes(0.547727,0.11;0.352273x0.77)
    dtype: object
    plt.subplots_adjust(wspace=0.7) 
    plt.show()



    Q1 = np.quantile(dat['quantity'], 0.25)
    Q3 = np.quantile(dat['quantity'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) 
    LC = Q3 - (1.5 * IQR) 

    dat.loc[(dat.quantity > UC), "quantity"].describe()

    count    5056.000000
    mean      103.483188
    std       108.429197
    min        36.000000
    25%        48.000000
    50%        72.000000
    75%       120.000000
    max      2400.000000
    Name: quantity, dtype: float64
    Q1 = np.quantile(dat['unitprice'], 0.25)
    Q3 = np.quantile(dat['unitprice'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) 
    LC = Q3 - (1.5 * IQR) 

    dat.loc[(dat.unitprice > UC), "unitprice"].describe()

    count    5458.000000
    mean       26.557292
    std       163.024353
    min         7.650000
    25%         8.500000
    50%         9.950000
    75%        16.950000
    max      4161.060000
    Name: unitprice, dtype: float64
    다음으로 이상치 탐지 방법으로 상자 수염 그림을 이용해보고자 한다. 상자그림에서 이상치는 울타리를 기준으로 이상치를 판단하는데, 위 울타리는 제3사분위수 + 1.5xIQR, 아래 울타리는 제 1사분위수 - 1.5xIQR로 정의된다. 울타리를 기준으로 이상치를 탐색해보면 분포의 치우침으로 인해서 너무 많은 관측치가 이상치로 탐지되는 것을 확인할 수 있다.

    단순히 이상치를 생각해보았을 때, unit price, quantity 값이 큰 관측치의 경우, 충성고객 or 우량 고객일 가능성이 높으며, 중요한 고객군으로 분류될 가능성이 높다. 따라서 통계적인 방법으로 확인했을 때의 이상치는 제거하지 않고, quantity < 0인 관측치만 이상치로 분류한 후 제거한다.

    dat = dat.loc[dat.quantity > 0, :]

    dat.quantity.describe()

    count    43156.000000
    mean        21.035638
    std         48.198779
    min          1.000000
    25%          6.000000
    50%         12.000000
    75%         18.000000
    max       2400.000000
    Name: quantity, dtype: float64
    24.1.3 kmeans 또는 DBSCAN 등의 기법을 활용하여 군집을 생성하시오.
    F, M 파생변수 생성
    F(고객별 거래빈도) : 각 고객별로 거래를 얼마나 했는지

    new_f = dat.groupby(['customerid']).agg(new_f = ('customerid', 'count')).reset_index()

    new_m = dat.assign(t_price = lambda x: x.unitprice*x.quantity).groupby(['customerid']).agg(new_m = ('t_price', 'sum')).reset_index()

    # dat = pd.merge(dat, new_f, left_on = 'customerid', right_on = 'customerid', how = 'left')
    # dat = pd.merge(dat, new_m, left_on = 'customerid', right_on = 'customerid', how = 'left')

    dat2 = pd.merge(new_f, new_m, left_on = 'customerid', right_on = 'customerid', how = 'inner')

    dat2 = dat2.astype({'customerid' : 'object'})

    M(고객별 총 구매액) : 각 고객별로 구매한 총 구매액

    k-means

    from sklearn.preprocessing import StandardScaler
    numeric_data = dat2.select_dtypes('number')
    stdscaler = StandardScaler()
    numeric_df = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)
    numeric_df.head(2)

          new_f     new_m
    0  0.242606  0.023383
    1 -0.234756 -0.118031
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    scores = []
    start_time = time.time()
    for i in range(2,10):
        fit_kmeans = KMeans(n_clusters=i, init='random', n_init = 10, random_state=0).fit(numeric_df)
        score = silhouette_score(numeric_df, fit_kmeans.labels_)
        scores.append(score)
        print("For n_clusters={0}, the silhouette score is {1}".format(i, score))

    For n_clusters=2, the silhouette score is 0.9639191618105983
    For n_clusters=3, the silhouette score is 0.7251022158137325
    For n_clusters=4, the silhouette score is 0.622033082611763
    For n_clusters=5, the silhouette score is 0.5599891737971372
    For n_clusters=6, the silhouette score is 0.5399232027673703
    For n_clusters=7, the silhouette score is 0.5501276800311155
    For n_clusters=8, the silhouette score is 0.4921183525433052
    For n_clusters=9, the silhouette score is 0.46717873003782084
    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    print("{}s".format(time.time()-start_time)) 

    0.3823668956756592s
    from sklearn.cluster import DBSCAN
    from sklearn.neighbors import NearestNeighbors 

    neighbors = NearestNeighbors(n_neighbors=8)
    neighbors_fit = neighbors.fit(numeric_df)
    distances, indices = neighbors_fit.kneighbors(numeric_df)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=0.15, color='black', linestyle='--', linewidth=3)
    plt.show();

    db = DBSCAN(eps=0.15, min_samples=8).fit(numeric_df)
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)

    Average silhouette method로 구한 최적의 k = 2이다.

    k-means를 선택한 이유

    dbscan의 경우 군집의 수를 따로 지정할 수 없음

    군집결과를 해석하여 고객군을 분류하는 것이 목적이므로, 군집의 수가 너무 적거나 많을 경우 고객군을 분류하기가 어려움
    k-means의 경우 군집평가지표를 통해서 적절한 군집의 수를 지정할 수 있음

    군집 결과를 해석하여 고객군을 분류하는데 용이함
    24.1.4 생성된 군집에 대하여 군집성능지표를 산출하고, 군집간 차이와 특성을 분석한 결과를 제시하시오.
    Average silhouette method를 통해 응집도, 분리도 측면에서 최적의 k를 선택하고자 한다. Average silhouette method는 각 
    별 평균 silhouette coefficient를 계산하고, 평균 silhouette coefficient값이 가장 큰 
    를 선택하는 방법이다. 개별 관측치의 silhouette coefficient는 seperation, compactness를 동시에 고려하여 정의된다. k = 2일 때, Average silhouette coefficient = 0.96로 가장 높은 것을 확인할 수 있다.

    print(scores)

    [0.9639191618105983, 0.7251022158137325, 0.622033082611763, 0.5599891737971372, 0.5399232027673703, 0.5501276800311155, 0.4921183525433052, 0.46717873003782084]
    kmeans = KMeans(n_clusters = 2, random_state=0)
    kmeans.fit(numeric_df)

    KMeans(n_clusters=2, random_state=0)
    label = kmeans.labels_
    dat2['cluster'] = label

    dat2['cluster'].value_counts()

    cluster
    0    406
    1      4
    Name: count, dtype: int64
    dat2.boxplot(column = ['new_f'], by = 'cluster')
    plt.show();



    dat2.groupby(['cluster'])['new_f'].describe()

             count         mean          std  ...     50%      75%     max
    cluster                                   ...                         
    0        406.0    81.977833    97.006005  ...    45.0   101.00   638.0
    1          4.0  2468.250000  2210.456420  ...  1740.0  2979.25  5677.0

    [2 rows x 8 columns]
    dat2.boxplot(column = ['new_m'], by = 'cluster')
    plt.show();



    pd.options.display.max_columns = None 
    dat2.groupby(['cluster'])['new_m'].describe()

             count           mean           std        min         25%   
    cluster                                                              
    0        406.0    2291.978473   3507.172999      51.56     459.650  \
    1          4.0  166552.310000  76583.340860  117379.63  122943.805   

                    50%        75%        max  
    cluster                                    
    0          1031.195    2678.38   31906.82  
    1        134311.795  177920.30  280206.02  
    생략
    24.1.5 군집별로 대표적인 추천상품을 구성하고, 군집별 추천 상품을 제시하고, 타군집과의 추천상품 차이를 설명하시오.
    dat = pd.merge(dat, dat2, left_on = ["customerid"], right_on = ["customerid"], how = 'left')

    result = dat.groupby(['cluster', 'stockcategory']).agg(count = ('stockcategory', 'count')).reset_index()
    result

          cluster                     stockcategory  count
    0           0     50'S CHRISTMAS GIFT BAG LARGE     10
    1           0                 DOLLY GIRL BEAKER     25
    2           0       I LOVE LONDON MINI BACKPACK     11
    3           0           NINE DRAWER OFFICE TIDY      4
    4           0        OVAL WALL MIRROR DIAMANTE       1
    ...       ...                               ...    ...
    4790        1  ZINC SWEETHEART WIRE LETTER RACK      2
    4791        1    ZINC T-LIGHT HOLDER STAR LARGE      4
    4792        1   ZINC T-LIGHT HOLDER STARS SMALL      7
    4793        1  ZINC WILLIE WINKIE  CANDLE STICK      7
    4794        1  ZINC WIRE SWEETHEART LETTER TRAY      1

    [4795 rows x 3 columns]
    (result
            .loc[result.cluster == 0, :]
            .sort_values(by = ['count'], ascending=False)
            .iloc[:5, :]
    )

          cluster                        stockcategory  count
    1726        0                              POSTAGE   1055
    1918        0  ROUND SNACK BOXES SET OF4 WOODLAND     270
    1836        0             REGENCY CAKESTAND 3 TIER    218
    1696        0     PLASTERS IN TIN WOODLAND ANIMALS    197
    1691        0       PLASTERS IN TIN CIRCUS PARADE     178
    (result
            .loc[result.cluster == 1, :]
            .sort_values(by = ['count'], ascending=False)
            .iloc[:5, :]
    )

          cluster                       stockcategory  count
    2951        1                            CARRIAGE     97
    4153        1            REGENCY CAKESTAND 3 TIER     76
    4213        1    ROSES REGENCY TEACUP AND SAUCER      51
    4312        1          SET OF 3 REGENCY CAKE TINS     48
    4684        1  WHITE HANGING HEART T-LIGHT HOLDER     42
    각 군집별 가장 많이 구매한 제품 top 5 필터링
    c0 = (result
            .loc[result.cluster == 0, :]
            .sort_values(by = ['count'], ascending=False)
            .iloc[:5, 1]
    )

    c1 = (result
            .loc[result.cluster == 1, :]
            .sort_values(by = ['count'], ascending=False)
            .iloc[:5, 1]
    )

    c_merge = pd.concat([c0, c1],axis=0)

    (dat
        .loc[dat.stockcategory.isin(c_merge)]
        .groupby(['cluster'])
        .agg({'unitprice' : 'mean'})
    )

             unitprice
    cluster           
    0        14.491458
    1        17.362125
    각 군집별 대표상품에 대해 제품 단가를 기준으로 보면 평균적으로 군집 0 < 군집 1인 것을 확인할 수 있음
    24.1.6 KNN을 활용하여 고객별 근접이웃분석을 수행하고 상품추천을 수행하는 방법을 기술하고, 구현하시오.
    고객번호 “12347”에 대한 상품추천 결과를 제시하시오

    KNN을 이용해서 고객별 근접 이웃을 정의

    ex) k = 5일 때, “12347”의 이웃 : “12500” “12627” “12524” “13815” “12378”
    K명의 이웃이 가장 자주 구매한 상품 계산

    “12347” 고객에게 해당 상품을 추천

    (dat2
       .loc[dat2['customerid'] == 12347, ['cluster']]
    )

       cluster
    0        0
    12347번 고객은 0번 군집에 속해있음
    knndat = dat2.loc[dat.cluster == 0, :]
    knndat2 = knndat.loc[:, ['new_f', 'new_m']]

    0번 군집 내에서 이웃을 계산

    이웃을 정의하기 위한 dist matrix를 정의해야 함

    dist matrix를 구하기 위한 feature로 new_f, new_m 을 이용

    from sklearn.neighbors import NearestNeighbors 

    neighbors = NearestNeighbors(n_neighbors=5)
    neighbors_fit = neighbors.fit(knndat2)
    distances, indices = neighbors_fit.kneighbors(knndat2)

    distances.shape

    (174, 5)
    indices.shape

    (174, 5)
    ind = indices.reshape(-1)
    indices2 = knndat.customerid[ind].to_numpy().reshape(-1, 5)
    result2 = pd.DataFrame(indices2, columns = ['k1','k2','k3', 'k4', 'k5'])
    result2.index = knndat.customerid
    result2

                   k1     k2     k3     k4     k5
    customerid                                   
    12347       12347  12500  12524  12449  12484
    12348       12348  12424  12349  12381  12523
    12349       12349  12424  12523  12407  12405
    12350       12350  12489  12519  12527  12532
    12352       12352  12483  12455  12397  12457
    ...           ...    ...    ...    ...    ...
    12562       12562  12502  12429  12553  12417
    12564       12564  12375  12491  12448  12355
    12565       12565  12445  12551  12531  12367
    12566       12566  12527  12532  12519  12538
    12567       12567  12451  12428  12435  12409

    [174 rows x 5 columns]
    dat.loc[dat.customerid.isin(['12500', '12524', '12449', '12484'])]

    Empty DataFrame
    Columns: [invoiceno, stockcode, stockcategory, quantity, invoicedate, unitprice, customerid, country, new_f, new_m, cluster]
    Index: []
    (dat
        .loc[dat.customerid.isin([12500, 12524, 12449, 12484])]
        .groupby(['stockcategory'])
        .agg(count = ('stockcategory', 'count'))
        .sort_values(by = ['count'], ascending=False)
        .reset_index()
    )

                               stockcategory  count
    0                                POSTAGE     25
    1                    SPACEBOY LUNCH BOX       6
    2    ROUND SNACK BOXES SET OF4 WOODLAND       5
    3                LUNCH BAG RED RETROSPOT      5
    4                     LUNCH BAG WOODLAND      5
    ..                                   ...    ...
    484          GREETING CARD, TWO SISTERS.      1
    485         GREETING CARD, STICKY GORDON      1
    486                GRAND CHOCOLATECANDLE      1
    487      GLASS JAR ENGLISH CONFECTIONERY      1
    488      ZINC T-LIGHT HOLDER STARS SMALL      1

    [489 rows x 2 columns]
    “12347”의 이웃들이 가장 자주 구매한 상품 top5를 추천

    POSTAGE, SPACEBOY LUNCH BOX, ROUND SNACK BOXES SET OF4 WOODLAND, LUNCH BAG RED RETROSPOT, LUNCH BAG WOODLAND

    24.2 통계분석
    24.2.1 은 가격과 이동평균(N=3)의 가격을 하나의 시계열 그래프로 작성하시오.
    dat = pd.DataFrame({'x' : [22.9, 23.4, 21.1, 25.7, 27.4, 30.6, 31.8, 30.2, 41.1]})
    roll_result = dat['x'].rolling(3).mean()
    roll_result.plot()
    plt.show();



    24.2.2 1 월 대비 9 월의 은 가격이 몇 % 올랐는지 계산 (반올림 소수 2 자리).
    (구하고 싶은 월 수치-비교하고 싶은 월 수치)/비교하고 싶은 월 수치 x 100

    print(np.round(((dat.x[8] - dat.x[0])/dat.x[0])*100, 2), '%')
    """
