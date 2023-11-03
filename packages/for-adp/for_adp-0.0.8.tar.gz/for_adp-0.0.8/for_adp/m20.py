def m20():
    """
    18  20회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import KBinsDiscretizer
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.ensemble import RandomForestRegressor
    from sklearn import set_config
    set_config(display="diagram")

    from sklearn.ensemble import RandomForestRegressor
    import xgboost as xgb
    from sklearn.svm import SVR

    18.1 머신러닝
    Data description

    1년치 온도 데이터가 수집되었고, 주어진 설명변수를 이용해서 실제 온도를 예측하는 문제입니다.

    year: 연도
    month: 월
    day: 일
    week: 요일
    temp_2: 2일 이전 최대 온도
    temp_1: 1일 이전 최대 온도
    average: 최대 온도 평균
    actual: 실제 최대 온도
    friend: 친구가 예측한 값, 평균 +- 20 사이의 임의의 숫자
    dat = pd.read_csv("./data/ex_data/temps.csv")
    dat = dat.drop(['forecast_noaa', 'forecast_acc', 'forecast_under'], axis = 1)

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 348 entries, 0 to 347
    Data columns (total 9 columns):
     #   Column   Non-Null Count  Dtype  
    ---  ------   --------------  -----  
     0   year     348 non-null    int64  
     1   month    348 non-null    int64  
     2   day      348 non-null    int64  
     3   week     348 non-null    object 
     4   temp_2   348 non-null    int64  
     5   temp_1   348 non-null    int64  
     6   average  348 non-null    float64
     7   actual   348 non-null    int64  
     8   friend   348 non-null    int64  
    dtypes: float64(1), int64(7), object(1)
    memory usage: 24.6+ KB
    dat['date'] = pd.to_datetime(dict(year=dat.year, month=dat.month, day=dat.day))
    dat.set_index('date', inplace = True)

    18.1.1 데이터 전처리를 실시하시오(10점).
    EDA
    결측치 처리
    필요 없는 변수 처리
    train/test 분리를 어떻게 할지 설명
    최종 전처리 데이터셋 제시
    EDA

    dat.describe()

             year       month         day  ...     average      actual      friend
    count   348.0  348.000000  348.000000  ...  348.000000  348.000000  348.000000
    mean   2016.0    6.477011   15.514368  ...   59.760632   62.543103   60.034483
    std       0.0    3.498380    8.772982  ...   10.527306   11.794146   15.626179
    min    2016.0    1.000000    1.000000  ...   45.100000   35.000000   28.000000
    25%    2016.0    3.000000    8.000000  ...   49.975000   54.000000   47.750000
    50%    2016.0    6.000000   15.000000  ...   58.200000   62.500000   60.000000
    75%    2016.0   10.000000   23.000000  ...   69.025000   71.000000   71.000000
    max    2016.0   12.000000   31.000000  ...   77.400000   92.000000   95.000000

    [8 rows x 8 columns]
    dat.hist();
    plt.tight_layout();
    plt.show();



    결측치 처리

    lag 변수(temp_1, temp_2)가 재대로 생성이 되어있는지 확인해볼 필요가 있음
    dat.isna().sum()

    year       0
    month      0
    day        0
    week       0
    temp_2     0
    temp_1     0
    average    0
    actual     0
    friend     0
    dtype: int64
    dat['actual'].shift(1).plot()
    dat['temp_1'].plot()
    plt.show();



    dat['actual'].shift(2).plot()
    dat['temp_2'].plot()
    plt.show();



    실제값으로 lag 변수를 생성했을 때 값이 일치하지 않는 것을 확인할 수 있음
    필요없는 변수 처리

    temp_1, temp_2변수 제거

    target 변수를 기준으로 lag변수 재생성

    friend 변수의 경우 친구가 예측한 값으로 예측에 필요한 정보가 없는 변수이므로 제거

    year변수는 값이 하나이므로 제거

    dat = dat.drop(['temp_1', 'temp_2', 'friend', 'year'], axis = 1)

    dat['temp_1'] = dat['actual'].shift(1)
    dat['temp_2'] = dat['actual'].shift(2)

    dat['temp_1'].head(3)

    date
    2016-01-01     NaN
    2016-01-02    45.0
    2016-01-03    44.0
    Name: temp_1, dtype: float64
    dat['temp_1'].backfill().head(3)

    date
    2016-01-01    45.0
    2016-01-02    45.0
    2016-01-03    44.0
    Name: temp_1, dtype: float64

    dat['temp_1'] = dat['temp_1'].backfill()
    dat['temp_2'] = dat['temp_2'].backfill()

    dat.isna().sum()

    month      0
    day        0
    week       0
    average    0
    actual     0
    temp_1     0
    temp_2     0
    dtype: int64
    num_columns = dat.select_dtypes('number').columns.tolist()
    cat_columns = dat.select_dtypes('object').columns.tolist()
    num_columns.remove('actual')


    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
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

    StandardScaler
    cat

    OneHotEncoder
    pre_dat = preprocess.fit_transform(dat)
    print('preprocess data dim : ', pre_dat.shape)

    preprocess data dim :  (348, 13)
    cat_encoder = preprocess.named_transformers_["cat"]["onehotencoder"]
    cat_names = list(cat_encoder.get_feature_names())
    full_name = num_columns + cat_names + ['actual']
    pd.DataFrame(pre_dat, columns = full_name).head(2)

          month       day   average    temp_1  ...  x0_Thurs  x0_Tues  x0_Wed  actual
    0 -1.567839 -1.656822 -1.347070 -1.493909  ...       0.0      0.0     0.0    45.0
    1 -1.567839 -1.542671 -1.337558 -1.493909  ...       0.0      0.0     0.0    44.0

    [2 rows x 13 columns]
    train/test 분할

    random split

    시간 순으로 나눌지, 혹은 random 하게 나눌지 구분

    1년 간의 온도는 1~9월까지는 증가하다가 10~12월에 감소하는 추세이므로, 시간순으로 나누게되면 모델 성능이 저하될 수 있음

    따라서 random split 진행

    pre_dat = pd.DataFrame(pre_dat, columns = full_name)

    y = pre_dat['actual']
    X = pre_dat.drop(['actual'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, shuffle = True, random_state = 0)

    18.1.2 Random forest 모델을 적합하시오(15점).
    예측기준선 수립 및 근거 제시
    하이퍼 파라미터 튜닝
    변수중요도 시각화
    예측 기준선을 모델의 유효성을 평가하는 지표로 해석하면, 반응변수의 평균값을 예측 기준선으로 정할 수 있음. 주어진 설명변수를 고려한 모형을 구축했을 때 반응변수의 평균값보다 예측력이 좋지 않다면, 모형을 구축하는 의미가 없기 때문임.

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    rf_pipe = Pipeline(
        [
            ("regressor", RandomForestRegressor(random_state=42))
        ]
    )

    RandomForest_param = {'regressor__max_features': np.arange(0.5, 1, 0.1)}

    RandomForest_search = GridSearchCV(estimator = rf_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_root_mean_squared_error')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV

    RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    print('Ramdom forest best parameters : ', RandomForest_search.best_params_)

    Ramdom forest best parameters :  {'regressor__max_features': 0.6}
    print('Random forest best score : ', -RandomForest_search.best_score_)

    Random forest best score :  4.72683507084527
    print('예측한계선 RMSE :', mean_squared_error(train_y, dat.iloc[train_X.index, :]['average'], squared = False))

    예측한계선 RMSE : 6.819504929392925
    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        RandomForest_search, train_X, train_y, n_repeats=10, random_state=42
    )

    features = train_X.columns
    importances = feature_importances.importances_mean
    # 
    # plt.bar(importances, features);
    # tick_values = np.arange(len(label_list))
    # plt.xticks(rotation=90)
    # plt.show();

    sorted_idx = feature_importances.importances_mean.argsort()
    fig = plt.figure(figsize=(12, 6))
    plt.barh(range(len(sorted_idx)), feature_importances.importances_mean[sorted_idx], align='center')

    <BarContainer object of 12 artists>
    plt.yticks(range(len(sorted_idx)), np.array(train_X.columns)[sorted_idx])

    ([<matplotlib.axis.YTick object at 0x172f18ee0>, <matplotlib.axis.YTick object at 0x172f07400>, <matplotlib.axis.YTick object at 0x172f02460>, <matplotlib.axis.YTick object at 0x1699a4820>, <matplotlib.axis.YTick object at 0x1699a9310>, <matplotlib.axis.YTick object at 0x1699a9dc0>, <matplotlib.axis.YTick object at 0x1699a40d0>, <matplotlib.axis.YTick object at 0x169999910>, <matplotlib.axis.YTick object at 0x1699af9a0>, <matplotlib.axis.YTick object at 0x1699b5490>, <matplotlib.axis.YTick object at 0x1699b5f40>, <matplotlib.axis.YTick object at 0x169999c70>], [Text(0, 0, 'x0_Thurs'), Text(0, 1, 'x0_Tues'), Text(0, 2, 'x0_Fri'), Text(0, 3, 'x0_Sat'), Text(0, 4, 'x0_Wed'), Text(0, 5, 'x0_Sun'), Text(0, 6, 'x0_Mon'), Text(0, 7, 'month'), Text(0, 8, 'day'), Text(0, 9, 'temp_2'), Text(0, 10, 'temp_1'), Text(0, 11, 'average')])
    plt.title('Permutation Importance')
    plt.show();



    18.1.3 SVM 모델을 적합하시오(15점).
    예측한계선을 설정
    하이퍼 파라미터 튜닝
    변수중요도 시각화
    svm_pipe = Pipeline(
        [
            ("regressor", SVR())
        ]
    )

    SVR_param = {'regressor__C': np.arange(1, 100, 20)}

    SVR_search = GridSearchCV(estimator = svm_pipe, 
                          param_grid = SVR_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_root_mean_squared_error')
    SVR_search.fit(train_X, train_y)

    GridSearchCV

    SVR
    from sklearn.metrics import mean_squared_error
    print('Ramdom forest best parameters : ', SVR_search.best_params_)

    Ramdom forest best parameters :  {'regressor__C': 21}
    print('Random forest best score : ', -SVR_search.best_score_)

    Random forest best score :  5.818465799450394
    print('예측한계선 RMSE :', mean_squared_error(train_y, dat.iloc[train_X.index, :]['average'], squared = False))

    예측한계선 RMSE : 6.819504929392925
    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        SVR_search, train_X, train_y, n_repeats=10, random_state=42
    )

    features = train_X.columns
    importances = feature_importances.importances_mean


    sorted_idx = feature_importances.importances_mean.argsort()
    fig = plt.figure(figsize=(12, 6))
    plt.barh(range(len(sorted_idx)), feature_importances.importances_mean[sorted_idx], align='center')

    <BarContainer object of 12 artists>
    plt.yticks(range(len(sorted_idx)), np.array(train_X.columns)[sorted_idx])

    ([<matplotlib.axis.YTick object at 0x1699a4b20>, <matplotlib.axis.YTick object at 0x1699999a0>, <matplotlib.axis.YTick object at 0x1699a4610>, <matplotlib.axis.YTick object at 0x169999220>, <matplotlib.axis.YTick object at 0x1699b5850>, <matplotlib.axis.YTick object at 0x1699a4dc0>, <matplotlib.axis.YTick object at 0x1699a9d00>, <matplotlib.axis.YTick object at 0x172f18310>, <matplotlib.axis.YTick object at 0x1699a6700>, <matplotlib.axis.YTick object at 0x1699a64c0>, <matplotlib.axis.YTick object at 0x17a122160>, <matplotlib.axis.YTick object at 0x17a119ca0>], [Text(0, 0, 'x0_Thurs'), Text(0, 1, 'x0_Fri'), Text(0, 2, 'x0_Wed'), Text(0, 3, 'x0_Mon'), Text(0, 4, 'x0_Tues'), Text(0, 5, 'x0_Sun'), Text(0, 6, 'x0_Sat'), Text(0, 7, 'day'), Text(0, 8, 'month'), Text(0, 9, 'temp_2'), Text(0, 10, 'average'), Text(0, 11, 'temp_1')])
    plt.title('Permutation Importance')
    plt.show();



    18.1.4 두 모델 중 최적의 모델을 선택하시오.
    Random forest, SVM 모델 결과 비교 후 최종 모델 선택
    두 모델의 장·단점 기술
    운영 관점에서 어떤 모델을 선택할 것인지 기술
    모델링 관련 개선 방향 제시
    모형 선택

    RMSE 기준으로 ramdom forest 모델을 선택
    pred = RandomForest_search.predict(test_X)

    print('예측한계선 RMSE :', mean_squared_error(pred, test_y, squared = False))

    예측한계선 RMSE : 4.895921334568777
    최종 검증 데이터에서의 성능은 RMSE = 4.89 정도인 것을 확인할 수 있다.

    SVM



    Random forest



    운영 관점에서 모형의 성능이 좋은 SVM 모델 선택

    속도 관점에서도 비교해볼 수 있음

    xgboost, lightgbm 같은 부스팅 모형을 함께 앙상블한다면 모형의 성능을 높일 수 있음

    18.2 군집분석
    Data description

    7주 동안의 전력 소비량 데이터(15분 간격으로 측정)입니다.

    year
    month
    day
    가구코드
    전력사용량
    18.2.1 군집분석을 실시 후 아래 표를 완성하시오(군집 5개로 고정)(10점).
    dat = pd.read_csv('./data/adp20_2.csv')
    dat['date'] = pd.to_datetime(dat['date'], format='mixed')

    clustering

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters = 5)
    kmeans.fit(dat['power'].to_numpy().reshape(-1, 1))


    KMeans
    KMeans(n_clusters=5)
    label = kmeans.labels_
    dat['cluster'] = label

    18.2.2 각 군집별로 heatmap을 그리시오(총 5개 heatmap 생성)(15점).
    dat['wday'] = dat['date'].dt.day_name()
    dat['hour'] = dat['date'].dt.hour


    cluster1 = (dat
        .loc[dat.cluster == 1]
        .groupby(['wday', 'hour'])
        .agg(mean_w = ('power', 'mean'))
        .reset_index()
    )

    cluster1 = cluster1.pivot(index = 'wday', columns = 'hour', values = 'mean_w')

    week_or = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    cluster1 = cluster1.loc[week_or]

    sns.heatmap(cluster1,annot = True)
    plt.show();



    4개 더 그리면 됨
    """
