def m9():
    """
    9  Modeling 2
    분류 문제도 회귀 문제와 sklearn을 이용한 접근 방식이 유사하기 때문에 예제 데이터를 중심으로 설명드리겠습니다.

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

    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import KBinsDiscretizer
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, balanced_accuracy_score, plot_roc_curve, roc_auc_score, roc_curve

    from sklearn import set_config
    set_config(display="diagram")

    9.1 데이터 불러오기
    데이콘에서 진행했던 신용카드 사용자 연체 예측 경진대회 데이터입니다.

    원 데이터는 다중 분류 문제이지만, 먼저 이진 분류 문제로 바꿔서 진행해보겠습니다.

    데이터 출처 https://www.dacon.io/competitions/official/235713/talkboard/402821/

    dat = pd.read_csv('./data/credit.csv')
    dat = dat.clean_names()
    dat = dat.drop(['index'], axis = 1)

    9.2 Data description
    index
    gender: 성별
    car: 차량 소유 여부
    reality: 부동산 소유 여부
    child_num: 자녀 수
    income_total: 연간 소득
    income_type: 소득 분류 [‘Commercial associate’, ‘Working’, ‘State servant’, ‘Pensioner’, ‘Student’]
    edu_type: 교육 수준 [‘Higher education’ ,‘Secondary / secondary special’, ‘Incomplete higher’, ‘Lower secondary’, ‘Academic degree’]
    family_type: 결혼 여부 [‘Married’, ‘Civil marriage’, ‘Separated’, ‘Single / not married’, ‘Widow’]
    house_type: 생활 방식 [‘Municipal apartment’, ‘House / apartment’, ‘With parents’, ‘Co-op apartment’, ‘Rented apartment’, ‘Office apartment’]
    DAYS_BIRTH: 출생일, 데이터 수집 당시 (0)부터 역으로 셈, 즉, -1은 데이터 수집일 하루 전에 태어났음을 의미
    DAYS_EMPLOYED: 업무 시작일, 데이터 수집 당시 (0)부터 역으로 셈, 즉, -1은 데이터 수집일 하루 전부터 일을 시작함을 의미. 양수 값은 고용되지 않은 상태를 의미함
    FLAG_MOBIL: 핸드폰 소유 여부
    work_phone: 업무용 전화 소유 여부
    phone: 전화 소유 여부
    email: 이메일 소유 여부
    occyp_type: 직업 유형
    family_size: 가족 규모
    begin_month: 신용카드 발급 월, 데이터 수집 당시 (0)부터 역으로 셈, 즉, -1은 데이터 수집일 한 달 전에 신용카드를 발급함을 의미
    credit : 사용자의 신용카드 대금 연체를 기준으로 한 신용도(값이 낮을 수록 높은 신용의 신용카드 사용자를 의미)
    0 : good (연체 안함)
    1 : bad (연체함)
    dat.head()

      gender car reality  child_num  ...   occyp_type family_size begin_month credit
    0      F   N       N          0  ...          NaN           2          -6   good
    1      F   N       Y          1  ...     Laborers           3          -5   good
    2      M   Y       Y          0  ...     Managers           2         -22    bad
    3      F   N       Y          0  ...  Sales staff           2         -37   good
    4      F   Y       Y          0  ...     Managers           2         -26    bad

    [5 rows x 19 columns]
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 26457 entries, 0 to 26456
    Data columns (total 19 columns):
     #   Column         Non-Null Count  Dtype  
    ---  ------         --------------  -----  
     0   gender         26457 non-null  object 
     1   car            26457 non-null  object 
     2   reality        26457 non-null  object 
     3   child_num      26457 non-null  int64  
     4   income_total   26457 non-null  float64
     5   income_type    26457 non-null  object 
     6   edu_type       26457 non-null  object 
     7   family_type    26457 non-null  object 
     8   house_type     26457 non-null  object 
     9   days_birth     26457 non-null  int64  
     10  days_employed  26457 non-null  int64  
     11  flag_mobil     26457 non-null  int64  
     12  work_phone     26457 non-null  int64  
     13  phone          26457 non-null  int64  
     14  email          26457 non-null  int64  
     15  occyp_type     18286 non-null  object 
     16  family_size    26457 non-null  int64  
     17  begin_month    26457 non-null  int64  
     18  credit         26457 non-null  object 
    dtypes: float64(1), int64(9), object(9)
    memory usage: 3.8+ MB
    dat.describe()

              child_num  income_total  ...   family_size   begin_month
    count  26457.000000  2.645700e+04  ...  26457.000000  26457.000000
    mean       0.428658  1.873065e+05  ...      2.196848    -26.123294
    std        0.747326  1.018784e+05  ...      0.916717     16.559550
    min        0.000000  2.700000e+04  ...      1.000000    -60.000000
    25%        0.000000  1.215000e+05  ...      2.000000    -39.000000
    50%        0.000000  1.575000e+05  ...      2.000000    -24.000000
    75%        1.000000  2.250000e+05  ...      3.000000    -12.000000
    max       19.000000  1.575000e+06  ...     20.000000      0.000000

    [8 rows x 10 columns]
    freq = dat['occyp_type'].value_counts(normalize = True)
    prob_columns = dat['occyp_type'].map(freq)
    dat['occyp_type'] = dat['occyp_type'].mask((prob_columns < 0.1) | (prob_columns.isnull()), 'other')

    dat['occyp_type'].value_counts()

    occyp_type
    other          14593
    Laborers        4512
    Core staff      2646
    Sales staff     2539
    Managers        2167
    Name: count, dtype: int64
    9.3 변수 속성 변환
    dat = dat.astype({'flag_mobil' : 'object', 'work_phone' : 'object', 'email' : 'object', 'phone' : 'object'})

    y = dat.credit
    X = dat.drop(['credit'], axis = 1)

    9.4 Data split(데이터 분할)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = y,  random_state = 0)

    9.5 Data preprocessing(데이터 전처리)
    num_columns = X.select_dtypes('number').columns.tolist()
    cat_columns = X.select_dtypes('object').columns.tolist()
    num_columns.remove('days_employed')


    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        StandardScaler()
    )

    bin_preprocess = make_pipeline(
        KBinsDiscretizer(n_bins = 4, strategy = 'quantile')
    )

    preprocess = ColumnTransformer(
        [('bin', bin_preprocess, ['days_employed']),
         ("num", num_preprocess, num_columns),
         ("cat", cat_preprocess, cat_columns)]
    )

    9.6 Modeling
    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'balanced_accuracy') # roc_auc, average_precision
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    bin

    KBinsDiscretizer
    num

    StandardScaler
    cat

    OneHotEncoder

    RandomForestClassifier
    9.6.1 분류 평가지표
    어떤 분류 지표를 선택해야 하는지는 데이터에 따라 달라집니다. 따라서 데이터의 의미를 파악해보고 어떤 지표가 중요한지 파악하는 것이 중요합니다. 예를 들어 암에 대해 양성인지 음성인지 분류하는 문제를 푼다고 했을 때 중요한 평가지표는 sensitivity로 볼 수 있습니다. sensitivity는 실제 암이 양성일 때 예측 결과에서도 양성으로 판단하는 비율을 의미하므로, sensitivity가 낮을 경우 심각한 문제가 발생할 수 있습니다.

    9.6.2 불균형 문제에서 분류 평가지표
    반응변수가 불균형일 경우 분류 평가지표를 선택하는데 주의가 필요합니다. 아래 예시를 확인해보겠습니다.

    모델 평가지표 예제

    confusion matrix 결과를 위에서 설명한 암에 대해 양성인지 음성인지 분류하는 문제에 대한 결과라고 생각해보겠습니다. 반응변수가 
    으로 매우 불균형한 데이터입니다.

    table1
    Actual events	Actual non-events
    Predicted events	1	0
    Predicted non-events	9	990
    accuracy : 


    sensitivity : 


    specificity : 


    precision : 

    Balanced accuracy : 


    F1 score : 

    table2
    Actual events	Actual non-events
    Predicted events	6	4
    Predicted non-events	10	980
    accuracy : 


    sensitivity : 


    specificity : 


    precision : 


    Balanced accuracy : 


    F1 score : 

    먼저 table1과 table2를 직관적으로 살펴보겠습니다. table1에 비해 table2가 더 좋은 table입니다. 왜냐하면 반응변수 범주가 불균형일 때, 다수 클래스를 정확히 분류하는 것보다 소수 클래스를 더 정확히 분류하는 것이 중요하기 때문입니다(table1의 경우 소수 범주를 정확히 분류한 경우가 
    이고, table2의 경우 
    입니다). 따라서 단순하게 보면 table2의 평가지표가 table1에 비해 높아야 합니다.

    이를 유념하고 table1과 table2에서 각각 구한 평가지표를 비교해보겠습니다. accuracy의 경우 table1이 table2에 비해 높은 것을 볼 수 있습니다. sensitivity의 경우 table2가 table1에 비해 높은 것을 볼 수 있습니다. accuracy 관점에서는 table1이 더 좋지만 데이터의 의미를 다시 살펴보면 실제 암이 양성일 때 예측 결과에서도 양성으로 판단하는 비율을 나타내는 sensitivity가 더 좋은 평가지표라는 것을 볼 수 있습니다. 따라서 sensitivity 관점에서 table2를 선택할 수 있습니다(또는 소수 범주를 더 정확히 분류한 table2를 선택했다고 생각해볼 수 있습니다).

    또한 sensitivity와 precision의 관계를 비교해보겠습니다. table1과 table2를 비교했을 때, sensitivity가 커지면 precision은 감소하는 것을 볼 수 있습니다. 즉, sensitivity와 precision은 trade-off 관계입니다.

    따라서 sensitivity와 precision을 동시에 고려하는 평가지표가 필요합니다. 대표적으로 balanced accuracy와 F1 score가 있습니다. balanced accuracy와 F1 score를 보면 table1에 비해 table2의 값이 더 높은 것을 볼 수 있습니다.

    정리하면 반응변수 범주 불균형 문제일 경우 precision과 recall을 동시에 고려하는 지표를 선택하는 것이 필요하고, 이 때 사용할 수 있는 것이 balanced accuracy와 F1 score입니다.

    9.6.3 Confusion matrix
    confusion matrix는 분류 모형의 성능을 평가하는데 이용하는 테이블입니다. train 데이터를 이용해서 학습시킨 random forest, logistic regression 두 모형이 있다고 해보겠습니다. 각 모형을 test 데이터에 적용해서 예측값을 뽑았을 때, 어떤 모형이 우수한지 평가할 수 있는 방법이 필요합니다. 이 때 이용할 수 있는 것이 confusion matrix 입니다. confusion matrix를 이용해서 계산되는 다앙햔 평가 지표가 있습니다. sklearn에서 제공하는 평가지표는 아래 그림과 같습니다.

    Predicted events	Predicted non-events
    Actual events	True Positive	False Negative
    Actual non-events	False Positive.	True Negative











    Example

    pred = RandomForest_search.predict(test_X)
    confusion_mat = confusion_matrix(test_y, pred)
    print(confusion_mat)

    [[2913  481]
     [ 956  942]]
    print(classification_report(test_y, pred, target_names = ['bad', 'good']))

                  precision    recall  f1-score   support

             bad       0.75      0.86      0.80      3394
            good       0.66      0.50      0.57      1898

        accuracy                           0.73      5292
       macro avg       0.71      0.68      0.68      5292
    weighted avg       0.72      0.73      0.72      5292
    classification_report()를 이용하면 precision, recall, accuracy 등을 산출할 수 있습니다. support는 각 범주의 샘플 수를 의미합니다. macro avg는 각 지표의 단순 평균을 의미합니다. weighted avg는 각 범주의 support를 이용해서 가중 평균을 계산합니다. 예를 들어 precision의 weigted avg는 


    입니다.

    9.6.4 ROC curve
    ROC curve는 모든 분류 기준값(threshold, cut off value)를 기준값에 대한 1-specificty, sensitivity를 x, y축으로 하여 그린 도표입니다. 이전에 모형에 대한 평가를 할 때, 예측값에 대한 confusion matrix를 구할 수 있다고 설명드렸습니다. 보통 confusion matrix를 구할 때, 분류 기준값은 0.5로 설정되며, 분류 기준값이 바뀌면 confusion matrix의 값도 바뀌게 됩니다. 즉, 분류 기준값 별로 confusion matrix가 하나씩 생성됩니다. 이렇게 분류기준값 별로 생성된 confusion matrix 값은 정리가 어렵기 때문에 보기 좋게 시각화한 것이 ROC curve입니다.

    ROC curve 예시



    Predicted events	Predicted non-events
    Actual events	True Positive	False Negative
    Actual non-events	False Positive	True Negative
    ROC curve가 어떻게 생성되는지 알아보겠습니다. 먼저 x 축은 FPR(=1-specificity), y 축은 TPR(=sensitivity)로 구성됩니다.

    True positive rate(TPR) : 


    False positive rate(FPR) : 


    TPR은 실제 발생한 event 중에서 모형을 통해서 옳게 예측한 비율입니다. 즉, 클수록 좋습니다. 반면에 FPR은 실제 발생하지 않은 event 중에서 모형을 통해서 잘못 예측한 비율입니다. 즉, 작을 수록 좋습니다. 따라서 TPR이 1이고 FPR이 0인 경우 그림처럼 perfect classifier가 됩니다. 이런 경우는 현실에서는 없고, 그림에서의 곡선처럼 보통 TPR의 감소폭보다 FPR의 감소폭이 더 빠르면 좋은 모형입니다.

    그림을 통해서 모형별로 곡선의 형태를 보고 비교할 수도 있지만, 평가지표를 통해서도 구분할 수 있습니다. 보통 평가지표로 AUC를 많이 사용합니다. AUC는 area under the roc curve의 약자로 ROC curve 아래의 면적을 의미합니다. 위에서 언급한 perfact classifier의 경우 AUC는 1이 되므로, 1과 가까울수록 좋은 모형입니다.

    ROC curve 그리는 법

    plot_roc_curve()를 이용해서 Roc curve를 시각화해볼 수 있습니다.

    roc_result = plot_roc_curve(RandomForest_search, test_X, test_y)
    roc_result.plot();
    plt.show()



    print("AUC for Random Forest: %f" % roc_result.roc_auc)

    AUC for Random Forest: 0.746556
    Caution
    sklearn 1.2버전부터 plot_roc_curve 대신 RocCurveDisplay 클래스를 이용하도록 수정되었습니다.

    auc score를 직접 구할 경우 roc_auc_score()를 이용할 수 있습니다.

    rf_auc = roc_auc_score(test_y, RandomForest_search.predict_proba(test_X)[:, 1])
    print("AUC for Random Forest: %f" % rf_auc)

    AUC for Random Forest: 0.746556
    9.6.5 cut off value
    class 불균형을 다루는 방법 중에 소수 범주에 더 큰 weight를 주기 위해 cut-off value(threshold)를 조정해줄 수 있습니다. default cut-off value는 
    이지만, 값을 조정해가면서 탐색함으로써 최적의 값을 찾을 수 있습니다.

    youden’s J statistic : 
    encoder = LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    test_y = encoder.fit_transform(test_y)

    fpr, tpr, thresholds = roc_curve(train_y, RandomForest_search.predict_proba(train_X)[:,1])

    best_threshold = thresholds[np.argmax(np.abs(1 - fpr+tpr))]
    print('best threshold :' , best_threshold)

    best threshold : 0.3803809523809523
    train 데이터를 통해 구한 best threshold를 test 데이터에 적용해볼 수 있습니다.

    prob_y = (RandomForest_search.predict_proba(test_X)[:,1] >= best_threshold).astype(int)
    print(classification_report(test_y, prob_y, target_names=['bad', 'good']))

                  precision    recall  f1-score   support

             bad       0.78      0.77      0.77      3394
            good       0.59      0.60      0.60      1898

        accuracy                           0.71      5292
       macro avg       0.69      0.69      0.69      5292
    weighted avg       0.71      0.71      0.71      5292
    9.7 Multi-classification
    sklearn에서 다중 분류 문제는 두 가지 방식으로 적용해볼 수 있습니다.

    OvO(one vs one) : 각 범주의 조합별로 이진 분류를 한 후 가장 많이 나온 범주로 예측하는 방법

    class1 vs class2 classifier : class1

    class1 vs class3 classifier : class1

    class2 vs class3 classifier : class2

    최종 class 1으로 예측

    OvR(one vs rest) : 각 범주별로 특정 범주 vs 그 외 범주로 나누어서 이진 분류를 수행 한 후 가장 높은 확률로 나온 범주로 예측하는 방법

    class 1 vs rest classifier : class1일 확률 0.8

    class 2 vs rest classifier : class2일 확률 0.3

    class 3 vs rest classifier : class3일 확률 0.4

    최종 class 1으로 예측

    OvO의 경우 target의 범주의 수가 많을 경우 조합의 개수가 기하급수적으로 늘어나므로 일반적으로 사용되지 않습니다. OvO의 경우 sklearn을 이용할 경우 저희가 배운 모형 중에서는 svm만 가능합니다.

    dat = pd.read_csv('./data/ex_data/credit_card/train.csv')
    dat = dat.clean_names()
    dat = dat.drop(['index'], axis = 1)

    freq = dat['occyp_type'].value_counts(normalize = True)
    prob_columns = dat['occyp_type'].map(freq)
    dat['occyp_type'] = dat['occyp_type'].mask((prob_columns < 0.1) | (prob_columns.isnull()), 'other')

    dat = dat.astype({'flag_mobil' : 'object', 'work_phone' : 'object', 'email' : 'object', 'phone' : 'object'})

    y = dat.credit
    X = dat.drop(['credit'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = y,  random_state = 0)

    num_columns = X.select_dtypes('number').columns.tolist()
    cat_columns = X.select_dtypes('object').columns.tolist()
    num_columns.remove('days_employed')


    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    num_preprocess = make_pipeline(
        StandardScaler()
    )

    bin_preprocess = make_pipeline(
        KBinsDiscretizer(n_bins = 4, strategy = 'quantile')
    )

    preprocess = ColumnTransformer(
        [('bin', bin_preprocess, ['days_employed']),
         ("num", num_preprocess, num_columns),
         ("cat", cat_preprocess, cat_columns)]
    )

    9.8 Modeling
    기존 이진 분류 문제와 동일한 세팅

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", RandomForestClassifier())
        ]
    )

    RandomForest_param = {'classifier__max_features': np.arange(0.5, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    RandomForest_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = RandomForest_param, 
                          cv = cv,
                          scoring = 'balanced_accuracy') # roc_auc, average_precision
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    bin

    KBinsDiscretizer
    num

    StandardScaler
    cat

    OneHotEncoder

    RandomForestClassifier
    9.9 confusion matrix
    다중분류 문제의 경우 평가지표는 각 범주별로 계산되며, 계산 방식은 이진 분류 문제와 거의 동일합니다.



    Example

    Recall A : 

    Specificity A : 


    Accuracy : 

    pred = RandomForest_search.predict(test_X)
    confusion_mat = confusion_matrix(test_y, pred)
    print(confusion_mat)

    [[ 157  106  381]
     [  61  588  605]
     [ 138  281 2975]]
    print(classification_report(test_y, pred, target_names = ['bad', 'NotBad', 'good']))

                  precision    recall  f1-score   support

             bad       0.44      0.24      0.31       644
          NotBad       0.60      0.47      0.53      1254
            good       0.75      0.88      0.81      3394

        accuracy                           0.70      5292
       macro avg       0.60      0.53      0.55      5292
    weighted avg       0.68      0.70      0.68      5292
    Accuracy

    tt = confusion_mat
    np.sum(np.diag(tt)) / np.sum(tt)

    0.7029478458049887
    Sensitivity

    sens1 = np.round(tt[0,0]/np.sum(tt[0,:]), 2)
    sens2 = np.round(tt[1,1]/np.sum(tt[1,:]), 2)
    sens3 = np.round(tt[2,2]/np.sum(tt[2,:]), 2)
    print(sens1, sens2, sens3)

    0.24 0.47 0.88
    Precision

    pre1 = np.round(tt[0,0]/np.sum(tt[:,0]), 2)
    pre2 = np.round(tt[1,1]/np.sum(tt[:,1]), 2)
    pre3 = np.round(tt[2,2]/np.sum(tt[:,2]), 2)
    print(pre1, pre2, pre3)

    0.44 0.6 0.75
    F1-Score

    np.round(2*((sens1*pre1)/(sens1 + pre1)), 2)

    0.31
    np.round(2*((sens2*pre2)/(sens2 + pre2)), 2)

    0.53
    np.round(2*((sens3*pre3)/(sens3 + pre3)), 2)

    0.81
    Balanced accuracy

    balanced_accuracy_score(test_y, pred)

    0.5297450629282007
    per_class = np.diag(confusion_mat) / confusion_mat.sum(axis=1)
    score = np.mean(per_class)
    print(score)

    0.5297450629282007
    참고 : https://arxiv.org/pdf/2008.05756.pdf

    9.9.1 ROC curve
    multi classification의 경우 ROC curve를 계산하는 방법이 패키지별로 다양합니다. 이 중 ovr 방식의 ROC curve를 그리는 법을 알아보겠습니다. sklearn 0.23.2 공식 문서의 튜토리얼 코드를 전부 참고했습니다.

    from sklearn.preprocessing import label_binarize
    from itertools import cycle
    from sklearn.metrics import roc_curve, auc

    ROC curve를 그리기 위해서는 먼저 label_binarize()를 이용해서 target을 one-hot encoding된 형태로 만들어줘야 합니다.

    y_score = RandomForest_search.predict_proba(test_X)
    y_test_bin = label_binarize(test_y, classes=[0, 1, 2])
    n_classes = y_test_bin.shape[1]

    각 class-vs-rest별로 ROC curve를 구합니다. 아래는 ROC curve를 시각화하는 코드입니다.

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
                 ''.format(i, roc_auc[i]))

    [<matplotlib.lines.Line2D object at 0x16ff093a0>]
    [<matplotlib.lines.Line2D object at 0x16ff09640>]
    [<matplotlib.lines.Line2D object at 0x16ff098e0>]
    plt.plot([0, 1], [0, 1], 'k--');
    plt.xlim([-0.05, 1.0]);
    plt.ylim([0.0, 1.05]);
    plt.xlabel('False Positive Rate');
    plt.ylabel('True Positive Rate');
    plt.title('Receiver operating characteristic for multi-class data');
    plt.legend(loc="lower right");
    plt.show();



    9.10 sklearn Multiclassification list
    참고 : https://scikit-learn.org/stable/modules/multiclass.html

    9.10.1 XGBOOST
    import xgboost as xgb

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", xgb.XGBClassifier()) # defaut : 'ovr'
        ]
    )

    Xgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    Xgb_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = Xgb_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    Xgb_search.fit(train_X, train_y)

    GridSearchCV(cv=KFold(n_splits=5, random_state=0, shuffle=True),
                 estimator=Pipeline(steps=[('preprocess',
                                            ColumnTransformer(transformers=[('bin',
                                                                             Pipeline(steps=[('kbinsdiscretizer',
                                                                                              KBinsDiscretizer(n_bins=4))]),
                                                                             ['days_employed']),
                                                                            ('num',
                                                                             Pipeline(steps=[('standardscaler',
                                                                                              StandardScaler())]),
                                                                             ['child_num',
                                                                              'income_total',
                                                                              'days_birth',
                                                                              'family_size',
                                                                              'begin_m...
                                                          max_cat_threshold=None,
                                                          max_cat_to_onehot=None,
                                                          max_delta_step=None,
                                                          max_depth=None,
                                                          max_leaves=None,
                                                          min_child_weight=None,
                                                          missing=nan,
                                                          monotone_constraints=None,
                                                          n_estimators=100,
                                                          n_jobs=None,
                                                          num_parallel_tree=None,
                                                          predictor=None,
                                                          random_state=None, ...))]),
                 param_grid={'classifier__learning_rate': array([0.01, 0.06, 0.11, 0.16, 0.21, 0.26])},
                 scoring='balanced_accuracy')
    9.10.2 decision tree
    from sklearn.tree import DecisionTreeClassifier

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", DecisionTreeClassifier()) # defaut : 'ovr'
        ]
    )

    decisiontree_param = {'classifier__ccp_alpha': np.arange(0.1, 1, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    decisiontree_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = decisiontree_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    decisiontree_search.fit(train_X, train_y)

    GridSearchCV(cv=KFold(n_splits=5, random_state=0, shuffle=True),
                 estimator=Pipeline(steps=[('preprocess',
                                            ColumnTransformer(transformers=[('bin',
                                                                             Pipeline(steps=[('kbinsdiscretizer',
                                                                                              KBinsDiscretizer(n_bins=4))]),
                                                                             ['days_employed']),
                                                                            ('num',
                                                                             Pipeline(steps=[('standardscaler',
                                                                                              StandardScaler())]),
                                                                             ['child_num',
                                                                              'income_total',
                                                                              'days_birth',
                                                                              'family_size',
                                                                              'begin_m...
                                                                             Pipeline(steps=[('onehotencoder',
                                                                                              OneHotEncoder(handle_unknown='ignore',
                                                                                                            sparse=False))]),
                                                                             ['gender',
                                                                              'car',
                                                                              'reality',
                                                                              'income_type',
                                                                              'edu_type',
                                                                              'family_type',
                                                                              'house_type',
                                                                              'flag_mobil',
                                                                              'work_phone',
                                                                              'phone',
                                                                              'email',
                                                                              'occyp_type'])])),
                                           ('classifier',
                                            DecisionTreeClassifier())]),
                 param_grid={'classifier__ccp_alpha': array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])},
                 scoring='balanced_accuracy')
    9.10.3 gbm
    from sklearn.ensemble import GradientBoostingClassifier

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", GradientBoostingClassifier()) # defaut : 'ovr'
        ]
    )

    GradientBoosting_param = {'classifier__learning_rate': np.arange(0.1, 0.5, 0.1)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    GradientBoosting_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = GradientBoosting_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    GradientBoosting_search.fit(train_X, train_y)

    GridSearchCV(cv=KFold(n_splits=5, random_state=0, shuffle=True),
                 estimator=Pipeline(steps=[('preprocess',
                                            ColumnTransformer(transformers=[('bin',
                                                                             Pipeline(steps=[('kbinsdiscretizer',
                                                                                              KBinsDiscretizer(n_bins=4))]),
                                                                             ['days_employed']),
                                                                            ('num',
                                                                             Pipeline(steps=[('standardscaler',
                                                                                              StandardScaler())]),
                                                                             ['child_num',
                                                                              'income_total',
                                                                              'days_birth',
                                                                              'family_size',
                                                                              'begin_m...
                                                                             Pipeline(steps=[('onehotencoder',
                                                                                              OneHotEncoder(handle_unknown='ignore',
                                                                                                            sparse=False))]),
                                                                             ['gender',
                                                                              'car',
                                                                              'reality',
                                                                              'income_type',
                                                                              'edu_type',
                                                                              'family_type',
                                                                              'house_type',
                                                                              'flag_mobil',
                                                                              'work_phone',
                                                                              'phone',
                                                                              'email',
                                                                              'occyp_type'])])),
                                           ('classifier',
                                            GradientBoostingClassifier())]),
                 param_grid={'classifier__learning_rate': array([0.1, 0.2, 0.3, 0.4])},
                 scoring='balanced_accuracy')
    9.10.4 Neural network
    from sklearn.neural_network import MLPClassifier

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", MLPClassifier()) # defaut : 'ovr'
        ]
    )

    MLP_param = {'classifier__learning_rate_init': np.arange(0.01, 0.2, 0.02)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    MLP_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = MLP_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    MLP_search.fit(train_X, train_y)

    GridSearchCV(cv=KFold(n_splits=5, random_state=0, shuffle=True),
                 estimator=Pipeline(steps=[('preprocess',
                                            ColumnTransformer(transformers=[('bin',
                                                                             Pipeline(steps=[('kbinsdiscretizer',
                                                                                              KBinsDiscretizer(n_bins=4))]),
                                                                             ['days_employed']),
                                                                            ('num',
                                                                             Pipeline(steps=[('standardscaler',
                                                                                              StandardScaler())]),
                                                                             ['child_num',
                                                                              'income_total',
                                                                              'days_birth',
                                                                              'family_size',
                                                                              'begin_m...
                                                                                              OneHotEncoder(handle_unknown='ignore',
                                                                                                            sparse=False))]),
                                                                             ['gender',
                                                                              'car',
                                                                              'reality',
                                                                              'income_type',
                                                                              'edu_type',
                                                                              'family_type',
                                                                              'house_type',
                                                                              'flag_mobil',
                                                                              'work_phone',
                                                                              'phone',
                                                                              'email',
                                                                              'occyp_type'])])),
                                           ('classifier', MLPClassifier())]),
                 param_grid={'classifier__learning_rate_init': array([0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19])},
                 scoring='balanced_accuracy')
    9.10.5 SVM
    decision_function_shape = ‘ovo’ or ‘ovr’
    from sklearn.svm import SVC

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", SVC(decision_function_shape = 'ovo')) # defaut : 'ovr'
        ]
    )

    SVC_param = {'classifier__C': np.arange(1, 100, 20)}
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    SVC_search = GridSearchCV(estimator = full_pipe, 
                          param_grid = SVC_param, 
                          cv = cv,
                          #cv = 5, # KFold 5
                          scoring = 'balanced_accuracy')
    SVR_search.fit(train_X, train_y)

    pred = SVR_search.predict(test_X)
    confusion_mat = confusion_matrix(test_y, pred)
    print(confusion_mat)

    print(classification_report(test_y, pred, target_names = ['bad', 'NotBad', 'good']))
    """
