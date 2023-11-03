def m29():
    """
    ADP python 기출문제
    27  29회차 기출문제
    27  29회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    Data description

    데이터 출처 : https://www.data.go.kr/data/15094266/fileData.do
    데이터 설명 : 대구도시공사_빅데이터_영구임대아파트 입주자 퇴거여부 예측을 위한 기계학습용 데이터_20201231
    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time


    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn import set_config
    import xgboost as xgb
    from collections import Counter
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve, f1_score
    from sklearn import set_config
    set_config(display="diagram")

    dat = pd.read_csv('data/adp29_1.csv')

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 86904 entries, 0 to 86903
    Data columns (total 23 columns):
     #   Column   Non-Null Count  Dtype  
    ---  ------   --------------  -----  
     0   순번       86904 non-null  int64  
     1   계약구분     86396 non-null  object 
     2   재계약횟수    86904 non-null  int64  
     3   거주개월     86904 non-null  int64  
     4   아파트 이름   86904 non-null  object 
     5   아파트 ID   86904 non-null  int64  
     6   아파트 평점   85679 non-null  float64
     7   호실고유번호   86904 non-null  int64  
     8   층        86904 non-null  int64  
     9   평형대      86904 non-null  int64  
     10  계약자고유번호  86904 non-null  int64  
     11  계약서고유번호  86904 non-null  int64  
     12  입주연도     86904 non-null  int64  
     13  퇴거연도     25762 non-null  float64
     14  거주연도     86904 non-null  int64  
     15  월세(원)    86904 non-null  float64
     16  보증금(원)   86904 non-null  int64  
     17  대표나이     86904 non-null  int64  
     18  나이       86904 non-null  int64  
     19  성별       86904 non-null  object 
     20  결혼여부     86904 non-null  object 
     21  거주자 수    86904 non-null  int64  
     22  퇴거여부     86904 non-null  object 
    dtypes: float64(3), int64(15), object(5)
    memory usage: 15.2+ MB
    27.1 문제1
    27.1.1 계약자고유번호를 기준으로 거주연도 별 여러개의 데이터가 쌓여 있다. 각 계약자고유번호에 대해 가장 최신의 거주연도 행만 남기시오.
    dat = (dat
        .groupby(['계약자고유번호'])
        .apply(lambda x: x.loc[x["거주연도"].idxmax()])
    )

    dat.head()

                순번 계약구분  재계약횟수  거주개월    아파트 이름  ...  나이  성별  결혼여부  거주자 수  퇴거여부
    계약자고유번호                                     ...                           
    1        12673   해지      4    88  지산5단지아파트  ...  35   남    기혼      2    퇴거
    6        12683   해지      7   174  지산5단지아파트  ...  27   남    미혼      1    퇴거
    14       12702   유효     10   237  지산5단지아파트  ...  66   남    미혼      1   미퇴거
    27       12789   유효     10   227  지산5단지아파트  ...  60   남    기혼      3   미퇴거
    40       12796   유효     10   222  지산5단지아파트  ...  57   여    미혼      2   미퇴거

    [5 rows x 23 columns]
    from matplotlib import font_manager, rc
    rc('font', family='AppleGothic')            ## 이 두 줄을 
    plt.rcParams['axes.unicode_minus'] = False 

    dat.hist()

    array([[<Axes: title={'center': '순번'}>,
            <Axes: title={'center': '재계약횟수'}>,
            <Axes: title={'center': '거주개월'}>,
            <Axes: title={'center': '아파트 ID'}>],
           [<Axes: title={'center': '아파트 평점'}>,
            <Axes: title={'center': '호실고유번호'}>,
            <Axes: title={'center': '층'}>, <Axes: title={'center': '평형대'}>],
           [<Axes: title={'center': '계약자고유번호'}>,
            <Axes: title={'center': '계약서고유번호'}>,
            <Axes: title={'center': '입주연도'}>,
            <Axes: title={'center': '퇴거연도'}>],
           [<Axes: title={'center': '거주연도'}>,
            <Axes: title={'center': '월세(원)'}>,
            <Axes: title={'center': '보증금(원)'}>,
            <Axes: title={'center': '대표나이'}>],
           [<Axes: title={'center': '나이'}>,
            <Axes: title={'center': '거주자 수'}>, <Axes: >, <Axes: >]],
          dtype=object)
    plt.tight_layout()
    plt.show();



    27.1.2 결측치를 처리하시오.
    dat.isna().sum()

    순번            0
    계약구분         61
    재계약횟수         0
    거주개월          0
    아파트 이름        0
    아파트 ID        0
    아파트 평점      140
    호실고유번호        0
    층             0
    평형대           0
    계약자고유번호       0
    계약서고유번호       0
    입주연도          0
    퇴거연도       6256
    거주연도          0
    월세(원)         0
    보증금(원)        0
    대표나이          0
    나이            0
    성별            0
    결혼여부          0
    거주자 수         0
    퇴거여부          0
    dtype: int64
    계약 구분 변수에 결측치 61개 존재

    아파트 평점 변수에 결측치 140개 존재

    퇴거연도에 결측치 6256개 존재

    dat.loc[dat['아파트 평점'].isna(), :].head(2)

                순번 계약구분  재계약횟수  거주개월    아파트 이름  ...  나이  성별  결혼여부  거주자 수  퇴거여부
    계약자고유번호                                     ...                           
    278      12189   유효     10   222  지산5단지아파트  ...  79   남    기혼      2   미퇴거
    743      11546   해지      5   107  지산5단지아파트  ...  80   여    미혼      1    퇴거

    [2 rows x 23 columns]
    퇴거 여부, 아파트 유형, 계약 구분 등의 변수를 확인했을 때, 해당 결측치의 경우 특징 존재 x

    아파트 평점 변수의 경우 결측치가 전체 데이터의 약 1%정도이므로 삭제

    dat.loc[dat['계약구분'].isna(), :].head(2)

                순번 계약구분  재계약횟수  거주개월    아파트 이름  ...  나이  성별  결혼여부  거주자 수  퇴거여부
    계약자고유번호                                     ...                           
    705      11517  NaN      7   156  지산5단지아파트  ...  74   남    기혼      2    퇴거
    2388     11496  NaN     10   228  지산5단지아파트  ...  60   여    미혼      1   미퇴거

    [2 rows x 23 columns]
    계약 구분 변수의 경우 유효, 해지로 나뉘고, 결측치가 존재하는 행의 경우 재계약 횟수가 여러 번인 케이스가 대부분임

    아파트 평점 변수의 경우 결측치가 전체 데이터의 약 0.5%정도이므로 삭제

    dat.loc[dat['퇴거연도'].isna(), :].head(2)

                순번 계약구분  재계약횟수  거주개월    아파트 이름  ...  나이  성별  결혼여부  거주자 수  퇴거여부
    계약자고유번호                                     ...                           
    14       12702   유효     10   237  지산5단지아파트  ...  66   남    미혼      1   미퇴거
    27       12789   유효     10   227  지산5단지아파트  ...  60   남    기혼      3   미퇴거

    [2 rows x 23 columns]
    퇴거연도 변수의 경우 해당 거주자가 퇴거를 안했을 때, 결측치가 생성됨

    퇴거여부 변수와 거주개월 변수가 존재하므로, 두 변수를 통해 퇴거연도를 유추할 수 있음

    따라서 퇴거연도 변수 제거

    dat = dat.loc[(dat['아파트 평점'].notna()) & (dat['계약구분'].notna())]
    dat = dat.drop(['퇴거연도'], axis = 1)

    27.1.3 이상치를 처리하시오.
    보증금, 월세의 경우 이상치 존재

    집값의 경우 지역별, 주변환경, 경제 요인 등 외부 요인에 따라 차이가 클 수 있음

    따라서 이상치 제거 x

    # 1분위수 계산
    Q1 = np.quantile(dat['월세(원)'], 0.25)
    # 3분위수 계산
    Q3 = np.quantile(dat['월세(원)'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) # 위 울타리
    LC = Q3 - (1.5 * IQR) # 위 울타리
    outlier1 = dat.loc[(dat['월세(원)'] > UC) | (dat['월세(원)'] < LC), :].index.tolist()

    # 1분위수 계산
    Q1 = np.quantile(dat['보증금(원)'], 0.25)
    # 3분위수 계산
    Q3 = np.quantile(dat['보증금(원)'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) # 위 울타리
    LC = Q3 - (1.5 * IQR) # 위 울타리
    outlier2 = dat.loc[(dat['보증금(원)'] > UC) | (dat['보증금(원)'] < LC), :].index.tolist()

    dat2 = dat.copy()
    dat2 = dat2.assign(outlier = np.where(dat2.index.isin(outlier1) | dat2.index.isin(outlier2), 1, 0))

    sns.scatterplot(x='월세(원)', 
                    y='보증금(원)', 
                    hue='outlier',
                    s=50, # marker size
                    data=dat2)
    plt.show();



    27.1.4 재계약 횟수의 중앙값을 기준으로 중앙값보다 크거나 같으면 ‘높음’, 작으면 ‘낮음’ 으로 하는 이분 변수를 구성하시오.
    y = dat['재계약횟수']
    X = dat.drop(['재계약횟수'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.3, shuffle = True, random_state = 0)

    cutoff = train_y.median()
    train_X['outcome_index'] = np.where(train_y >= cutoff, '높음', '낮음')
    test_X['outcome_index'] = np.where(test_y >= cutoff, '높음', '낮음')

    27.1.5 차원축소의 필요성을 논하고, 필요에 따라 차원을 축소하고 불필요하다면 그 근거를 논하시오.
    변수간 상관관계가 높은 고차원 데이터의 경우 모델 학습 시 과적합될 가능성이 있으며, 계산량이 많아져 모델 효율성이 떨어질 수 있음

    변수 간 상관관계가 높다는 의미는 변수 간 중복되는 정보가 있다는 의미로도 볼 수 있으므로, 적절한 차원 축소 기법을 통해 과적합을 방지하고 모델의 계산 효율성을 확보하는 것이 합리적일 수 있음

    주어진 데이터는 변수간 상관관계가 대부분 0.4 이하로 높지 않으므로, 차원 축소 고려 안함

    num_columns = ['거주개월', '아파트 평점', '층', '평형대', '월세(원)', '보증금(원)', '대표나이', '나이', '거주자 수']
    corr = train_X[num_columns].corr()
    sns.heatmap(corr, annot = True);
    plt.tight_layout()
    plt.show();



    27.1.6 재계약 횟수 이분변수를 활용하여 세그먼트를 구분하고 각 세그먼트의 특징을 분석하시오.
    f, axes = plt.subplots(ncols = 3)
    sns.boxplot(x = "outcome_index", y = "거주개월", data = train_X, ax = axes[0])
    sns.boxplot(x = "outcome_index", y = "아파트 평점", data = train_X, ax = axes[1])
    sns.boxplot(x = "outcome_index", y = "층", data = train_X, ax = axes[2])
    plt.tight_layout()
    plt.show();



    재계약횟수가 높은 경우 거주 개월 수도 높은 경향이 있음
    f, axes = plt.subplots(ncols = 3)
    sns.boxplot(x = "outcome_index", y = "평형대", data = train_X, ax = axes[0])
    sns.boxplot(x = "outcome_index", y = "월세(원)", data = train_X, ax = axes[1])
    sns.boxplot(x = "outcome_index", y = "보증금(원)", data = train_X, ax = axes[2])
    plt.tight_layout()
    plt.show();



    재계약횟수가 낮은 경우 평형대는 대부분 12평대인 경향이 있음

    재계약횟수가 높은 경우 월세가 높은 경향이 있음

    재계약횟수가 높은 경우 보증금이 높은 경향이 있음

    f, axes = plt.subplots(ncols = 3)
    sns.boxplot(x = "outcome_index", y = "대표나이", data = train_X, ax = axes[0])
    sns.boxplot(x = "outcome_index", y = "나이", data = train_X, ax = axes[1])
    sns.boxplot(x = "outcome_index", y = "거주자 수", data = train_X, ax = axes[2])
    plt.tight_layout()
    plt.show();



    재계약횟수가 높은 경우 거주 나이대는 높은 경향이 있음

    재계약횟수가 높은 경우 대표자 나이대는 높은 경향이 있음

    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(train_X, ['outcome_index', '계약구분'])

    (<Figure size 1400x1000 with 3 Axes>, {('높음', '유효'): (0.0, 0.0, 0.5219572978413578, 0.7131354957441913), ('높음', '해지'): (0.0, 0.7164577548804039, 0.5219572978413578, 0.283542245119596), ('낮음', '유효'): (0.5269324222194672, 0.0, 0.4730675777805328, 0.47782684704130046), ('낮음', '해지'): (0.5269324222194672, 0.4811491061775131, 0.4730675777805328, 0.5188508938224868)})
    plt.show();



    재계약 횟수가 높은 경우 계약도 유효한 경향이 있음
    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(train_X, ['outcome_index', '아파트 이름'])

    (<Figure size 1400x1000 with 3 Axes>, {('높음', '지산5단지아파트'): (0.0, 0.0, 0.5219572978413578, 0.1602360369522841), ('높음', '비둘기아파트'): (0.0, 0.16352551063649462, 0.5219572978413578, 0.39886854818204937), ('높음', '용지아파트'): (0.0, 0.5656835325027546, 0.5219572978413578, 0.38747987117552346), ('높음', '까치아파트'): (0.0, 0.9564528773624885, 0.5219572978413578, 0.02436647173489279), ('높음', '강남아파트'): (0.0, 0.9841088227815918, 0.5219572978413578, 0.0158911772184083), ('낮음', '지산5단지아파트'): (0.5269324222194672, 0.0, 0.4730675777805328, 0.13939108208780762), ('낮음', '비둘기아파트'): (0.5269324222194672, 0.14268055577201816, 0.4730675777805328, 0.4482723688106854), ('낮음', '용지아파트'): (0.5269324222194672, 0.594242398266914, 0.4730675777805328, 0.3699562052896529), ('낮음', '까치아파트'): (0.5269324222194672, 0.9674880772407776, 0.4730675777805328, 0.019286816389507983), ('낮음', '강남아파트'): (0.5269324222194672, 0.990064367314496, 0.4730675777805328, 0.009935632685504122)})
    plt.show();



    아파트 이름과 계약 구분 변수 간에는 연관성이 존재하지 않음
    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(train_X, ['outcome_index', '성별'])

    (<Figure size 1400x1000 with 3 Axes>, {('높음', '여'): (0.0, 0.0, 0.5219572978413578, 0.6114882757956569), ('높음', '남'): (0.0, 0.6148105349318694, 0.5219572978413578, 0.3851894650681304), ('낮음', '여'): (0.5269324222194672, 0.0, 0.4730675777805328, 0.5244584973393396), ('낮음', '남'): (0.5269324222194672, 0.5277807564755522, 0.4730675777805328, 0.47221924352444766)})
    plt.show();



    재계약 횟수가 높은 경우 집주인이 여성인 경향이 있음
    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(train_X, ['outcome_index', '결혼여부'])

    (<Figure size 1400x1000 with 3 Axes>, {('높음', '미혼'): (0.0, 0.0, 0.5219572978413578, 0.8401945206798593), ('높음', '기혼'): (0.0, 0.8435167798160719, 0.5219572978413578, 0.156483220183928), ('낮음', '미혼'): (0.5269324222194672, 0.0, 0.4730675777805328, 0.89397005539722), ('낮음', '기혼'): (0.5269324222194672, 0.8972923145334325, 0.4730675777805328, 0.10270768546656736)})
    plt.show();



    재계약 횟수가 낮은 경우 미혼인 경향이 있음
    27.1.7 재계약 횟수 변수를 종속변수로 하는 회귀 분석을 두 가지 이상의 방법론을 통해 수행하고 최종 모델을 결정하시오.
    train_y = train_X['outcome_index']
    test_y = test_X['outcome_index']

    train_X = train_X.drop(['outcome_index'], axis = 1)
    test_X = test_X.drop(['outcome_index'], axis = 1)

    num_columns = ['거주개월', '아파트 평점', '층', '평형대', '월세(원)', '보증금(원)', '대표나이', '나이', '거주자 수']

    cat_columns = train_X.select_dtypes('object').columns

    재계약횟수 이분변수를 종속변수로 하는 분류 분석을 두가지 이상의 방법론을 통해 수행하고 최종 모델을 결정하시오.
    encoding_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        StandardScaler()
    )

    preprocess = ColumnTransformer(
        [("num_process", num_preprocess, num_columns), 
        ("cat_process", encoding_preprocess, cat_columns)]
        , remainder='passthrough'
    )

    from sklearn.ensemble import RandomForestClassifier

    pipe_rf = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    start_time = time.time()
    RandomForest_search = GridSearchCV(estimator = pipe_rf, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'accuracy') # roc_auc, average_precision
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler
    cat_process

    OneHotEncoder

    RandomForestClassifier
    print('Random Forest best score : ', RandomForest_search.best_score_)

    Random Forest best score :  0.9736722799853308
    from sklearn.tree import DecisionTreeClassifier

    pipe_dt = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", DecisionTreeClassifier())
        ]
    )

    decisiontree_param = {'classifier__ccp_alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    start_time = time.time()
    decisiontree_search = GridSearchCV(estimator = pipe_dt, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          scoring = 'accuracy')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    num_process

    StandardScaler
    cat_process

    OneHotEncoder

    DecisionTreeClassifier
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.9594525775341705
    모델의 balanced accuracy를 확인해보면 rf가 dt에 비해 근소 우위에 있는 것으로 보이므로 random forest 모형 선택
    pred_rf = RandomForest_search.predict(test_X)
    print(classification_report(test_y, pred_rf))

                  precision    recall  f1-score   support

              낮음       0.99      0.97      0.98      1480
              높음       0.97      0.99      0.98      1565

        accuracy                           0.98      3045
       macro avg       0.98      0.98      0.98      3045
    weighted avg       0.98      0.98      0.98      3045
    print(balanced_accuracy_score(test_y, pred_rf))

    0.9789731024954667
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.97인 것을 확인할 수 있다.

    27.1.8 최종 채택한 모델에서 각각 유의하게 작용하는 변수를 확인 하고 설명하시오.
    from sklearn.inspection import permutation_importance

    feature_importances = permutation_importance(
        RandomForest_search, train_X, train_y, n_repeats=10, random_state=42
    )

    features = train_X.columns
    importances = feature_importances.importances_mean

    col_ind = num_columns + cat_columns.to_list()

    f_imp = pd.DataFrame({'변수중요도' : importances, '변수' : features})
    f_imp = f_imp.loc[f_imp['변수'].isin(col_ind), :]

    plt.bar(f_imp['변수'], f_imp['변수중요도'])

    <BarContainer object of 14 artists>
    plt.xticks(rotation=90)

    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [Text(0, 0, '계약구분'), Text(1, 0, '거주개월'), Text(2, 0, '아파트 이름'), Text(3, 0, '아파트 평점'), Text(4, 0, '층'), Text(5, 0, '평형대'), Text(6, 0, '월세(원)'), Text(7, 0, '보증금(원)'), Text(8, 0, '대표나이'), Text(9, 0, '나이'), Text(10, 0, '성별'), Text(11, 0, '결혼여부'), Text(12, 0, '거주자 수'), Text(13, 0, '퇴거여부')])
    plt.tight_layout()
    plt.show();



    모델에 유의하게 작용하는 변수는 permutation importance를 통해 확인할 수 있음

    permutation importance는 모델을 학습시킨 이후(post-hoc) 특정 변수의 관측치를 shuffle했을 때의 예측력을 비교해서 feature importance를 계산하는 방법

    예측력이 많이 떨어질 경우 예측에 중요한 변수, 예측력이 조금 떨어지는 변수는 중요하지 않은 변수로 볼 수 있음

    permutation importance plot을 확인해보면 거주개월, 보증금(원) 변수가 유의미한 변수로 보임

    27.1.9 해당 데이터 분석결과로 얻을 수 있는 점을 제시하시오.
    from sklearn.inspection import partial_dependence
    from sklearn.inspection import plot_partial_dependence

    fig, ax = plt.subplots(figsize=(10, 10))
    #plt.subplots_adjust(top=0.9)
    plot_partial_dependence(estimator=RandomForest_search, 
                            X=train_X, 
                            features=['거주개월', '보증금(원)'], # 관심변수 
                            percentiles=(0, 1), # 최소, 최대 
                            ax=ax)

    <sklearn.inspection._plot.partial_dependence.PartialDependenceDisplay object at 0x1791ef040>

    plt.subplots_adjust(top=0.9, hspace = 0.5, wspace = 0.3) # hspace : 서브 플랏 행 간 간격 조절                      
    plt.show();



    permutation importance plot을 뽑은 거주개월, 보증금(원) 변수에 대해서 partial dependence plot으로 재계약횟수(높음, 낮음) 변수와의 관계를 확인함

    거주개월이 100을 넘어갈 경우 재계약횟수(높음)일 확률이 매우 높아지는 것으로 보임

    보증금의 경우 0.2를 넘어갈 경우 재계약횟수(높음)일 확률이 매우 높아지는 것으로 보임

    특징 및 활용 방안 도출(생략)

    27.2 문제2
    27.3 각 회차별로 1번 타자의 출루 (1,2,3루타와 사사구(볼넷, 몸에맞는공))가 있는 경우에 대해 득점이 발생 했는지 확인하고자 한다. 이를 위한 전처리를 수행하시오. (단, 첫 번째 혹은 두 번째 타자가 홈런을 친 경우 해당 회차 데이터 제외)
    dat = pd.read_csv('data/adp29_2.csv')

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 200 entries, 0 to 199
    Data columns (total 28 columns):
     #   Column   Non-Null Count  Dtype  
    ---  ------   --------------  -----  
     0   game_id  200 non-null    int64  
     1   a1_1     188 non-null    float64
     2   a1_2     200 non-null    int64  
     3   a2_1     200 non-null    object 
     4   a2_2     200 non-null    int64  
     5   a3_1     200 non-null    int64  
     6   a3_2     200 non-null    int64  
     7   a4_1     200 non-null    object 
     8   a4_2     200 non-null    int64  
     9   a5_1     200 non-null    int64  
     10  a5_2     200 non-null    int64  
     11  a6_1     200 non-null    int64  
     12  a6_2     200 non-null    int64  
     13  a7_1     200 non-null    object 
     14  a7_2     200 non-null    int64  
     15  a8_1     200 non-null    int64  
     16  a8_2     200 non-null    int64  
     17  a9_1     200 non-null    int64  
     18  a9_2     200 non-null    int64  
     19  b1       200 non-null    int64  
     20  b2       200 non-null    int64  
     21  b3       200 non-null    int64  
     22  b4       200 non-null    int64  
     23  b5       200 non-null    int64  
     24  b6       200 non-null    int64  
     25  b7       200 non-null    int64  
     26  b8       200 non-null    int64  
     27  b9       200 non-null    int64  
    dtypes: float64(1), int64(24), object(3)
    memory usage: 43.9+ KB
    dat.isna().sum()

    game_id     0
    a1_1       12
    a1_2        0
    a2_1        0
    a2_2        0
    a3_1        0
    a3_2        0
    a4_1        0
    a4_2        0
    a5_1        0
    a5_2        0
    a6_1        0
    a6_2        0
    a7_1        0
    a7_2        0
    a8_1        0
    a8_2        0
    a9_1        0
    a9_2        0
    b1          0
    b2          0
    b3          0
    b4          0
    b5          0
    b6          0
    b7          0
    b8          0
    b9          0
    dtype: int64
    결측치의 경우 a1_1(1회 첫 타자의 행동) 변수에 10개 존재함
    dat.a2_1.value_counts()

    a2_1
    5    87
    7    47
    1    30
    6    14
    4    11
    2     9
    :     2
    Name: count, dtype: int64
    dat.a4_1.value_counts()

    a4_1
    5    95
    7    29
    1    26
    6    25
    2    10
    4     6
    &     5
    8     3
    3     1
    Name: count, dtype: int64
    dat.a7_1.value_counts()

    a7_1
    5    68
    7    43
    1    29
    6    22
    2    20
    4    11
    "     3
    3     2
    8     2
    Name: count, dtype: int64
    특수문자의 경우 데이터 라벨링 오류로 판단하여 제거
    #dat.shape
    dat = dat.loc[dat.a2_1 != ':', :]
    dat = dat.loc[dat.a4_1 != '&', :]
    dat = dat.loc[dat.a7_1 != '"', :]

    야구 특성상 이닝별, 특정 게임별로 타자의 컨디션이 다르므로, a1_1(1회 첫 타자의 행동) 변수의 결측치를 대치하는 것은 부적절할 수 있음

    결측치는 전체의 5%정도이므로 제거함

    dat = dat.loc[dat.a1_1.notna(), :]

    dat = dat.astype({'a2_1' : 'int64', 'a4_1' : 'int64', 'a7_1' : 'int64', 'a1_1' : 'int64'})

    dat.hist()

    array([[<Axes: title={'center': 'game_id'}>,
            <Axes: title={'center': 'a1_1'}>,
            <Axes: title={'center': 'a1_2'}>,
            <Axes: title={'center': 'a2_1'}>,
            <Axes: title={'center': 'a2_2'}>],
           [<Axes: title={'center': 'a3_1'}>,
            <Axes: title={'center': 'a3_2'}>,
            <Axes: title={'center': 'a4_1'}>,
            <Axes: title={'center': 'a4_2'}>,
            <Axes: title={'center': 'a5_1'}>],
           [<Axes: title={'center': 'a5_2'}>,
            <Axes: title={'center': 'a6_1'}>,
            <Axes: title={'center': 'a6_2'}>,
            <Axes: title={'center': 'a7_1'}>,
            <Axes: title={'center': 'a7_2'}>],
           [<Axes: title={'center': 'a8_1'}>,
            <Axes: title={'center': 'a8_2'}>,
            <Axes: title={'center': 'a9_1'}>,
            <Axes: title={'center': 'a9_2'}>, <Axes: title={'center': 'b1'}>],
           [<Axes: title={'center': 'b2'}>, <Axes: title={'center': 'b3'}>,
            <Axes: title={'center': 'b4'}>, <Axes: title={'center': 'b5'}>,
            <Axes: title={'center': 'b6'}>],
           [<Axes: title={'center': 'b7'}>, <Axes: title={'center': 'b8'}>,
            <Axes: title={'center': 'b9'}>, <Axes: >, <Axes: >]], dtype=object)
    #plt.tight_layout()
    plt.show();



    sub_dat1 = pd.melt(dat, 
                       id_vars = ['game_id'], 
                       value_vars = dat.columns[dat.columns.str.endswith('_1')],
                       var_name = 'ining1', 
                       value_name = 'first_move', 
                       ignore_index = False)


    sub_dat2 = pd.melt(dat, 
                       id_vars = ['game_id'], 
                       value_vars = dat.columns[dat.columns.str.endswith('_2')],
                       var_name = 'ining2', 
                       value_name = 'second_move', 
                       ignore_index = False)

    sub_dat2

           game_id ining2  second_move
    0    201900016   a1_2            5
    1    201900023   a1_2            4
    2    201900103   a1_2            6
    3    201900112   a1_2            7
    4    201900131   a1_2            1
    ..         ...    ...          ...
    194  201902327   a9_2            5
    195  201902346   a9_2            1
    196  201902365   a9_2            9
    198  201902392   a9_2            7
    199  201902394   a9_2            5

    [1620 rows x 3 columns]

    dat2 = pd.merge(sub_dat1, sub_dat2, on = ['game_id'], how = 'inner')
    dat2.head()

         game_id ining1  first_move ining2  second_move
    0  201900016   a1_1           5   a1_2            5
    1  201900016   a1_1           5   a2_2            5
    2  201900016   a1_1           5   a3_2            5
    3  201900016   a1_1           5   a4_2            5
    4  201900016   a1_1           5   a5_2            5
    sub_dat3 = pd.melt(dat, 
                       id_vars = ['game_id'], 
                       value_vars = dat.columns[dat.columns.str.startswith('b')],
                       var_name = 'ining', 
                       value_name = 'score', 
                       ignore_index = False)


    dat3 = pd.merge(dat2, sub_dat3, on = ['game_id'], how = 'inner')
    dat3

              game_id ining1  first_move ining2  second_move ining  score
    0       201900016   a1_1           5   a1_2            5    b1      0
    1       201900016   a1_1           5   a1_2            5    b2      0
    2       201900016   a1_1           5   a1_2            5    b3      0
    3       201900016   a1_1           5   a1_2            5    b4      0
    4       201900016   a1_1           5   a1_2            5    b5      0
    ...           ...    ...         ...    ...          ...   ...    ...
    131215  201902394   a9_1           4   a9_2            5    b5      0
    131216  201902394   a9_1           4   a9_2            5    b6      4
    131217  201902394   a9_1           4   a9_2            5    b7      0
    131218  201902394   a9_1           4   a9_2            5    b8      0
    131219  201902394   a9_1           4   a9_2            5    b9      1

    [131220 rows x 7 columns]
    1번 타자의 출루 (1,2,3루타와 사사구(볼넷, 몸에맞는공))가 있는 경우
    dat3 = dat3.loc[dat3['first_move'].isin([1, 2, 3, 6, 8]), :]

    첫 번째 혹은 두 번째 타자가 홈런을 친 경우 해당 회차 데이터 제외
    dat3 = dat3.loc[dat3['second_move'] != 4, :]
    dat3.head()

           game_id ining1  first_move ining2  second_move ining  score
    567  201900016   a8_1           1   a1_2            5    b1      0
    568  201900016   a8_1           1   a1_2            5    b2      0
    569  201900016   a8_1           1   a1_2            5    b3      0
    570  201900016   a8_1           1   a1_2            5    b4      0
    571  201900016   a8_1           1   a1_2            5    b5      0
    27.3.1 Logistic Regression을 적용하고 2번타자의 희생번트 여부에 대한 회귀 계수 검정을 실시하시오.
    득점 발생 여부 변수 생성
    dat3['score_index'] = np.where(dat3.score != 0, 1, 0)

    dat3['bunt'] = np.where(dat3.second_move == 9, 1, 0)

    logistic regression 모형 적합
    import pandas as pd
    import statsmodels.formula.api as smf

    log_reg = smf.logit("score_index ~ C(first_move) + C(bunt)", data = dat3).fit()

    Optimization terminated successfully.
             Current function value: 0.671802
             Iterations 4
    print(log_reg.summary())

                               Logit Regression Results                           
    ==============================================================================
    Dep. Variable:            score_index   No. Observations:                39033
    Model:                          Logit   Df Residuals:                    39027
    Method:                           MLE   Df Model:                            5
    Date:                Mon, 30 Oct 2023   Pseudo R-squ.:               0.0009564
    Time:                        23:56:05   Log-Likelihood:                -26222.
    converged:                       True   LL-Null:                       -26248.
    Covariance Type:            nonrobust   LLR p-value:                 1.258e-09
    ======================================================================================
                             coef    std err          z      P>|z|      [0.025      0.975]
    --------------------------------------------------------------------------------------
    Intercept             -0.4636      0.016    -29.086      0.000      -0.495      -0.432
    C(first_move)[T.2]     0.1407      0.026      5.336      0.000       0.089       0.192
    C(first_move)[T.3]     0.2598      0.089      2.929      0.003       0.086       0.434
    C(first_move)[T.6]     0.0856      0.025      3.427      0.001       0.037       0.135
    C(first_move)[T.8]    -0.1360      0.062     -2.201      0.028      -0.257      -0.015
    C(bunt)[T.1]          -0.0801      0.045     -1.791      0.073      -0.168       0.008
    ======================================================================================
    해석시 exp 취해서 오즈비로 변환
    odds_ratios = pd.DataFrame(
        {
            "OR": log_reg.params,
            "Lower CI": log_reg.conf_int()[0],
            "Upper CI": log_reg.conf_int()[1],
        }
    )
    odds_ratios = np.exp(odds_ratios)

    print(odds_ratios)

                              OR  Lower CI  Upper CI
    Intercept           0.629016  0.609669  0.648976
    C(first_move)[T.2]  1.151086  1.093110  1.212137
    C(first_move)[T.3]  1.296612  1.089770  1.542713
    C(first_move)[T.6]  1.089379  1.037328  1.144042
    C(first_move)[T.8]  0.872800  0.773202  0.985228
    C(bunt)[T.1]        0.922981  0.845490  1.007574
    희생 번트 여부에 대한 회귀계수 검정 결과를 보면, 유의수준 5%에서 Z = -1.791, p-value = 0.073로 희생번트 여부는 통계적으로 유의하지 않다.

    희생 번트 여부를 통제했을 때, 2루타를 쳐서 득점할 오즈는 1루타 대비 약 1.15배이다.

    생략

    Caution
    dummy 변수는 한 범주가 통계적으로 비유의해도, 삭제하면 안됩니다.

    27.3.2 SMOTE (random_state =0 지정)를 적용하여 data imbalance를 해결하시오.
    final_data = dat3.loc[:, ['first_move', 'second_move', 'score_index']]
    final_data.astype({'first_move' : 'object', 'second_move' : 'object'})

           first_move second_move  score_index
    567             1           5            0
    568             1           5            0
    569             1           5            0
    570             1           5            0
    571             1           5            0
    ...           ...         ...          ...
    130972          2           5            0
    130973          2           5            1
    130974          2           5            0
    130975          2           5            0
    130976          2           5            1

    [39033 rows x 3 columns]
    y = final_data.score_index
    X = final_data.drop(['score_index'], axis = 1)

    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    분할 이유 생략
    print('y:', Counter(train_y))

    y: Counter({0: 18770, 1: 12456})
    from imblearn.over_sampling import SMOTE
    smote = SMOTE(random_state = 0)
    train_X_smote, train_y_smote = smote.fit_resample(train_X, train_y)
    print(Counter(train_y_smote))

    Counter({0: 18770, 1: 18770})
    27.3.3 Logistic Regression을 적용하고 결과를 분석하시오.
    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_score
    # num_preprocess = make_pipeline(
    #     StandardScaler()
    # )

    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer([('cat', cat_preprocess, train_X.columns)], remainder='passthrough')



    pipe_lg = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", LogisticRegression()) 
        ]
    )

    pipe_lg.fit(train_X, train_y)

    Pipeline
    preprocess: ColumnTransformer
    cat

    OneHotEncoder

    SMOTE

    LogisticRegression
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)
    cv_score = cross_val_score(pipe_lg, train_X, train_y, scoring='balanced_accuracy', cv = cv)


    print('Logistic regression best score : ', np.mean(cv_score))

    Logistic regression best score :  0.5192628344874523
    27.3.4 XGBoost 적용하고 결과를 분석하시오.
    import xgboost as xgb
    xgb_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", xgb.XGBClassifier()) 
        ]
    )

    Xgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Xgb_search = GridSearchCV(estimator = xgb_pipe, 
                          param_grid = Xgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    Xgb_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    cat

    OneHotEncoder

    SMOTE

    XGBClassifier
    print('XGBOOST best score : ', Xgb_search.best_score_)

    XGBOOST best score :  0.5169764356328828
    교차검증 score 비교 결과 logistic regression 모형이 balanced accuracy = 0.516으로 가장 좋으므로, logistic regression 모형을 최종 모형으로 선택한다.

    pred_lg = pipe_lg.predict(test_X)
    print(classification_report(test_y, pred_lg))

                  precision    recall  f1-score   support

               0       0.63      0.49      0.55      4704
               1       0.42      0.56      0.48      3103

        accuracy                           0.52      7807
       macro avg       0.52      0.53      0.52      7807
    weighted avg       0.55      0.52      0.52      7807
    print(balanced_accuracy_score(test_y, pred_lg))

    0.5253334152707168
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.52인 것을 확인할 수 있다.
    """
