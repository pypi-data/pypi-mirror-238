def m19():
    """
    17  19회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    17.1 고객 이탈 분류 문제
    17.1.1 Data description
    시험과 비슷한 데이터

    Attrition_flag : target variable, 이탈 고객인지 유무
    Gender: 성별
    customer age : 고객의 나이
    income category : 고객이 속한 소득 범주
    card category : 고객이 갖고 있는 카드 범주
    month inactive : 신용카드를 사용할 때 비활성 금액
    credit limit : 카드 한도
    total revolving balance : 다음달로 이월되는 미지급 금액
    average utilization ratio : 사용 한도와 비교해서 사용 중인 금액의 비율
    open to buy : 특정 고객에게 할당된 평균 사용 가능 금액
    https://www.kaggle.com/sakshigoyal7/credit-card-customers

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

    dat = pd.read_csv('./data/ex_data/BankChurners.csv')
    dat = dat.clean_names()
    dat = dat.loc[:, ['attrition_flag', 'gender', 'customer_age', 'income_category', 'card_category', 
               'credit_limit', 'total_revolving_bal', 'avg_utilization_ratio', 'avg_open_to_buy', 
               'months_inactive_12_mon']]

    17.1.2 EDA를 실시하시오(시각화 포함)(5점).
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10127 entries, 0 to 10126
    Data columns (total 10 columns):
     #   Column                  Non-Null Count  Dtype  
    ---  ------                  --------------  -----  
     0   attrition_flag          10127 non-null  object 
     1   gender                  10127 non-null  object 
     2   customer_age            10127 non-null  int64  
     3   income_category         10127 non-null  object 
     4   card_category           10127 non-null  object 
     5   credit_limit            10127 non-null  float64
     6   total_revolving_bal     10127 non-null  int64  
     7   avg_utilization_ratio   10127 non-null  float64
     8   avg_open_to_buy         10127 non-null  float64
     9   months_inactive_12_mon  10127 non-null  int64  
    dtypes: float64(3), int64(3), object(4)
    memory usage: 791.3+ KB
    dat.head()

          attrition_flag gender  ...  avg_open_to_buy months_inactive_12_mon
    0  Existing Customer      M  ...          11914.0                      1
    1  Existing Customer      F  ...           7392.0                      1
    2  Existing Customer      M  ...           3418.0                      1
    3  Existing Customer      F  ...            796.0                      4
    4  Existing Customer      M  ...           4716.0                      1

    [5 rows x 10 columns]
    visualization

    y = dat['attrition_flag']
    X = dat.drop(['attrition_flag'], axis = 1)

    pd.options.display.max_columns = None # full 출력 옵션 
    X.describe();

    X.hist()

    array([[<Axes: title={'center': 'customer_age'}>,
            <Axes: title={'center': 'credit_limit'}>],
           [<Axes: title={'center': 'total_revolving_bal'}>,
            <Axes: title={'center': 'avg_utilization_ratio'}>],
           [<Axes: title={'center': 'avg_open_to_buy'}>,
            <Axes: title={'center': 'months_inactive_12_mon'}>]], dtype=object)
    plt.tight_layout();
    plt.show();



    X.select_dtypes('object').columns

    Index(['gender', 'income_category', 'card_category'], dtype='object')
    sns.countplot(X['gender'])
    plt.show();



    sns.countplot(X['income_category'])
    plt.show();



    sns.countplot(X['card_category'])
    plt.show();



    sns.countplot(y)
    plt.show();



    corr = X.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.tight_layout();
    plt.show();



    17.1.3 모형을 적합하시오(15점).
    train/test 7:3 분할
    분류모형 3개 적합
    confusion matrix 출력
    dat = dat.assign(attrition_flag = np.where(dat['attrition_flag'] == 'Attrited Customer', 1, 0))
    y = dat['attrition_flag']
    X = dat.drop(['attrition_flag'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = dat['attrition_flag'], random_state = 0)

    num_columns = train_X.select_dtypes('number').columns
    cat_columns = train_X.select_dtypes('object').columns

    num_pipe = Pipeline([("scaler", StandardScaler())])

    cat_pipe = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer(
        [("num_process", num_pipe, num_columns), 
        ("cat_process", cat_pipe, cat_columns)]
        , remainder='passthrough'
    )

    Random forest

    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.ensemble import RandomForestClassifier
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    pipe_rf = Pipeline(
        [
            ("preprocess", preprocess),
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
    preprocess: ColumnTransformer
    num_process

    StandardScaler
    cat_process

    OneHotEncoder

    RandomOverSampler

    RandomForestClassifier
    print("{}s".format(time.time()-start_time))

    42.78236699104309s
    print('RandomForest best score : ', RandomForest_search.best_score_)

    RandomForest best score :  0.6527054042168832
    from sklearn.tree import DecisionTreeClassifier

    pipe_dt = Pipeline(
        [
            ("preprocess", preprocess),
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
    preprocess: ColumnTransformer
    num_process

    StandardScaler
    cat_process

    OneHotEncoder

    RandomOverSampler

    DecisionTreeClassifier
    print("{}s".format(time.time()-start_time))

    2.2448649406433105s
    print('decision tree best score : ', decisiontree_search.best_score_)

    decision tree best score :  0.540998731403529
    import xgboost as xgb

    pipe_xgb = Pipeline(
        [
            ("preprocess", preprocess),
            ("oversampling", RandomOverSampler(sampling_strategy='minority')),
            ("classifier", xgb.XGBClassifier()) # y label 수치형이어야 함
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
    preprocess: ColumnTransformer
    num_process

    StandardScaler
    cat_process

    OneHotEncoder

    RandomOverSampler

    XGBClassifier
    print("{}s".format(time.time()-start_time))

    12.89982795715332s
    print('XGBOOST best score : ', xgb_search.best_score_)

    XGBOOST best score :  0.7540835942259816
    balanced accuracy 비교 결과 XGBOOST 모형을 선택한다.

    pred_xgb = xgb_search.predict(test_X)
    print(classification_report(test_y, pred_xgb))

                  precision    recall  f1-score   support

               0       0.95      0.79      0.86      1701
               1       0.42      0.76      0.54       325

        accuracy                           0.79      2026
       macro avg       0.68      0.78      0.70      2026
    weighted avg       0.86      0.79      0.81      2026
    print(balanced_accuracy_score(test_y, pred_xgb))

    0.7789517478406367
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.75인 것을 확인할 수 있다.

    17.1.4 위에서 실시한 분류 모형 3개를 앙상블하여 예측하고 result.csv로 파일 제출(30점)
    Averaging(soft voting)

    classification일 때 예측값을 평균내는 것은 부적절
    따라서 예측값 대신 예측 확률값을 평균 내서 최종 앙상블 결과로 산출
    result = pd.DataFrame({'rf_prob' : RandomForest_search.predict_proba(test_X)[:, 0],
                           'dt_prob' : decisiontree_search.predict_proba(test_X)[:, 0],
                           'xgb_prob' : xgb_search.predict_proba(test_X)[:, 0]})

    result['average'] = (result.rf_prob + result.dt_prob + result.xgb_prob)/3

    result['pred'] = np.where(result.average > 0.5, 0, 1)
    result

          rf_prob   dt_prob  xgb_prob   average  pred
    0        0.98  0.692367  0.652633  0.775000     0
    1        0.75  0.692367  0.639067  0.693811     0
    2        0.90  0.692367  0.519013  0.703793     0
    3        0.98  0.692367  0.757041  0.809803     0
    4        0.98  0.692367  0.675992  0.782786     0
    ...       ...       ...       ...       ...   ...
    2021     0.54  0.239571  0.341529  0.373700     1
    2022     1.00  0.692367  0.757041  0.816469     0
    2023     0.10  0.692367  0.377966  0.390111     1
    2024     0.76  0.239571  0.309105  0.436225     1
    2025     0.77  0.239571  0.336537  0.448702     1

    [2026 rows x 5 columns]
    print(classification_report(test_y, result.pred))

                  precision    recall  f1-score   support

               0       0.93      0.87      0.90      1701
               1       0.49      0.65      0.56       325

        accuracy                           0.83      2026
       macro avg       0.71      0.76      0.73      2026
    weighted avg       0.86      0.83      0.84      2026
    print(balanced_accuracy_score(test_y, result.pred))

    0.7584090806313029
    Voting(hard voting)

    다수결 투표에 의해 최종 예측값을 산출하는 방식
    모형이 3개 이므로 2개 이상 예측 결과가 같은 경우 최종 예측값으로 산출
    pred_dt = decisiontree_search.predict(test_X)
    pred_rf = RandomForest_search.predict(test_X)


    result2 = pd.DataFrame({'rf_pred' : pred_rf,
                           'dt_pred' : pred_dt,
                           'xgb_pred' : pred_xgb})

    result2['pred'] = np.where((result2.rf_pred == 0) & (result2.dt_pred == 0), 0,
                              np.where((result2.rf_pred == 0) & (result2.xgb_pred == 0), 0,
                                      np.where((result2.dt_pred == 0) & (result2.xgb_pred == 0), 0, 1)))

    print(classification_report(test_y, result2.pred))

                  precision    recall  f1-score   support

               0       0.93      0.86      0.89      1701
               1       0.48      0.68      0.56       325

        accuracy                           0.83      2026
       macro avg       0.71      0.77      0.73      2026
    weighted avg       0.86      0.83      0.84      2026
    print(balanced_accuracy_score(test_y, result2.pred))         

    0.7701098901098901
    weighted average

    모델 별로 예측 정확도가 다르기 때문에 예측 정확도가 높은 모델에 더 큰 가중치를 부여한 후 평균을 내는 방식
    예측 평가 지표는 임의로 선택하면 됨(모든 모델에 공통으로)
    rf_w = 0.66 / (0.66 + 0.5 + 0.78)
    dt_w = 0.5 / (0.66 + 0.5 + 0.78)
    xgb_w = 0.78 / (0.66 + 0.5 + 0.78)

    result['w_average'] = (result.rf_prob*rf_w) + (result.dt_prob*dt_w) + (result.xgb_prob*xgb_w)
    result['pred_w'] = np.where(result.w_average > 0.5, 0, 1)

    print(classification_report(test_y, result.pred_w))

                  precision    recall  f1-score   support

               0       0.93      0.87      0.90      1701
               1       0.48      0.64      0.55       325

        accuracy                           0.83      2026
       macro avg       0.70      0.75      0.72      2026
    weighted avg       0.86      0.83      0.84      2026
    print(balanced_accuracy_score(test_y, result.pred_w))     

    0.7544503233392122
    17.2 통계분석
    17.2.1 Data description
    날짜 및 주가 수익률 데이터로 time series 변환 전 데이터 제공

    주가 데이터는 계절 추세가 있는 데이터를 못찾아서 river flow에 대한 데이터로 대체함

    17.2.2 시계열 데이터의 정규성과 이분산성을 분석하시오(시각화 포함)(10점).
    dat = pd.read_csv("data/ex_data/flow.csv")
    dat.columns = ['value']

    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf, pacf
    import pmdarima as pm

    dat.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(dat['value'], ax = ax1)
    plot_pacf(dat['value'], ax = ax2, method = 'ywm')
    plt.show();



    계절 추세가 존재하는 것으로 보임
    일반 추세도 존재? 확인 필요
    분산이 증가하는 패턴은 없는 것으로 보임
    from pmdarima.arima.utils import nsdiffs
    #cht = pm.arima.CHTest(m=12)
    #cht.estimate_seasonal_differencing_term(trans_dat)
    nsdiffs(dat, m = 12, max_D=12, test='ch')

    0
    계절 추세 존재 여부 확인 : Canova-Hansen test 결과를 바탕으로 추천된 계절 차분 차수는 0인 것을 확인할 수 있음

    from pmdarima.arima.utils import ndiffs
    ndiffs(dat, test='kpss')

    1
    일반 추세 존재 여부 확인 : KPSS test 결과를 바탕으로 추천된 일반 차분 차수는 1인 것을 확인할 수 있음

    17.2.3 시계열 데이터가 정규성이 아니라면, 고정시계열이 있는지 확인하고 이를 처리하시오(15점).
    계절 차분

    그래프를 보면 추세가 없고, 분산이 변화하는 패턴이 없으므로 정상성 만족

    dat_diff2 = dat.diff(12)
    dat_diff2.dropna(inplace = True)
    dat_diff2.plot();
    plt.show();



    fig, ax1 = plt.subplots(1, 1, figsize=(16,6))
    plot_acf(dat_diff2['value'], ax = ax1)
    plt.show();



    일반 차분

    ACF가 12주기로 커지는 패턴이 존재하므로, 계절성이 존재함
    dat_diff = dat.diff()
    dat_diff.dropna(inplace = True)
    dat_diff.plot();
    plt.show();



    fig, ax1 = plt.subplots(1, 1, figsize=(16,6))
    plot_acf(dat_diff['value'], ax = ax1, lags = 48)
    plt.show();



    일반차분 + 계절차분

    그래프를 보면 추세가 없고, 분산이 변화하는 패턴이 없으므로 정상성 만족
    dat_diff3 = dat_diff.diff(12)
    dat_diff3.dropna(inplace = True)
    dat_diff3.plot()
    plt.show();



    fig, ax1 = plt.subplots(1, 1, figsize=(16,6))
    plot_acf(dat_diff3['value'], ax = ax1, lags = 48)
    plt.show();



    최종적으로 계절 차분만 해도 추세가 무작위 변동으로 바뀌었기 때문에 정상성 만족
    모수가 적은 모형이 합리적인 모형이므로 굳이 일반 차분까지 고려 x
    17.2.4 SARIMA 분석을 실시하고, 여러 파라미터를 적용해보고 최적의 모형을 제시하시오(15점).
    fig, ax1 = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(dat_diff2['value'], ax = ax1[0])
    plot_pacf(dat_diff2['value'], ax = ax1[1])
    plt.show();



    후보모형

    ARIMA(1, 0, 0)(0, 1, 2)_12
    절편 비유의
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat, order=(1, 0, 0), seasonal_order=(0, 1, 2, 12), trend = 't').fit()
    print(model.summary())

                                           SARIMAX Results                                       
    =============================================================================================
    Dep. Variable:                                 value   No. Observations:                  600
    Model:             ARIMA(1, 0, 0)x(0, 1, [1, 2], 12)   Log Likelihood                -619.666
    Date:                               Mon, 30 Oct 2023   AIC                           1249.331
    Time:                                       23:35:30   BIC                           1271.215
    Sample:                                            0   HQIC                          1257.858
                                                   - 600                                         
    Covariance Type:                                 opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    x1            -0.0011      0.001     -1.426      0.154      -0.003       0.000
    ar.L1          0.5148      0.023     22.522      0.000       0.470       0.560
    ma.S.L12      -0.8388      0.025    -33.466      0.000      -0.888      -0.790
    ma.S.L24      -0.0527      0.025     -2.080      0.038      -0.102      -0.003
    sigma2         0.4667      0.012     38.296      0.000       0.443       0.491
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.27   Jarque-Bera (JB):              1683.16
    Prob(Q):                              0.60   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.62   Skew:                             0.26
    Prob(H) (two-sided):                  0.00   Kurtosis:                        11.27
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    ma.S.L24 모수 비유의
    model = ARIMA(dat, order=(1, 0, 0), seasonal_order=(0, 1, 2, 12)).fit()
    print(model.summary())

                                           SARIMAX Results                                       
    =============================================================================================
    Dep. Variable:                                 value   No. Observations:                  600
    Model:             ARIMA(1, 0, 0)x(0, 1, [1, 2], 12)   Log Likelihood                -621.013
    Date:                               Mon, 30 Oct 2023   AIC                           1250.026
    Time:                                       23:35:34   BIC                           1267.533
    Sample:                                            0   HQIC                          1256.847
                                                   - 600                                         
    Covariance Type:                                 opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ar.L1          0.5212      0.023     22.828      0.000       0.476       0.566
    ma.S.L12      -0.8330      0.024    -34.185      0.000      -0.881      -0.785
    ma.S.L24      -0.0482      0.025     -1.936      0.053      -0.097       0.001
    sigma2         0.4696      0.012     38.106      0.000       0.445       0.494
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.14   Jarque-Bera (JB):              1670.85
    Prob(Q):                              0.71   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.62   Skew:                             0.30
    Prob(H) (two-sided):                  0.00   Kurtosis:                        11.24
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    비유의한 모수 제거 후 재적합
    모든 모수 유의
    model2 = ARIMA(dat, order=(1, 0, 0), seasonal_order=(0, 1, [1,0], 12)).fit()
    print(model2.summary())

                                         SARIMAX Results                                      
    ==========================================================================================
    Dep. Variable:                              value   No. Observations:                  600
    Model:             ARIMA(1, 0, 0)x(0, 1, [1], 12)   Log Likelihood                -621.617
    Date:                            Mon, 30 Oct 2023   AIC                           1249.234
    Time:                                    23:35:35   BIC                           1262.365
    Sample:                                         0   HQIC                          1254.350
                                                - 600                                         
    Covariance Type:                              opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ar.L1          0.5209      0.022     23.257      0.000       0.477       0.565
    ma.S.L12      -0.8738      0.012    -73.447      0.000      -0.897      -0.850
    sigma2         0.4707      0.012     38.399      0.000       0.447       0.495
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.13   Jarque-Bera (JB):              1689.77
    Prob(Q):                              0.72   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.62   Skew:                             0.31
    Prob(H) (two-sided):                  0.00   Kurtosis:                        11.28
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 가정 만족

    답안 작성 다른 기출 참고

    ARIMA(1, 0, 0)(0, 1, 1)[12] 잠정 모형 선택

    sm.stats.acorr_ljungbox(model2.resid, lags=[24])

          lb_stat  lb_pvalue
    24  32.050888   0.125736
    model2.resid.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model2.resid, ax = ax1)
    model2.resid.hist(ax = ax2)
    plt.show();



    auto.arima

    ARIMA(1,0,0)(2,1,1)[12] intercept 모형 선택
    model3 = pm.auto_arima(dat.value, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=12,
                       d=0,
                       seasonal=True,   
                       start_P=0, 
                       D=1, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,0,0)(0,1,1)[12] intercept   : AIC=1428.314, Time=0.26 sec
     ARIMA(0,0,0)(0,1,0)[12] intercept   : AIC=1730.709, Time=0.01 sec
     ARIMA(1,0,0)(1,1,0)[12] intercept   : AIC=1421.648, Time=0.24 sec
     ARIMA(0,0,1)(0,1,1)[12] intercept   : AIC=inf, Time=0.87 sec
     ARIMA(0,0,0)(0,1,0)[12]             : AIC=1728.791, Time=0.01 sec
     ARIMA(1,0,0)(0,1,0)[12] intercept   : AIC=1549.407, Time=0.04 sec
     ARIMA(1,0,0)(2,1,0)[12] intercept   : AIC=1359.722, Time=3.52 sec
     ARIMA(1,0,0)(2,1,1)[12] intercept   : AIC=1249.893, Time=5.63 sec
     ARIMA(1,0,0)(1,1,1)[12] intercept   : AIC=inf, Time=0.49 sec
     ARIMA(1,0,0)(2,1,2)[12] intercept   : AIC=1251.610, Time=7.10 sec
     ARIMA(1,0,0)(1,1,2)[12] intercept   : AIC=inf, Time=4.58 sec
     ARIMA(0,0,0)(2,1,1)[12] intercept   : AIC=1421.134, Time=4.13 sec
     ARIMA(2,0,0)(2,1,1)[12] intercept   : AIC=1251.077, Time=5.77 sec
     ARIMA(1,0,1)(2,1,1)[12] intercept   : AIC=1251.095, Time=5.81 sec
     ARIMA(0,0,1)(2,1,1)[12] intercept   : AIC=1278.750, Time=5.07 sec
     ARIMA(2,0,1)(2,1,1)[12] intercept   : AIC=1253.077, Time=5.95 sec
     ARIMA(1,0,0)(2,1,1)[12]             : AIC=1250.350, Time=3.85 sec

    Best model:  ARIMA(1,0,0)(2,1,1)[12] intercept
    Total fit time: 53.335 seconds
    절편, ar.S.L12 비유의
    model3.summary()

    SARIMAX Results
    Dep. Variable:	y	No. Observations:	600
    Model:	SARIMAX(1, 0, 0)x(2, 1, [1], 12)	Log Likelihood	-618.946
    Date:	Mon, 30 Oct 2023	AIC	1249.893
    Time:	23:36:30	BIC	1276.153
    Sample:	0	HQIC	1260.125
    - 600		
    Covariance Type:	opg		
    coef	std err	z	P>|z|	[0.025	0.975]
    intercept	-0.0066	0.005	-1.390	0.164	-0.016	0.003
    ar.L1	0.5092	0.023	21.964	0.000	0.464	0.555
    ar.S.L12	0.0378	0.031	1.229	0.219	-0.022	0.098
    ar.S.L24	-0.0601	0.025	-2.404	0.016	-0.109	-0.011
    ma.S.L12	-0.8785	0.018	-48.562	0.000	-0.914	-0.843
    sigma2	0.4658	0.013	36.248	0.000	0.441	0.491
    Ljung-Box (L1) (Q):	0.23	Jarque-Bera (JB):	1541.47
    Prob(Q):	0.63	Prob(JB):	0.00
    Heteroskedasticity (H):	0.62	Skew:	0.25
    Prob(H) (two-sided):	0.00	Kurtosis:	10.92

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    비유의한 모수 제거 후 모든 모수 유의
    model3_1 = ARIMA(dat, order=(1, 0, 0), seasonal_order=([0,1], 1, 1, 12)).fit()
    print(model3_1.summary())

                                          SARIMAX Results                                       
    ============================================================================================
    Dep. Variable:                                value   No. Observations:                  600
    Model:             ARIMA(1, 0, 0)x([2], 1, [1], 12)   Log Likelihood                -620.384
    Date:                              Mon, 30 Oct 2023   AIC                           1248.768
    Time:                                      23:36:34   BIC                           1266.275
    Sample:                                           0   HQIC                          1255.589
                                                  - 600                                         
    Covariance Type:                                opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ar.L1          0.5135      0.023     22.550      0.000       0.469       0.558
    ar.S.L24      -0.0724      0.023     -3.089      0.002      -0.118      -0.026
    ma.S.L12      -0.8557      0.014    -61.398      0.000      -0.883      -0.828
    sigma2         0.4688      0.013     36.064      0.000       0.443       0.494
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.11   Jarque-Bera (JB):              1499.65
    Prob(Q):                              0.74   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.61   Skew:                             0.30
    Prob(H) (two-sided):                  0.00   Kurtosis:                        10.80
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 가정 만족

    절편과 ar.S.L12 항이 제거된 ARIMA(1,0,0)(2,1,1)[12] 잠정 모형 선택

    sm.stats.acorr_ljungbox(model3_1.resid, lags=[24])

          lb_stat  lb_pvalue
    24  27.653677   0.274918
    model3_1.resid.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model3_1.resid, ax = ax1)
    model3_1.resid.hist(ax = ax2)
    plt.show();



    model3_1.aic

    1248.7681268409451
    model2.aic

    1249.234425203858
    model3_1.bic

    1266.2750346325397
    model2.bic

    1262.364606047554
    aic, bic 기준으로 ARIMA(1, 0, 0)(0, 1, 1)[12] 최종 모형으로 선택
    17.2.5 위에서 제시한 모델의 잔차와 잡음에 대해 시각화하고 분석하시오(10점).
    sm.stats.acorr_ljungbox(model2.resid, lags=[24])

          lb_stat  lb_pvalue
    24  32.050888   0.125736
    model2.resid.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model2.resid, ax = ax1)
    model2.resid.hist(ax = ax2)
    plt.show();




    # model2.plot_diagnostics()
    # plt.show();

     : 
     ~ 
     시차 시까지 잔차 사이에 자기상관이 없다.

    ljung box test 결과 유의수준 0.05에서 Q* = 32.050888, p-value = 0.125736로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 24시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.

    잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.

    잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.
    """
