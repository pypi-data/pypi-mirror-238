def m18():
    """
    16  18회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from imblearn.over_sampling import RandomOverSampler
    from collections import Counter
    from datetime import datetime
    from sklearn.preprocessing import OneHotEncoder, StandardScaler, KBinsDiscretizer
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve, f1_score
    from sklearn import set_config
    set_config(display="diagram")

    16.1 머신러닝
    시험 데이터 : ID, grade, days, count, amount
    grade가 0, 1, 2, 3, 4인 다중 분류 문제
    시험 문제와 비슷한 데이터가 없어서 다른 데이터로 대체
    Data descriptions

    Zillow의 집값에 대한 데이터로 각 행은 고유한 주택을 나타냅니다. 주어진 설명변수로 주택가격 범위를 예측하는 다중분류 문제입니다.

    uid: A unique identifier
    city: 텍사스 주 오스틴 주변 마을
    description: Zillow list에 대한 설명
    latitude: Latitude
    longitude: Longitude
    garageSpaces: 차고의 수
    hasSpa: spa 공간의 유무
    yearBuilt: 건축년도
    numOfPatioAndPorchFeatures: patio or 베란다의 개수
    lotSizeSqFt: 거실 포함 부동산 부지 크기
    avgSchoolRating: 학교 유형에 따른 평균 학교 등급
    MedianStudentsPerTeacher: Zillow list에 있는 모든 학교의 교사당 학생 수 중앙값
    numOfBathrooms: 욕실의 수
    numOfBedrooms: 침실의 수
    priceRange: price ranges
    dat = pd.read_csv("./data/ex_data/house.csv")
    dat = dat.drop(['description', 'uid'], axis = 1)

    dat = dat.clean_names()

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10000 entries, 0 to 9999
    Data columns (total 14 columns):
     #   Column                      Non-Null Count  Dtype  
    ---  ------                      --------------  -----  
     0   city                        10000 non-null  object 
     1   hometype                    10000 non-null  object 
     2   latitude                    10000 non-null  float64
     3   longitude                   10000 non-null  float64
     4   garagespaces                10000 non-null  int64  
     5   hasspa                      10000 non-null  bool   
     6   yearbuilt                   10000 non-null  int64  
     7   numofpatioandporchfeatures  10000 non-null  int64  
     8   lotsizesqft                 10000 non-null  float64
     9   avgschoolrating             10000 non-null  float64
     10  medianstudentsperteacher    10000 non-null  int64  
     11  numofbathrooms              10000 non-null  float64
     12  numofbedrooms               10000 non-null  int64  
     13  pricerange                  10000 non-null  object 
    dtypes: bool(1), float64(5), int64(5), object(3)
    memory usage: 1.0+ MB
    y = dat['pricerange']
    X = dat.drop(['pricerange'], axis = 1)

    16.1.1 EDA를 실시하시오(시각화 포함).
    dat.describe()

               latitude     longitude  ...  numofbathrooms  numofbedrooms
    count  10000.000000  10000.000000  ...    10000.000000   10000.000000
    mean      30.291191    -97.778476  ...        2.692100       3.449200
    std        0.097075      0.084543  ...        0.979206       0.813441
    min       30.085030    -98.020477  ...        1.000000       1.000000
    25%       30.202516    -97.838594  ...        2.000000       3.000000
    50%       30.283664    -97.769680  ...        3.000000       3.000000
    75%       30.366375    -97.718313  ...        3.000000       4.000000
    max       30.517323    -97.570633  ...       10.000000      10.000000

    [8 rows x 10 columns]
    dat.hist();
    plt.subplots_adjust(top=0.9, hspace = 0.9, wspace = 0.5);
    plt.show();



    sns.countplot(dat['city'])
    plt.xticks(rotation=45);
    plt.show();



    sns.countplot(dat['hometype'])
    plt.xticks(rotation=45);
    plt.show();



    sns.countplot(dat['pricerange'])
    plt.xticks(rotation=45);
    plt.show();



    16.1.2 결측치를 처리하시오.
    dat.isna().sum()

    city                          0
    hometype                      0
    latitude                      0
    longitude                     0
    garagespaces                  0
    hasspa                        0
    yearbuilt                     0
    numofpatioandporchfeatures    0
    lotsizesqft                   0
    avgschoolrating               0
    medianstudentsperteacher      0
    numofbathrooms                0
    numofbedrooms                 0
    pricerange                    0
    dtype: int64
    결측치 존재 x
    16.1.3 파생변수를 2개 생성하고, 생성 이유를 기술하시오.
    sns.scatterplot(x='latitude', 
                    y='longitude', 
                    hue='pricerange',
                    s=50, # marker size
                    data=dat)
    plt.show();



    dat['location'] = np.where(dat['longitude'] >= -97.7, 1, 
    np.where((dat['latitude']<=30.2) &(dat['longitude']<= -97.7), 2, 3))

    sns.scatterplot(x='latitude', 
                    y='longitude', 
                    hue='location',
                    s=50, # marker size
                    data=dat)
    plt.show();



    freq = dat['hometype'].value_counts(normalize = True)
    prob_columns = dat['hometype'].map(freq)
    dat['hometype'] = dat['hometype'].mask(prob_columns < 0.1, 'other')
    dat['hometype'].value_counts()

    hometype
    Single Family    9427
    other             573
    Name: count, dtype: int64
    freq = dat['city'].value_counts(normalize = True)
    prob_columns = dat['city'].map(freq)
    dat['city'] = dat['city'].mask(prob_columns < 0.1, 'other')
    dat['city'].value_counts()

    city
    austin    9898
    other      102
    Name: count, dtype: int64
    num_columns = X.select_dtypes('number').columns.tolist()
    cat_columns = X.select_dtypes(['object', 'bool']).columns.tolist()

    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        StandardScaler()
    )


    preprocess = ColumnTransformer(
        [
         ("num", num_preprocess, num_columns),
         ("cat", cat_preprocess, cat_columns)
         ]
    )

    pre_dat_X = preprocess.fit_transform(X)

    16.1.4 train/test를 7:3으로 분할하시오.
    train_X, test_X, train_y, test_y = train_test_split(pre_dat_X, y, test_size = 0.2, stratify = y, random_state = 0)

    16.1.5 SOM을 실시하고, confusion matrix를 출력하시오.
    SOM(Self Organizing Map)은 고차원 데이터를 군집화하기 위한 신경망의 일종으로, 위상 구조를 유지하면서 고차원 데이터를 저차원으로 매핑하는 방법입니다.



    그림에서 input vector는 데이터의 행 벡터를 의미합니다. 실제로는 행 벡터를 쌓은 전체 데이터가 input matrix로 들어갑니다. 또한 feature map의 각 노드에는 여러 개의 입력 벡터가 들어올 수 있습니다. weight는 feature map의 각 노드의 위치를 표현하는 값입니다. weight matrix를 적절하게 업데이트해서 데이터에 맞게 매핑하는 것이 som의 기본 원리입니다.

    weight 초기화

    유클리디안 거리를 이용해서 best matching unit(BMU) 선택

    Example



    유클리디안 거리가 가장 가까운 노드를 BMU로 선택

    best matching unit(BMU)과 인접 노드의 weight 업데이트

    이웃은 반지름(radius)를 이용해서 지정

    feature map의 크기가 
    의 경우 radius = 
     추천(정답없음)

    2~3번 사전에 설정된 반복횟수만큼 반복

    #from sklearn_som.som import SOM
    from minisom import MiniSom  

    def classify(som, data):
        "Classifies each sample in data in one of the classes definited
        using the method labels_map.
        Returns a list of the same length of data where the i-th element
        is the class assigned to data[i].
        "
        winmap = som.labels_map(train_X, train_y)
        default_class = np.sum(list(winmap.values())).most_common()[0][0]
        result = []
        for d in data:
            win_position = som.winner(d)
            if win_position in winmap:
                result.append(winmap[win_position].most_common()[0][0])
            else:
                result.append(default_class)
        return result

    som = MiniSom(10, 10, train_X.shape[1], sigma=3, learning_rate=0.5, 
                  neighborhood_function='triangle', random_seed=10)

    som.pca_weights_init(train_X) # numpy.array로 넣어줘야됨
    som.train_random(train_X, 500, verbose=False)
    print(classification_report(test_y, classify(som, test_X)))

                   precision    recall  f1-score   support

         0-250000       0.59      0.32      0.41       250
    250000-350000       0.46      0.63      0.53       471
    350000-450000       0.43      0.32      0.37       460
    450000-650000       0.42      0.40      0.41       455
          650000+       0.54      0.66      0.59       364

         accuracy                           0.47      2000
        macro avg       0.49      0.47      0.46      2000
     weighted avg       0.47      0.47      0.46      2000
    16.1.6 Random forest, 다층신경망 포함 분류모형을 4개 구축하고, F1 score, ROC curve를 생성하시오.
    cat_encoder = preprocess.named_transformers_["cat"]["onehotencoder"]
    cat_names = list(cat_encoder.get_feature_names())
    full_name = num_columns + cat_names
    train_X = pd.DataFrame(train_X, columns = full_name)
    test_X = pd.DataFrame(test_X, columns = full_name)

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Random forest

    from sklearn.ensemble import RandomForestClassifier
    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}
    rf_pipe = Pipeline(
        [
            ("classifier", RandomForestClassifier(random_state=42))
        ]
    )

    RandomForest_search = GridSearchCV(estimator = rf_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'balanced_accuracy')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV

    RandomForestClassifier
    print('RandomForest best score : ', RandomForest_search.best_score_)

    RandomForest best score :  0.6070264172412683
    mlp

    normalize를 해줬을 때, gradient descent로 최적 해를 구할 때 속도 개선 가능, 지역 최적해로 수렴하는 현상 개선 가능
    from sklearn.neural_network import MLPClassifier

    mlp_pipe = Pipeline(
        [
            ("classifier", MLPClassifier())
        ]
    )

    MLP_param = {'classifier__learning_rate_init': np.arange(0.01, 0.2, 0.02)}

    MLP_search = GridSearchCV(estimator = mlp_pipe, 
                          param_grid = MLP_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    MLP_search.fit(train_X, train_y)

    GridSearchCV

    MLPClassifier
    print('MLP best score : ', MLP_search.best_score_)

    MLP best score :  0.5765511171336651
    lightgbm

    from lightgbm import LGBMClassifier

    pipe_lgb = Pipeline(
        [
            ("classifier", LGBMClassifier())
        ]
    )
    #LGBMClassifier().get_params()
    lgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}

    lgb_search = GridSearchCV(estimator = pipe_lgb, 
                          param_grid = lgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    lgb_search.fit(train_X, train_y)

    GridSearchCV

    LGBMClassifier
    print('LGBM best score : ', lgb_search.best_score_)

    LGBM best score :  0.6094230147478779
    Decision tree

    from sklearn.tree import DecisionTreeClassifier

    dt_pipe = Pipeline(
        [
            ("classifier", DecisionTreeClassifier()) # defaut : 'ovr'
        ]
    )

    decisiontree_param = {'classifier__ccp_alpha': np.arange(0.1, 1, 0.1)}

    decisiontree_search = GridSearchCV(estimator = dt_pipe, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV

    DecisionTreeClassifier
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.2
    balanced accuracy 비교 결과 Random forest 모형을 선택한다.

    pred_rf = RandomForest_search.predict(test_X)
    print(classification_report(test_y, pred_rf))

                   precision    recall  f1-score   support

         0-250000       0.67      0.52      0.59       250
    250000-350000       0.59      0.63      0.61       471
    350000-450000       0.51      0.51      0.51       460
    450000-650000       0.56      0.58      0.57       455
          650000+       0.75      0.75      0.75       364

         accuracy                           0.60      2000
        macro avg       0.61      0.60      0.60      2000
     weighted avg       0.60      0.60      0.60      2000
    print(balanced_accuracy_score(test_y, pred_rf))

    0.5991623827478716
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.59인 것을 확인할 수 있다.

    ROC curve

    from sklearn.preprocessing import label_binarize
    from itertools import cycle
    from sklearn.metrics import roc_curve, auc

    y_score = RandomForest_search.predict_proba(test_X)
    test_y.value_counts()

    pricerange
    250000-350000    471
    350000-450000    460
    450000-650000    455
    650000+          364
    0-250000         250
    Name: count, dtype: int64
    y_index = {'0-250000': 0, '250000-350000': 1, '350000-450000': 2, '450000-650000': 3, '650000+': 4}

    test_y = [y_index[item] for item in test_y]

    y_test_bin = label_binarize(test_y, classes=[0, 1, 2, 3, 4])
    n_classes = y_test_bin.shape[1]

    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    colors = cycle(['blue', 'red', 'green'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                 ''.format(i, roc_auc[i]));

    plt.plot([0, 1], [0, 1], 'k--');
    plt.xlim([-0.05, 1.0]);
    plt.ylim([0.0, 1.05]);
    plt.xlabel('False Positive Rate');
    plt.ylabel('True Positive Rate');
    plt.title('Receiver operating characteristic for multi-class data');
    plt.legend(loc="lower right");
    plt.show();



    16.2 텍스트 마이닝(영어)
    16.2.1 빈출명사 top10을 bar chart로 시각화하시오.
    file = open("./data/ex_data/wikistat.txt", mode='r', encoding='cp949')
    doc = file.read()
    file.close()

    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform([doc])
    word_counts = pd.DataFrame(matrix.toarray(),
                          columns=vectorizer.get_feature_names())

    word_counts

       18th  5th  actual  additional  ...  variability  variation  working  years
    0     1    1       1           1  ...            1          2        1      1

    [1 rows x 199 columns]
    (
    word_counts
               .T
               .sort_values(by=0, ascending=False)
               .head(10)
               .plot(kind = 'bar', legend = False)
    )

    <Axes: >
    plt.show();



    16.3 시계열분석


    frequency 값 지정 시 참고

    ex8_2b 데이터는 데이터 설명이 따로 없는 예제 데이터이므로 freq 지정 안함

    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf, pacf

    dat = pd.read_csv('./data/ex_data/timeseries/ex8_2b.csv')

    # with open('./data/ex_data/timeseries/ex8_2b.txt') as file:
    #     data = file.read().split()
    # dat = pd.DataFrame(data, columns = ['value'])

    16.3.1 정상성 확인
    정상성 만족

    추세가 존재하지 않고, 시간에 따라 분산이 증가 혹은 감소하는 패턴이 없으며, acf도 1~2시차를 제외하면 모두 신뢰구간 안에 포함하는 것을 확인할 수 있음

    kpss test 결과 유의수준 0.05에서 p-value = 0.1 로 크기 때문에 귀무가설을 기각할 수 없음, 해당 데이터는 정상성을 만족함

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    dat.plot(ax = ax1)

    <Axes: >
    plot_acf(dat.value, ax2)

    <Figure size 3200x1200 with 2 Axes>
    plt.show();



    from statsmodels.tsa.stattools import kpss
    print('test statistic: %f' % kpss(dat)[0])

    test statistic: 0.169926
    print('p-value: %f' % kpss(dat)[1])

    p-value: 0.100000
    16.3.2 ARIMA 모델 3가지 제시
    AR(1)

    ACF 감소, PACF 절단
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat, order=(1,0,0), trend = 'c').fit()
    print(model.summary())

                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  value   No. Observations:                  100
    Model:                 ARIMA(1, 0, 0)   Log Likelihood                -257.078
    Date:                Mon, 30 Oct 2023   AIC                            520.156
    Time:                        23:29:24   BIC                            527.972
    Sample:                             0   HQIC                           523.319
                                    - 100                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    const        100.4527      0.864    116.330      0.000      98.760     102.145
    ar.L1          0.6231      0.089      7.038      0.000       0.450       0.797
    sigma2         9.9620      1.177      8.462      0.000       7.655      12.269
    ===================================================================================
    Ljung-Box (L1) (Q):                   1.05   Jarque-Bera (JB):                 5.61
    Prob(Q):                              0.31   Prob(JB):                         0.06
    Heteroskedasticity (H):               2.80   Skew:                            -0.32
    Prob(H) (two-sided):                  0.00   Kurtosis:                         3.97
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    신뢰구간을 확인해본 결과, 절편 포함 ma1항 모두 신뢰구간에 0을 포함하지 않으므로 유의함

    가정 만족
    sm.stats.acorr_ljungbox(model.resid, lags=[10])

         lb_stat  lb_pvalue
    10  7.062426   0.719539
     : 
     ~ 
     시차 시까지 잔차 사이에 자기상관이 없다.

    ljung box test 결과 유의수준 0.05에서 Q* = 7.062426, p-value = 0.719539로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 10시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.

    model.resid.plot()

    <Axes: >
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model.resid, ax = ax1)

    <Figure size 3200x1200 with 2 Axes>
    model.resid.hist(ax = ax2)

    <Axes: >
    plt.show();



    잔차의 acf plot을 확인해본 결과 대체로 신뢰구간 안에 값이 포함되어 있는 것을 확인할 수 있다.

    잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.

    잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.

     잠정 모형으로 선택

    auto.arima

    import pmdarima as pm

    model2 = pm.auto_arima(dat.value, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=1,          
                       seasonal=False,   
                       start_P=0, 
                       D=None, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,0,0)(0,0,0)[0]             : AIC=1208.175, Time=0.00 sec
     ARIMA(1,0,0)(0,0,0)[0]             : AIC=inf, Time=0.01 sec
     ARIMA(0,0,1)(0,0,0)[0]             : AIC=inf, Time=0.06 sec
     ARIMA(1,0,1)(0,0,0)[0]             : AIC=535.268, Time=0.02 sec
     ARIMA(2,0,1)(0,0,0)[0]             : AIC=536.654, Time=0.02 sec
     ARIMA(1,0,2)(0,0,0)[0]             : AIC=537.266, Time=0.03 sec
     ARIMA(0,0,2)(0,0,0)[0]             : AIC=inf, Time=0.03 sec
     ARIMA(2,0,0)(0,0,0)[0]             : AIC=inf, Time=0.02 sec
     ARIMA(2,0,2)(0,0,0)[0]             : AIC=538.261, Time=0.04 sec
     ARIMA(1,0,1)(0,0,0)[0] intercept   : AIC=520.136, Time=0.06 sec
     ARIMA(0,0,1)(0,0,0)[0] intercept   : AIC=539.552, Time=0.01 sec
     ARIMA(1,0,0)(0,0,0)[0] intercept   : AIC=520.164, Time=0.02 sec
     ARIMA(2,0,1)(0,0,0)[0] intercept   : AIC=520.152, Time=0.05 sec
     ARIMA(1,0,2)(0,0,0)[0] intercept   : AIC=517.986, Time=0.10 sec
     ARIMA(0,0,2)(0,0,0)[0] intercept   : AIC=523.566, Time=0.02 sec
     ARIMA(2,0,2)(0,0,0)[0] intercept   : AIC=520.296, Time=0.05 sec
     ARIMA(1,0,3)(0,0,0)[0] intercept   : AIC=520.035, Time=0.09 sec
     ARIMA(0,0,3)(0,0,0)[0] intercept   : AIC=518.931, Time=0.02 sec
     ARIMA(2,0,3)(0,0,0)[0] intercept   : AIC=521.979, Time=0.10 sec

    Best model:  ARIMA(1,0,2)(0,0,0)[0] intercept
    Total fit time: 0.757 seconds
    ma1 모수 비유의
    model2.summary()

    <class 'statsmodels.iolib.summary.Summary'>
   
                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                      y   No. Observations:                  100
    Model:               SARIMAX(1, 0, 2)   Log Likelihood                -253.993
    Date:                Mon, 30 Oct 2023   AIC                            517.986
    Time:                        23:29:27   BIC                            531.012
    Sample:                             0   HQIC                           523.258
                                    - 100                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    intercept     46.0366     17.730      2.596      0.009      11.286      80.787
    ar.L1          0.5418      0.177      3.064      0.002       0.195       0.888
    ma.L1         -0.0110      0.187     -0.059      0.953      -0.377       0.355
    ma.L2          0.2920      0.147      1.988      0.047       0.004       0.580
    sigma2         9.3555      1.178      7.942      0.000       7.047      11.664
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.01   Jarque-Bera (JB):                 4.96
    Prob(Q):                              0.94   Prob(JB):                         0.08
    Heteroskedasticity (H):               2.39   Skew:                            -0.30
    Prob(H) (two-sided):                  0.01   Kurtosis:                         3.92
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    
    비유의한 모수 제외 후 모든 모수 유의
    model3 = ARIMA(dat.value, order=(1, 0, [0, 1]), trend ='c').fit()
    print(model3.summary())

                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  value   No. Observations:                  100
    Model:               ARIMA(1, 0, [2])   Log Likelihood                -253.993
    Date:                Mon, 30 Oct 2023   AIC                            515.987
    Time:                        23:29:28   BIC                            526.408
    Sample:                             0   HQIC                           520.204
                                    - 100                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    const        100.4733      0.883    113.777      0.000      98.742     102.204
    ar.L1          0.5315      0.112      4.756      0.000       0.312       0.751
    ma.L2          0.2974      0.139      2.148      0.032       0.026       0.569
    sigma2         9.3483      1.157      8.083      0.000       7.081      11.615
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.00   Jarque-Bera (JB):                 5.01
    Prob(Q):                              0.95   Prob(JB):                         0.08
    Heteroskedasticity (H):               2.39   Skew:                            -0.30
    Prob(H) (two-sided):                  0.01   Kurtosis:                         3.92
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    가정 만족
    sm.stats.acorr_ljungbox(model3.resid, lags=[10])

         lb_stat  lb_pvalue
    10  1.724681   0.998048
    pm.tsdisplay(model3.resid, lag_max=20, title="", show=True)



    16.3.3 최적 모델 선택, 이유 설명
    ma1 항이 제거된 ARMA(1,2) 모형

    print(model.aic)

    520.1563632603085
    print(model3.aic)

    515.9869099700779
    print(model.bic)

    527.9718738182728
    print(model3.bic)

    526.4075907140303
    16.3.4 선행 시차까지 예측 및 실제 결과와 비교 시각화(평가지표를 선택한 이유 제시)
    train/test 데이터 분할 후 적합했을 때 그릴 수 있음

    시계열분석 자료 예제 참고

    RMSE : 직관적인 지표이지만, 크기에 영향을 받기 때문에 모델별로 비교할 때 주의 필요

    MAPE : 크기에 의존적인 RMSE의 단점을 극복함, 0 값 근처에 값이 생성될 경우 값이 너무 커지는 문제가 있음

    MASE 25회 기출 작성 내용 참고

    fore = model3.forecast(steps=27, alpha=0.05)

    fig, ax = plt.subplots(1, 1, figsize = (15, 5))
    ax.plot(dat.value)

    [<matplotlib.lines.Line2D object at 0x17ed4be20>]
    ax.plot(fore)

    [<matplotlib.lines.Line2D object at 0x17ed4bdc0>]
    plt.show();
    """
