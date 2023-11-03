def m10():
    """
    10  Homework1 solution
    데이터 출처 : https://www.kaggle.com/competitions/bike-sharing-demand/data

    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import time
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime

    from sklearn.preprocessing import KBinsDiscretizer
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn import set_config
    set_config(display="diagram")

    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import BaggingRegressor

    EDA에 이용했던 데이터를 다시 불러오겠습니다.

    dat = pd.read_csv('./data/ex_data/bikesharingdata/train2.csv')

    y = dat['count']
    X = dat.drop(['count'], axis = 1)

    10.1 1. 시각화 및 탐색적 자료분석을 수행하시오.
    10.1.1 변수 속성 확인
    dat.head()

                  datetime  season  holiday  ...  casual  registered  count
    0  2011-01-01 00:00:00       1        0  ...       3          13     16
    1  2011-01-01 01:00:00       1        0  ...       8          32     40
    2  2011-01-01 02:00:00       1        0  ...       5          27     32
    3  2011-01-01 03:00:00       1        0  ...       3          10     13
    4  2011-01-01 04:00:00       1        0  ...       0           1      1

    [5 rows x 12 columns]
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10886 entries, 0 to 10885
    Data columns (total 12 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   datetime    10886 non-null  object 
     1   season      10886 non-null  int64  
     2   holiday     10886 non-null  int64  
     3   workingday  10886 non-null  int64  
     4   weather     10886 non-null  int64  
     5   temp        10886 non-null  float64
     6   atemp       10886 non-null  float64
     7   humidity    10779 non-null  float64
     8   windspeed   10886 non-null  float64
     9   casual      10886 non-null  int64  
     10  registered  10886 non-null  int64  
     11  count       10886 non-null  int64  
    dtypes: float64(4), int64(7), object(1)
    memory usage: 1020.7+ KB
    10.1.2 결측치 확인
    dat.isna().sum()

    datetime        0
    season          0
    holiday         0
    workingday      0
    weather         0
    temp            0
    atemp           0
    humidity      107
    windspeed       0
    casual          0
    registered      0
    count           0
    dtype: int64
    humidity에 결측치 존재, 결측치 대치 필요
    10.1.3 변수 속성 변경
    dat = dat.astype({'datetime' : 'datetime64[ns]', 'weather' : 'int64', 'season' : 'object', 'workingday' : 'object', 'holiday' : 'object'})

    # pd.to_datetime(dat['datetime'])

    10.1.4 날짜 변수 생성
    dat['year'] = dat['datetime'].dt.year
    dat['month'] = dat['datetime'].dt.month
    dat['day'] = dat['datetime'].dt.day
    dat['wday'] = dat['datetime'].dt.day_name()
    dat['hour'] = dat['datetime'].dt.hour

    dat = dat.drop(['datetime'], axis = 1)
    #dat.info()

    pd.options.display.max_columns = None # full 출력 옵션 
    dat.describe(include = 'all')

             season  holiday  workingday       weather         temp         atemp   
    count   10886.0  10886.0     10886.0  10886.000000  10886.00000  10886.000000  \
    unique      4.0      2.0         2.0           NaN          NaN           NaN   
    top         4.0      0.0         1.0           NaN          NaN           NaN   
    freq     2734.0  10575.0      7412.0           NaN          NaN           NaN   
    mean        NaN      NaN         NaN      1.418427     20.23086     23.655084   
    std         NaN      NaN         NaN      0.633839      7.79159      8.474601   
    min         NaN      NaN         NaN      1.000000      0.82000      0.760000   
    25%         NaN      NaN         NaN      1.000000     13.94000     16.665000   
    50%         NaN      NaN         NaN      1.000000     20.50000     24.240000   
    75%         NaN      NaN         NaN      2.000000     26.24000     31.060000   
    max         NaN      NaN         NaN      4.000000     41.00000     45.455000   

                humidity     windspeed        casual    registered         count   
    count   10779.000000  10886.000000  10886.000000  10886.000000  10886.000000  \
    unique           NaN           NaN           NaN           NaN           NaN   
    top              NaN           NaN           NaN           NaN           NaN   
    freq             NaN           NaN           NaN           NaN           NaN   
    mean       61.795992     12.799395     36.021955    155.552177    191.574132   
    std        19.318786      8.164537     49.960477    151.039033    181.144454   
    min         0.000000      0.000000      0.000000      0.000000      1.000000   
    25%        47.000000      7.001500      4.000000     36.000000     42.000000   
    50%        61.000000     12.998000     17.000000    118.000000    145.000000   
    75%        78.000000     16.997900     49.000000    222.000000    284.000000   
    max       100.000000     56.996900    367.000000    886.000000    977.000000   

                    year         month           day      wday          hour  
    count   10886.000000  10886.000000  10886.000000     10886  10886.000000  
    unique           NaN           NaN           NaN         7           NaN  
    top              NaN           NaN           NaN  Saturday           NaN  
    freq             NaN           NaN           NaN      1584           NaN  
    mean     2011.501929      6.521495      9.992559       NaN     11.541613  
    std         0.500019      3.444373      5.476608       NaN      6.915838  
    min      2011.000000      1.000000      1.000000       NaN      0.000000  
    25%      2011.000000      4.000000      5.000000       NaN      6.000000  
    50%      2012.000000      7.000000     10.000000       NaN     12.000000  
    75%      2012.000000     10.000000     15.000000       NaN     18.000000  
    max      2012.000000     12.000000     19.000000       NaN     23.000000  
    10.2 일변량 데이터 시각화
    dat.select_dtypes('number').hist()

    array([[<Axes: title={'center': 'weather'}>,
            <Axes: title={'center': 'temp'}>,
            <Axes: title={'center': 'atemp'}>],
           [<Axes: title={'center': 'humidity'}>,
            <Axes: title={'center': 'windspeed'}>,
            <Axes: title={'center': 'casual'}>],
           [<Axes: title={'center': 'registered'}>,
            <Axes: title={'center': 'count'}>,
            <Axes: title={'center': 'year'}>],
           [<Axes: title={'center': 'month'}>,
            <Axes: title={'center': 'day'}>,
            <Axes: title={'center': 'hour'}>]], dtype=object)
    plt.show()



    plt.clf()

    dat.select_dtypes('object').columns

    Index(['season', 'holiday', 'workingday', 'wday'], dtype='object')
    f, axes = plt.subplots(ncols = 2, nrows = 2, figsize = (20,4))
    sns.countplot(dat['season'], ax = axes[0, 0])
    sns.countplot(dat['holiday'], ax = axes[0, 1])
    sns.countplot(dat['workingday'], ax = axes[1, 0])
    sns.countplot(dat['weather'], ax = axes[1, 1])
    #sns.countplot(dat['wday'], ax = axes[1, 1])
    plt.show()



    plt.clf()

    우측으로 긴 꼬리를 갖는 분포이고, count 횟수가 0인 케이스가 많은 것을 볼 수 있음

    섭씨 온도와 체감온도의 분포는 거의 동일한 것을 볼 수 있음

    체감온도는 섭씨온도에서 풍속을 반영해서 계산하므로, 섭씨 온도 변수와 풍속 변수 제거를 고려해볼 수 있음

    count, registered, causal의 분포를 보면 0의 비율이 매우 많은 우측으로 긴꼬리를 갖는 분포이고, 과대산포(평균에 비해 분산이 매우 큰 경우)되어있는 것을 볼 수 있음

    weather의 경우 4인 케이스의 빈도가 매우 적은 것을 확인할 수 있음

    holiday의 경우 휴일인 케이스는 매우 적은 것을 확인할 수 있음

    10.3 이변량 변수 시각화
    10.3.1 계절(season)에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['season', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour',y='count',hue='season', data = group_dat)
    plt.show()



    plt.clf()

    season(계절 (1 = spring, 2 = summer, 3 = fall, 4 = winter))의 경우 description이 잘못 기입되어 있음

    대체로 봄과 여름에 수요가 가장 많고, 겨울에 수요가 가장 적음

    시간대는 출퇴근 시간대에 수요가 가장 많음

    10.3.2 날씨(weather)에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['weather', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour', y='count', hue='weather', data = group_dat)
    plt.show()



    plt.clf()

    날씨가 좋을 때 rental 횟수가 가장 많고, 날씨가 안좋을 때 rental 횟수가 가장 적음

    시간대는 출퇴근 시간대에 수요가 가장 많음

    10.3.2.1 요일(wday)에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['wday', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour', y='count', hue='wday', data = group_dat)
    plt.show()



    plt.clf()

    주중의 경우 출퇴근 시간대에 수요가 가장 많음

    주말의 경우 
    시 여가 시간대에 수요가 가장 많음

    주중과 주말의 수요 차이가 뚜렷하므로, 주중 or 주말을 구분하는 이진변수 생성 고려

    10.3.2.2 휴일 유무(holiday)에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['holiday', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour', y='count', hue='holiday', data = group_dat)
    plt.show()



    plt.clf()

    공휴일의 경우 날짜가 적으므로 수요의 크기를 비교하는 것은 적절하지 않음

    공휴일이 아닐 경우 workingday 변수와 동일하며, 공휴일의 경우 시간대로 보면 
     까지 상대적으로 수요가 있음

    10.3.2.3 workingday에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['workingday', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour', y='count', hue='workingday', data = group_dat)
    plt.show()



    plt.clf()

    주말과 공휴일의 경우 
    시에 수요가 높음

    주중의 경우 출퇴근 시간대에 수요가 높음

    10.3.2.4 month에 따른 시간 vs count 그래프
    group_dat = dat.groupby(['month', 'hour']).agg({'count' : 'sum'}).reset_index()
    sns.pointplot(x='hour', y='count', hue='month', data = group_dat)
    plt.show()



    plt.clf()

    겨울의 경우 수요가 가장 적고, 봄, 여름, 가을의 경우 상대적으로 수요가 높음
    10.3.2.5 hour에 따른 registered vs casual 그래프
    dat.groupby('hour').boxplot(column = ['registered'], subplots = False)
    plt.show()



    plt.clf()

    dat.groupby('hour').boxplot(column = ['casual'], subplots = False)
    plt.show()



    plt.clf()

    수요의 패턴은 boxplot으로 시각화해볼 수도 있음

    실제로는 causal + registered = count

    10.4 2. 결측치를 식별 및 결측치 대치를 실시하고, 해당 대치방법을 선택한 이유를 작성하시오.
    10.5 3. 범주형 변수 중 변환이 필요할 경우 변환을 실시하고, 해당 변환을 실시한 이유를 서술하시오.
    10.6 4. 추가적인 전처리가 필요한 경우 실시하고, 이유를 제시하시오.
    dat['weather'].value_counts()

    weather
    1    7192
    2    2834
    3     859
    4       1
    Name: count, dtype: int64
    dat['windspeed'].value_counts()

    windspeed
    0.0000     1313
    8.9981     1120
    11.0014    1057
    12.9980    1042
    7.0015     1034
    15.0013     961
    6.0032      872
    16.9979     824
    19.0012     676
    19.9995     492
    22.0028     372
    23.9994     274
    26.0027     235
    27.9993     187
    30.0026     111
    31.0009      89
    32.9975      80
    35.0008      58
    39.0007      27
    36.9974      22
    43.0006      12
    40.9973      11
    43.9989       8
    46.0022       3
    56.9969       2
    47.9988       2
    51.9987       1
    50.0021       1
    Name: count, dtype: int64
    weather는 class 불균형이 존재함

    범주 통합 고려
    freq = dat['weather'].value_counts(normalize = True)
    prob_columns = dat['weather'].map(freq)
    dat['weather'] = dat['weather'].mask(prob_columns < 0.1, '3')
    dat['weather'].value_counts()

    weather
    1    7192
    2    2834
    3     860
    Name: count, dtype: int64
    dat['weather'] = dat['weather'].astype(int)

    num_columns = dat.select_dtypes('number').columns.tolist()
    cat_columns = dat.select_dtypes('object').columns.tolist()
    num_columns.remove('count')

    cat_preprocess = make_pipeline(
        #SimpleImputer(strategy="constant", fill_value="NA"),
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5),
        StandardScaler()
    )

    preprocess = ColumnTransformer(
        [("num", num_preprocess, num_columns),
        ("cat", cat_preprocess, cat_columns)], 
        remainder='passthrough'
    )

    preprocess

    ColumnTransformer
    num
    iterativeimputer: IterativeImputer

    RandomForestRegressor

    StandardScaler
    cat

    OneHotEncoder
    pre_dat = preprocess.fit_transform(dat)
    print('preprocess data dim : ', pre_dat.shape)

    preprocess data dim :  (10886, 27)
    pre_dat[:, 26]

    array([ 16.,  40.,  32., ..., 168., 129.,  88.])
    cat_encoder = preprocess.named_transformers_["cat"]["onehotencoder"]
    cat_names = list(cat_encoder.get_feature_names())
    full_name = num_columns + cat_names + ['count']
    pd.DataFrame(pre_dat, columns = full_name).head(2)

        weather      temp     atemp  humidity  windspeed    casual  registered   
    0 -0.660348 -1.333661 -1.092737  0.995670  -1.567754 -0.660992   -0.943854  \
    1 -0.660348 -1.438907 -1.182421  0.943705  -1.567754 -0.560908   -0.818052   

           year     month      day      hour  x0_1  x0_2  x0_3  x0_4  x1_0  x1_1   
    0 -1.003866 -1.603121 -1.64207 -1.668944   1.0   0.0   0.0   0.0   1.0   0.0  \
    1 -1.003866 -1.603121 -1.64207 -1.524341   1.0   0.0   0.0   0.0   1.0   0.0   

       x2_0  x2_1  x3_Friday  x3_Monday  x3_Saturday  x3_Sunday  x3_Thursday   
    0   1.0   0.0        0.0        0.0          1.0        0.0          0.0  \
    1   1.0   0.0        0.0        0.0          1.0        0.0          0.0   

       x3_Tuesday  x3_Wednesday  count  
    0         0.0           0.0   16.0  
    1         0.0           0.0   40.0  
    windspeed 변수에 결측치 존재

    random forest를 이용하여 결측치를 대치함

    Random forest를 이용해서 결측치를 대치함 결측치를 처리하는 방법은 크게 대표값을 이용하는 방법과 모델을 이용하는 방법이 있다.

    대표값을 이용한 방법 중 대표적으로 평균대치법이 있다. 평균대치법은 해당 변수의 대표값인 평균으로 결측치를 대치하는 방법으로 단점으로는 결측치 수가 많을 때 분포가 왜곡되는 문제가 있을 수 있다.

    모델을 이용한 방법 중 대표적으로 random forest를 이용한 방법이 있다. random forest를 이용한 방법은 boostrap sample에서 변수를 랜덤하게 선택하여 개별 tree를 생성하고, 개별 tree에서 나온 예측값을 평균내서 나온 값을 이용해서 결측치를 대치하는 방법이다.

    random forest를 이용해서 결측치를 대치한 이유는 대표값을 이용하는 방법에 비해서 다른 변수의 정보를 이용해서 결측치를 대치할 수 있기 때문에 더 많은 정보를 활용해서 결측치를 대치할 수 있기 때문이다.

    season, wday, holiday, workingday 변수에 대해 인코딩을 실시함
    범주형 변수 변환 방법은 크게 3가지가 있다. 첫 번째로, label encoding 방법은 범주형 변수의 각 값에 알파벳 순서대로 정수값을 할당하는 방법이다. 두 번째로, one-hot encoding 방법은 범주형 변수의 각 수준(levels)별로 변수를 생성하며, 생성된 개별 변수는 각 수준에 해당하는 경우 1, 해당하지 않는 경우 0으로 구성된다. 세 번째로, dummy coding의 경우 one-hot encoding과 유사하지만 각 수준(levels) - 1개 만큼 변수를 생성하며, 생성된 개별 변수는 각 수준에 해당하는 경우 1, 해당하지 않는 경우 0으로 구성된다.

    이 중 one-hot encoding을 선택한 이유는 label encoding과 비교했을 때, 범주에 수치정보가 반영되는 문제점이 없으며, 범주형 변수의 각 수준(levels)이 크지 않기 때문에 one-hot encoding의 문제점 중 하나인 차원이 늘어남에 따라 계산량이 증가하는 문제 또한 미미하기 때문이다. 또한 앞으로 적합시킬 모델이 glm 계열 모델이 아니기 때문에 one-hot encoding의 문제점 중 하나인 glm 모델일 때 범주형 변수 간의 다중공선성 문제 또한 없기 때문이다.

    weather의 경우 class 불균형

    범주형 변수의 class가 많을 경우, 범주형 변수 인코딩 시 차원이 늘어나는 문제가 있음

    이에 따라 모형 적합시 속도가 느려지는 단점이 있으므로 의미가 퇴색되지 않는 선에서 각 범주형 변수의 class의 빈도가 너무 적을 경우 병합시키는 것을 고려해볼 수 있음

    10.7 세 가지 모델을 임의로 선택하여 적합하고, 속도 측면, 예측력 측면에서 가장 적합한 모델을 선택하시오.
    dat = pd.DataFrame(pre_dat, columns = full_name)
    y = dat['count']
    X = dat.drop(['count'], axis = 1)

    from sklearn.model_selection import train_test_split

    bins = np.nanquantile(y, np.arange(0, 1, 0.1))
    y_binned = np.digitize(y, bins)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = y_binned, random_state = 0)

    데이터를 분할하는 방법은 대표적으로 simple random sampling, strata sampling이 있다. 첫 번째로, simple random sampling은 데이터를 무작위로 특정 비율로 분할하는 방법이다. 두 번째로, strata sampling은 class 불균형 문제에 대한 해결 방안으로 지정된 범주형 변수의 각 class에 해당하는 하위 샘플에 별도로 simple random sampling을 통해서 데이터를 분할하고, 이후 결합하는 방식으로 전체 데이터셋을 분할하는 방법이다. strata sampling은 연속형 변수의 경우 quantile을 기준으로 비닝을 함으로써 범주형 변수에서 시행하는 것과 같은 방식으로 진행된다.

    count의 분포의 경우 우측으로 긴꼬리를 갖는 분포이므로, quantile을 기준으로 적절한 비닝을 통해 strata sampling을 진행한다면 train/test의 분포를 유사하게 유지할 수 있다고 판단했다.

    f, axes = plt.subplots(ncols = 2, nrows = 1, figsize = (20,4))
    train_y.hist(ax = axes[0]);
    test_y.hist(ax = axes[1]);
    plt.show();



    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_param = {'regressor__max_features': np.arange(0.5, 1, 0.1)}
    decisiontree_param = {'regressor__ccp_alpha': np.arange(0.1, 1, 0.1)}
    Bagging_param = {'regressor__max_samples': np.arange(0.1, 1, 0.1)}

    rf_pipe = Pipeline(
        [
            ("regressor", RandomForestRegressor(random_state=42))
        ]
    )

    bagg_pipe = Pipeline(
        [
            ("regressor", BaggingRegressor())
        ]
    )

    dt_pipe = Pipeline(
        [
            ("regressor", DecisionTreeRegressor())
        ]
    )

    start_time = time.time()
    RandomForest_search = GridSearchCV(estimator = rf_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_root_mean_squared_error')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV

    RandomForestRegressor
    print("{}s".format(time.time()-start_time))

    39.141223192214966s
    start_time = time.time()
    bagg_search = GridSearchCV(estimator = bagg_pipe, 
                          param_grid = Bagging_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_root_mean_squared_error')
    bagg_search.fit(train_X, train_y)

    GridSearchCV

    BaggingRegressor
    print("{}s".format(time.time()-start_time))

    5.89637303352356s
    start_time = time.time()
    dt_search = GridSearchCV(estimator = dt_pipe, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_root_mean_squared_error')
    dt_search.fit(train_X, train_y)

    GridSearchCV

    DecisionTreeRegressor
    print("{}s".format(time.time()-start_time))

    3.0743513107299805s
    print('Random forest best score : ', -RandomForest_search.best_score_)

    Random forest best score :  3.733956352658087
    print('bagged tree best score : ', -bagg_search.best_score_)

    bagged tree best score :  4.52369042264544
    print('dt_search best score : ', -dt_search.best_score_)

    dt_search best score :  7.8168919617894135
    Model	속도	성능
    decision tree	3.503 sec	7.694
    bagged tree	5.975 sec	4.625
    random forest	40.642 sec	3.753
    RMSE를 기준으로 예측력을 비교해본 결과 random forest가 가장 우수한 모형으로 보인다. 속도 측면에서는 decision tree가 
    으로 가장 빠른 모형이다. 최종적으로 비교해보면 성능 측면에서 random forest의 성능이 좋으므로, random forest 모형을 선택한다.

    10.8 선택한 모델의 한계점에 대해 설명하고, 보완할 점이 무엇인지 작성하시오.
    Tip
    한계점 및 보완할 점은 해석력 측면에서 작성하는 것이 작성하기 쉬움

    Random forest 모형의 경우 변수 중요도, shapley value 등과 같은 방식으로 변수별 중요도를 시각화할 수 있지만 회귀분석과 같이 직관적인 해석이 어렵다는 문제가 있다.

    이러한 문제를 해결하기 위해서 patial dependence plot과 같이 변수별 영향력을 간접적으로 시각화한다면 해석력을 높일 수 있을 것이다. 또한 회귀분석과 같이 개별 변수의 영향력을 직관적으로 해석할 수 있는 모형을 다시 적합해서 별도의 모델을 구축한다면 해석력을 높일 수 있다.
    """
