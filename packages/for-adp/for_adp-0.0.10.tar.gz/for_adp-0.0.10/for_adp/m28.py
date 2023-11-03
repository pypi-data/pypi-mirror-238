def m28():
    """
        ADP python 기출문제
    26  28회차 기출문제
    26  28회차 기출문제
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
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve, f1_score
    from sklearn import set_config
    set_config(display="diagram")

    Data description

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

    absences : 결석 횟수(0 ~ 80) —> 결석 유무

    dat = pd.read_csv('./data/adp28.csv')

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 395 entries, 0 to 394
    Data columns (total 12 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   sex         395 non-null    object
     1   age         395 non-null    int64 
     2   pstatus     395 non-null    object
     3   medu        395 non-null    int64 
     4   fedu        395 non-null    int64 
     5   guardian    395 non-null    object
     6   traveltime  395 non-null    int64 
     7   studytime   395 non-null    int64 
     8   failures    395 non-null    object
     9   freetime    395 non-null    int64 
     10  famrel      395 non-null    int64 
     11  absences    395 non-null    int64 
    dtypes: int64(8), object(4)
    memory usage: 37.2+ KB
    dat = dat.assign(absences = np.where(dat['absences'] == 0, 'Yes', 'No'))

    26.0.1 EDA를 실시하시오.
    26.0.1.1 데이터 품질을 살펴보고, 차원축소가 필요한지 검토하시오.
    데이터에 함정이 있었음. (failures 변수는 설명을 보면 numeric인데, A, T가 들어 있었고, 0~1은 숫자 그대로이고, A, T는 4로 바꾸어야 함)

    dat.hist();
    plt.subplots_adjust(top=0.9, hspace = 0.5, wspace = 0.3);
    plt.show();



    #dat.select_dtypes('object').columns
    f, axes = plt.subplots(ncols = 2, nrows = 3, figsize = (20,4))
    sns.countplot(dat['sex'], ax = axes[0, 0])
    sns.countplot(dat['pstatus'], ax = axes[0, 1])
    sns.countplot(dat['guardian'], ax = axes[1, 0])
    sns.countplot(dat['failures'], ax = axes[1, 1])
    sns.countplot(dat['absences'], ax = axes[2, 0])
    plt.subplots_adjust(top=0.9, hspace = 0.5, wspace = 0.7)
    plt.show();



    failures(학사경고횟수)는 수치형 변수이지만 A, T 값이 존재함에 따라 범주형 변수로 인식됨

    데이터 수집 과정 혹은 코딩상의 문제이므로, 데이터 정합성을 고려하여 삭제 후 수치형으로 변환

    dat = dat.loc[~dat.failures.isin(['A', 'T'])]
    dat = dat.astype({'failures' : 'int64'})

    corr = dat.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.show();



    변수간 상관관계가 높은 고차원 데이터의 경우 모델 학습 시 과적합될 가능성이 있으며, 계산량이 많아져 모델 효율성이 떨어질 수 있음

    변수 간 상관관계가 높다는 의미는 변수 간 중복되는 정보가 있다는 의미로도 볼 수 있으므로, 적절한 차원 축소 기법을 통해 과적합을 방지하고 모델의 계산 효율성을 확보하는 것이 합리적일 수 있음

    주어진 데이터는 변수 개수가 많지 않고, 변수간 상관관계가 높지 않으므로, 차원 축소 고려 안함

    26.0.2 위에서 적용한 것이 과적합이라는 전제하에, 이를 해결하기 위한 방법을 2개 제시하고 구현하시오.
    차원 축소 : 위의 내용 참고

    Oversampling or undersampling

    반응변수 범주의 빈도가 불균형할 경우 다수 범주에 과적합되어 소수 범주에 대한 예측 성능이 떨어지는 문제가 발생할 수 있다. 이를 해결하기 위해 오버샘플링 혹은 언더샘플링을 고려해볼 수 있다.

    오버샘플링은 반응변수의 빈도가 불균형일 때 빈도가 낮은 levels에 해당하는 표본을 복원 추출을 통해 빈도가 높은 levels에 해당하는 표본의 수만큼 관측치를 복제함으로써 클래스 균형을 맞추는 방법이다.

    언더샘플링은 클래스가 불균형일 때 빈도가 높은 levels에 해당하는 표본을 빈도가 적은 levels에 해당하는 표본의 수만큼 무작위 추출해서 클래스 균형을 맞추는 방법이다.

    이상치 제거 과정에서 데이터의 소실이 발생했기 때문에 언더샘플링을 할 경우 더욱더 많은 데이터가 제거되므로 너무 많은 정보의 손실이 발생된다. 따라서 오버샘플링을 고려해볼 수 있다.

    dat = dat.assign(absences = np.where(dat['absences'] == 'Yes', 1, 0))
    y = dat['absences']
    X = dat.drop(['absences'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = dat['absences'], random_state = 0)

    PCA

    num_columns = train_X.select_dtypes('number').columns

    pca_pipe = Pipeline([("scaler", StandardScaler()), 
                         ("PCA", PCA(n_components= 0.8, svd_solver='full'))])

    preprocess1 = ColumnTransformer(
        [("num_process", pca_pipe, num_columns)]
    )

    PCA_train_X = pd.DataFrame(preprocess1.fit_transform(train_X))
    #PCA_test_X = pd.DataFrame(preprocess2.transform(test_X))

    PCA_train_X.columns = ['PC'+str(i) for i in range(PCA_train_X.shape[1])]
    PCA_train_X.head()

            PC0       PC1       PC2       PC3       PC4       PC5
    0  1.042815 -0.485500  0.086446  0.732200 -0.048440  0.668696
    1 -2.020462  0.326171  0.211770 -0.498618  0.188831 -0.945393
    2  0.843073  0.393607  0.555315 -0.931509 -0.843650  0.204153
    3 -2.482668  0.946843 -0.137243 -0.149993 -0.059408 -0.180378
    4 -0.416141 -0.204214 -1.339924 -0.574988  0.267688 -0.915290
    # PCA_test_X.columns = ['PC'+str(i) for i in range(PCA_test_X.shape[1])]

    Upsampling

    oversample = RandomOverSampler(sampling_strategy='minority')
    train_X_over, train_y_over = oversample.fit_resample(train_X, train_y)
    print(Counter(train_y_over))

    Counter({0: 209, 1: 209})
    26.0.3 Random forest, neural network, Lightgbm 알고리즘 적용하여 F1 score를 구하고 성능을 비교하시오.
    cat_columns = train_X.select_dtypes('object').columns

    encoding_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer(
        [("num_process", pca_pipe, num_columns), 
        ("cat_process", encoding_preprocess, cat_columns)]
        , remainder='passthrough'
    )

    Random forest

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.ensemble import RandomForestClassifier

    pipe_rf = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_search = GridSearchCV(estimator = pipe_rf, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder

    RandomOverSampler

    RandomForestClassifier
    print('Random Forest best score : ', RandomForest_search.best_score_)

    Random Forest best score :  0.510345245967839
    neural network

    from sklearn.neural_network import MLPClassifier

    mlp_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", MLPClassifier())
        ]
    )

    MLP_param = {'classifier__learning_rate_init': np.arange(0.01, 0.2, 0.02)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    MLP_search = GridSearchCV(estimator = mlp_pipe, 
                          param_grid = MLP_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    MLP_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder

    RandomOverSampler

    MLPClassifier
    print('MLP best score : ', MLP_search.best_score_)

    MLP best score :  0.5194332283035749
    lightgbm

    from lightgbm import LGBMClassifier

    pipe_lgb = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", LGBMClassifier())
        ]
    )
    #LGBMClassifier().get_params()
    lgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    lgb_search = GridSearchCV(estimator = pipe_lgb, 
                          param_grid = lgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    lgb_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder

    RandomOverSampler

    LGBMClassifier
    print('LGBM best score : ', lgb_search.best_score_)

    LGBM best score :  0.5040360787408285
    교차검증 score 기준으로 MLP가 balanced accuracy = 0.52로 가장 좋음
    pred_mlp = MLP_search.predict(test_X)
    print(classification_report(test_y, pred_mlp))

                  precision    recall  f1-score   support

               0       0.61      0.52      0.56        52
               1       0.17      0.23      0.19        22

        accuracy                           0.43        74
       macro avg       0.39      0.37      0.38        74
    weighted avg       0.48      0.43      0.45        74
    print(balanced_accuracy_score(test_y, pred_mlp))

    0.3732517482517483
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.46인 것을 확인할 수 있다.

    26.0.4 hard voting, soft voting
    hard voting

    다수결 투표에 의해 최종 예측값을 산출하는 방식

    모형이 3개 이므로 2개 이상 예측 결과가 같은 경우 최종 예측값으로 산출

    from sklearn.ensemble import VotingClassifier
    RandomForest_search.best_params_

    {'classifier__max_features': 0.6}
    MLP_search.best_params_

    {'classifier__learning_rate_init': 0.16999999999999998}
    lgb_search.best_params_

    {'classifier__learning_rate': 0.01}
    voting_hard = VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(max_features = 0.6)),
        ('mlp', MLPClassifier(learning_rate_init = 0.12999999999999998)),
        ('lgb', LGBMClassifier(learning_rate =  0.16000000000000003))
    ], voting='hard')

    pipe_voting1 = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", voting_hard)
        ]
    )

    pipe_voting1.fit(train_X, train_y)

    Pipeline
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder

    RandomOverSampler
    classifier: VotingClassifier
    rf

    RandomForestClassifier
    mlp

    MLPClassifier
    lgb

    LGBMClassifier
    pred_voting_hard = pipe_voting1.predict(test_X)
    print(classification_report(test_y, pred_voting_hard))

                  precision    recall  f1-score   support

               0       0.66      0.63      0.65        52
               1       0.21      0.23      0.22        22

        accuracy                           0.51        74
       macro avg       0.43      0.43      0.43        74
    weighted avg       0.53      0.51      0.52        74
    print(balanced_accuracy_score(test_y, pred_voting_hard))

    0.43094405594405594
    soft voting

    classification일 때 예측값을 평균내는 것은 부적절

    따라서 예측값 대신 예측 확률값을 평균 내서 최종 앙상블 결과로 산출

    voting_soft = VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(max_features = 0.6)),
        ('mlp', MLPClassifier(learning_rate_init = 0.12999999999999998)),
        ('lgb', LGBMClassifier(learning_rate =  0.16000000000000003))
    ], voting='soft')

    pipe_voting2 = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", voting_soft)
        ]
    )

    pipe_voting2.fit(train_X, train_y)

    Pipeline
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder

    RandomOverSampler
    classifier: VotingClassifier
    rf

    RandomForestClassifier
    mlp

    MLPClassifier
    lgb

    LGBMClassifier
    pred_voting_soft = pipe_voting2.predict(test_X)
    print(classification_report(test_y, pred_voting_soft))

                  precision    recall  f1-score   support

               0       0.67      0.62      0.64        52
               1       0.23      0.27      0.25        22

        accuracy                           0.51        74
       macro avg       0.45      0.44      0.44        74
    weighted avg       0.54      0.51      0.52        74
    print(balanced_accuracy_score(test_y, pred_voting_soft))

    0.44405594405594406
    26.0.5 추가적인 처리 방안이 있으면 제시하시오.
    더미코딩을 했을 때, 데이터의 차원이 늘어나서 계산량이 많아지는 문제가 있으므로, 이를 해결하기 위해서 class 빈도가 낮은 경우 병합을 통해 범주형 변수별 class의 개수를 줄여서 더미코딩을 했을 때, 차원이 늘어나는 문제를 해결할 수 있음

    또한 변수선택을 통해 예측에 필요한 변수를 뽑고, 계산 속도 및 예측 성능을 개선해볼 수 있음

    feature importance가 높은 변수를 선택

    recursive feature elimination을 통해 변수중요도가 낮은 변수를 하나씩 제거해가면서 모델의 성능을 보고 변수 선택을 해볼 수 있음

    absences와 연관이 있는 변수를 찾기 위해 통계 검정을 해보고 검정 결과 유의한 변수를 선택해볼 수 있음

    이 중 recursive feature elimination을 적용해보면 다음과 같다.

    from sklearn.feature_selection import RFE, RFECV

    pipe_voting3 = Pipeline(
        [
            ("preprocess", preprocess),
            ('feat_sel', RFE(estimator=RandomForestClassifier(), step=1)),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", voting_soft)
        ]
    )

    rfe_param = {'feat_sel__n_features_to_select': [4,5,6,7,8,9,10]}
    voting_search = GridSearchCV(estimator = pipe_voting3, 
                          param_grid = rfe_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    voting_search.fit(train_X, train_y)                      

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler

    PCA
    cat_process

    OneHotEncoder
    feat_sel: RFE

    RandomForestClassifier

    RandomOverSampler
    classifier: VotingClassifier
    rf

    RandomForestClassifier
    mlp

    MLPClassifier
    lgb

    LGBMClassifier
    print(voting_search.best_params_) 

    {'feat_sel__n_features_to_select': 7}
    #rfe_features = voting_search.best_estimator_.named_steps['feat_sel'].get_support(indices=True)
    #voting_search.best_estimator_.named_steps['preprocess'].get_feature_names()

    pred_voting_soft_rfe = voting_search.predict(test_X)
    print(classification_report(test_y, pred_voting_soft_rfe))

                  precision    recall  f1-score   support

               0       0.68      0.62      0.65        52
               1       0.26      0.32      0.29        22

        accuracy                           0.53        74
       macro avg       0.47      0.47      0.47        74
    weighted avg       0.56      0.53      0.54        74
    print(balanced_accuracy_score(test_y, pred_voting_soft_rfe))

    0.46678321678321677

    # roc_result = plot_roc_curve(voting_search, test_X, test_y)
    # roc_result.plot();
    # plt.show(); 
    # 
    # print("AUC for voting classifier: %f" % roc_result.roc_auc)

    축소모형과 full 모형의 결과를 비교해보면 balanced accuracy, f1-score 등 모든 지표에서 full 모형이 우세하므로, full 모형을 선택하였다.

    학교 운영시스템에 적용한다면 검토사항은 무엇이 있을지 제시하시오.

    모형 성능이 낮으므로, 학교 시스템에 직접 적용하는데 한계가 있다. 결석 유무와 관련이 있는 다른 정보를 수집하는 것이 필요해보인다.

    다만 결석 유무에 관련이 있는 변수를 파악해보면 다음과 같다.

    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        pipe_voting2, train_X, train_y, n_repeats=10, random_state=42
    )

    features = train_X.columns
    importances = feature_importances.importances_mean

    plt.bar(features, importances)

    <BarContainer object of 11 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Text(0, 0, 'sex'), Text(1, 0, 'age'), Text(2, 0, 'pstatus'), Text(3, 0, 'medu'), Text(4, 0, 'fedu'), Text(5, 0, 'guardian'), Text(6, 0, 'traveltime'), Text(7, 0, 'studytime'), Text(8, 0, 'failures'), Text(9, 0, 'freetime'), Text(10, 0, 'famrel')])
    plt.tight_layout()
    plt.show();



    feature importance plot을 통해 결석 유무와 관련이 있는 변수를 추려보면 age, traveltime, studytime, freetime, famrel 등의 변수이다. 해당 변수와 반응변수 간의 관계를 살펴보면 다음과 같다.

    from sklearn.inspection import partial_dependence
    from sklearn.inspection import plot_partial_dependence
    #from sklearn.inspection import PartialDependenceDisplay

    selected_columns = ['age', 'traveltime', 'studytime', 'freetime', 'famrel']

    fig, ax = plt.subplots(figsize=(5, 5))
    plt.subplots_adjust(top=0.9, hspace=0.7)
    plot_partial_dependence(estimator=pipe_voting2, 
                            X=train_X, 
                            features=selected_columns, # 관심변수 
                            percentiles=(0, 1), # 최소, 최대 
                            ax=ax)

    <sklearn.inspection._plot.partial_dependence.PartialDependenceDisplay object at 0x16bd38b80>
    plt.tight_layout()                        
    plt.show();



    해석 예시

    나이가 들어갈수록, 결석할 확률은 낮아지는 경향이 있다.

    저학년의 경우 학교에 적응하는 시간이 필요하므로, 학교를 성실히 다닐 수 있도록, 조기 교육이 필요해보인다.
    등하교기간이 늘어날수록, 결석할 확률은 낮아지는 경향이 있다.

    자유시간이 매우 낮거나, 매우 높을 때, 결석할 확률은 낮아지는 경향이 있다.

    학사경고횟수가 늘어날수록, 결석할 확률은 높아지는 경향이 있다.

    학사경고를 받은 학생의 경우 학교에 적응할 수 있도록, 체벌과 인성 교육을 함께 진행하는 것이 필요해보인다.
    가족관계가 좋을수록, 결석할 확률은 높아지는 경향이 있다.

    해당 결과는 데이터 수집 과정에 대해 조사해볼 필요가 있어보인다.

    실제 데이터의 분포를 확인했을 때, 결석을 한 학생의 경우 가족 관계가 대부분 4 ~5 사이인 것을 확인할 수 있다.

    가족관계의 경우 단순하게 설문조사를 할 경우 민감한 질문에 해당하므로, 왜곡된 결과를 도출할 수 있다.
    25  27회차 기출문제
    27  29회차 기출문제

    Copyright 2023, Don Don

    """