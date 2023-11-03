def m24():
    """
     24회차 기출문제
    22.1 머신러닝
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from sklearn.preprocessing import StandardScaler
    from datetime import datetime
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve
    from sklearn import set_config
    set_config(display="diagram")

    22.1.1 Data description
    sex : 성별

    age : 나이

    pstatus : 부모와의 동거 유무(T : 동거 o, A : 동거 x)

    medu : 엄마의 교육수준

    0 : none

    1 : 초등교육(초등학교)

    2 : 5 ~ 9th edu

    3 : 중등교육(중학교, 고등학교)

    4 : 고등교육(대학, 대학원수준)

    fedu : 아빠의 교육수준

    0 : none

    1 : 초등교육(초등학교)

    2 : 5 ~ 9th edu(5~9학년)

    3 : 중등교육(중학교, 고등학교)

    4 : 고등교육(대학, 대학원수준)

    guardian : 주보호자

    어머니

    아버지

    기타

    traveltime : 등하교기간

    1 : 15분 이하

    2 : 15분 ~ 30분 이하

    3 : 30분 ~ 1시간 이하

    4 : 1시간 이상

    studytime : 학습시간

    1 : 2시간 이하

    2 : 2~5시간 이하

    3 : 5~10시간 이하

    4 : 10시간 이상

    failure : 학사경고 횟수

    freetime : 자유시간(1 : 매우 낮음 ~ 5 : 매우 높음)

    famrel : 가족관계(1 : 매우나쁨 ~ 5 : 매우우수)

    데이터 불러오기

    dat = pd.read_csv('./data/adp24.csv')
    dat = dat.clean_names()

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 395 entries, 0 to 394
    Data columns (total 12 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   sex         395 non-null    object 
     1   age         395 non-null    int64  
     2   pstatus     395 non-null    object 
     3   medu        391 non-null    float64
     4   fedu        395 non-null    int64  
     5   guardian    395 non-null    object 
     6   traveltime  395 non-null    int64  
     7   studytime   395 non-null    int64  
     8   failures    395 non-null    int64  
     9   freetime    395 non-null    int64  
     10  famrel      395 non-null    int64  
     11  absences    389 non-null    float64
    dtypes: float64(2), int64(7), object(3)
    memory usage: 37.2+ KB
    dat = dat.astype({'traveltime' : 'object', 'studytime' : 'object', 'freetime' : 'object', 'famrel' : 'object'})

    22.1.2 탐색적 데이터 분석을 실시하시오. 논리적이고 타당한 근거를 들어 작성하시오.(시각화 포함)
    범주형 변수 시각화

    dat.select_dtypes('object').columns

    Index(['sex', 'pstatus', 'guardian', 'traveltime', 'studytime', 'freetime',
           'famrel'],
          dtype='object')
    f, axes = plt.subplots(nrows = 3, ncols = 3, figsize = (20,4))
    sns.countplot(dat['sex'], ax = axes[0, 0])
    sns.countplot(dat['pstatus'], ax = axes[0, 1])
    sns.countplot(dat['medu'], ax = axes[0, 2])
    sns.countplot(dat['fedu'], ax = axes[1, 0])
    sns.countplot(dat['guardian'], ax = axes[1, 1])
    sns.countplot(dat['traveltime'], ax = axes[1, 2])
    sns.countplot(dat['studytime'], ax = axes[2, 0])
    sns.countplot(dat['freetime'], ax = axes[2, 1])
    sns.countplot(dat['famrel'], ax = axes[2, 2])
    plt.subplots_adjust(top=0.9, hspace = 0.5, wspace = 0.3)              
    plt.show();



    가족관계(famrel)의 경우 1~2에 해당하는 빈도가 매우 작으므로, class 불균형이 의심됨

    아빠의 교육수준(fedu)의 경우 0에 해당하는 빈도가 매우 작으므로, class 불균형이 의심됨

    엄마의 교육수준(medu)의 경우 0에 해당하는 빈도가 매우 작으므로, class 불균형이 의심되며, 또한 결측치가 존재함

    traveltime의 경우 3~4에 해당하는 빈도가 매우 작으므로, class 불균형이 의심됨

    연속형 변수 시각화

    dat.select_dtypes('number').hist();
    plt.show();



    결석횟수(absences)의 경우 우측으로 긴꼬리를 갖는 분포로 보임. 40회 이상 결석한 경우가 존재하므로 이상치를 확인해볼 필요가 있음

    age의 경우 15~19세가 가장 많고, 20세 이상인 경우도 존재함

    학사경고횟수(failures)의 경우 0회가 가장 많고, 1~3회가 순임

    결측치 확인

    dat.isna().sum()

    sex           0
    age           0
    pstatus       0
    medu          4
    fedu          0
    guardian      0
    traveltime    0
    studytime     0
    failures      0
    freetime      0
    famrel        0
    absences      6
    dtype: int64
    medu, absences에 결측치가 존재함. 적절한 결측치 대치 방법을 통해 처리해줄 필요가 있음
    변수 간 관계 시각화

    corr = dat.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.show()



    f, axes = plt.subplots(ncols = 2, figsize = (20,4))
    sns.boxplot(x = "guardian", y = "absences", data = dat, ax = axes[0])
    axes[0].set_title('guardian vs absences boxplot')
    sns.boxplot(x = "sex", y = "absences", data = dat, ax = axes[1])
    axes[1].set_title('sex vs absences boxplot')
    plt.show();



    주보호자가 부모님이 아닌 other의 경우 결석횟수가 높은 경향이 있음

    성별에 따른 결석횟수는 차이가 없어보이지만, 여성의 경우 남성에 비해 결석횟수가 40회 이상인 관측치가 존재함

    plt.clf()
    f, axes = plt.subplots(ncols = 2, figsize = (20,4))
    sns.boxplot(x = "famrel", y = "absences", data = dat, ax = axes[0])
    axes[0].set_title('famrel vs absences boxplot')
    sns.boxplot(x = "pstatus", y = "absences", data = dat, ax = axes[1])
    axes[1].set_title('pstatus vs absences boxplot')
    plt.show();



    가족관계(famrel)가 4~5로 좋음에도 불구하고 결석횟수가 40회 이상인 케이스가 존재함

    부모와 동거를 안하는 경우 결석횟수가 더 높은 경향이 있으며, 부모와 동거를 안하는 경우 결석횟수가 80회 이상인 케이스가 존재함

    22.1.3 탐색적 데이터 분석을 통해 데이터를 전처리 하는 과정을 거치시오. 전처리를 통해, 향후 예측분석에 미칠 영향을 논리적이고 타당한 근거를 들어 제시하시오.(시각화 포함)
    dat = dat.dropna(subset = ['absences'])

    absences의 경우 전체 데이터에서 결측치가 6개 존재하며, target variable로 결측치가 존재할 경우 모형 성능을 평가하기 어려우므로, 데이터를 삭제함
    y = dat.absences
    X = dat.drop(['absences'], axis = 1)
    cat_columns = X.select_dtypes('object').columns

    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.impute import KNNImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline

    impute_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5, initial_strategy = 'most_frequent')
    )
    encoding_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer(
        [("imputation", impute_preprocess, ['medu']), 
         ("cat", encoding_preprocess, cat_columns)], 
         remainder='passthrough'
    )

    결측치 대치

    연속형 변수인 absences의 경우 Random forest를 이용해서 결측치를 대치함 결측치를 처리하는 방법은 크게 대표값을 이용하는 방법과 모델을 이용하는 방법이 있다.
    대표값을 이용한 방법 중 대표적으로 평균대치법이 있다. 평균대치법은 해당 변수의 대표값인 평균으로 결측치를 대치하는 방법으로 단점으로는 결측치 수가 많을 때 분포가 왜곡되는 문제가 있을 수 있다.

    모델을 이용한 방법 중 대표적으로 Random forest를 이용한 방법이 있다. Random forest를 이용한 방법은 boostrap sample에서 개별 tree를 생성하고, 개별 tree에서 나온 예측값을 평균내서 나온 값을 이용해서 결측치를 대치하는 방법이다.

    Random forest를 이용해서 결측치를 대치한 이유는 대표값을 이용하는 방법에 비해서 다른 변수의 정보를 이용해서 결측치를 대치할 수 있기 때문에 더 많은 정보를 활용해서 결측치를 대치할 수 있기 때문이다.

    범주형 변수 인코딩

    범주형 변수에 대해 원핫인코딩을 실시해줌

    범주형 변수 변환 방법은 크게 3가지가 있다. 첫 번째로, label encoding 방법은 범주형 변수의 각 값에 알파벳 순서대로 정수값을 할당하는 방법이다. 두 번째로, one-hot encoding 방법은 범주형 변수의 각 수준(levels)별로 변수를 생성하며, 생성된 개별 변수는 각 수준에 해당하는 경우 1, 해당하지 않는 경우 0으로 구성된다. 세 번째로, dummy coding의 경우 one-hot encoding과 유사하지만 각 수준(levels) - 1개 만큼 변수를 생성하며, 생성된 개별 변수는 각 수준에 해당하는 경우 1, 해당하지 않는 경우 0으로 구성된다.

    이 중 one-hot encoding을 선택한 이유는 label encoding과 비교했을 때, 범주에 수치정보가 반영되는 문제점이 없으며, 범주형 변수의 각 수준(levels)이 크지 않기 때문에 one-hot encoding의 문제점 중 하나인 차원이 늘어남에 따라 계산량이 증가하는 문제 또한 미미하기 때문이다. 또한 앞으로 적합시킬 모델이 glm 계열 모델이 아니기 때문에 one-hot encoding의 문제점 중 하나인 glm 모델일 때 범주형 변수 간의 다중공선성 문제 또한 없기 때문이다.

    이상치 처리

    EDA 결과 이상치로 의심되는 관측치에 대해서 변수 간 의미를 파악해보면, absences가 40회 이상인 경우는 전부 여성이며, 특이 사항으로는 가족관계가 4~5점으로 매우 좋지만, 결석횟수가 높다. 다만 종합적으로 판단했을 때, 실생활에서 충분히 발생할 수 있는 케이스이므로 이상치로 판단하고 제거하지 않았다.

    22.1.4 전처리를 진행하는데 시간이 부족하여 수행하지 못한 전처리 기법과 수행 방법을 제시하고, 향후 예측분석에 미칠 영향을 논리적이고 타당한 근거를 들어 제시하시오.
    범주형 변수 class 축소
    범주형 변수의 class가 많을 경우, 범주형 변수 인코딩 시 차원이 늘어나는 문제가 있다. 이에 따라 모형 적합시 속도가 느려지는 단점이 있다. 따라서 의미가 퇴색되지 않는 선에서 각 범주형 변수의 class의 빈도가 너무 적을 경우 병합시키는 것이 적절할 것이다.

    freq = train_X['famrel'].value_counts(normalize = True)
    print(freq)

    famrel
    4    0.495177
    5    0.273312
    3    0.170418
    2    0.041801
    1    0.019293
    Name: proportion, dtype: float64
    prob_columns = train_X['famrel'].map(freq)
    train_X['famrel'] = train_X['famrel'].mask(prob_columns < 0.1, 'other')
    train_X['famrel'].value_counts()

    famrel
    4        154
    5         85
    3         53
    other     19
    Name: count, dtype: int64
    test_X['famrel'] = np.where(test_X['famrel'].isin([1, 2]), 'other', test_X['famrel'])

    test_X['famrel'].value_counts()

    famrel
    4        37
    5        19
    3        15
    other     7
    Name: count, dtype: int64

    train_X['famrel'] = train_X['famrel'].astype(str)
    test_X['famrel'] = test_X['famrel'].astype(str)

    22.1.5 위 데이터를 바탕으로 예측 분석에 적합한 알고리즘을 3개 이상 추천하고, 이들 중 2개를 선정하여 이를 선정한 이유를 타당한 근거를 들어 제시하시오.
    decision tree

    random forest

    XGBOOST

    알고리즘 설명, 해석력, 예측력 관점에서 서술

    22.1.6 예측분석을 적용하여 평가할 때의 평가 지표를 선정하고 평가 지표를 선정한 이유를 논리적이고 타당한 근거를 들어 제시하시오.
    MAE(이상치 처리를 안했을 때)
    EDA 결과 absences에 이상치로 의심되는 케이스가 존재함. RMSE에 비해 이상치에 비교적 강건한 MAE를 지표로 선택함

    22.1.7 선정한 2개의 알고리즘을 바탕으로 분석을 진행하고, 이를 선정한 평가지표와 함께 나타내시오. (시각화 포함)
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.impute import KNNImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold

    cat_columns = train_X.select_dtypes('object').columns

    impute_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5)
    )
    encoding_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer(
        [("imputation", impute_preprocess, ['medu']), 
         ("cat", encoding_preprocess, cat_columns)], 
         remainder='passthrough'
    )

    Decision tree

    from sklearn.tree import DecisionTreeRegressor
    full_pipe1 = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", DecisionTreeRegressor())
        ]
    )

    decisiontree_param = {'regressor__ccp_alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    decisiontree_search = GridSearchCV(estimator = full_pipe1, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_absolute_error')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    cat

    OneHotEncoder

    DecisionTreeRegressor
    print('decision tree best score : ', -decisiontree_search.best_score_)

    decision tree best score :  6.183806839789584
    Random forest

    full_pipe2 = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", RandomForestRegressor())
        ]
    )

    RandomForest_param = {'regressor__max_features': np.arange(0.5, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_search = GridSearchCV(estimator = full_pipe2, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_absolute_error')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    cat

    OneHotEncoder

    RandomForestRegressor
    print('Random Forest best score : ', -RandomForest_search.best_score_)

    Random Forest best score :  5.69306394313998
    지표별 시각화

    cv_result1 = pd.DataFrame(decisiontree_search.cv_results_)
    cv_result2 = pd.DataFrame(RandomForest_search.cv_results_)

    cv_result1['mean_test_score'] = np.absolute(cv_result1['mean_test_score'])
    cv_result2['mean_test_score'] = np.absolute(cv_result2['mean_test_score'])

    cv_result1.plot(x = 'param_regressor__ccp_alpha', y = 'mean_test_score')
    plt.show();



    cv_result2.plot(x = 'param_regressor__max_features', y = 'mean_test_score')
    plt.show();



    22.1.8 위에서 구축한 모델의 일반화 가능성에 대해서 논리적으로 타당한 근거를 바탕으로 제시하시오.
    교차검증 결과를 바탕으로 Random forest 모형을 선택한다. 최종 검증 데이터에 적용했을 때 성능을 보면 MAE = 4.55인 것을 확인할 수 있다.

    print('테스트 MAE score :', np.absolute(RandomForest_search.score(test_X, test_y)))

    테스트 MAE score : 4.565314407814408
    방법2

    해당 모형이 새로운 데이터셋이 들어왔을 때에도 비슷한 예측력을 보이는지로 해석해볼 수 있음

    train/test를 묶은 all data set에서 새로운 데이터셋을 랜덤샘플로 생성함

    tuning 완료한 모형에 대해서 새로운 데이터셋을 적용했을 때, 예측값과 실제값의 상관관계가 대체로 0.7 ~ 0.8 정도로 나오므로 일반화 가능

    pred = RandomForest_search.predict(test_X)
    np.corrcoef(pred, test_y)[0,1]

    0.19906684836893587
    train = pd.concat([train_X, train_y], axis = 1)
    test = pd.concat([test_X, test_y], axis = 1)

    all_dat = pd.concat([train, test], axis = 0)

    N = 1000
    cor_result = []
    for i in range(1, N):
        sub_dat = all_dat.sample(frac=0.6,random_state=i)
        pred = RandomForest_search.predict(sub_dat)
        cor_result.append(np.corrcoef(pred, sub_dat['absences'])[0,1])

    result = pd.DataFrame(cor_result, columns = ['cor'])
    result.plot(kind = 'box')
    plt.show();



    22.1.9 앞서 구축한 모델을 더욱 발전시키기 위한 방법을 서술하고 그 방법이 모델에 어떤 영향을 미칠 수 있는지를 타당한 근거를 들어 제시하시오.
    변수선택을 통해 예측에 필요한 변수를 뽑고, 계산 속도 및 예측 성능을 개선해볼 수 있음

    feature importance가 높은 변수를 선택

    recursive feature elimination을 통해 변수중요도가 낮은 변수를 하나씩 제거해가면서 모델의 성능을 보고 변수 선택을 해볼 수 있음

    absences와 연관이 있는 변수를 찾기 위해 통계 검정을 해보고 검정 결과 유의한 변수를 선택해볼 수 있음

    22.1.10 Example


    from sklearn.feature_selection import RFE, RFECV

    from sklearn.model_selection import RandomizedSearchCV

    full_pipe1_1 = Pipeline(
        [
            ("preprocess", preprocess),
            ('feat_sel', RFE(estimator=RandomForestRegressor(), step=1)),
            ("regressor", RandomForestRegressor())
        ]
    )       

    RandomForest_search_param2 = {
                           'feat_sel__n_features_to_select': [4,5,6,7,8,9,10], 
                           'regressor__max_features': np.arange(0.5, 1, 0.1)
                          }
    # 
    # search = RandomizedSearchCV(estimator=pipe,
    #                             param_distributions=decisiontree_param2, ...)
    # search.fit(X, y)

    RandomForest_search2 = GridSearchCV(estimator = full_pipe1_1, 
                          param_grid = RandomForest_search_param2, 
                          cv = cv,
                          scoring = 'neg_mean_absolute_error')
    RandomForest_search2.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    cat

    OneHotEncoder
    feat_sel: RFE

    RandomForestRegressor

    RandomForestRegressor
    RandomForest_search2.best_params_

    {'feat_sel__n_features_to_select': 9, 'regressor__max_features': 0.5}
    print('테스트 MAE score :', np.absolute(RandomForest_search2.score(test_X, test_y)))

    테스트 MAE score : 4.598533666120206
    """