def m8():
    """
    8  Modeling 1

    import pandas as pd 
    import numpy as np 
    import janitor
    from sklearn import set_config
    set_config(display="diagram")

    EDA에 이용했던 데이터를 다시 불러오겠습니다.

    dat = pd.read_csv('./data/ex_data/adp1.csv')
    y = dat.grade
    X = dat.drop(['grade'], axis = 1)

    from sklearn.model_selection import train_test_split

    데이터 전처리 전 data leakage 방지를 위해 데이터를 train/test로 분할합니다.

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    전처리 pipeline

    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.linear_model import LinearRegression

    num_columns = train_X.select_dtypes('number').columns.tolist()
    cat_columns = train_X.select_dtypes('object').columns.tolist()

    cat_preprocess = make_pipeline(
        #SimpleImputer(strategy="constant", fill_value="NA"),
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        SimpleImputer(strategy="mean"), 
        StandardScaler()
    )
    preprocess = ColumnTransformer(
        [("num", num_preprocess, num_columns),
        ("cat", cat_preprocess, cat_columns)]
    )
    preprocess

    ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder
    시험에서는 각 머신러닝 모델링 문제의 경우 나오는 형식이 정형화되어 있습니다. 따라서 해당 문제에 정확히 답변을 할 수 있을 만큼만 준비를 하면 됩니다. 나오는 기본적인 문제 형식은 다음과 같습니다.

    머신러닝 모형 선택 후 각 알고리즘의 공통점 제시

    각 모형에 대해 간략하게 서술

    모형별 공통점 도출(주관적)

    예측 분석에 적합한 알고리즘인지 설명(주관적)

    현업에서 모형을 이용할 때 주의 사항(주관적)

    속도 및 예측력 비교

    최적 모형 선택 후 선택 이유 제시

    속도 측면에서 모형 선택

    예측력 측면에서 모형 선택

    최종 모형 도출

    지금까지 기출에 나온 모형은 다음과 같습니다.

    SVM

    XGBOOST

    Random forest

    Multiple linear regression

    Ridge regression

    Lasso regression

    Neural network

    lightgbm

    sklearn 패키지에서 지원하는 모형 중 시험에 나올 수 있는 추가적인 모형은 다음과 같습니다.

    elastic net regression

    decision tree

    gbm

    knn

    etc..

    8.1 Pipeline
    전처리 및 모델링 과정에는 이전 챕터에서 설명한 sklearn 패키지의 Pipeline을 이용해보겠습니다.ADP 시험에서 Pipeline을 이용하는 이유는 여러가지 모델을 pipeline workflow를 이용해서 한번에 처리할 수 있기 때문에 시간을 절약할 수 있습니다.

    Pipeline workflow

    pipeline의 workflow는 모델을 적합하는 순서와 동일합니다.

    validation셋 생성
    튜닝할 초매개변수 지정
    모델 학습 및 최적의 초매개변수 선택
    test 데이터를 이용한 최종 예측
    Pipeline을 이용해서 학습할 때 주의점

    adp 시험은 모형 성능을 평가하는 시험이 아닙니다. 따라서 모델 튜닝 과정은 빠른 시간 내에 진행하고 넘어가는 것이 바람직합니다.

    validation set 구성 시 적당한 fold 값 지정(3~5)
    튜닝해야할 초매개변수 지정 시 너무 많은 파라미터를 넣지 말 것
    8.2 회귀 지표 선택 기준
    회귀지표의 경우 각 지표별로 다른 특징을 갖기 때문에 적절한 지표를 선택하는 것이 필요합니다.

    MSE : 


    MAE : 


    R-square : 


    MSE는 직관적으로 예측값과 실제값 사이의 평균 차이에 대한 측도입니다. 즉, MSE가 크다는 것은 예측값과 실제값 사이의 차이가 크다는 것을 의미합니다. MSE의 경우 일부 예측치에서 실제값과 차이가 클 경우, 차이는 제곱되기 때문에 MSE 값이 커지는 경향이 있습니다.

    이를 보정할 수 있는 것이 MAE입니다. MAE는 MSE와 달리 실제값과 예측값의 차이의 절대값을 이용하므로, 일부 예측치에서 실제값과 차이가 클 경우 MSE에 비해 변동이 크지 않습니다.

    R-square의 경우 반응변수의 변동을 모델이 얼마나 설명하는지에 대한 비율을 의미합니다. R-square는 반응변수의 변동에 의존합니다. 예를 들어 test 셋의 반응변수의 분산이 
    , 모델을 통해 구한 MSE가 
    이라고 가정해보겠습니다. 
    는 대략 
    입니다. 만약 또다른 test 셋에서 반응변수의 분산이 
    이고, 모델을 통해 구한 MSE가 
    이라고 가정해보면 
    는 대략 
    가 됩니다. 따라서 반응변수의 분산에 따라 
    은 변할 수 있습니다.

    또한 
    는 linear regression에서만 정상적으로 작동합니다. linear regression이 아닐 경우 
    로 분리되지 않기 때문에 
    를 그대로 사용할 수 없습니다. 이에 따라 모델별로 
    와 비슷한 측도로 
    를 따로 정의해서 사용합니다.

    따라서 정리하면 회귀문제에서는 기본적으로 MSE를 사용하고, 반응변수에 이상치가 많을 경우 MAE도 같이 고려해볼 수 있습니다. R-square의 경우 선형회귀모형에 한정해서 사용하고, 다른 모형을 이용할 경우 
    를 따로 지정해서 사용할 수 있습니다.

    8.3 분류 지표 선택 기준
    Accuracy : 정확도(분류 챕터 설명 참고)

    ROC : sensitivity, specificity로 구한 ROC curve 아래 면적(분류 챕터 설명 참고)

    balance 데이터의 경우 Accuracy, ROC 둘 다 사용해도 무관하지만, imbalance data의 경우 ROC를 사용해야 합니다. 따라서 시험에서는 그냥 ROC를 사용하는 것이 적절합니다.

    지표에 대한 자세한 설명은 분류 챕터에서 설명하겠습니다.

    Important
    GridSearchCV를 적용할 때, scoring 옵션에는 해당 지표에 맞는 별칭이 들어가야 합니다.

    평가 지표	별칭
    -MAE	‘neg_mean_absolute_error’
    -MSE	‘neg_mean_squared_error’
    -RMSE	‘neg_root_mean_squared_error’
    R squared	‘r2’
    평가지표	별칭
    accuracy	‘accuracy’
    balanced accuracy	‘balanced_accuracy’
    f1 score	‘f1’
    precision	‘precision’
    recall	‘recall’
    AUC	‘roc_auc’
    추가 지표 참고 : https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter

    8.4 Bias, variance trade off
    훈련 데이터 
    과 각 
    에 대응하는 
    가 존재할 때,



    로 표현할 수 있습니다. 
    은 irreducible error로 noise를 의미합니다. 머신러닝의 주요 목적은 
    와 최대한 가까운 
    를 찾는 것입니다. 따라서 
    가 훈련 데이터 내부의 평균제곱오차 뿐만 아니라 훈련 데이터 밖의 검증 데이터에서도 평균제곱오차가 최소라면 가장 이상적일 것입니다.

    검증 데이터에 대한 기대검정오차는 다음과 같이 세 가지로 분해될 수 있습니다.



    기대검정오차를 최소화하기 위해서는 
    과 
    를 최소화해야 합니다. 여기서 분산과 편향은 아래의 이미지에 나온 직관과 동일하지만, 모형 관점에서 보면 분산은 데이터가 바뀌었을 때,
    가 변하는 정도를 의미합니다. 편향은 
    의 평균과 실제값 사이의 차이를 의미합니다.



    하지만 편향과 분산은 trade off 관계이므로 동시에 최소화하는 것은 불가능합니다.



    편향과 분산 trade off 관계를 도식화한 그림을 보면 Model complexity(polynomial의 차수)가 복잡해질수록 total error는 일정 부분 감소하다가 빠르게 증가합니다. bias-variance 관점에서 보면 두 가지를 모두 낮추는 것은 불가능하므로 타협점을 찾는 것이 필요합니다.

    Example



    Prediction Error for K = 1 : 2.0974

    Prediction Error for K = 5 : 1.3907

    Prediction Error for K = 10 : 1.2469

    Prediction Error for K = 33 : 1.21589

    Prediction Error for K = 66 : 1.3760

    Prediction Error for K = 100 : 1.4286

    그래프를 보면 
    일 때, bias는 거의 0이지만, 분산은 매우 큰 unstable한 모델이 생성되는 것을 볼 수 있습니다. 
    가 커질수록 bias는 커지고, 분산은 작아지는 stable한 모형이 생성되는 것을 볼 수 있습니다. prediction error(새로운 관측치 
    에 대한 예측 오차)를 보면 bias-variance trade-off 그림과 같이 
    일 때 약 
    로 가장 크고, 
    일 때 가장 작아지고, 
    일 때, 다시 늘어나는 것을 볼 수 있습니다.

    8.5 KNN
    knn은 새로운 관측치가 주어졌을 때, 관측치 주변의 가장 가까운 이웃을 이용해서 분류 및 예측을 수행하는 방법입니다. 모델을 따로 학습하는 것이 아니라 새로운 데이터가 들어오고, 모든 계산이 될 때까지 연기되는 lazy learning의 일종입니다. 분류 문제의 경우 주로 major voting(다수결)로 분류되며, 회귀 문제의 경우 최근접 이웃 간의 평균값을 산출합니다.

    Example

    검은색 점은 train data이고, test data로 
     관측치가 들어온 경우입니다. 
    를 
    로 정할 경우 
    에 가장 가까운 이웃을 기준으로 2개의 관측치를 선택하고, 회귀 문제의 경우 평균을 내서 예측 결과를 산출합니다. 분류일 경우는 major voting(다수결)으로 이웃 중 가장 많은 범주를 예측값으로 산출합니다.



    이 때, 가까운 이웃을 정하는 기준이 필요합니다. 이웃을 정의하기 위해서 특정 거리 기준을 이용합니다. 많이 사용하는 거리 기준은 다음과 같습니다.

    유클리디안 거리 : 
    변수개수

    마할라노비스 거리 : 
    변수개수

    Note
    거리를 이용하기 때문에 스케일에 민감할 수 있으므로, 표준화를 진행해줘야 함

    최적의 
    는 cross validation을 통해 도출할 수 있습니다.

    from sklearn.neighbors import KNeighborsRegressor

    KNeighborsRegressor()

    n_neighbors = 5(default) : 이웃의 수
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", KNeighborsRegressor())
        ]
    )

    KNeighborsRegressor().get_params()

    {'algorithm': 'auto', 'leaf_size': 30, 'metric': 'minkowski', 'metric_params': None, 'n_jobs': None, 'n_neighbors': 5, 'p': 2, 'weights': 'uniform'}
    from sklearn.model_selection import GridSearchCV, KFold

    knn_param = {'regressor__n_neighbors': np.arange(5, 10, 1)}

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    knn_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = knn_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    knn_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    KNeighborsRegressor
    교차검증 세부 결과는 .cv_results_에 저장되어 있습니다. 각 parameter 별로 split_숫자_test_score는 반복 횟수별 교차 검증 결과를 의미합니다. mean_test_score는 split_숫자_test_score의 평균값을 의미합니다. std_test_score는 split_숫자_test_score의 표준편차를 의미합니다. rank_test_score는 mean_test_score를 기준으로 순위를 매긴 결과입니다.

    pd.DataFrame(knn_search.cv_results_)

       mean_fit_time  std_fit_time  ...  std_test_score  rank_test_score
    0       0.003132      0.001086  ...        1.299494                5
    1       0.002528      0.000031  ...        1.151810                4
    2       0.002498      0.000026  ...        0.912858                3
    3       0.002487      0.000030  ...        1.267924                2
    4       0.002476      0.000026  ...        1.218151                1

    [5 rows x 14 columns]
    결과를 보면 최적의 파라미터는 k = 9이며, mean_test_score는 -8.638363인 것을 확인할 수 있습니다. 해당 지표는 -MSE이므로 RMSE로 변환해보겠습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 2.93 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', knn_search.best_params_)

    best 파라미터 조합 : {'regressor__n_neighbors': 9}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(knn_search.best_score_))) # -8.638363

    교차검증 RMSE score : 2.9391092598745505
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.23 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(knn_search.score(test_X, test_y))))

    테스트 RMSE score : 3.23921170850139
    8.6 Penalized Regression
    다중회귀모형에서는 LSE(MSE가 최소가 되는 계수를 계산하는 방법)로 추정량 
    를 구할 수 있습니다. 이렇게 구한 추정량 
    은 BLUE(Best Linear Unbiased Estimator)의 성질, 즉 비편향 추정량 중에서 분산이 작은 성질이 있습니다.

    penalty term이 필요한 이유

    LSE를 이용하면 비편향 추정량 중에서 분산이 가장 작은 추정량을 구할 수 있지만 위에서 설명한 bias-variance trade off 관계를 보면 total error 관점에서는 안좋을 수 있습니다. 따라서 penalty term을 추가한 모형을 통해 bias를 조금 포기하고 variance를 효과적으로 낮추는 모형이 필요합니다. 이러한 모형이 Ridge, LASSO, Elastic net regression 등입니다.

    Ridge, LASSO, ELASTIC NET의 특징

    Ridge regression

    제약식을 통해서 중요하지 않은 변수의 영향력을 감소시킴. 즉, 회귀계수 값을 축소함

    변수 간 상관관계가 높은 상황에서 예측 성능이 높음

    LASSO regression

    제약식을 통해서 중요하지 않은 변수의 영향력을 감소시킴

    Ridge regression과의 차이점은 중요하지 않은 변수에 해당하는 회귀계수 값을 
    으로 만듦으로써 변수 선택 기능이 있음

    Elastic net regression

    변수 간 상관관계를 반영한 모형

    상관관계가 큰 모형을 동시에 선택 or 배제하는 특성이 있음

    Note
    Penalized regression의 자세한 개념은 통계반 내용을 참고하시기 바랍니다.

    8.7 LASSO regression
    alpha = 1 : LASSO regression

    lambda : 규제항에 해당하는 초매개변수

    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    from sklearn.model_selection import cross_val_score

    먼저 사전에 정의한 전처리 pipeline과 함께 Lasso()를 불러와서 pipeline을 생성해주었습니다.

    Lasso()

    alpha = 1(default)
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", Lasso())
        ]
    )

    from sklearn.model_selection import GridSearchCV, KFold

    Cross validation과 함께 parameter 튜닝을 진행해보겠습니다. 먼저 모델별 parameter의 명칭은 .get_params()을 이용해서 확인할 수 있습니다. Lasso의 경우 alpha인 것을 확인할 수 있습니다.

    Lasso().get_params()

    {'alpha': 1.0, 'copy_X': True, 'fit_intercept': True, 'max_iter': 1000, 'normalize': False, 'positive': False, 'precompute': False, 'random_state': None, 'selection': 'cyclic', 'tol': 0.0001, 'warm_start': False}
    parameter의 범위를 지정해주었습니다. 이 때, Pipeline을 통해 Grid search를 적용할 경우 (모델 별칭)__(모델 파라미터) 형태로 지정해주어야 합니다.

    lasso_param = {'regressor__alpha': np.arange(0.1, 1, 0.1)}

    5 fold 교차검증을 정의해주었습니다.

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    정의한 각 prameter별 Grid search는 GridSearchCV()를 통해 진행해볼 수 있습니다.

    GridSearchCV()

    estimator : pipeline or model object

    param_grid : 튜닝할 파라미터(dict)

    scoring : 교차검증시 평가지표

    n_jobs = None(default) : 병렬 처리 옵션(-1 : 전체 core)

    refit = True(default) : 전체 데이터셋에 best parameter를 다시 fit할지 여부

    lasso_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = lasso_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    lasso_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    Lasso
    최적의 파라미터는 alpha = 1인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.05 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', lasso_search.best_params_)

    best 파라미터 조합 : {'regressor__alpha': 0.1}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(lasso_search.best_score_)))

    교차검증 RMSE score : 3.057805356062849
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.11 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(lasso_search.score(test_X, test_y))))

    테스트 RMSE score : 3.116063370080646
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        lasso_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.8 Ridge regression
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", Ridge())
        ]
    )

    Ridge().get_params()

    {'alpha': 1.0, 'copy_X': True, 'fit_intercept': True, 'max_iter': None, 'normalize': False, 'random_state': None, 'solver': 'auto', 'tol': 0.001}
    Ridge_param = {'regressor__alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Ridge_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = Ridge_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    Ridge_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    Ridge
    최적의 파라미터는 alpha = 0.9인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.05 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', Ridge_search.best_params_)

    best 파라미터 조합 : {'regressor__alpha': 0.9}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(Ridge_search.best_score_)))

    교차검증 RMSE score : 3.0557965786939754
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.18 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(Ridge_search.score(test_X, test_y))))

    테스트 RMSE score : 3.186416636967227
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        Ridge_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.9 Elastic net regression
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", ElasticNet())
        ]
    )

    ElasticNet().get_params()

    {'alpha': 1.0, 'copy_X': True, 'fit_intercept': True, 'l1_ratio': 0.5, 'max_iter': 1000, 'normalize': False, 'positive': False, 'precompute': False, 'random_state': None, 'selection': 'cyclic', 'tol': 0.0001, 'warm_start': False}
    ElasticNet_param = {'regressor__alpha': np.arange(0.1, 1, 0.1), 
                        'regressor__l1_ratio' : np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    ElasticNet_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = ElasticNet_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    ElasticNet_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    ElasticNet
    최적의 파라미터는 alpha = 0.1, l1 ratio = 0.4인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.03 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', ElasticNet_search.best_params_)

    best 파라미터 조합 : {'regressor__alpha': 0.1, 'regressor__l1_ratio': 0.4}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(ElasticNet_search.best_score_)))

    교차검증 RMSE score : 3.03934806294181
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.14 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(ElasticNet_search.score(test_X, test_y))))

    테스트 RMSE score : 3.140696717092505
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        ElasticNet_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.10 Decision tree
    의사결정나무는 나무구조를 활용한 의사결정 규칙을 통해서 분류 혹은 예측을 수행하는 방법입니다. 전체적인 모형의 형태는 다음과 같습니다.

    의사결정나무 예시

    기본적인 의사결정나무는 훈련 데이터를 동질적인 하위 그룹(ex. 
    )으로 분할한 다음 각 하위 그룹에 적절한 값을 채웁니다(ex. 평균 or major vote). 적절한 정지 규칙이 충족될 때까지 계속 반복해서 가지를 뻗어나가게 되며, 분할이 완료된 이후에는 마지막 leaf node에 해당하는 값들을 평균 or major vote를 취해서 최종 예측값을 산출합니다.

    회귀 예시





    분류 예시





    분할 기준

    위 그림처럼 공간을 분할하기 위해서는 tree의 분할 규칙을 정해야 합니다. tree의 분할 규칙은 다음과 같이 정할 수 있습니다.

    회귀 : 분할공간내의평균

    분류 : gini index, cross entropy

    Example

    분류 문제에서 cross entropy는 다음과 같이 정의할 수 있습니다.







    cross entropy를 이용해서 Information gain은 다음과 같이 정의합니다.


    Information gain을 최대화하는 X를 찾으면 분할 변수로 지정됩니다.

    T	T	T
    T	F	T
    T	T	T
    T	F	T
    F	T	T
    F	F	F
    F	T	F
    F	F	F
























    계산 결과 
    이 분할 변수로 선택된 것을 볼 수 있습니다.

    가 연속형 변수일 경우 분할 변수와 분할점은 다음과 같이 계산할 수 있습니다.



    를 최대화하는 
    가 분할점이 됩니다. 분할 변수와 분할점을 차례로 넣고 
    를 계산 후 최대화하는 
    를 찾으면 됩니다.

    Early stopping

    너무 복잡한 의사결정나무를 생성할 경우 과적합이 발생하게 되어 일반화 성능이 저하될 수 있습니다. 따라서 적절한 나무의 깊이를 정해서 트리의 크기를 제한할 수 있습니다. early stopping은 나무의 깊이 혹은 leaf node의 크기를 제한하는 방법입니다. 나무의 깊이를 특정 깊이까지만 제한할 경우 과적합을 피할 수 있으므로 예측에 있어서 분산이 상대적으로 작습니다. 그러나 나무의 깊이를 얕게 할 경우 편향이 커지게 되므로 적절한 기준을 정하는 것이 중요합니다. leaf node의 크기(leaf node의 관측치의 개수)를 제한할 경우 깊이를 제한하는 것과 마찬가지로 과적합을 피할 수 있습니다.



    Cost complexity pruning

    아주 큰 트리를 만든 후 가지치기를 통해 최적의 서브 트리를 얻는 방법입니다. 모든 가능한 서브 트리를 고려하는 대신에 아래 식에서 
     값의 변화에 따라 선택된 서브 트리를 고려합니다. 최적의 
    는 cross validation을 통해서 도출됩니다.

    full tree를 기준으로 보면 
    는 다른 트리에 비해 가장 낮지만, terminal node의 수는 가장 많습니다. full tree에서 depth를 하나씩 줄여나갈 경우, 
    는 늘어나지만, terminal node의 수는 감소하게 됩니다. 
    를 적절하게 조절했을 때, 트리의 depth가 줄었을 때 
    의 증가량보다 
    가 작을 경우 prune 된 트리가 선택되게 됩니다.

    의수




    장점

    비모수적 방법이므로 데이터에 대한 가정 없이 사용 가능

    모델 학습 결과에 대한 뚜렷한 설명력 제공

    단점

    예측력의 분산이 큼

    새로운 데이터에 대한 예측이 불안정하다는 의미
    계단식으로 예측값이 생성되므로 기준값의 경계에서 예측 오차가 클 수 있음

    Note
    tree 계열 모형(decision tree, random forest, gbm, XGBOOST, lightgbm, .. etc)의 경우 알고리즘 특성상 스케일링에 영향을 받지 않습니다.

    from sklearn.tree import DecisionTreeRegressor

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", DecisionTreeRegressor())
        ]
    )

    DecisionTreeRegressor().get_params()

    {'ccp_alpha': 0.0, 'criterion': 'mse', 'max_depth': None, 'max_features': None, 'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'min_impurity_split': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'presort': 'deprecated', 'random_state': None, 'splitter': 'best'}
    decisiontree_param = {'regressor__ccp_alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    decisiontree_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    DecisionTreeRegressor
    최적의 파라미터는 ccp_alpha = 0.3인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.07 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', decisiontree_search.best_params_)

    best 파라미터 조합 : {'regressor__ccp_alpha': 0.30000000000000004}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(decisiontree_search.best_score_)))

    교차검증 RMSE score : 3.0748675958922695
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.19 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(decisiontree_search.score(test_X, test_y))))

    테스트 RMSE score : 3.194271297114146
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        decisiontree_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.11 Bagging
    Bagging은 boostrap aggregating의 약자로 통계 학습 방법의 분산을 줄이기 위한 일반화된 방법입니다. Bagging의 주요 아이디어는 다음과 같습니다. 독립적인 관측치 
     이 주어졌을 때(분산이 
    )인), 
    의 분산은 

    로 줄어들게 됩니다. 이 개념을 일반화하면, 모집단으로부터 많은 train 데이터셋을 취하고, 각 train 데이터셋 별로 모델을 적합시킨 후 평균을 취하면, 분산을 줄일 수 있다는 의미입니다. 그러나 보통 train 데이터셋은 하나만 갖고 있기 때문에, 이 개념을 곧바로 적용할 수 없습니다. 따라서 붓스트랩 표본을 이용해서 이를 보완합니다.

    개의 붓스트랩 표본이 있을 때, 각 붓스트랩 표본별로 
     모델을 적합시킬 수 있습니다. 최종적으로 각 붓스트랩 표본별로 생성된 모델의 예측 결과를 회귀문제의 경우 평균내서 최종 결과를 도출합니다. 분류 문제의 경우 major voting을 통해 B개의 예측값 중 가장 많이 나온 값을 취합니다.





    8.12 Bagged tree
    Bagging은 의사결정나무에 적용했을 때 특히 유용합니다. prune 되지 않은 의사결정나무의 경우, 편향은 낮지만 분산이 높은 모형입니다. 따라서 의사결정나무에 Bagging을 적용할 경우 편향은 낮지만 단일 의사결정나무에 비해서는 분산이 낮은 모형을 구할 수 있습니다.



    from sklearn.ensemble import BaggingRegressor

    BaggingRegressor()

    estimator = None(DecisionTreeRegressor()) : sklearn에서 지원하는 모형

    max_samples = 1(default) : estimator를 적합할 때 사용할 데이터 비율

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", BaggingRegressor())
        ]
    )

    BaggingRegressor().get_params()

    {'base_estimator': None, 'bootstrap': True, 'bootstrap_features': False, 'max_features': 1.0, 'max_samples': 1.0, 'n_estimators': 10, 'n_jobs': None, 'oob_score': False, 'random_state': None, 'verbose': 0, 'warm_start': False}
    Bagging_param = {'regressor__max_samples': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Bagging_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = Bagging_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    Bagging_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    BaggingRegressor
    최적의 파라미터는 max_samples = 0.2인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.01 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', Bagging_search.best_params_)

    best 파라미터 조합 : {'regressor__max_samples': 0.1}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(Bagging_search.best_score_)))

    교차검증 RMSE score : 3.000372176407594
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.22 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(Bagging_search.score(test_X, test_y))))

    테스트 RMSE score : 3.450303551079904
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        Bagging_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.13 Random forest
    랜덤 포레스트는 bagging을 통해서 각 붓스트랩 표본별로 개별 의사결정나무를 만들 때 전체 변수 
    개를 고려하는 것이 아니라 무작위로 
    개(
    )만 고려합니다(
    ). 
    일 때 bagged tree와 랜덤포레스트는 같습니다. 보통 
    은 
    로 설정합니다.

    변수 전체(
    )를 고려하는 것이 아니라 
    개만 고려하는 이유는 보통 데이터셋이 주어졌을 때 변수별로 상관성이 높은 경우가 대부분입니다. 다른 변수 간의 상관성이 매우 높은 변수가 존재한다고 했을 때, 배깅을 통해 개별 트리를 생성할 경우 root node에는 변수 간의 상관성이 높은 변수가 있게 됩니다. 이 경우 배깅으로 생성된 개별 트리들은 서로 유사할 것이며, 상관성이 높을 것입니다. 상관성이 높은 값을 평균내는 경우 상관성이 낮은 값을 평균 내는 것보다 분산 감소의 폭이 크지 않습니다. 따라서 배깅으로 인한 분산 감소 효과가 줄어들게 됩니다.

    변수를 무작위로 뽑아서 일부만 고려할 경우 상관성이 높은 변수가 계속 뽑히는 것을 줄일 수 있고, 다른 변수들에 기회가 갈 수 있습니다. 즉 개별 트리 간의 상관성을 줄일 수 있습니다.

    from sklearn.ensemble import RandomForestRegressor

    RandomForestRegressor()

    max_features = 1(default) : 트리를 분할할 때 사용할 feature 비율
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", RandomForestRegressor())
        ]
    )

    RandomForestRegressor().get_params()

    {'bootstrap': True, 'ccp_alpha': 0.0, 'criterion': 'mse', 'max_depth': None, 'max_features': 'auto', 'max_leaf_nodes': None, 'max_samples': None, 'min_impurity_decrease': 0.0, 'min_impurity_split': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'n_estimators': 100, 'n_jobs': None, 'oob_score': False, 'random_state': None, 'verbose': 0, 'warm_start': False}
    RandomForest_param = {'regressor__max_features': np.arange(0.5, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    RandomForestRegressor
    최적의 파라미터는 max_features = 0.89인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.04 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', RandomForest_search.best_params_)

    best 파라미터 조합 : {'regressor__max_features': 0.7999999999999999}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(RandomForest_search.best_score_)))

    교차검증 RMSE score : 3.0332955726006245
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.19 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(RandomForest_search.score(test_X, test_y))))

    테스트 RMSE score : 3.1859273714597167
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        RandomForest_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.14 GBM
    Boosting

    부스팅은 배깅과 유사하지만 붓스트랩을 이용하지 않고, 트리가 순차적으로 업데이트된다는 점에서 차이가 있습니다. 주어진 모델에 대해 모델의 잔차(모델이 설명하지 못한 정보)에 새로운 의사결정나무를 적합시킵니다. 이렇게 생성된 의사결정나무를 이전에 주어진 모형의 결과와 더해서 새로운 예측값을 산출하고, 잔차를 업데이트합니다.



    개별 트리는 깊이가 깊지 않은(depth : 
    ) weaked tree로 생성됨

    트리의 개수가 너무 많을 경우, 즉 너무 많이 잔차를 업데이트할 경우 과적합될 수 있으므로, 트리의 개수를 적절하게 조절하는 것이 중요

    잔차를 업데이트할 때, 수축 파라미터(learning rate)가 존재함

    세부 내용 : https://dondonkim.netlify.app/posts/2021-06-12-gradient-boosting-regression/gbm.html

    회귀 트리에서의 boosting

    from sklearn.ensemble import GradientBoostingRegressor

    GradientBoostingRegressor()

    learning_rate = 0.1(default)

    n_estimators = default=100 : 반복 수

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", GradientBoostingRegressor())
        ]
    )

    GradientBoostingRegressor().get_params()

    {'alpha': 0.9, 'ccp_alpha': 0.0, 'criterion': 'friedman_mse', 'init': None, 'learning_rate': 0.1, 'loss': 'ls', 'max_depth': 3, 'max_features': None, 'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'min_impurity_split': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'n_estimators': 100, 'n_iter_no_change': None, 'presort': 'deprecated', 'random_state': None, 'subsample': 1.0, 'tol': 0.0001, 'validation_fraction': 0.1, 'verbose': 0, 'warm_start': False}
    GradientBoosting_param = {'regressor__learning_rate': np.arange(0.1, 0.5, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    GradientBoosting_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = GradientBoosting_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    GradientBoosting_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    GradientBoostingRegressor
    최적의 파라미터는 learning_rate = 0.1인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.16 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', GradientBoosting_search.best_params_)

    best 파라미터 조합 : {'regressor__learning_rate': 0.1}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(GradientBoosting_search.best_score_)))

    교차검증 RMSE score : 3.1569186691108695
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.29 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(GradientBoosting_search.score(test_X, test_y))))

    테스트 RMSE score : 3.289302086946367
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        GradientBoosting_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    #plt.clf()
    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.15 XGBOOST
    xgboost는 GBM과 전체적인 모형의 구조는 비슷하지만, 기존 부스팅에 비해 몇 가지 이점을 제공합니다.

    Regularization : 과적합을 방지하는 정규화 파라미터가 존재합니다.
    Early stopping : 추가되는 트리가 개선되지 않을 때, 모델 학습을 중지할 수 있습니다.
    Parallel processing : GPU 및 Spark 와의 호환성을 지원하는 분산처리 엔진을 이용해서 병렬처리를 할 수 있습니다.
    Loss function : 사용자가 사전에 정의한 손실함수를 이용할 수 있습니다.
    Continue with existing model : 학습한 모델의 결과를 저장하고, 이후에 해당 모델로 돌아가서 다시 학습할 수 있습니다. 즉, 모델 학습을 중지했을 때 모델을 처음부터 시작하지 않고도 모델을 계속 학습할 수 있습니다.
    Different base learners : base learner로 의사결정나무 말고도 일반화선형모형 또한 적용할 수 있습니다.
    초매개변수 별 설명

    n_estimators : 반복 수

    iteration이 클 경우 overfitting 문제가 생길 수 있고, 계산량 증가
    max_depth : 트리 최대 depth(default : 
    )

    범위 : 

    값이 작을 수록 overfitting 방지

    eta : learning rate(default : 
    )

    범위 : 

    각 iteration 마다 생성되는 개별 트리의 영향력을 낮추는 역할이므로, 값이 작을수록 regularization 효과가 큼(즉, overfitting 방지)

    gamma(
    ) : Minimum loss reduction(default : 
    )

    범위 : 

    각 iteration 마다 생성되는 트리를 어떻게 pruning할 것인지에 관한 파라미터로 gamma 값이 클수록 regularization 효과가 큼(즉, overfitting 방지)

    일 경우 pruning 실시

    colsample_bytree : 각 iteration 마다 생성되는 트리에 사용할 feature의 비율(default : 
    )

    범위 : 

    값이 작을 수록 overfitting 방지

    min_child_weight : 각 iteration 마다 생성되는 트리의 각 leaf node에 필요한 instance의 수 (default : 
    )

    범위 : 

    값이 클수록 overfitting 방지

    subsample : 각 iteration 마다 생성되는 트리에 사용할 훈련 데이터의 비율(default : 
    )

    범위 : 

     이하로 설정할 경우 데이터의 일부만 뽑기 때문에 overfitting 방지

    import xgboost as xgb

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", xgb.XGBRegressor())
        ]
    )

    xgb.XGBRegressor().get_params()

    {'objective': 'reg:squarederror', 'base_score': None, 'booster': None, 'callbacks': None, 'colsample_bylevel': None, 'colsample_bynode': None, 'colsample_bytree': None, 'early_stopping_rounds': None, 'enable_categorical': False, 'eval_metric': None, 'feature_types': None, 'gamma': None, 'gpu_id': None, 'grow_policy': None, 'importance_type': None, 'interaction_constraints': None, 'learning_rate': None, 'max_bin': None, 'max_cat_threshold': None, 'max_cat_to_onehot': None, 'max_delta_step': None, 'max_depth': None, 'max_leaves': None, 'min_child_weight': None, 'missing': nan, 'monotone_constraints': None, 'n_estimators': 100, 'n_jobs': None, 'num_parallel_tree': None, 'predictor': None, 'random_state': None, 'reg_alpha': None, 'reg_lambda': None, 'sampling_method': None, 'scale_pos_weight': None, 'subsample': None, 'tree_method': None, 'validate_parameters': None, 'verbosity': None}
    Xgb_param = {'regressor__learning_rate': np.arange(0.01, 0.3, 0.05)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Xgb_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = Xgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    Xgb_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    XGBRegressor
    최적의 파라미터는 learning_rate = 0.06인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.32 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', Xgb_search.best_params_)

    best 파라미터 조합 : {'regressor__learning_rate': 0.060000000000000005}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(Xgb_search.best_score_)))

    교차검증 RMSE score : 3.32145724947022
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.35 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(Xgb_search.score(test_X, test_y))))

    테스트 RMSE score : 3.350485615561976
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        Xgb_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    #plt.clf()
    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.16 SVM
    분류 문제에서 svm의 기본 아이디어는 마진(margin)을 최대화하는 초평면을 찾는 것입니다. 이진 분류 문제에서 마진은 각 범주 간 관측치 사이의 최단 거리를 의미합니다. 선형 svm의 경우 크게 두 가지로 나눌 수 있습니다.

    hard margin classifier

    이진 분류 문제에서 두 클래스를 분리하는 각 클래스 간 가장 가까운 관측치 사이의 거리를 최대화하는 최적의 선형 결정경계를 찾는 방법입니다.






    간단한 예시와 함께 수식을 해석해보겠습니다.



    파란색 점과 빨간색 점을 임의로 생성한 후 검은색 선형 결정경계를 생성했습니다.


    각 support vector는 똑같이 정의해볼 수 있습니다.


    vector 형식으로 표현해보면 선형 결정경계 및 support vector는 다음과 같이 정의할 수 있습니다.





    두 support vector 사이에 거리는 다음과 같습니다.





     를 최대화하는 것은 

    을 최소화하는 것과 같습니다. 따라서 목적함수 식은 다음과 같이 정의됩니다.



    다음으로 support vector 밖의 점들을 보겠습니다. support vector에 
     값을 대입해보겠습니다. 
    을 대입하면 
    입니다. 
    을 대입해보면 
    입니다.

    즉, 제약식은 다음과 같이 정의할 수 있습니다.


    이는 다음과 같은 꼴로 바꿀 수 있습니다.



    soft margin classifier

    hard margin classifier의 경우 일부 관측치가 마진의 경계 혹은 반대 방향에 있을 경우 분류 초평면의 변동이 클 수 있습니다. 또한 선형 결정경계로 완벽하게 분리되지 않을 수 있습니다. soft margin classifier는 일부 관측치가 잘못 분류되는 것을 허용(제약조건을 완화)함으로써 hard margin classifier에 비해 더 강건한 분류 모형을 구축합니다.







    추가된 수식을 그림과 함께 해석해보겠습니다.



    이전과 달리 margin 안에 잘못 분류된 관측치가 존재하는 것을 볼 수 있습니다. 잘못 분류된 점과 support vector 사이의 거리는 다음과 같이 표현할 수 있습니다.





    해당 점의 경우 오분류된 관측치이므로 support vector 사이의 거리의 절반인 1보다 클 것입니다(
    ).



    반면에 위 그래프의 점을 보면 올바르게 분류되었으므로 support vector 사이의 거리의 절반인 1보다 작을 것입니다(
    ). 즉, 
    는 hard margin classifier에서 제약을 어느 정도 허용할 것인지를 나타내는 값이라고 볼 수 있습니다.

    그렇다면, 얼마만큼 허용하는 것이 좋을까요? 이는 튜닝 파라미터로 설정하여, 교차검증을 통해 최적의 값을 구할 수 있습니다.파라미터를 보면 C(cost) 파라미터가 존재합니다. C는 관측치가 잘못 분류되는 것을 허용하는 것의 크기를 조절하는 파라미터입니다.



    hard margin classifier, soft margin classifier 둘다 quadratic programming 문제이므로, 라그랑지안 승수법을 이용해서 최적해를 구할 수 있습니다.

    kernel SVM

    svm의 경우 기본적으로 선형 분류를 합니다. 따라서 선형 결정경계를 이용해서 분류하기 어려운 경우 적용하기 어렵습니다. 이를 극복하기 위해서 kernel 함수를 이용합니다. 직관적인 아이디어는 아래 그림과 같습니다. 왼쪽 2차원 그림을 보면 2차원 상에서는 직선으로 분류할 수 없는 문제임을 알 수 있습니다. 그러나 오른쪽 그림과 같이 polynomial function을 이용해서 고차원에 매핑시킬 경우 선형 분류가 가능합니다.



    kernel 종류

    polynomial function

    Radial basis function

    기타 등등

    단점

    적절한 kernel을 정하기가 어려움

    학습 속도가 오래걸림

    scale, degree 파라미터는 polynomial kernel을 정의할 때 사용되는 파라미터로, 해당 파라미터도 교차검증을 통해 최적의 값을 구할 수 있습니다.

    Example : polynomial kernal


    Support vector regression

    regression 문제에서도 support vector machine의 아이디어가 비슷하게 적용됩니다. 대표적인 방법으로 
    -insensitive loss regression이 있습니다. 일반적으로 선형회귀에서는 squared loss를 최소화하는 직선을 찾습니다. 선형회귀는 이상치에 민감한 특성이 있습니다. 선형 회귀와 달리 SVR에서는 loss function으로 
    -insensitive loss를 이용합니다. 
    -insensitive loss를 보면 실제값과 예측값의 차이가 
     내에 있을 경우 loss를 0으로 합니다. 즉, 마진 안에 데이터는 회귀직선을 피팅하는데 영향을 주지 않습니다. 이는 적정 범위 
     내에서 실제값과 예측값의 차이를 허용한다는 의미로 볼 수 있습니다. 이상치가 존재하는 데이터를 완벽하게 피팅하는 것이 아니라 
     만큼의 차이를 허용하므로 이상치에 강건한 모형을 구축할 수 있습니다. SVR도 SVM과 동일하게 kernel 트릭을 적용할 수 있으며, quadratic programming 문제이므로, 라그랑지안 승수법을 이용해서 최적해를 구할 수 있습니다.





    Note
    거리를 이용하기 때문에 스케일에 민감할 수 있으므로, 표준화를 진행해줘야 함

    from sklearn.svm import SVR

    SVR()

    kernel = ‘rbf’(default) : ‘poly’, ‘linear’, .. etc

    degree = 3(default)

    C = 1(default)

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", SVR())
        ]
    )

    SVR().get_params()

    {'C': 1.0, 'cache_size': 200, 'coef0': 0.0, 'degree': 3, 'epsilon': 0.1, 'gamma': 'scale', 'kernel': 'rbf', 'max_iter': -1, 'shrinking': True, 'tol': 0.001, 'verbose': False}
    SVR_param = {'regressor__C': np.arange(1, 100, 20)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    SVR_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = SVR_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    SVR_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    SVR
    최적의 파라미터는 C = 1인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 2.96 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', SVR_search.best_params_)

    best 파라미터 조합 : {'regressor__C': 1}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(SVR_search.best_score_)))

    교차검증 RMSE score : 2.9660685528814463
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 3.14 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(SVR_search.score(test_X, test_y))))

    테스트 RMSE score : 3.1475107820313637
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        SVR_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    #plt.clf()
    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.17 Neural network
    neural network는 
    가 input으로 주어지고, 비선형함수를 이용해서 target 
    를 예측하는 모형입니다. 이전의 다른 모형도 비선형함수를 이용하지만 신경망과의 차이는 모델의 특정 구조입니다. neural network 모형의 경우 아래 그림과 같은 구조를 갖습니다.



    가 주어졌을 때, 첫 번째 layer는 변수가 입력되는 input layer이고, 각 노드는 unit입니다. 화살표는 각 input이 총 5개의 hidden unit에 공급되는 것을 나타냅니다. 해당 그림을 수식으로 나타내면 다음과 같습니다.






    수식을 하나씩 살펴보면 
    를 input으로 하는 
    가 존재합니다. 
    는 활성화함수(activation function)로 사전에 함수의 형태를 정해야 합니다. 
    는 보통, reLU 함수 혹은 sigmoid 함수와 같이 비선형함수를 이용합니다.




    는 그림을 통해 보면 hidden layer의 각 unit과 같습니다. hidden layer를 통과한 후에는 마지막으로 output layer에 값이 공급됩니다.




    의 값을 도출하기 위한 
    , 
     파라미터는 데이터를 통해 추정됩니다. 회귀문제의 경우 loss function을 
     loss로 정의하고, gradient descent 알고리즘을 통해 구할 수 있습니다(혹은, ADAgrad, ADAM, ADAdelta 등등 여러 알고리즘이 있습니다).

    neural network라는 이름은 hidden unit을 뇌의 뉴런과 유사하다고 생각하는데서 유래되었습니다. hidden layer와 각 unit은 분석가가 custom 할 수 있기 때문에 얼마든지 복잡해질 수 있습니다.

    보통 neural network를 fitting하는 것은 tensorflow, keras, pytorch를 이용하는데, 각 패키지를 이용하면 모델 구조를 효율적으로 커스텀할 수 있습니다. 다만 해당 패키지를 이용하기 위해서는 패키지에 대한 숙련된 지식이 필요합니다.

    시험에서는 성능에 크게 상관없이 neural network 모형을 fitting하는 문제가 나왔으므로, sklearn 패키지에 내장되어있는 MLP를 이용하는 것이 효율적입니다.

    hidden_layer_sizes : hidden unit의 수

    hidden unit의 수가 늘어날수록, 더 복잡한 모형
    alpha : regularization parameter

    overfitting 방지를 위해 loss function에 regularization term에 을 추가할 때 들어가는 값
    gradient descent 알고리즘을 이용해서 최적해를 구할 때, input 
    의 scale이 다를 경우 알고리즘의 수렴 속도가 느려지는 문제가 있습니다.

    Note
    neural network도 다른 알고리즘과 비슷하게, 모델 학습 속도 및 성능 개선을 위해 표준화를 진행해줘야 합니다.



    from sklearn.neural_network import MLPRegressor

    MLPRegressor()

    hidden_layer_sizes = (100,)

    alpha = 0.0001(default)

    learning_rate_init : solver parameter

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", MLPRegressor())
        ]
    )

    MLPRegressor().get_params()

    {'activation': 'relu', 'alpha': 0.0001, 'batch_size': 'auto', 'beta_1': 0.9, 'beta_2': 0.999, 'early_stopping': False, 'epsilon': 1e-08, 'hidden_layer_sizes': (100,), 'learning_rate': 'constant', 'learning_rate_init': 0.001, 'max_fun': 15000, 'max_iter': 200, 'momentum': 0.9, 'n_iter_no_change': 10, 'nesterovs_momentum': True, 'power_t': 0.5, 'random_state': None, 'shuffle': True, 'solver': 'adam', 'tol': 0.0001, 'validation_fraction': 0.1, 'verbose': False, 'warm_start': False}
    MLP_param = {'regressor__learning_rate_init': np.arange(0.01, 0.2, 0.02)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    MLP_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = MLP_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'neg_mean_squared_error')
    MLP_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    MLPRegressor
    최적의 파라미터는 learning_rate = 0.16인 것을 확인할 수 있습니다. 교차검증시 RMSE 기준 best score를 확인해보면 대략 3.5 정도인 것을 확인할 수 있습니다.

    print('best 파라미터 조합 :', MLP_search.best_params_)

    best 파라미터 조합 : {'regressor__learning_rate_init': 0.01}
    print('교차검증 RMSE score :', np.sqrt(np.absolute(MLP_search.best_score_)))

    교차검증 RMSE score : 3.381258265755003
    최종적으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다. test 데이터의 성능은 RMSE = 4.08 정도인 것을 확인할 수 있습니다.

    print('테스트 RMSE score :', np.sqrt(np.absolute(MLP_search.score(test_X, test_y))))

    테스트 RMSE score : 3.693332418430044
    Permutation importance plot

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        MLP_search, train_X, train_y, n_repeats=10, random_state=42
    )

    import matplotlib.pyplot as plt

    #plt.clf()
    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 10 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [Text(0, 0, 'school'), Text(1, 0, 'sex'), Text(2, 0, 'paid'), Text(3, 0, 'famrel'), Text(4, 0, 'freetime'), Text(5, 0, 'goout'), Text(6, 0, 'Dalc'), Text(7, 0, 'Walc'), Text(8, 0, 'health'), Text(9, 0, 'absences')])
    plt.show()



    8.18 Permutation importance
    permutation importance는 모델을 학습시킨 이후(post-hoc) 특정 변수의 관측치를 shuffle했을 때의 예측력을 비교해서 feature importance를 계산하는 방법

    알고리즘 특성상 특정 모델에 국한된 방법이 아니라 어떤 모델이든 적용할 수 있는 방법

    Example

    https://www.kaggle.com/code/dansbecker/permutation-importance/tutorial permutation importance의 직관적인 아이디어를 이해하기 위해 예시를 살펴보겠습니다.예시에서는 10살 때의 개인 신상 정보를 이용해서 10년 후 20살 때의 키를 예측하려고 합니다. 직관적으로 변수 중 20살 때의 키를 예측하는데 중요한 변수는 10살 때의 키에 관한 변수인 것을 알 수 있습니다. 반면에 10살 때 갖고 있는 양말의 수는 상대적으로 중요한 변수가 아닐 것입니다.

    이러한 직관에서 출발하면 다음과 같은 질문을 해볼 수 있습니다. validation셋에서 특정 변수의 관측치를 shuffle하고, 나머지 변수를 고정시키면 예측 정확도에 어떤 영향을 미칠까?

    특정 한 변수의 관측치만 행방향으로 무작위로 섞을 경우 당연히 모델의 예측력은 감소하게 될 것입니다. 다만 변수별로 예측력 감소의 크기는 차이가 있을 것입니다. 위의 예시로 보면 10살 때의 키에 관한 변수를 shuffle 했을 때 모델의 예측력은 많이 떨어지지만, 10살 때 갖고 있는 양말의 수에 관한 변수를 shuffle 했을 때는 모델의 예측력에 큰 차이가 없을 것입니다. 따라서 예측력이 많이 떨어질 경우 예측에 중요한 변수, 예측력이 조금 떨어지는 변수는 중요하지 않은 변수로 볼 수 있습니다. 이러한 직관이 purmutaion importance의 아이디어입니다.

    Process

    학습이 끝난 모델 세팅
    한 변수의 관측치를 shuffling한 데이터를 이용해서 동일하게 예측을 진행
    예측치와 실제값의 차이를 나타내는 loss function을 이용해서 shuffling 후에 얼마나 loss가 커졌는지 계산
    loss의 증감을 이용해서 feature importance를 계산
    모든 변수에 대해 반복
    장점

    계산 속도가 빠름

    특정 변수를 제거하고 재학습을 시키는 것이 아니라 특정 변수 하나를 permutation하는 것이므로 상대적으로 계산량 감소
    사용 범위가 넓고, 직관적임

    상대적으로 일관된 feature importance를 측정할 수 있음

    단점

    무작위로 shuffling 하다보면 비현실적인 값이 나올 수도 있음
    8.19 Partial dependence plot
    partial dependence plot은 설명 변수가 target variable에 어떤 영향을 미쳤는지를 보여줍니다. partial dependence plot은 pumutation importance와 마찬가지로 모델을 학습한 후(post-hoc) 계산됩니다.

    Process



    학습이완료된임의의모델
    관심변수
    외나머지변수


    를 안다고 할 때, 
     는 데이터셋으로 부터 주어진 값이므로 
    에 값을 넣어서 값을 얻을 수 있습니다. 
    는 학습이 완료된 모델이지만 적분이 불가능하므로 monte carlo integration을 이용해서 근사적으로 계산합니다.



    Note
    관심변수 외에 다른 변수들의 값이 고정되어 있을 때 관심 변수 값에 따라 모델의 예측값이 어떻게 변화하는지를 보는 것입니다.

    from sklearn.inspection import partial_dependence
    from sklearn.inspection import plot_partial_dependence
    #from sklearn.inspection import PartialDependenceDisplay

    import matplotlib.pyplot as plt

    num_columns = train_X.select_dtypes('number').columns.tolist()

    fig, ax = plt.subplots(figsize=(5, 5))
    #plt.subplots_adjust(top=0.9)
    plot_partial_dependence(estimator=MLP_search, 
                            X=train_X, 
                            features=num_columns, # 관심변수 
                            percentiles=(0, 1), # 최소, 최대 
                            ax=ax)

    <sklearn.inspection._plot.partial_dependence.PartialDependenceDisplay object at 0x17e19bb50>
    plt.subplots_adjust(top=0.9, hspace = 0.5, wspace = 0.3) # hspace : 서브 플랏 행 간 간격 조절                      
    plt.show()



    """
