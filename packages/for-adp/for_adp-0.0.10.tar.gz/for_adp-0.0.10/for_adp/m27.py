def m27():
    """
     27회차 기출문제
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

    25.1 머신러닝
    Description

    신용카드 사기 탐지 모형 개발

    amount : 거래금액

    time : Time contains the seconds elapsed between each transaction and the first transaction in the dataset

    V1 ~ V17 : PCA에 의해 얻어진 주성분 값, 즉 마스킹 됨

    25.1.1 EDA를 실시하시오
    dat = pd.read_csv("./data/fraud.csv")

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1234 entries, 0 to 1233
    Data columns (total 20 columns):
     #   Column  Non-Null Count  Dtype  
    ---  ------  --------------  -----  
     0   v1      1234 non-null   float64
     1   v2      1234 non-null   float64
     2   v3      1234 non-null   float64
     3   v4      1234 non-null   float64
     4   v5      1234 non-null   float64
     5   v6      1234 non-null   float64
     6   v7      1234 non-null   float64
     7   v8      1234 non-null   float64
     8   v9      1234 non-null   float64
     9   v10     1234 non-null   float64
     10  v11     1234 non-null   float64
     11  v12     1234 non-null   float64
     12  v13     1234 non-null   float64
     13  v14     1234 non-null   float64
     14  v15     1234 non-null   float64
     15  v16     1234 non-null   float64
     16  v17     1234 non-null   float64
     17  time    1234 non-null   int64  
     18  amount  1234 non-null   float64
     19  class   1234 non-null   int64  
    dtypes: float64(18), int64(2)
    memory usage: 192.9 KB
    dat.head()

             v1        v2        v3        v4  ...       v17    time  amount  class
    0  1.920111  0.054060 -1.652592  1.436783  ... -0.126476  123532   64.80      0
    1  0.326698  0.163725 -2.816580 -2.698640  ...  1.248596  137386   40.35      0
    2 -0.347783  0.648108  0.545413 -2.528817  ... -1.093126    3374    1.00      0
    3  1.389609 -0.250475 -0.064093 -0.733402  ...  0.164981   74774   15.00      0
    4  1.543634 -1.188639  0.586426 -1.419308  ...  0.287147    1609    6.40      0

    [5 rows x 20 columns]
    dat.describe()

                    v1           v2  ...       amount        class
    count  1234.000000  1234.000000  ...  1234.000000  1234.000000
    mean     -0.110618     0.104890  ...    90.938987     0.033225
    std       2.273262     1.732450  ...   216.402630     0.179297
    min     -28.524268   -13.207144  ...     0.000000     0.000000
    25%      -0.998934    -0.599064  ...     5.942500     0.000000
    50%       0.027135     0.077232  ...    20.000000     0.000000
    75%       1.311592     0.816358  ...    72.750000     0.000000
    max       2.327704    15.876923  ...  2297.740000     1.000000

    [8 rows x 20 columns]
    dat.isna().sum()

    v1        0
    v2        0
    v3        0
    v4        0
    v5        0
    v6        0
    v7        0
    v8        0
    v9        0
    v10       0
    v11       0
    v12       0
    v13       0
    v14       0
    v15       0
    v16       0
    v17       0
    time      0
    amount    0
    class     0
    dtype: int64
    dat.select_dtypes('number').hist();
    plt.show();



    sns.countplot(dat['class'])
    plt.show()



    dat['class'].value_counts()

    class
    0    1193
    1      41
    Name: count, dtype: int64
    corr = dat.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True);
    plt.show();



    V2는 amount와 상관관계 존재
    25.1.2 차원축소가 필요한지 검토하라. 2개 이상의 후보 알고리즘을 비교하고, 1개를 추천하라
    차원축소 필요 이유

    마스킹된 변수 간에는 높은 상관관계가 존재함

    고차원 데이터의 경우 모델 학습 시 과적합될 가능성이 있으며, 계산량이 많아져 모델 효율성이 떨어질 수 있음

    또한 마스킹된 변수 간 상관관계가 높다는 의미는 변수 간 중복되는 정보가 있다는 의미로도 볼 수 있으므로, 적절한 차원 축소 기법을 통해 과적합을 방지하고 모델의 계산 효율성을 확보하는 것이 합리적일 수 있음

    PCA



    pca example
    kernel pca example

    데이터의 정보를 최대한 보존하는 축으로 데이터를 사영시켜 차원축소 하는 기법

    PCA는 단순히 정보를 최대한 보존하는(분산을 최대화하는) 축을 찾는 것이므로, 데이터의 비선형구조가 있을 경우 이를 고려할 수 없음

    Kernel PCA

    PCA에 kernel 트릭을 적용한 방법

    PCA의 단점인 데이터의 비선형구조가 있을 경우 이를 고려할 수 없는 문제를 kernel 트릭을 적용하여 고차원에 데이터를 매핑한 후 PCA를 적용함으로써, 데이터의 비선형구조를 고려할 수 있음

    데이터가 클 경우 kernel metrix 계산 시 계산량이 많음

    적절한 kernel 선택과 kernel 내 parameter 선택에 따라 성능이 유동적임

    25.1.3 추천한 알고리즘을 구현하고, 정당성을 제시하라
    y = dat['class']
    X = dat.drop(['class'], axis = 1)

    from sklearn.model_selection import train_test_split

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.3, random_state = 0)

    Kernel PCA

    from sklearn.decomposition import KernelPCA
    from sklearn.preprocessing import StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold

    kpca_pipe = Pipeline([("scaler", StandardScaler()), 
                         ("KernelPCA", KernelPCA(n_components= 10, kernel = 'rbf'))])

    preprocess1 = ColumnTransformer(
        [("num_process", kpca_pipe, train_X.columns)]
    )

    kPCA_result = preprocess1.fit_transform(train_X)
    #kpca = preprocess1.named_transformers_['num_process']['KernelPCA']
    kPCA_result[:2, :]

    array([[ 0.02589736, -0.02854755, -0.22153142, -0.13002611,  0.0182968 ,
             0.45650914,  0.21733701, -0.06397221,  0.18023294,  0.11099174],
           [-0.14480173,  0.11798178,  0.01235826,  0.13322507, -0.25753315,
             0.11180673,  0.03121911, -0.10355833,  0.2621308 ,  0.1763202 ]])
    kernel PCA의 경우 num_comp를 구하는 기준에 대한 정해진 method는 딱히 없음
    Note
    kernel pca의 경우 데이터가 클 때, 시간이 오래걸리므로 데이터가 클 때는 계산량 문제로 kPCA보다는 PCA를 사용한다고 작성하는 것이 답안 작성에는 더 쉬울 것 같습니다.

    답안 예시 : kernel PCA는 데이터가 클 경우 kernel metrix 계산 시 계산량이 많은 단점이 존재하며, 적절한 kernel 선택과 kernel 내 parameter 선택에 따라 성능이 유동적이다. 따라서 계산량이 비교적 적고, 정보를 최대한 보존하는(분산을 최대화하는) 축을 찾는 PCA를 고려한다.

    25.1.4 Over sampling / under sampling의 장단점을 기술하라. 적절한 샘플링을 제안하고 구현하라.
    Over sampling

    오버샘플링은 소수 범주 내 관측치를 복원추출을 통해 늘리는 방법입니다.

    장점

    under sampling처럼 데이터를 잃지 않고, 소수 범주를 잘 분류할 가능성이 있음

    단점

    소수 범주를 복원추출을 통해 값을 복제하므로, 소수 범주에 과적합될 수 있음

    데이터의 크기가 증가하므로 모델 적합시 계산량이 더 많아짐

    from imblearn.over_sampling import RandomOverSampler
    from collections import Counter
    oversample = RandomOverSampler(sampling_strategy='minority')
    train_X_over, train_y_over = oversample.fit_resample(train_X, train_y)
    print(Counter(train_y_over))

    Counter({0: 833, 1: 833})
    Under sampling

    언더 샘플링은 다수 범주의 관측치를 랜덤 샘플링을 통해 일부만 추출하므로써 다수 범주의 빈도를 줄이는 방법입니다.

    장점

    랜덤샘플링을 통해 다수 범주의 관측치를 제거하기 때문에 모델 적합시 계산 속도가 향상됨

    단점

    관측치를 제거하기 때문에 정보의 손실 발생함

    범주 불균형이 너무 심할 경우 소수 범주의 빈도가 작기 때문에 사용이 어려움

    from imblearn.under_sampling import RandomUnderSampler
    from collections import Counter
    undersample = RandomUnderSampler(sampling_strategy='majority')
    train_X_under, train_y_under = undersample.fit_resample(train_X, train_y)
    print(Counter(train_y_under))

    Counter({0: 30, 1: 30})
    25.1.5 이전 결과를 활용하여 사기 분류 모델 2개를 구현하고 성능을 비교하라
    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.ensemble import RandomForestClassifier

    pipe_rf = Pipeline(
        [
            ("preprocess", preprocess1),
            ("smote", RandomOverSampler(sampling_strategy='minority')),
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
    num_process

    StandardScaler

    KernelPCA

    RandomOverSampler

    RandomForestClassifier
    print("{}s".format(time.time()-start_time))

    10.148869037628174s
    print('Random Forest best score : ', RandomForest_search.best_score_)

    Random Forest best score :  0.7682861417659433
    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.tree import DecisionTreeClassifier

    pipe_dt = Pipeline(
        [
            ("preprocess", preprocess1),
            ("smote", RandomOverSampler(sampling_strategy='minority')),
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
    num_process

    StandardScaler

    KernelPCA

    RandomOverSampler

    DecisionTreeClassifier
    print("{}s".format(time.time()-start_time))

    4.70135498046875s
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.8340258921492175
    교차검증 스코어 비교 결과 decision tree 모형이 balanced accuracy = 0.83으로 가장 높은 것을 볼 수 있다. 따라서 decision tree 모형을 최종 모형으로 선택한다.

    pred_dt = decisiontree_search.predict(test_X)
    print(classification_report(test_y, pred_dt))

                  precision    recall  f1-score   support

               0       0.99      0.96      0.98       360
               1       0.38      0.82      0.51        11

        accuracy                           0.95       371
       macro avg       0.68      0.89      0.75       371
    weighted avg       0.98      0.95      0.96       371
    print(balanced_accuracy_score(test_y, pred_dt))

    0.8882575757575758
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.88인 것을 확인할 수 있다.

    25.1.6 2에서 도출된 데이터에 대해 이상탐지(anomaly detection) 방법을 사용하여 신용카드 사기 데이터를 식별하라.
    2개 이상 탐지 방법(후보 알고리즘)을 도출하여 장단점을 비교하라
    이상치 탐지 방법은 boxplot을 이용한 방법과 군집 알고리즘 중 DBSCAN 알고리즘을 이용한 방법이 있습니다.

    boxplot

    먼저 boxplot을 이용한 접근 방법은 울타리 밖의 관측치를 이상치로 정의합니다.

    울타리는 다음과 같이 정의됩니다.

    위 울타리(upper fence) : 

    아래 울타리(lower fence) : 

    장점은 일변량 변수의 통계량을 이용한 접근 방법이므로 계산량이 적고, 쉽게 이상치를 식별할 수 있습니다. 단점은 일변량 분포의 정보만 활용가능합니다.

    DBSCAN DBSCAN은 단순하게, 하나의 관측치를 기준으로 반경 
     내에 관측치가 
    이상 있으면 하나의 군집으로 인식하는 알고리즘입니다.

    먼저 (start point)와 임의의 다른 관측치 사이의 거리를 계산하고 eps 내에 이웃 관측치를 찾습니다. 이웃 관측치가 
     이상 있으면 중심점(core point)로 인식하며, 다른 core point에는 속하지만 이웃 관측치가 
     미만일 경우 border point로 인식합니다. 또한 다른 core point에는 속하지않고, 이웃 관측치가 
     미만일 경우 noise point로 인식하며, 다른 관측치에 대해 동일한 방식으로 core point, border point, noise point인지 확인합니다. core point가 다른 core point에 속해 있을 경우 core point 간에는 하나의 군집으로 인식합니다. 여기서 noise point는 이상치로 인식할 수 있습니다.

    장점은 기하학적인 정보를 갖는 형태에서도 군집 성능이 우수하며, 노이즈 포인트를 쉽게 식별할 수 있습니다. eps, MinPTS의 값에 따라 이상치 탐지의 성능이 유동적입니다.

    알고리즘 1개를 추천하라
    시나리오 1 : PCA를 이용해서 차원 축소한 결과를 이용하므로, 주요 주성분 축, PC1, PC2에 데이터의 정보가 모여있습니다. 따라서 PC1, PC2를 기준으로 boxplot을 이용한 이상치 탐지 방법을 고려해볼 수 있습니다.

    시나리오 2: DBSCAN을 이용해서 다변량 데이터의 공간 구조를 이용합니다. eps의 변화에 따라 이상치 탐지의 성능이 유동적인 문제를 보완하기 위해 k-nearest neighbor distance(euclidean distance 이용)를 이용하여, elbow point를 정함으로써 이를 보완할 수 있습니다.

    4-1 알고리즘을 구현하고 도출 결과를 제시하라
    from sklearn.decomposition import PCA
    pca_pipe = Pipeline([("scaler", StandardScaler()), 
                         ("PCA", PCA(n_components= 0.8, svd_solver='full'))])

    preprocess2 = ColumnTransformer(
        [("num_process", pca_pipe, train_X.columns)]
    )
    PCA_train_X = pd.DataFrame(preprocess2.fit_transform(train_X))
    PCA_test_X = pd.DataFrame(preprocess2.transform(test_X))

    PCA_train_X.columns = ['PC'+str(i) for i in range(PCA_train_X.shape[1])]

    PCA_test_X.columns = ['PC'+str(i) for i in range(PCA_test_X.shape[1])]

    Boxplot

    pca_train = pd.concat([PCA_train_X, train_y.reset_index(drop = True)], axis = 1)
    pca_test = pd.concat([PCA_test_X, test_y.reset_index(drop = True)], axis = 1)

    pca_train_new = pca_train.loc[:, ['PC0', 'PC1', 'class']]
    pca_test_new = pca_test.loc[:, ['PC0', 'PC1', 'class']]

    Q1_1 = np.quantile(pca_train_new.PC0, 0.25)
    Q3_1 = np.quantile(pca_train_new.PC0, 0.75)
    IQR_1 = Q3_1 - Q1_1
    UC_1 = Q3_1 + (1.5 * IQR_1) 
    LC_1 = Q3_1 - (1.5 * IQR_1) 

    outlier1 = pca_test_new.loc[(pca_test_new.PC0 > UC_1) | (pca_test_new.PC0 < LC_1), :].index.tolist()

    Q1_2 = np.quantile(pca_train_new.PC1, 0.25)
    Q3_2 = np.quantile(pca_train_new.PC1, 0.75)
    IQR_2 = Q3_2 - Q1_2
    UC_2 = Q3_2 + (1.5 * IQR_2) 
    LC_2 = Q3_2 - (1.5 * IQR_2) 

    outlier2 = pca_test_new.loc[(pca_test_new.PC1 > UC_2) | (pca_test_new.PC1 < LC_2), :].index.tolist()


    pca_test_new = pca_test_new.assign(outlier = np.where(pca_test_new.index.isin(outlier1) | pca_test_new.index.isin(outlier2), 1, 0))

    print(classification_report(pca_test_new['class'], pca_test_new['outlier']))

                  precision    recall  f1-score   support

               0       1.00      0.79      0.88       360
               1       0.12      0.91      0.21        11

        accuracy                           0.80       371
       macro avg       0.56      0.85      0.55       371
    weighted avg       0.97      0.80      0.86       371
    sns.scatterplot(x='PC0', 
                    y='PC1', 
                    hue='outlier',
                    s=100, # marker size
                    data=pca_test_new)
    plt.show();



    DBSCAN

    # pca_train = pd.concat([PCA_train_X, train_y.reset_index(drop = True)], axis = 1)
    # pca_test = pd.concat([PCA_test_X, test_y.reset_index(drop = True)], axis = 1)

    from sklearn.neighbors import NearestNeighbors 
    neighbors = NearestNeighbors(n_neighbors=20)
    neighbors_fit = neighbors.fit(pca_train)
    distances, indices = neighbors_fit.kneighbors(pca_train)

    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.axhline(y=3.5, color='black', linestyle='--', linewidth=3)
    plt.show();



    from sklearn.cluster import DBSCAN
    db = DBSCAN(eps=3.5, min_samples=20).fit(pca_train)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    pred = db.fit_predict(pca_test)
    print('pred outlier count : ', list(pred).count(-1))

    pred outlier count :  16
    pred = pd.DataFrame(pred.reshape(-1, 1), columns = ['outlier'])
    pred = pred.replace(-1, 1)

    test_y.shape

    (371,)
    pred.shape

    (371, 1)
    db_result = pd.concat([test_y.reset_index(drop = True), pred.reset_index(drop = True)], axis = 1)

    print(classification_report(db_result['class'], db_result['outlier']))

                  precision    recall  f1-score   support

               0       0.99      0.98      0.99       360
               1       0.56      0.82      0.67        11

        accuracy                           0.98       371
       macro avg       0.78      0.90      0.83       371
    weighted avg       0.98      0.98      0.98       371
    PC1_2 = pca_test.loc[:, ['PC0', 'PC1']]
    db_result2 = pd.concat([PC1_2, db_result], axis = 1)

    sns.scatterplot(x='PC0', 
                    y='PC1', 
                    hue='outlier',
                    s=100, # marker size
                    data=db_result2)
    plt.show();



    3-2, 4-2의 결과에 대해 분석가로서 종합적인 결론을 제시하라
    print('dbscan: \n', confusion_matrix(db_result['class'], db_result['outlier']))

    dbscan: 
     [[353   7]
     [  2   9]]
    print('boxplot: \n', confusion_matrix(pca_test_new['class'], pca_test_new['outlier']))

    boxplot: 
     [[285  75]
     [  1  10]]
    print('decision tree: \n', confusion_matrix(test_y, pred_dt))

    decision tree: 
     [[345  15]
     [  2   9]]
    모형 성능 측면에서 보면 anomaly detection 방법을 적용한 것에 비해 supervised learning으로 학습한 모형의 성능이 미미하게 우수하지만, 큰 차이는 없었다.

    anomaly detection과 supervised learning을 비교해보면 두 방법론 다 반응변수의 불균형이 심할 때, 적용할 수 있는 방법이다. 차이점은 anomaly detection의 경우 target이 없어도 적용할 수 있는 방법이다.

    신용카드 사기 탐지 여부를 탐지하는 모형을 운영하는 관점에서 봤을 때, target이 있는 과거 데이터를 활용할 수 있으므로, supervised learnig으로 학습한 모형을 활용하는 것이 적절할 수 있다.

    """
