def m22():
    """
    20  22회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    20.1 머신러닝
    미국 국립 당뇨병 연구소의 데이터 일부로 피마 인디언의 21세 이상여성이 대상입니다. 데이터를 수집한 목적은 특정 변수를 활용해서 피마 인디언의 당뇨병 유무를 예측하는 것입니다.

    Data description

    Pregnancies : 임신 횟수
    Glucose : 혈장 포도당 농도
    pressure : 혈압 (mm Hg)
    triceps : 삼두 피부 두께 (mm)
    insulin : 2시간 혈청 인슐린 (mu U/ml)
    BMI : bmi 지수(
    체중
    키

    )
    DiabetesPedigreeFunction : 당뇨유전인자
    Age : 나이(years)
    Outcome : 당뇨 유무
    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from imblearn.over_sampling import RandomOverSampler
    from imblearn.under_sampling import RandomUnderSampler
    from collections import Counter
    from datetime import datetime
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve, f1_score
    from sklearn import set_config
    set_config(display="diagram")

    dat = pd.read_csv('./data/ex_data/diabetes.csv')
    dat = dat.clean_names()

    dat.head()

       pregnancies  glucose  bloodpressure  ...  diabetespedigreefunction  age  outcome
    0            6      148             72  ...                     0.627   50        1
    1            1       85             66  ...                     0.351   31        0
    2            8      183             64  ...                     0.672   32        1
    3            1       89             66  ...                     0.167   21        0
    4            0      137             40  ...                     2.288   33        1

    [5 rows x 9 columns]
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 768 entries, 0 to 767
    Data columns (total 9 columns):
     #   Column                    Non-Null Count  Dtype  
    ---  ------                    --------------  -----  
     0   pregnancies               768 non-null    int64  
     1   glucose                   768 non-null    int64  
     2   bloodpressure             768 non-null    int64  
     3   skinthickness             768 non-null    int64  
     4   insulin                   768 non-null    int64  
     5   bmi                       768 non-null    float64
     6   diabetespedigreefunction  768 non-null    float64
     7   age                       768 non-null    int64  
     8   outcome                   768 non-null    int64  
    dtypes: float64(2), int64(7)
    memory usage: 54.1 KB
    20.1.1 탐색적 데이터 분석을 수행하시오(시각화 포함).
    y = dat['outcome']
    X = dat.drop(['outcome'], axis = 1)

    pd.options.display.max_columns = None # full 출력 옵션 
    X.describe()

           pregnancies     glucose  bloodpressure  skinthickness     insulin   
    count   768.000000  768.000000     768.000000     768.000000  768.000000  \
    mean      3.845052  120.894531      69.105469      20.536458   79.799479   
    std       3.369578   31.972618      19.355807      15.952218  115.244002   
    min       0.000000    0.000000       0.000000       0.000000    0.000000   
    25%       1.000000   99.000000      62.000000       0.000000    0.000000   
    50%       3.000000  117.000000      72.000000      23.000000   30.500000   
    75%       6.000000  140.250000      80.000000      32.000000  127.250000   
    max      17.000000  199.000000     122.000000      99.000000  846.000000   

                  bmi  diabetespedigreefunction         age  
    count  768.000000                768.000000  768.000000  
    mean    31.992578                  0.471876   33.240885  
    std      7.884160                  0.331329   11.760232  
    min      0.000000                  0.078000   21.000000  
    25%     27.300000                  0.243750   24.000000  
    50%     32.000000                  0.372500   29.000000  
    75%     36.600000                  0.626250   41.000000  
    max     67.100000                  2.420000   81.000000  
    X.hist();
    plt.show();



    sns.countplot(y)
    plt.show();



    corr = X.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.tight_layout()
    plt.show();



    glucose(혈장 포도당 농도)가 0인 경우가 존재함

    혈압이 0인 경우가 존재함

    삼두 피부 두께가 0인 경우가 존재함

    bmi가 0인 경우가 존재함

    outcome(당뇨 유무)의 경우 class 불균형 존재

    age(나이), diabetespedigreefuncion(당뇨유전인자), pregnancies(임신횟수), insulin 등의 경우 우측으로 긴꼬리를 갖는 분포임

    age(나이)와 pregnancies(임신횟수) 사이에는 양의 상관관계(0.54)가 존재함

    insulin(2시간 혈청 인슐린)과 skin_thickness(삼두 피부 두께) 사이에는 양의 상관관계(0.44)가 존재함

    20.1.2 이상치를 처리하시오.
    dat2 = dat.loc[(dat.bloodpressure != 0) & (dat.skinthickness != 0) & (dat.bmi != 0)]

    bmi 지수가 0인 경우 제거

    skin thickness(삼두 피부 두께)가 0인 경우 제거

    blood_pressure(혈압)이 0인 경우 제거

    개별 instance는 사람이고, bmi, skin thickness, blood_pressure는 0은 나올 수 없으므로 데이터 입력 오류에 따른 이상치로 판단하여 제거함

    y = dat2['outcome']
    X = dat2.drop(['outcome'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = dat2['outcome'], random_state = 0)

    Q1 = np.quantile(train_X.pregnancies, 0.25)
    Q3 = np.quantile(train_X.pregnancies, 0.75)
    IQR = Q3 - Q1
    UC = Q3 + (1.5 * IQR) 
    LC = Q3 - (1.5 * IQR) 

    train_X.loc[(train_X.pregnancies > UC) | (train_X.pregnancies < LC), :]

         pregnancies  glucose  bloodpressure  skinthickness  insulin   bmi   
    298           14      100             78             25      184  36.6  \
    455           14      175             62             30        0  33.6   
    159           17      163             72             41      114  40.9   

         diabetespedigreefunction  age  
    298                     0.412   46  
    455                     0.212   38  
    159                     0.817   47  
    outlier = train_X.loc[(train_X.pregnancies > UC) | (train_X.pregnancies < LC), :].index.tolist()

    train_X_eda = train_X.copy()
    train_X_eda = train_X_eda.assign(outlier = np.where(train_X_eda.index.isin(outlier), 1, 0))

    sns.scatterplot(x='age', 
                    y='pregnancies',
                    hue='outlier',
                    s=100, # marker size
                    data=train_X_eda)
    plt.show();



    boxplot의 위 울타리를 기준으로 이상치를 뽑았을 때 나이가 40~50대에 임신 횟수가 12번 이상인 경우에 해당함

    일반적이지 않지만 원주민 대상이므로, 임신이 가능한 나이를 15살로 고려해보면 산술적으로 가능한 경우에 해당하므로 이상치로 제외하지 않음

    Note
    방법론을 통해 이상치 확인 후 곧바로 제거하지 않고, 변수 의미 혹은 이상치에 대한 통계량 확인 후 이상치 판단 필요(왜 이상치로 판단했는지 주관적인 해석)
    20.1.3 앞선 두 단계에서 얻은 향후 분석시 고려사항에 대해 작성하시오.
    반응변수(당뇨 유무)를 보면 yes의 빈도가 no의 빈도보다 많은 편향된 분포 형태임

    반응변수의 클래스가 불균형할 경우, 빈도가 큰 범주에 해당하는 관측치 쪽으로 편향된 분류 경계선이 생성될 수 있음

    적절한 분류 경계선이 생성될 수 있도록, 언더샘플링, 오버샘플링을 고려해볼 수 있음

    이진분류의 cut-off value를 0.5가 아니라 다른 값으로 조정함으로써, 빈도가 작은 범주에 해당하는 데이터에 더 큰 가중치를 부여할 수 있음

    20.1.4 클래스 불균형을 처리하시오.
    업샘플링 과정에 대해 설명하고 결과를 작성하시오.
    업샘플링은 클래스가 불균형일 때 빈도가 낮은 levels에 해당하는 표본을 복원 추출을 통해 빈도가 높은 levels에 해당하는 표본의 수만큼 관측치를 복제함으로써 클래스 균형을 맞추는 방법이다.

    oversample = RandomOverSampler(sampling_strategy='minority')
    train_X_over, train_y_over = oversample.fit_resample(train_X, train_y)
    print(Counter(train_y_over))

    Counter({0: 286, 1: 286})
    언더샘플링 과정에 대해 설명하고 결과를 작성하시오.
    다운샘플링은 클래스가 불균형일 때 빈도가 높은 levels에 해당하는 표본을 빈도가 적은 levels에 해당하는 표본의 수만큼 무작위 추출해서 클래스 균형을 맞추는 방법이다.

    undersample = RandomUnderSampler(sampling_strategy='majority')
    train_X_under, train_y_under = undersample.fit_resample(train_X, train_y)
    print(Counter(train_y_under))

    Counter({0: 143, 1: 143})
    둘 중 한가지를 선택하고 이유를 작성하시오.
    오버샘플링을 선택함

    이상치 제거 과정에서 데이터의 소실이 발생했기 때문에 언더샘플링을 할 경우 더욱더 많은 데이터가 제거되므로 너무 많은 정보의 손실이 발생된다.

    20.1.5 최소 3개 이상 모델을 제시하고, 정확도 측면의 모델 1개와 속도 측면의 모델 1개를 구현하시오.
    Random forest

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.ensemble import RandomForestClassifier
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    pipe_rf = Pipeline(
        [
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}

    start_time = time.time()
    RandomForest_search = GridSearchCV(estimator = pipe_rf, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV

    RandomOverSampler

    RandomForestClassifier
    print("{}s".format(time.time()-start_time))

    2.1542577743530273s
    print('RandomForest best score : ', RandomForest_search.best_score_)

    RandomForest best score :  0.743738439371468
    from sklearn.tree import DecisionTreeClassifier

    pipe_dt = Pipeline(
        [
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
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

    RandomOverSampler

    DecisionTreeClassifier
    print("{}s".format(time.time()-start_time))

    0.13738799095153809s
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.6579620283236937
    import xgboost as xgb

    pipe_xgb = Pipeline(
        [
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", xgb.XGBClassifier())
        ]
    )

    Xgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}

    start_time = time.time()
    xgb_search = GridSearchCV(estimator = pipe_xgb, 
                          param_grid = Xgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    xgb_search.fit(train_X, train_y)

    GridSearchCV

    RandomOverSampler

    XGBClassifier
    print("{}s".format(time.time()-start_time))

    4.033076047897339s
    print('XGBOOST best score : ', xgb_search.best_score_)

    XGBOOST best score :  0.7323879268722724
    속도

    rf : Time difference of 2.73 secs

    decision tree : Time difference of 0.17 secs

    xgboost : Time difference of 3.59 secs

    속도 측면 decision tree가 가장 좋다.

    balanced accuracy 기준

    Random forest가 가장 좋다.
    pred_rf = RandomForest_search.predict(test_X)
    print(classification_report(test_y, pred_rf))

                  precision    recall  f1-score   support

               0       0.83      0.82      0.83        72
               1       0.65      0.67      0.66        36

        accuracy                           0.77       108
       macro avg       0.74      0.74      0.74       108
    weighted avg       0.77      0.77      0.77       108
    print(balanced_accuracy_score(test_y, pred_rf))

    0.7430555555555556
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.69인 것을 확인할 수 있다.

    20.1.6 모델별로 비교하고 결과를 설명하시오.
    반응변수에 class불균형이 있으므로, weighted avg 지표를 활용한다.

    sensitivity(실제 당뇨병이 있을 때 예측 결과에서도 당뇨병이 있다고 판단하는 비율)를 기준으로 보면 rf>xgb>dt 순이다.

    precision(예측 결과 당뇨병이 있을 때 실제로 당뇨병이 있는 비율)을 기준으로 보면 rf>xgb>dt 순이다.

    Balanced accuracy(

    )를 기준으로 보면 rf>xgb>dt 순이다.

    F1 score를 기준으로 보면 rf>xgb>dt 순이다.

    반응변수의 각 범주간 빈도가 불균형할 때, 소수 범주에 비해서 다수 범주에 더 많은 가중치가 부여되어 소수 범주에 대한 분류를 어렵게 한다. 따라서 이러한 문제를 보완할 수 있는 평가지표를 고려해야 하므로, 위에 제시한 평가지표 중 Balanced accuracy와 F1 score를 고려해볼 수 있다. 지표를 비교해보면 balanced accuracy, F1 score, precision 등 모든 지표에서 random forest 모형이 우세하다. 따라서 최종적으로 random forest 모형을 선택한다.

    20.1.7 속도 측면의 개선을 위해 차원 축소를 수행하고, 예측 성능 및 속도 면에서의 결과를 작성하시오.
    pca_pipe = Pipeline([("scaler", StandardScaler()), 
                         ("PCA", PCA(n_components= 0.8, svd_solver='full'))])

    preprocess = ColumnTransformer(
        [("num_process", pca_pipe, train_X.columns)], 
        remainder='passthrough'
    )

    pipe_rf2 = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}

    start_time = time.time()
    RandomForest_search2 = GridSearchCV(estimator = pipe_rf2, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    RandomForest_search2.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA

    RandomOverSampler

    RandomForestClassifier
    print("{}s".format(time.time()-start_time))

    2.1927738189697266s
    pred_rf2 = RandomForest_search2.predict(test_X)
    print(classification_report(test_y, pred_rf2))

                  precision    recall  f1-score   support

               0       0.86      0.76      0.81        72
               1       0.61      0.75      0.67        36

        accuracy                           0.76       108
       macro avg       0.74      0.76      0.74       108
    weighted avg       0.78      0.76      0.76       108
    print(balanced_accuracy_score(test_y, pred_rf2))

    0.7569444444444444
    속도

    차원 축소 전 : Time difference of 2.73 secs

    차원 축소 후 : Time difference of 2.65 secs

    미미하게 차원 축소 후에 속도가 감소했다.

    모델 성능

    balanced accuracy, precision, F1 score 등 모든 지표에서 차원 축소 후 성능이 전체적으로 낮아졌다.
    """