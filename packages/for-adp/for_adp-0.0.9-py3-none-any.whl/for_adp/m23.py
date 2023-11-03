def m23():
    """
    21  23회차 기출문제
    21  23회차 기출문제
    Libraries

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
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve
    from sklearn import set_config

    21.1 머신러닝
    21.1.1 Data description
    temperature : 온도(섭씨)

    Humidity : 습도(%)

    Light : 밝기(lux)

    Co2 : 이산화탄소 농도(ppm)

    Occupancy : 방 이용 유무(1 : 이용 x, 0 : 이용 o)

    https://archive.ics.uci.edu/ml/datasets/Occupancy+Detection+

    dat = pd.read_csv('./data/ex_data/dat9.csv')

    y = dat.occupancy
    X = dat.drop(['occupancy'], axis = 1)

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 300 entries, 0 to 299
    Data columns (total 5 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   temperature  300 non-null    float64
     1   humidity     300 non-null    float64
     2   light        300 non-null    float64
     3   co2          295 non-null    float64
     4   occupancy    300 non-null    int64  
    dtypes: float64(4), int64(1)
    memory usage: 11.8 KB
    21.1.2 데이터를 탐색하고 탐색 결과를 제시하시오
    Summary

    dat.describe()

           temperature    humidity        light          co2   occupancy
    count   300.000000  300.000000   300.000000   295.000000  300.000000
    mean     21.780052   28.181973   424.539667   927.995876    0.880000
    std       0.950689    4.459320   180.400411   323.542741    0.325504
    min      19.200000   17.600000     0.000000   418.000000    0.000000
    25%      21.290000   25.211250   428.250000   696.975000    1.000000
    50%      21.790000   27.943750   444.000000   891.250000    1.000000
    75%      22.200000   31.260000   472.333333  1069.375000    1.000000
    max      24.390000   39.067500  1380.000000  2022.500000    1.000000
    X.select_dtypes('number').hist();
    plt.show()



    sns.countplot(y);
    plt.show()



    plt.clf() # 초기화 
    corr = X.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.show()



    f, axes = plt.subplots(ncols = 2, figsize = (20,4))

    sns.boxplot(x = "occupancy", y = "temperature", data = dat, ax = axes[0])
    axes[0].set_title('occupancy vs temperature boxplot')

    sns.boxplot(x = "occupancy", y = "light", data = dat, ax = axes[1])
    axes[1].set_title('occupancy vs light boxplot')

    plt.show()



    dat.groupby(['occupancy'])['light'].agg(['min', 'mean', 'max'])

                 min        mean     max
    occupancy                           
    0            0.0   14.638889   360.0
    1          393.0  480.435227  1380.0
    21.1.3 결측치를 탐색하고, 결측치 대체 방법 한 가지를 수행하고, 해당 방법을 사용한 근거를 제시하시오
    21회차와 동일
    dat.isna().sum()

    temperature    0
    humidity       0
    light          0
    co2            5
    occupancy      0
    dtype: int64
    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor

    impute_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5)
    )

    preprocess = ColumnTransformer(
        [("imputation", impute_preprocess, X.columns)]
    )

    from sklearn import set_config
    set_config(display="diagram")
    preprocess

    ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    imp_train_X = preprocess.fit_transform(train_X)
    imp_test_X = preprocess.transform(test_X)

    train_X = pd.DataFrame(imp_train_X, columns = X.columns)
    test_X = pd.DataFrame(imp_test_X, columns = X.columns)

    train_X.isna().sum()

    temperature    0
    humidity       0
    light          0
    co2            0
    dtype: int64
    21.1.4 추가적으로 데이터 질을 향상시킬만한 내용 작성(구현 안하고 설명만해도 됨)
    생략
    21.1.5 데이터 불균형을 식별하고 불균형을 처리할 오버샘플링 기법 두 가지를 제시하시오
    sns.countplot(train_y);
    plt.show()



    train_y.value_counts()

    occupancy
    1    211
    0     29
    Name: count, dtype: int64
    simple oversampling

    단순오버샘플링은 클래스가 불균형일 때 빈도가 낮은 levels에 해당하는 표본을 복원 추출을 통해 빈도가 높은 levels에 해당하는 표본의 수만큼 관측치를 복제함으로써 클래스 균형을 맞추는 방법이다.

    from imblearn.over_sampling import RandomOverSampler
    from collections import Counter
    oversample = RandomOverSampler(sampling_strategy='minority')
    train_X_over, train_y_over = oversample.fit_resample(train_X, train_y)
    print(Counter(train_y_over))

    Counter({0: 211, 1: 211})
    SMOTE

    SMOTE는 먼저 분류 개수가 적은 쪽의 데이터의 샘플을 취한 뒤 이 샘플의 k 최근접 이웃k nearest neighbor을 찾습니다. 그리고 현재 샘플과 이들 k개 이웃 간의 차difference를 구하고, 이 차이에 0 ~ 1 사이의 임의의 값을 곱하여 원래 샘플에 더합니다. 이렇게 만든 새로운 샘플을 훈련 데이터에 추가합니다. 결과적으로 SMOTE는 기존의 샘플을 주변의 이웃을 고려해 약간씩 이동시킨 점들을 추가하는 방식으로 동작합니다.





    from imblearn.over_sampling import SMOTE
    smote = SMOTE()
    train_X_smote, train_y_smote = smote.fit_resample(train_X, train_y)
    print(Counter(train_y_smote))

    Counter({0: 211, 1: 211})
    Randomly Over Sampling Examples (ROSE)

    ROSE는 smooth boostrap을 적용하여 리샘플링하는 방법입니다. smooth boostrap이란 resampling된 관측치에 평균이 0이고 정규분포를 따르는 아주 작은 양의 random noise을 더해 새로운 표본을 생성하는 원리를 따릅니다. ROSE는 sampling_strategy='minority', shrinkage = 1로 설정할 경우 적당한 양의 random noise를 추가하여 소수 클래스를 늘립니다.

    상세 : https://dondonkim.netlify.app/posts/2022-11-16-rose/rose

    from imblearn.over_sampling import RandomOverSampler
    from collections import Counter
    rose = RandomOverSampler(sampling_strategy='minority', shrinkage= 1)
    train_X_rose, train_y_rose = oversample.fit_resample(train_X, train_y)
    print(Counter(train_y_rose))

    Caution
    ROSE의 경우 imblearn = 0.8 버전부터 작동합니다. 시험장 설치 패키지는 imblearn = 0이므로 시험 전 패키지 업데이트 가능 여부를 확인해야 합니다.

    21.1.6 오버샘플링한 데이터셋을 각각 제시하고, 오버샘플링 기법별 장·단점을 작성하시오
    simple oversampling

    장점

    under sampling 처럼 데이터를 잃지 않고, 소수 범주를 잘 분류할 가능성이 있음
    단점

    소수 범주를 복원추출을 통해 값을 복제하므로, 소수 범주에 과적합될 수 있음

    데이터의 크기가 증가하므로 모델 적합시 계산량이 더 많아짐

    SMOTE

    장점

    under sampling 처럼 데이터를 잃지 않고, 소수 범주를 잘 분류할 가능성이 있음

    관측치를 단순히 복제하는 것이 아니므로, Simple oversampling에 비해 과적합을 완화할 수 있음

    단점

    데이터의 크기가 증가하므로 모델 적합시 계산량이 더 많아짐

    값에 따라 성능이 유동적임

    소수 클래스의 정보만 사용하므로, 다수 클래스에 대한 정보가 전혀 고려되지 않음

    ROSE

    장점

    오버샘플링과 under sampling의 장점을 동시에 갖음
    단점

    데이터의 크기가 증가하므로 모델 적합시 계산량이 더 많아짐

    smoothing parameter에 따라 성능이 유동적임

    print('oversampling y:', Counter(train_y_over))

    oversampling y: Counter({0: 211, 1: 211})
    print('SMOTE y:', Counter(train_y_smote))

    SMOTE y: Counter({0: 211, 1: 211})
    print('oversampling X:', train_X_over.shape)

    oversampling X: (422, 4)
    print('SMOTE X:', train_X_over.shape)

    SMOTE X: (422, 4)
    21.1.7 오버샘플링 데이터셋을 이용해서 정확도 측면 모형과 속도 측면 모형을 각각 제시하시오
    num_preprocess = make_pipeline(
        StandardScaler()
    )

    preprocess = ColumnTransformer(
        [("imputation", impute_preprocess, X.columns), 
         ("num", num_preprocess, X.columns)]
    )

    Random forest

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.ensemble import RandomForestClassifier

    pipe_rf = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    start_time = time.time()
    RandomForest_search = GridSearchCV(estimator = pipe_rf, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'balanced_accuracy') # roc_auc, average_precision
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    num

    StandardScaler

    SMOTE

    RandomForestClassifier
    print("{}s".format(time.time()-start_time))

    12.398420095443726s
    print('Random Forest best score : ', RandomForest_search.best_score_)

    Random Forest best score :  0.9888888888888889
    Decision tree

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.tree import DecisionTreeClassifier

    pipe_dt = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", DecisionTreeClassifier())
        ]
    )

    decisiontree_param = {'classifier__ccp_alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    start_time = time.time()
    decisiontree_search = GridSearchCV(estimator = pipe_dt, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    num

    StandardScaler

    SMOTE

    DecisionTreeClassifier
    print("{}s".format(time.time()-start_time))

    10.079651117324829s
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.9888888888888889
    logistic reg

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.linear_model import LogisticRegression

    pipe_lg = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", LogisticRegression())
        ]
    )
    #LogisticRegression().get_params()

    start_time = time.time()
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)
    #logistic_param = [{'classifier__C':[0.001, 0.01, 0.1, 1, 10, 100]}]
    logistic_param = [{'classifier__penalty':['none', 'elasticnet', 'l1', 'l2']}]

    logistic_search = GridSearchCV(estimator = pipe_lg, 
                          param_grid = logistic_param,
                          cv = cv,
                          scoring = 'balanced_accuracy')
    logistic_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    num

    StandardScaler

    SMOTE

    LogisticRegression
    print("{}s".format(time.time()-start_time))

    5.0353920459747314s
    print('logistic regression best score : ', logistic_search.best_score_)

    logistic regression best score :  0.9777777777777779
    complete seperation 문제

    일 경우 
    이고, 
    일 경우 
    로 완벽하게 분리됨

    X 변수로 Y를 완벽하게 분리 가능하므로 모형이 필요 없음

    complete seperation이 깨지는 새로운 데이터가 들어올경우 모델 성능이 심하게 왜곡될 수 있음

    logistic regression의 경우 solver에 따라 알고리즘 수렴이 안될 수 있음

    penalized logistic regression 모형 적합 고려

    추가 자료 : https://dondonkim.netlify.app/posts/com_sep/com_sep.html

    21.1.8 둘 중 하나의 모형을 선택하고 분류 결과와 함께 이유를 제시하시오
    속도 관점 : logistic regression

    정확도 관점 : Random forest

    예측 정확도와 속도 측면에서 비교해보고 모델 선택 이유 작성

    예측 성능은 logistic regression, Random forest 모두 precision, recall, accuracy 등 분류 지표 모두 0.94 ~ 0.98인 것을 확인할 수 있음

    속도 측면에서 logistic regression 모형이 가장 빠르므로, 최종 모형은 logistic regression 모형으로 선택함

    pred = logistic_search.predict(test_X)
    print(classification_report(test_y, pred))

                  precision    recall  f1-score   support

               0       1.00      1.00      1.00         7
               1       1.00      1.00      1.00        53

        accuracy                           1.00        60
       macro avg       1.00      1.00      1.00        60
    weighted avg       1.00      1.00      1.00        60
    print(balanced_accuracy_score(test_y, pred))

    1.0
    분류모형의 성능이 1이 나온 이유는 EDA 과정에서 확인할 수 있습니다.

    occupancy ~ light의 boxplot과 통계량을 보면 occupancy 0, 1에 따라 light가 완벽하게 분리되는 것을 확인할 수 있습니다. 변수의 의미를 생각해보면 방을 이용하지 않을 경우 불은 꺼져있을 것이고, 방을 이용할 경우 불이 켜져있는 것은 당연하다고 볼 수 있습니다. 따라서 이상치가 없다는 가정 하에 light 변수만 있으면 모형을 이용하지 않아도 occupancy를 정확히 예측할 수 있습니다.

    현재 수집된 데이터에서는 light 변수를 이용해서 occupancy를 완벽하게 설명할 수 있지만, 데이터가 더 수집되어 이상치가 존재할 경우(방이 비어있어도 light > 400인 케이스) 모형을 통한 예측이 필요하며, 추가 변수가 수집되면 더 강건한 예측을 할 수 있을 것입니다.

    21.1.9 원데이터와 비교해서 오버샘플링이 미친 영향에 대해 작성하시오
    정확도, 속도 측면에서 비교

    pipe_lg2 = Pipeline(
        [
            ("preprocess", preprocess),
            #("smote", SMOTE(random_state = 0)),
            ("classifier", LogisticRegression())
        ]
    )

    start_time = time.time()
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)
    logistic_param = [{'classifier__penalty':['none', 'elasticnet', 'l1', 'l2']}]

    logistic_search = GridSearchCV(estimator = pipe_lg2, 
                          param_grid = logistic_param,
                          cv = cv,
                          scoring = 'balanced_accuracy')
    logistic_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    num

    StandardScaler

    LogisticRegression
    print("{}s".format(time.time()-start_time))

    5.061459064483643s
    print('logistic regression best score : ', logistic_search.best_score_)

    logistic regression best score :  0.9777777777777779
    pred = logistic_search.predict(test_X)
    print(classification_report(test_y, pred))

                  precision    recall  f1-score   support

               0       1.00      1.00      1.00         7
               1       1.00      1.00      1.00        53

        accuracy                           1.00        60
       macro avg       1.00      1.00      1.00        60
    weighted avg       1.00      1.00      1.00        60
    21.2 통계분석
    21.2.1 주어진 데이터를 이용해서 다음을 수행하시오.
    covid_data = pd.read_csv("./data/ex_data/covid_data.csv")
    covid_data.head()

       country        date  confirmed
    0  Belarus  2020-01-22          0
    1  Belarus  2020-01-23          0
    2  Belarus  2020-01-24          0
    3  Belarus  2020-01-25          0
    4  Belarus  2020-01-26          0
    covid_data['date']=pd.to_datetime(covid_data['date'])
    #df=covid_data[['date','country','confirmed']].set_index('date') 

    dat = covid_data.pivot(index='date', columns='country', values='confirmed')
    dat.plot()
    plt.legend(loc='upper left', prop={'size': 7})
    plt.show();



    import pandas as pd
    import numpy as np
    df=pd.read_csv("./data/ex_data/covid_data.csv")
    from datetime import datetime
    df['date']=pd.to_datetime(df['date'])
    dat=df.pivot(index='date',columns='country',values='confirmed')

    21.2.2 acf 사용해서 distance를 계산하시오 (10)
    문제의도는 시계열 자료의 특성을 반영한 거리를 구하라는 것

    거리를 구하는 이유는 각 시계열 자료 간 dissimilarity(비유사도)를 측정하기 위한 것이라고 볼 수 있음

    위의 데이터로 예를 들면 벨기에와 우리나라의 누적확진자 데이터가 있을 때, 두 국가 간 시간에 따른 누적 확진자의 변화의 패턴이 유사한지를 측정하는 것이라고 볼 수 있음

    보통 거리를 측정할 때, euclidean distance를 사용하는데, 시계열 자료에 그대로 사용했을 때는 문제가 발생할 수 있음

    대안으로 ACF distance, DTW(dynamic time warping) 등등..

    Example



    x는 정규분포에서 생성한 데이터이고, y는 x에서 lag 
    만큼 이동시킨 데이터, z는 사인함수를 통해 생성한 x, y와는 관련 없는 데이터라고 볼 수 있음

    x, y, z의 거리를 측정했을 때(비유사도를 측정했을 때) 우리가 원하는 결과는 x, y는 가깝고, z는 멀기를 원함

    euclidean distance

          [,1]     [,2]     [,3]
    x 3.832425 3.729637 4.117309
    y 3.832425 3.729637 4.117309
    z 5.814576 5.832570 5.849725
             x        y
    y  0.00000         
    z 32.05793 32.05793
    ACF distance



    그냥 acf distance를 구했을 때
    euclidean distance와 동일하게 시계열의 특성을 반영하지 못하는 것을 알 수 있음

              x         y
    y 0.0000000          
    z 0.6122848 0.6122848
    차분하고 acf distance를 구했을 때
    추세가 존재하므로, 차분을 한 후 acf distance를 구했을 때, 시계열의 특성을 반영한 정확한 acf distance를 구할 수 있음




        Ljung-Box test

    data:  Residuals
    Q* = 6.4727, df = 10, p-value = 0.7741

    Model df: 0.   Total lags used: 10
             x        y
    y 0.000000         
    z 3.394669 3.394669
    DTW

             x        y
    y  0.00000         
    z 49.83993 49.83993
    설명 참고 : https://medium.com/walmartglobaltech/time-series-similarity-using-dynamic-time-warping-explained-9d09119e48ec

    DTW, acf distance의 경우 시계열의 특성을 잘 반영해서 dissimilarity를 측정함

    R 응용시계열분석 참고 : “부분적으로 왜곡되거나 변형된 파형에 대해서도 적절하게 매칭됨”
    주의할 점은 acf distance의 경우 정상 시계열과 유사하게 만들어주고 진행해줘야 재대로 작동함

    from statsmodels.graphics.tsaplots import acf

    dat_diff = dat.diff()
    dat_diff.dropna(inplace = True)
    mat = np.zeros((dat_diff.shape))

    for i in range(0, mat.shape[1]):
        mat[:, i] = acf(dat_diff.iloc[:, i], nlags = mat.shape[0])

    mat.shape

    (106, 31)
    각 행(국가별)별 acf 값을 이용해서 유클리디안 거리 계산

    acf distance 수식에서 weight를 identity로 설정할 경우, acf에 euclidean distance 적용한 것과 동일함

    from sklearn.metrics.pairwise import euclidean_distances
    print(mat.T.shape)

    (31, 106)
    ucl_dist = euclidean_distances(mat.T)
    ucl_dist[:3, :3]

    array([[0.        , 1.10205567, 0.39722941],
           [1.10205567, 0.        , 1.28898662],
           [0.39722941, 1.28898662, 0.        ]])
    ucl_dist.shape

    (31, 31)
    21.2.3 계층적 군집 분석을 위한 덴드로그램을 작성하시오 (10)
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import silhouette_score
    scores = []

    for i in range(2,10):
        fit_hk = AgglomerativeClustering(n_clusters=i, linkage = 'ward').fit(ucl_dist)
        score = silhouette_score(ucl_dist, fit_hk.labels_)
        scores.append(score)

    plt.figure(figsize=(11,8.5))
    plt.plot(range(2,10), np.array(scores), 'bx-')
    plt.xlabel('Number of clusters $k$')
    plt.ylabel('Average Silhouette')
    plt.title('Average Silhouette method showing the optimal $k$')
    plt.show()



    hk = AgglomerativeClustering(n_clusters = 2, linkage = 'ward')
    hk.fit(ucl_dist)


    AgglomerativeClustering
    AgglomerativeClustering()
    hk.labels_

    array([0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0])
    from scipy.cluster.hierarchy import dendrogram, linkage

    Z = linkage(ucl_dist, method="ward")
    fig = plt.figure(figsize=(10, 6))
    dendrogram(Z, labels = dat.columns)

    {'icoord': [[25.0, 25.0, 35.0, 35.0], [15.0, 15.0, 30.0, 30.0], [5.0, 5.0, 22.5, 22.5], [55.0, 55.0, 65.0, 65.0], [45.0, 45.0, 60.0, 60.0], [75.0, 75.0, 85.0, 85.0], [95.0, 95.0, 105.0, 105.0], [80.0, 80.0, 100.0, 100.0], [52.5, 52.5, 90.0, 90.0], [135.0, 135.0, 145.0, 145.0], [125.0, 125.0, 140.0, 140.0], [115.0, 115.0, 132.5, 132.5], [71.25, 71.25, 123.75, 123.75], [175.0, 175.0, 185.0, 185.0], [165.0, 165.0, 180.0, 180.0], [155.0, 155.0, 172.5, 172.5], [225.0, 225.0, 235.0, 235.0], [215.0, 215.0, 230.0, 230.0], [205.0, 205.0, 222.5, 222.5], [195.0, 195.0, 213.75, 213.75], [245.0, 245.0, 255.0, 255.0], [275.0, 275.0, 285.0, 285.0], [295.0, 295.0, 305.0, 305.0], [280.0, 280.0, 300.0, 300.0], [265.0, 265.0, 290.0, 290.0], [250.0, 250.0, 277.5, 277.5], [204.375, 204.375, 263.75, 263.75], [163.75, 163.75, 234.0625, 234.0625], [97.5, 97.5, 198.90625, 198.90625], [13.75, 13.75, 148.203125, 148.203125]], 'dcoord': [[0.0, 1.0527478542771198, 1.0527478542771198, 0.0], [0.0, 3.859319114559353, 3.859319114559353, 1.0527478542771198], [0.0, 5.674726592430349, 5.674726592430349, 3.859319114559353], [0.0, 0.41528928045031527, 0.41528928045031527, 0.0], [0.0, 0.6701943674145989, 0.6701943674145989, 0.41528928045031527], [0.0, 0.24670306343134826, 0.24670306343134826, 0.0], [0.0, 0.56690617321949, 0.56690617321949, 0.0], [0.24670306343134826, 1.0885425361993082, 1.0885425361993082, 0.56690617321949], [0.6701943674145989, 1.3628576905044443, 1.3628576905044443, 1.0885425361993082], [0.0, 0.44977382358733037, 0.44977382358733037, 0.0], [0.0, 0.784468395111007, 0.784468395111007, 0.44977382358733037], [0.0, 2.0382643930526467, 2.0382643930526467, 0.784468395111007], [1.3628576905044443, 2.7157319717386144, 2.7157319717386144, 2.0382643930526467], [0.0, 1.3355316997412632, 1.3355316997412632, 0.0], [0.0, 2.124000090117547, 2.124000090117547, 1.3355316997412632], [0.0, 3.1109974971589165, 3.1109974971589165, 2.124000090117547], [0.0, 0.6840660634757866, 0.6840660634757866, 0.0], [0.0, 0.987964731640529, 0.987964731640529, 0.6840660634757866], [0.0, 1.4889360187567307, 1.4889360187567307, 0.987964731640529], [0.0, 2.7342847262652796, 2.7342847262652796, 1.4889360187567307], [0.0, 1.3585057812739159, 1.3585057812739159, 0.0], [0.0, 0.7037602036692634, 0.7037602036692634, 0.0], [0.0, 1.509060388676905, 1.509060388676905, 0.0], [0.7037602036692634, 1.9093043323934211, 1.9093043323934211, 1.509060388676905], [0.0, 3.0030999470616533, 3.0030999470616533, 1.9093043323934211], [1.3585057812739159, 4.002546546132745, 4.002546546132745, 3.0030999470616533], [2.7342847262652796, 7.548210832075151, 7.548210832075151, 4.002546546132745], [3.1109974971589165, 11.13825368278012, 11.13825368278012, 7.548210832075151], [2.7157319717386144, 13.044088492933103, 13.044088492933103, 11.13825368278012], [5.674726592430349, 19.84076029212809, 19.84076029212809, 13.044088492933103]], 'ivl': ['Ecuador', 'Korea, South', 'China', 'France', 'Singapore', 'Belarus', 'Russia', 'Qatar', 'Saudi Arabia', 'India', 'Mexico', 'Chile', 'Peru', 'Brazil', 'Pakistan', 'Switzerland', 'Germany', 'Israel', 'Spain', 'United Arab Emirates', 'US', 'Canada', 'Sweden', 'United Kingdom', 'Ireland', 'Portugal', 'Italy', 'Iran', 'Netherlands', 'Belgium', 'Turkey'], 'leaves': [6, 14, 5, 7, 23, 0, 21, 20, 22, 9, 15, 4, 18, 2, 17, 26, 8, 12, 24, 29, 28, 3, 25, 30, 11, 19, 13, 10, 16, 1, 27], 'color_list': ['C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C0'], 'leaves_color_list': ['C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2']}
    plt.show();



    21.2.4 DTW
    시험 문제에서는 ACF distance를 구하라고 했으므로, ACF distance를 이용한 방법으로 답안 작성

    dtw는 참고용으로 알고 있으므로 참고용으로 알고 있으면 됨

    Caution
    dtaidistance는 패키지 지원 목록에 없으므로, 시험 시작 전 패키지 설치 여부를 확인해야 합니다.

    #conda install -c conda-forge dtaidistance
    from dtaidistance import dtw
    dtw_dat = dat.to_numpy()
    dtw_dat.T.shape

    (31, 107)
    ds = dtw.distance_matrix(dtw_dat.T)
    ds.shape

    (31, 31)
    from scipy.cluster.hierarchy import dendrogram, linkage

    Z = linkage(ds, method="ward")
    fig = plt.figure(figsize=(10, 6))
    dendrogram(Z, labels = dat.columns)

    {'icoord': [[45.0, 45.0, 55.0, 55.0], [35.0, 35.0, 50.0, 50.0], [25.0, 25.0, 42.5, 42.5], [15.0, 15.0, 33.75, 33.75], [75.0, 75.0, 85.0, 85.0], [105.0, 105.0, 115.0, 115.0], [95.0, 95.0, 110.0, 110.0], [80.0, 80.0, 102.5, 102.5], [65.0, 65.0, 91.25, 91.25], [145.0, 145.0, 155.0, 155.0], [135.0, 135.0, 150.0, 150.0], [125.0, 125.0, 142.5, 142.5], [165.0, 165.0, 175.0, 175.0], [195.0, 195.0, 205.0, 205.0], [185.0, 185.0, 200.0, 200.0], [170.0, 170.0, 192.5, 192.5], [133.75, 133.75, 181.25, 181.25], [78.125, 78.125, 157.5, 157.5], [24.375, 24.375, 117.8125, 117.8125], [225.0, 225.0, 235.0, 235.0], [245.0, 245.0, 255.0, 255.0], [230.0, 230.0, 250.0, 250.0], [215.0, 215.0, 240.0, 240.0], [265.0, 265.0, 275.0, 275.0], [295.0, 295.0, 305.0, 305.0], [285.0, 285.0, 300.0, 300.0], [270.0, 270.0, 292.5, 292.5], [227.5, 227.5, 281.25, 281.25], [71.09375, 71.09375, 254.375, 254.375], [5.0, 5.0, 162.734375, 162.734375]], 'dcoord': [[0.0, 46323.715636506415, 46323.715636506415, 0.0], [0.0, 214707.81665344635, 214707.81665344635, 46323.715636506415], [0.0, 325285.9422442786, 325285.9422442786, 214707.81665344635], [0.0, 421051.31054276327, 421051.31054276327, 325285.9422442786], [0.0, 10831.72361197574, 10831.72361197574, 0.0], [0.0, 19452.87274885495, 19452.87274885495, 0.0], [0.0, 47267.88865238856, 47267.88865238856, 19452.87274885495], [10831.72361197574, 141811.67848258084, 141811.67848258084, 47267.88865238856], [0.0, 258077.94532341327, 258077.94532341327, 141811.67848258084], [0.0, 3844.8178235263345, 3844.8178235263345, 0.0], [0.0, 16869.882197653376, 16869.882197653376, 3844.8178235263345], [0.0, 63937.52154690531, 63937.52154690531, 16869.882197653376], [0.0, 69088.48879503047, 69088.48879503047, 0.0], [0.0, 50594.52216032559, 50594.52216032559, 0.0], [0.0, 98366.37224076824, 98366.37224076824, 50594.52216032559], [69088.48879503047, 147306.9819813678, 147306.9819813678, 98366.37224076824], [63937.52154690531, 319758.7694455556, 319758.7694455556, 147306.9819813678], [258077.94532341327, 652504.1635955876, 652504.1635955876, 319758.7694455556], [421051.31054276327, 1898831.5025490103, 1898831.5025490103, 652504.1635955876], [0.0, 466886.797495732, 466886.797495732, 0.0], [0.0, 533646.385836569, 533646.385836569, 0.0], [466886.797495732, 791182.5782902628, 791182.5782902628, 533646.385836569], [0.0, 1218845.4797868552, 1218845.4797868552, 791182.5782902628], [0.0, 269080.70587745286, 269080.70587745286, 0.0], [0.0, 84535.37052377063, 84535.37052377063, 0.0], [0.0, 414990.42143985175, 414990.42143985175, 84535.37052377063], [269080.70587745286, 2068088.351507191, 2068088.351507191, 414990.42143985175], [1218845.4797868552, 4543479.827545615, 4543479.827545615, 2068088.351507191], [1898831.5025490103, 10311091.548271729, 10311091.548271729, 4543479.827545615], [0.0, 33200790.995586287, 33200790.995586287, 10311091.548271729]], 'ivl': ['US', 'Canada', 'Netherlands', 'Belgium', 'India', 'Peru', 'Korea, South', 'Israel', 'United Arab Emirates', 'Qatar', 'Belarus', 'Singapore', 'Ireland', 'Sweden', 'Chile', 'Pakistan', 'Mexico', 'Portugal', 'Switzerland', 'Ecuador', 'Saudi Arabia', 'China', 'Russia', 'Turkey', 'Brazil', 'Iran', 'Italy', 'Spain', 'United Kingdom', 'France', 'Germany'], 'leaves': [28, 3, 16, 1, 9, 18, 14, 12, 29, 20, 0, 23, 11, 25, 4, 17, 15, 19, 26, 6, 22, 5, 21, 27, 2, 10, 13, 24, 30, 7, 8], 'color_list': ['C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C0'], 'leaves_color_list': ['C0', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1']}
    plt.show();

    """
