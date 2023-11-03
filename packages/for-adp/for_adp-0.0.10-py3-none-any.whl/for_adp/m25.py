def m25():
     """
    ADP python 기출문제
    23  25회차 기출문제
    23  25회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    23.1 머신러닝
    RFM(Recency, Frequency, Momentary) 모델을 이용하여 고객 세분화를 하는 문제입니다.

    23.1.1 Data description
    invoice_no : 송장번호

    stock code : 재고 코드

    description : 설명

    quantity : 수량

    invoice date : 송장 일자

    unit price : 단가

    customer id : 고객 id

    import pandas as pd 
    import numpy as np 
    #import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from sklearn.preprocessing import StandardScaler

    dat = pd.read_csv("data/retail2.csv")

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 39087 entries, 0 to 39086
    Data columns (total 7 columns):
     #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
     0   invoice_no    39087 non-null  object 
     1   stock_code    39087 non-null  object 
     2   description   39087 non-null  object 
     3   quantity      39087 non-null  int64  
     4   invoice_date  39087 non-null  object 
     5   unit_price    39087 non-null  float64
     6   customer_id   38146 non-null  float64
    dtypes: float64(2), int64(1), object(4)
    memory usage: 2.1+ MB
    dat = dat.astype({'customer_id' : 'object'})

    23.1.2 F(고객별 거래빈도), M(고객별 총 구매액) 파생변수 생성 및 EDA를 실시하시오.
    dat.describe()

               quantity    unit_price
    count  39087.000000  39087.000000
    mean      19.701538      4.764918
    std       45.018238     49.199668
    min     -480.000000      0.000000
    25%        4.000000      1.250000
    50%       10.000000      1.950000
    75%       16.000000      3.750000
    max     2400.000000   4161.060000
    dat.isna().sum()

    invoice_no        0
    stock_code        0
    description       0
    quantity          0
    invoice_date      0
    unit_price        0
    customer_id     941
    dtype: int64
    dat.select_dtypes(['int', 'float']).hist();
    plt.show()



    고객 id가 결측치이므로, 어떤 고객이 거래를 했는지 특정할 수 없음

    고객 id가 결측치가 아닌 고객의 정보 중 일부가 결측치 처리되었을 수도 있고, 혹은 새로운 고객의 정보가 결측치 처리되었을 수도 있음

    알 수 없으므로, 확인 후 제거

    dat = dat.dropna(axis = 0)
    dat.isna().sum()

    invoice_no      0
    stock_code      0
    description     0
    quantity        0
    invoice_date    0
    unit_price      0
    customer_id     0
    dtype: int64
    #dat.shape

    수량과 단가는 0 미만이 나올 수 없으므로, 결측치로 판단함

    수량이 0 미만인 경우, 단가가 0 미만인 경우 제거

    dat = dat[(dat['quantity'] >= 0) & (dat['unit_price'] >= 0)]

    F(고객별 거래빈도) : 각 고객별로 거래를 얼마나 했는지

    #new_f = dat.groupby(['customer_id'])['customer_id'].agg('count')

    new_f = dat.groupby(['customer_id']).agg(new_f = ('customer_id', 'count')).reset_index()
    new_f

         customer_id  new_f
    0        12350.0     17
    1        12352.0     85
    2        12354.0     58
    3        12356.0     59
    4        12357.0    131
    ..           ...    ...
    299      14335.0     63
    300      14646.0   2080
    301      14911.0   5677
    302      16321.0     12
    303      17097.0    211

    [304 rows x 2 columns]
    M(고객별 총 구매액) : 각 고객별로 구매한 총 구매액

    총 구매액은 총구매액단가수량
    으로 구할 수 있음
    new_m = dat.assign(t_price = lambda x: x.unit_price*x.quantity).groupby(['customer_id']).agg(new_m = ('t_price', 'sum')).reset_index()

    new_m

         customer_id      new_m
    0        12350.0     334.40
    1        12352.0    2506.04
    2        12354.0    1079.40
    3        12356.0    2811.43
    4        12357.0    6207.67
    ..           ...        ...
    299      14335.0     468.26
    300      14646.0  280206.02
    301      14911.0  143825.06
    302      16321.0     373.65
    303      17097.0     954.42

    [304 rows x 2 columns]
    dat = pd.merge(dat, new_f, left_on = 'customer_id', right_on = 'customer_id', how = 'left')

    dat = pd.merge(dat, new_m, left_on = 'customer_id', right_on = 'customer_id', how = 'left')

    dat.head()

      invoice_no stock_code  ... new_f    new_m
    0     536370      22728  ...   247  7281.38
    1     536370      22727  ...   247  7281.38
    2     536370      22726  ...   247  7281.38
    3     536370      21724  ...   247  7281.38
    4     536370      21883  ...   247  7281.38

    [5 rows x 9 columns]
    corr = dat.select_dtypes(['float', 'int']).corr()
    sns.heatmap(corr, annot = True);
    plt.show();



    23.1.3 이상치를 탐색하고, 적절하게 처리하시오.
    dat.select_dtypes(['float', 'int']).hist()

    array([[<Axes: title={'center': 'quantity'}>,
            <Axes: title={'center': 'unit_price'}>],
           [<Axes: title={'center': 'new_f'}>,
            <Axes: title={'center': 'new_m'}>]], dtype=object)
    plt.show();



    quantity를 기준으로 상자그림의 울타리 밖의 이상치를 탐색하고자 함

    dat.select_dtypes(['float', 'int']).plot(
        kind='box', 
        subplots=True, 
        sharey=False, 
        figsize=(10, 6)
    )

    quantity         Axes(0.125,0.11;0.168478x0.77)
    unit_price    Axes(0.327174,0.11;0.168478x0.77)
    new_f         Axes(0.529348,0.11;0.168478x0.77)
    new_m         Axes(0.731522,0.11;0.168478x0.77)
    dtype: object
    plt.subplots_adjust(wspace=0.7) 
    plt.show()




    #num_columns = dat.select_dtypes(['float', 'int']).columns
    # long_df = pd.melt(dat,
    #         value_vars = num_columns, 
    #         var_name = 'num_variable', 
    #         value_name = 'value', 
    #         ignore_index = False)
    # 
    # sns.catplot(data=long_df, 
    #             y='value', 
    #             col='num_variable', col_wrap=2, 
    #             kind='box', sharey=False)
    # plt.show()

    # 1분위수 계산
    Q1 = np.quantile(dat['quantity'], 0.25)
    # 3분위수 계산
    Q3 = np.quantile(dat['quantity'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) # 위 울타리
    LC = Q3 - (1.5 * IQR) # 위 울타리


    dat.loc[(dat.quantity > UC), "quantity"].describe()

    count    3865.000000
    mean      109.979301
    std       102.628544
    min        40.000000
    25%        48.000000
    50%        96.000000
    75%       128.000000
    max      2400.000000
    Name: quantity, dtype: float64
    dat.loc[(dat.quantity > UC), "quantity"].hist()
    plt.show()



    dat.select_dtypes(['float', 'int']).loc[(dat.quantity > UC), :].plot(
        kind='box', 
        subplots=True, 
        sharey=False, 
        figsize=(10, 6)
    )

    quantity         Axes(0.125,0.11;0.168478x0.77)
    unit_price    Axes(0.327174,0.11;0.168478x0.77)
    new_f         Axes(0.529348,0.11;0.168478x0.77)
    new_m         Axes(0.731522,0.11;0.168478x0.77)
    dtype: object
    plt.subplots_adjust(wspace=0.7) 
    plt.show()



    F : 각 고객별로 거래를 얼마나 했는지

    M : 각 고객별로 구매한 총 구매액

    F와 M의 관계에 따른 이상치를 탐색해보면 다음과 같음

    총 거래 횟수는 많지만 총 구매액은 많지 않음 : 소액 결제를 여러번 한 고객(충성 고객)

    총 거래횟수는 적지만 총 구매액은 매우 많음 : 고액 결제를 한번에 하는 고객(우량 고객)

    두 고객 모두 중요한 고객이므로 이상치로 제거하지 않음

    23.1.4 군집분석 실시 및 최적 모델 탐색, 군집 결과의 적합성을 응집성, 분리도 측면에서 설명하시오.
    Average silhouette method를 통해 응집도, 분리도 측면에서 모델을 비교하고자 한다. Average silhouette method는 각 
    별 평균 silhouette coefficient를 계산하고, 평균 silhouette coefficient값이 가장 큰 
    를 선택하는 방법이다. 개별 관측치의 silhouette coefficient는 seperation, compactness를 동시에 고려하여 정의된다.

    from sklearn.preprocessing import StandardScaler

    numeric_data = dat.select_dtypes('number')
    stdscaler = StandardScaler()
    numeric_df = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)
    numeric_df.head(2)

       quantity  unit_price     new_f     new_m
    0  0.068914   -0.008202 -0.489686 -0.528276
    1  0.068914   -0.008202 -0.489686 -0.528276
    K-MEANS

    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    scores = []
    start_time = time.time()
    for i in range(2,10):
        fit_kmeans = KMeans(n_clusters=i, init='random', n_init = 10, random_state=0).fit(numeric_df)
        score = silhouette_score(numeric_df, fit_kmeans.labels_)
        scores.append(score)
        print("For n_clusters={0}, the silhouette score is {1}".format(i, score))

    For n_clusters=2, the silhouette score is 0.7595114276450207
    For n_clusters=3, the silhouette score is 0.795750259995016
    For n_clusters=4, the silhouette score is 0.7964197291222544
    For n_clusters=5, the silhouette score is 0.8153426867663607
    For n_clusters=6, the silhouette score is 0.7845815075839802
    For n_clusters=7, the silhouette score is 0.7770936798362289
    For n_clusters=8, the silhouette score is 0.7496698744678254
    For n_clusters=9, the silhouette score is 0.5660242217163186
    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    print("{}s".format(time.time()-start_time)) # 84.5147180557251s

    79.37774467468262s
    print(scores)

    [0.7595114276450207, 0.795750259995016, 0.7964197291222544, 0.8153426867663607, 0.7845815075839802, 0.7770936798362289, 0.7496698744678254, 0.5660242217163186]
    일 때, average silhouette coefficient는 
    이다.

    hierarchical clustering

    from sklearn.cluster import AgglomerativeClustering

    scores = []

    start_time = time.time()
    for i in range(2,10):
        fit_hk = AgglomerativeClustering(n_clusters=i, linkage = 'ward').fit(numeric_df)
        score = silhouette_score(numeric_df, fit_hk.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    print("{}s".format(time.time()-start_time)) # 278.5629301071167s

    231.60777592658997s
    scores

    [0.7619422934621358, 0.763467057930147, 0.797749239479647, 0.809840324581582, 0.8115200162710757, 0.8127135412401228, 0.7912695667774956, 0.7826086202846356]
    일 때, average silhouette coefficient는 
    이다.

    average silhouette coefficient를 기준으로 최적의 군집 알고리즘은 k-means이며, 군집 개수가 4일 때이다.

    23.1.5 군집분석 결과를 바탕으로 군집별 특성 및 비즈니스적인 의견을 제시하시오.
    kmeans = KMeans(n_clusters = 4, random_state=0)
    kmeans.fit(numeric_df)

    KMeans(n_clusters=4, random_state=0)
    label = kmeans.labels_
    dat['cluster'] = label
    dat.head(2)

      invoice_no stock_code                description  ...  new_f    new_m  cluster
    0     536370      22728  ALARM CLOCK BAKELIKE PINK  ...    247  7281.38        0
    1     536370      22727   ALARM CLOCK BAKELIKE RED  ...    247  7281.38        0

    [2 rows x 10 columns]
    dat.cluster.value_counts()

    cluster
    0    28624
    1     6227
    3     2209
    2        2
    Name: count, dtype: int64
    dat.boxplot(column = ['quantity'], by = 'cluster')
    plt.show();



    dat.groupby(['cluster'])['quantity'].describe()

               count        mean         std   min   25%    50%    75%     max
    cluster                                                                   
    0        28624.0   13.076649   14.708244   1.0   5.0   10.0   12.0   144.0
    1         6227.0   12.550185   12.689622   1.0   4.0   12.0   12.0   108.0
    2            2.0    1.000000    0.000000   1.0   1.0    1.0    1.0     1.0
    3         2209.0  145.169307  123.021959  48.0  96.0  100.0  192.0  2400.0
    구매량이 가장 많은 군집은 평균적으로 
     순서이며, 
    번 군집의 경우 이상치가 존재함
    dat.boxplot(column = ['unit_price'], by = 'cluster')
    plt.show();



    dat.groupby(['cluster'])['unit_price'].describe()

               count         mean        std  ...      50%      75%      max
    cluster                                   ...                           
    0        28624.0     3.817360  16.809854  ...     1.95     3.75  1241.98
    1         6227.0     4.679313  30.969086  ...     2.10     4.95  1687.17
    2            2.0  4161.060000   0.000000  ...  4161.06  4161.06  4161.06
    3         2209.0     1.479108   1.140459  ...     1.45     1.79    12.75

    [4 rows x 8 columns]
    구매단가 기준으로 가장 많은 군집은 평균적으로 
     순서이며, 
    번 군집의 경우 이상치가 존재함
    dat = dat.assign(t_price = dat.unit_price*dat.quantity)

    dat.boxplot(column = ['t_price'], by = 'cluster')
    plt.show();



    dat.groupby(['cluster'])['t_price'].describe()

               count         mean         std  ...      50%      75%      max
    cluster                                    ...                           
    0        28624.0    26.311627   39.149721  ...    17.00    24.96  1241.98
    1         6227.0    27.229513   43.918883  ...    17.34    25.50  1687.17
    2            2.0  4161.060000    0.000000  ...  4161.06  4161.06  4161.06
    3         2209.0   192.486713  217.494050  ...   140.40   232.00  4992.00

    [4 rows x 8 columns]
    수익이 가장 많은 군집은 평균적으로 
     순이며, 각 군집별로 이상치가 존재함
    비즈니스적인 의견

    번 군집의 경우 구매 수량은 매우 적지만, 총 구매액이 매우 큰 고객이 존재함(VVIP고객)

    VVIP 고객만을 위한 프라이빗한 프로모션 제공 필요
    번 군집의 경우 총 구매량은 많고, 구매단가는 적으며, 총 구매액은 많은 충성고객임

    충성 고객이므로, 충성도를 더욱더 높이기 위해 많이 구매한 고객에 한해서 한정 기간 사용할 수 있는 쿠폰 제공
    번 군집의 경우 구매 수량은 적고, 구매 단가도 적으며, 총 구매액도 낮은 편에 속함

    이탈할 확률이 매우 높은 고객이므로, 경쟁사 대비 더 높은 프로모션 혜택 제공
    번 군집의 경우 구매 수량이 많은 고객이 존재하며, 구매 단가는 적고, 총 구매액이 매우 큰 고객이 존재함(VIP고객)

    대량 구매를 하는 고객이므로, 경쟁사와 비교하여 대량 구매시 할인 프로모션 제공
    23.2 시계열분석
    시계열분석 자료에 있는 SARIMA 데이터와 같습니다.

    우리나라에 입국한 관광객 수
    train : 1981.1 ~ 1991.12
    test : 1992.1 ~ 1992.12
    tour = pd.read_csv('./data/ex_data/timeseries/tour.csv')
    dat = tour.rename(columns = {'index' : 'date'})
    dat['date'] = pd.to_datetime(dat['date'], format = '%Y %b')

    import datetime
    dat['date'] = dat['date'].dt.strftime('%Y-%m')
    dat.index = dat['date']
    dat = dat.drop(['date'], axis = 1)

    23.2.1 데이터를 탐색하시오
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf, pacf

    dat.plot()
    plt.show();



    결측치가 존재할 경우 missing = 'drop'로 설정 필요
    plot_acf(dat.value, missing = 'drop')
    plt.show();



    분산 증가, 로그 변환 필요

    결측치가 존재함

    추세가 존재함

    계절성이 존재함

    23.2.2 결측치 확인 및 결측치를 대치하시오
    TEST_SIZE = 12
    train, test = dat.iloc[:-TEST_SIZE], dat.iloc[-TEST_SIZE:]
    train.shape, test.shape

    ((132, 1), (12, 1))
    train.plot()
    plt.show();



    1981년 말부터 1982년 초 사이에 결측치가 존재함
    선형 외삽

    train2 = train.copy()
    train2 = train2.assign(locf=train2.value.fillna(method = 'ffill'))
    train2['linear'] = train2.value.interpolate(method='linear')
    train2[train2.value.isna()]

             value     locf   linear
    date                            
    1981-10    NaN  95866.0  91009.0
    1981-11    NaN  95866.0  86152.0
    1981-12    NaN  95866.0  81295.0
    1982-01    NaN  95866.0  76438.0
    train['value'] = train.value.interpolate(method='linear')

    시계열 결측치 대치 방법은 크게 LOCF(Last Observation Carried Forward)과 선형 외삽 방법이 있음

    선형 외삽은 결측치 주변 실제값 사이의 관계를 이용하므로 시계열의 경향성을 반영하여 결측치 대치 가능

    결과를 보면 직전 시점 관측치로 결측치를 대치하는 LOCF에 비해 선형 외삽를 이용한 방법이 시계열의 경향성을 반영하여 결측치를 대치해주는 것을 확인할 수 있음

    23.2.3 계절성을 포함하는 시계열 모델을 구축하고 정확도 측면에서 제시하시오
    시간에 따라 분산이 늘어나는 경향이 있으므로, 분산 안정화 변환을 실시함
    from scipy import stats
    lambda_result = stats.boxcox(train['value'])
    print(lambda_result[1])

    -0.2108815164230156
    boxcox 변환을 위한 람다 값은 -0.21이므로, 0에 가깝기 때문에 log 변환을 실시함
    train['value'] = np.log(train['value'])
    test['value'] = np.log(test['value'])

    train.plot()
    plt.show();



    log 변환 결과, 시간에 따라 분산이 일정하게 안정화된 것을 볼 수 있음
    d = 1일 때 (일반 차분)

    추세와 계절성이 함께 존재하므로, 일반차분과 계절차분을 고려해볼 수 있음
    from statsmodels.tsa.stattools import kpss

    print('test statistic: %f' % kpss(train)[0])

    test statistic: 1.933121
    print('p-value: %f' % kpss(train)[1])

    p-value: 0.010000
    kpss test 결과 유의수준 0.05에서 p-value = 0.01 로 작기 때문에 귀무가설을 기각, 해당 데이터는 정상성을 만족하지 않으며, 차분 필요
    from pmdarima.arima.utils import nsdiffs

    #cht = pm.arima.CHTest(m=12)
    #cht.estimate_seasonal_differencing_term(trans_dat)
    nsdiffs(train,
                m=12, 
                max_D=12,
                test='ch')

    0
    계절성 존재 여부 확인 : Canova-Hansen test 결과를 바탕으로 추천된 계절 차분 차수는 0인 것을 확인할 수 있음

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train['value'], ax = ax1)
    plot_pacf(train['value'], ax = ax2, method = 'ywm')
    plt.show();



    d=1의 경우

    추세 그래프를 보았을 때, 12를 주기로 일정한 패턴의 진폭을 보이는 것을 확인할 수 있으며, acf plot을 보면 추세는 제거되었지만 12를 주기로 acf 값이 커지는 것을 볼 수 있음

    따라서 추가적으로 계절 차분을 고려해볼 수 있음

    train_diff = train.diff()
    train_diff.plot()
    plt.show();



    train_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train_diff['value'], ax = ax1)
    plot_pacf(train_diff['value'], ax = ax2, method = 'ywm')
    plt.show();



    print('test statistic: %f' % kpss(train_diff)[0])

    test statistic: 0.013907
    print('p-value: %f' % kpss(train_diff)[1])

    p-value: 0.100000
    kpss test 결과 유의수준 0.05에서 p-value = 0.1로 크기 때문에 귀무가설을 기각할 수 없음, 해당 데이터는 정상성 만족

    kpss test 결과 추세는 제거된 것을 확인할 수 있음

    kpss test는 계절성은 반영 x
    D=1의 경우

    추세는 계절 차분만으로도 해결되는 경우가 있음

    계절 차분 결과, 추세 그래프와 acf plot을 확인해보면 추세가 존재하고, acf가 천천히 감소하는 것을 확인할 수 있음

    추가적인 일반 차분을 고려함

    train_diff2 = train.diff(12)
    train_diff2.dropna(inplace = True)
    train_diff2.plot();
    plt.show();



    fig, ax1 = plt.subplots(1, 1, figsize=(16,6))
    plot_acf(train_diff2['value'], ax = ax1)
    plt.show();



    d=1, D=1의 경우

    정상성 확보

    최적의 차분 : d = 1, D = 1

    train_diff3 = train_diff.diff(12)
    train_diff3.plot()
    plt.show();



    Model fitting

    train_diff3.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train_diff3['value'], ax = ax1, lags = 40)
    plot_pacf(train_diff3['value'], ax = ax2, method = 'ywm', lags = 40)
    plt.show();



    계절형 확인

    ACF 12차 근처에서만 유의적 : P = 0, Q = 1
    비계절형 확인

    ACF 절단, PACF 감소 : p = 0, q = 1
    후보 모형

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(train, order=(0,1,1), seasonal_order=(0, 1, 1, 12)).fit()
    print(model.summary())

                                        SARIMAX Results                                     
    ========================================================================================
    Dep. Variable:                            value   No. Observations:                  132
    Model:             ARIMA(0, 1, 1)x(0, 1, 1, 12)   Log Likelihood                 162.049
    Date:                          Mon, 30 Oct 2023   AIC                           -318.098
    Time:                                  01:37:41   BIC                           -309.761
    Sample:                              01-01-1981   HQIC                          -314.712
                                       - 12-01-1991                                         
    Covariance Type:                            opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ma.L1         -0.6035      0.080     -7.591      0.000      -0.759      -0.448
    ma.S.L12      -0.5751      0.102     -5.656      0.000      -0.774      -0.376
    sigma2         0.0037      0.000      9.809      0.000       0.003       0.004
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.12   Jarque-Bera (JB):                25.79
    Prob(Q):                              0.73   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.80   Skew:                             0.70
    Prob(H) (two-sided):                  0.49   Kurtosis:                         4.80
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    model.plot_diagnostics()
    plt.show();



    sm.stats.acorr_ljungbox(model.resid, lags=[24])

          lb_stat  lb_pvalue
    24  23.944809   0.464757
    신뢰구간을 확인해본 결과, ma1, sma1 모두 신뢰구간에 0을 포함하지 않으므로 유의함

     : 
     ~ 
     시차 시까지 잔차 사이에 자기상관이 없다.

    ljung box test 결과 유의수준 0.05에서 Q* = 30.56, p-value = 0.46로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 24시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.

    잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.

    잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.

     잠정 모형으로 선택

    auto.arima 이용

    import pmdarima as pm

    model2 = pm.auto_arima(train, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=12,             
                       d=1,          
                       seasonal=True,   
                       start_P=0, 
                       D=1, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,1,0)(0,1,1)[12]             : AIC=-282.638, Time=0.11 sec
     ARIMA(0,1,0)(0,1,0)[12]             : AIC=-250.935, Time=0.02 sec
     ARIMA(1,1,0)(1,1,0)[12]             : AIC=-302.540, Time=0.17 sec
     ARIMA(0,1,1)(0,1,1)[12]             : AIC=-318.098, Time=0.17 sec
     ARIMA(0,1,1)(0,1,0)[12]             : AIC=-290.045, Time=0.04 sec
     ARIMA(0,1,1)(1,1,1)[12]             : AIC=-317.982, Time=0.19 sec
     ARIMA(0,1,1)(0,1,2)[12]             : AIC=-317.830, Time=1.23 sec
     ARIMA(0,1,1)(1,1,0)[12]             : AIC=-317.285, Time=0.08 sec
     ARIMA(0,1,1)(1,1,2)[12]             : AIC=-317.157, Time=1.52 sec
     ARIMA(1,1,1)(0,1,1)[12]             : AIC=-316.294, Time=0.25 sec
     ARIMA(0,1,2)(0,1,1)[12]             : AIC=-316.403, Time=0.22 sec
     ARIMA(1,1,0)(0,1,1)[12]             : AIC=-305.334, Time=0.14 sec
     ARIMA(1,1,2)(0,1,1)[12]             : AIC=-314.607, Time=0.40 sec
     ARIMA(0,1,1)(0,1,1)[12] intercept   : AIC=-316.416, Time=0.20 sec

    Best model:  ARIMA(0,1,1)(0,1,1)[12]          
    Total fit time: 4.735 seconds
    를 최종 모형으로 선택
    실제값과 예측값 비교

    prediction, confint = model2.predict(n_periods=TEST_SIZE, return_conf_int=True)

    prediction = np.exp(prediction)
    confint = np.exp(confint)

    train['value'] = np.exp(train['value'])
    test['value'] = np.exp(test['value'])
    full_dat = pd.concat([train, test], axis = 0)

    cf = pd.DataFrame(confint)
    prediction_series = pd.Series(prediction,index=test.index)
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    ax.plot(full_dat.value)
    ax.plot(prediction_series)
    ax.fill_between(prediction_series.index,
                    cf[0],
                    cf[1],color='grey',alpha=.3)
    plt.show();



    예측 성능 확인

    def MASE(training_series, testing_series, prediction_series):

        n = training_series.shape[0]
        d = np.abs(  np.diff( training_series) ).sum()/(n-1)

        errors = np.abs(testing_series - prediction_series )
        return errors.mean()/d

    MASE(train['value'].to_numpy(), test['value'].to_numpy(), prediction.to_numpy())

    3.0536922197264906
    23.2.4 업무에 적용할 수 있는지, 판단근거와 함께 서술하시오
    예측 성능을 비교하기 위해 MASE를 고려함

    MASE는 RMSE, MAE와 달리 scale에 의존하지 않기 때문에, 값의 비교가 용이함

    MASE가 1보다 크다는 의미는 학습 데이터에서의 naive forecast(ex.) 
    , 
    )보다 모형에서의 오차가 더 크다고 볼 수 있음

    MASE를 기준으로 보면 test 데이터를 기준으로 
    로 
    보다 큼

    즉, 일반화 불가능

    따라서 해당 모형을 이용하는 것은 적절하지 않고, 대안 모형을 활용해야 함

    LSTM, prophet 등 다른 시계열 모형을 대안으로 고려
    """
    