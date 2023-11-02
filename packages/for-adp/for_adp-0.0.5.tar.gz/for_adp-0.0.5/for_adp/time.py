def time():

    """
    시계열 코드

    tour = pd.read_csv('C:/Users/tsrif/Desktop/oneDrive/ADP/machine/data/ex_data/timeseries/tour92.txt')

    dat = tour.rename(columns = {'index' : 'date'})
    dat['date'] = pd.to_datetime(dat['date'], format = '%Y %b')

    import datetime
    dat['date'] = dat['date'].dt.strftime('%Y-%m')
    dat.index = dat['date']
    dat = dat.drop(['date'], axis = 1)


    데이터 탐색

    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf, pacf
    dat.plot()
    plt.show();

    #결측치가 존재할 경우 missing = 'drop'로 설정 필요
    plot_acf(dat.value, missing = 'drop')
    plt.show();

    #분산확인(boxcox 변환)
    # 결측치 확인
    #추세확인, 계절성 확인

    #결측치 확인 및 대체
    # 테스트 분할
    TEST_SIZE = 12
    train, test = dat.iloc[:-TEST_SIZE], dat.iloc[-TEST_SIZE:]
    train.shape, test.shape

    train.plot()
    plt.show();
    #결측치 확인

    #선형외삽, 
    #선형외삽법은 결측치 양쪽의 값들을 사용하여 선형으로 값을 채우는 방법입니다.
    # LOCF(Last Observation Carried Forward) 방법으로 결측치가 발생한 시점에서 가장 가까운 자료 값으로 결측치를 대체하는 방법이다.

    #train2 = train.copy()
    #train2 = train2.assign(locf=train2.value.fillna(method = 'ffill'))
    #train2['linear'] = train2.value.interpolate(method='linear')
    #train2[train2.value.isna()]

    train['value'] = train.value.interpolate(method='linear')

    #시계열 모델 구축
     # 분산 안정화
    from scipy import stats
    lambda_result = stats.boxcox(train['value'])
    print(lambda_result[1])
    # Box-Cox 혹은 lambda 보고 그냥 로그 변환
    # Box-Cox 변환
    import numpy as np
    from scipy import stats
    transformed_data, lambda_ = stats.boxcox(data)

    # 변환된 데이터와 lambda 값을 출력
    print("Transformed Data:", transformed_data)
    print("Lambda:", lambda_)

    def boxcox_inverse(data, lambda_):
        if lambda_ == 0:
            return np.exp(data)
        else:
            return np.exp(np.log(lambda_ * data + 1) / lambda_)

    # 역변환
    original_data = boxcox_inverse(transformed_data, lambda_)

    train['value'] = np.log(train['value'])
    test['value'] = np.log(test['value'])
    #or
    train['value'], lambda_ = stats.boxcox(train['value'])
    #test['value'], lambda_ = stats.boxcox(test['value'])




    train.plot()
    plt.show();


    시계열 데이터에서 변동성의 정상성을 검정하는 방법 중 하나는 ARCH 효과를 검정하는 것입니다
    import numpy as np
    import pandas as pd
    from statsmodels.stats.diagnostic import het_arch

    # ARCH 효과 검정
    test_stat, p_value, _, _ = het_arch(returns)

    print(f'ARCH 효과 검정 통계량: {test_stat}')
    print(f'p-value: {p_value}')

    # p-value 해석
    if p_value < 0.05:
        print("ARCH 효과가 존재합니다 (분산이 시간에 따라 변합니다).")
    else:
        print("ARCH 효과가 존재하지 않습니다 (분산이 일정합니다).")
    # 시간에 따라 분산이 일정하게 안정화 확인

    #d = 1일 때 (일반 차분)

    #추세와 계절성이 함께 존재하므로, 일반차분과 계절차분을 고려해볼 수 있음 

    #kpss test

    from statsmodels.tsa.stattools import kpss

    print('test statistic: %f' % kpss(train)[0])
    print('p-value: %f' % kpss(train)[1])

    #kpss test 결과 유의수준 0.05에서 p-value = 0.01 로 작기 때문에 귀무가설을 기각, 해당 데이터는 정상성을 만족하지 않으며, 차분 필요

    #계절성 확인
    from pmdarima.arima.utils import nsdiffs
    #cht = pm.arima.CHTest(m=12)
    #cht.estimate_seasonal_differencing_term(trans_dat)
    nsdiffs(train,
                m=12, 
                max_D=12,
                test='ch')

    #계절성 존재 여부 확인 : Canova-Hansen test 결과를 바탕으로 추천된 계절 차분 차수는 0인 것을 확인할 수 있음
    #lag으로 조절
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train['value'], ax = ax1, lags = 40)
    ax1.set_xlim([0, 30]) #축범위 조절
    plot_pacf(train['value'], ax = ax2, method = 'ywm', lags = 40)
    ax2.set_xlim([0, 30]) #축범위 조절

    plt.show();

    #해석
    #d=1의 경우

    #추세 그래프를 보았을 때, 12를 주기로 일정한 패턴의 진폭을 보이는 것을 확인할 수 있으며, acf plot을 보면 추세는 제거되었지만 12를 주기로 acf 값이 커지는 것을 볼 수 있음
    #따라서 추가적으로 계절 차분을 고려해볼 수 있음
    #d = 1 수행 일반차분
    train_diff = train.diff()
    train_diff.plot()
    plt.show();

    train_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train_diff['value'], ax = ax1)
    plot_pacf(train_diff['value'], ax = ax2, method = 'ywm')
    plt.show();

    print('test statistic: %f' % kpss(train_diff)[0])
    print('p-value: %f' % kpss(train_diff)[1])

    #kpss test 결과 유의수준 0.05에서 p-value = 0.1로 크기 때문에 귀무가설을 기각할 수 없음, 해당 데이터는 정상성 만족

    #kpss test 결과 추세는 제거된 것을 확인할 수 있음
    #kpss test는 계절성은 반영 x

    #계절성 1
    D=1의 경우

    #추세는 계절 차분만으로도 해결되는 경우가 있음
    #계절 차분 결과, 추세 그래프와 acf plot을 확인해보면 추세가 존재하고, acf가 천천히 감소하는 것을 확인할 수 있음
    #추가적인 일반 차분을 고려함

    train_diff2 = train.diff(12) #계절성
    train_diff2.dropna(inplace = True)
    train_diff2.plot();
    plt.show();

    fig, ax1 = plt.subplots(1, 1, figsize=(16,6))
    plot_acf(train_diff2['value'], ax = ax1)
    plt.show();

    #d=1, D=1의 경우
    #정상성 확보
    #최적의 차분 : d = 1, D = 1

    train_diff3 = train_diff.diff(12)
    train_diff3.plot()
    plt.show();

    #모델링 fitting
    train_diff3.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(train_diff3['value'], ax = ax1, lags = 40)
    plot_pacf(train_diff3['value'], ax = ax2, method = 'ywm', lags = 40)
    plt.show();

    #계절형 확인(계절형 주기인 12근처에서 확인)
    #ACF 12차 근처에서만 유의적 : P = 0, Q = 1
    #ACF 12에서 절단, PACF 12배수 지수적감소
    #둘다 지수적 감소면 ARIMA(0,1,1)(1,1,1)12
    #비계절형 확인(앞에서 확인)
    #ACF 절단, PACF 감소 : p = 0, q = 1
    #후보 모형
    #ARIMA(0,1,1)(0,1,1)12

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(train, order=(0,1,1),
                  seasonal_order=(0, 1, 1, 12)).fit()
    print(model.summary())

    model.plot_diagnostics()
    plt.tight_layout()

    plt.show();

    sm.stats.acorr_ljungbox(model.resid, lags=[24])

    #신뢰구간을 확인해본 결과, ma1, sma1 모두 신뢰구간에 0을 포함하지 않으므로 유의함
    # 귀무가설 : 0~24 시차까지 잔차 사이에 자기상관이 없다.
    #ljung box test 결과 유의수준 0.05에서 Q* = 30.56, p-value = 0.46로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 24시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.
    #잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.
    #잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.

    # auto arima 이용

    import pmdarima as pm
    model2 = pm.auto_arima(train, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=12,             #계절성
                       d=1,          # 차분
                       seasonal=True,   
                       start_P=0, 
                       D=1,      #계절차분
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)
    #Best model:  ARIMA(0,1,1)(0,1,1)[12]

    #실제값과 예측값 비교(역변환 필수!)
    prediction, confint = model2.predict(n_periods=TEST_SIZE, return_conf_int=True)

    prediction = np.exp(prediction)
    confint = np.exp(confint)
    or
    prediction = boxcox_inverse (prediction, lambda_)
    confint = boxcox_inverse (confint, lambda_)


    train_or['value'] = boxcox_inverse(train['value'], lambda_)


    train ['value'] = np.exp(train['value'])
    test['value'] = np.exp(test['value'])
    full_dat = pd.concat([train_or, test_or], axis = 0)

    cf = pd.DataFrame(confint)
    prediction_series = pd.Series(prediction,index=test.index)
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))

    ax.plot(full_dat.value)
    ax.plot(prediction_series)
    ax.fill_between(prediction_series.index,
                    cf[0],
                    cf[1],color='grey',alpha=.3)
    plt.show();

    23.2.4 업무에 적용할 수 있는지, 판단근거와 함께 서술하시오
    예측 성능을 비교하기 위해 MASE를 고려함
    def MASE(training_series, testing_series, prediction_series):

        n = training_series.shape[0]
        d = np.abs(  np.diff( training_series) ).sum()/(n-1)

        errors = np.abs(testing_series - prediction_series )
        return errors.mean()/d

    MASE(train['value'].to_numpy(), test['value'].to_numpy(), prediction.to_numpy())
    MASE는 RMSE, MAE와 달리 scale에 의존하지 않기 때문에, 값의 비교가 용이함

    MASE가 1보다 크다는 의미는 학습 데이터에서의 naive forecast(ex.) 모형에서의 오차가 더 크다고 볼 수 있음

    MASE를 기준으로 보면 test 데이터를 기준으로 MASE = 3.05로 1보다 큼

    즉, 일반화 불가능

    따라서 해당 모형을 이용하는 것은 적절하지 않고, 대안 모형을 활용해야 함

    LSTM, prophet 등 다른 시계열 모형을 대안으로 고려


    Arima 실습

    시계열 그림, SACF 작성
    추세가 있는지 확인

    추세가 있으므로 차분이 필요해보임

    acf plot을 보면 천천히 감소하므로 차분이 필요해보임

    시간에 따라 분산이 일정한지 확인

    시간에 따라 분산은 일정해보임
    dat.plot()
    plt.show();

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat['value'], ax = ax1, lags = 40)
    ax1.set_xlim([0, 30]) #축범위 조절

    plot_pacf(dat['value'], ax = ax2, method = 'ywm', lags = 40)
    ax1.set_xlim([0, 30]) #축범위 조절
    )
    plt.show();

    차분 차수 결정
    귀무가설 : 데이터가 정상성(stationarity)을 만족한다

    kpss test 결과 유의수준 0.05에서 p-value = 0.01 로 작기 때문에 귀무가설을 기각한다. 따라서 해당 데이터는 정상성을 만족하지 않으며, 차분이 필요해보인다.

    from statsmodels.tsa.stattools import kpss
    print('test statistic: %f' % kpss(dat)[0])
    print('p-value: %f' % kpss(dat)[1])

    차분 결과 확인
    원자료 확률보행과정

    차분 이후 백색잡음과정

    dat_diff = dat.diff()
    dat_diff.plot()
    plt.show();

    dat_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff['value'], ax = ax1)
    plot_pacf(dat_diff['value'], ax = ax2, method = 'ywm')
    plt.show();

    print('test statistic: %f' % kpss(dat_diff)[0])
    print('p-value: %f' % kpss(dat_diff)[1])

    kpss test 결과 유의수준 0.05에서 p-value = 0.1 로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 차분한 데이터는 정상성을 만족한다.

    후보모형 : ARIMA(0, 1, 2)

    다른 모형을 고려해볼 수도 있음(주관적)

    ARIMA(0, 1, 2)
    신뢰구간을 통해 절편 포함 여부 및 모수 유의성 확인

    신뢰구간이 0을 포함하는 경우 해당 모수 비유의

    ma2 비유의
    trend = 't' : 차분모형에 대한 절편 포함 여부

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat.value, order=(0,1,2), trend = 't').fit()
    print(model.summary())

    비유의한 모수 빼고 다시 적합

    다른 모수 전부 유의
    비유의한 모수를 제외할 경우 [1, 0] : [ma1, ma2]로 지정하면 ma2 제외됨

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat.value, order=(0, 1, [1, 0]), trend = 't').fit()
    print(model.summary())

    모형 가정 확인
    오차에 대해 백색잡음과정을 가정했으므로, 잔차를 통해 백색잡음과정이 맞는지 확인하는 절차가 필요함
    서로 독립이고, 평균이 0이고, 상수분산 을 가지며 많은 경우 정규분포를 가정함

    잔차의 패턴이 0을 중심으로 추세가 없는 랜덤한 형태인지 확인

    잔차의 정규성 확인

    acf plot 확인 : 신뢰구간 안에 거의 대부분 포함되어 있어야함

    k시차 시까지 잔차사이에 자기상관이 없다
    비계절형의 경우 보통 lag 10차시까지 검정
    sm.stats.acorr_ljungbox(model.resid, lags=[10])
    model.resid.plot()
    plt.show();
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model.resid, ax = ax1)
    model.resid.hist(ax = ax2)
    plt.show();

    신뢰구간을 확인해본 결과, 절편 포함 ma1항 모두 신뢰구간에 0을 포함하지 않으므로 유의함.
    0~10 시차 시까지 잔차 사이에 자기상관이 없다.
    ljung box test 결과 유의수준 0.05에서 Q* = 10.87, p-value = 0.36로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 10시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다
    잔차의 acf plot을 확인해본 결과 대체로 신뢰구간 안에 값이 포함되어 있는 것을 확인할 수 있다.

    잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.

    잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.

    Auto.arima
    # pmdarima==2.0.1
    #from pmdarima.pipeline import Pipeline
    import pmdarima as pm

    model2 = pm.auto_arima(dat.value, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=1,             #계절성
                       d=1,          # 차분
                       seasonal=False,   #계절성있을경우
                       start_P=0, 
                       D=None, #계절 차분
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)
    Best model:  ARIMA(0,1,3)(0,0,0)[0] intercept

    model2.summary()
    절편 포함 여부 및 모수 유의성 확인
    모든 모수 유의

    모형 검진
    가정 만족

    sm.stats.acorr_ljungbox(model2.resid(), lags=[10])
    model.resid.plot()
    plt.show();

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model2.resid(), ax = ax1)
    model2.resid().hist(ax = ax2)
    plt.show();

    pm.tsdisplay를 이용하면 한번에 시각화 가능
    pm.tsdisplay(model2.resid(), lag_max=20, title="", show=True)

    aic, bic를 비교해서 최종 후보모형 선택
    print(model.aic)
    print(model2.aic())

    예측

    prediction, confint = model2.predict(n_periods = 20, return_conf_int=True)
    cf = pd.DataFrame(confint)
    prediction_series = pd.Series(prediction)
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    ax.plot(dat.value)
    ax.plot(prediction_series)
    plt.show();

    차분 차수 결정

    일반 차분 실시 : ACF가 시차 1, 2, …에서 매우 천천히 감소하는 경우
    계절 차분 실시 : ACF가 시차 s, 2s, … 에서 매우 천천히 감소하는 경우
    일반적인 경우 d + D는 2이하로 함

    AR(p, P), MA(q, Q) 차수 결정
    비계절형 차수 p, q : ACF, PACF를 이용한 일반적인 모형 인식 방법 사용
    계절형 차수 P, Q : ACF, PACF에서 시차 s, 2s, 3s, …을 대상으로 인식

    절편 포함 여부 결정
    이전과 동일하게 신뢰구간을 이용해서 절편 포함 여부 결정
    2번 차분을 한 경우 절편은 모형에 포함 x

    1. 평균 절대 오차 (Mean Absolute Error, MAE)
    특성: 각 예측 오차의 절대값을 취해 평균을 낸 것입니다. 이 측도는 모든 오류를 동일하게 취급합니다.
    사용 상황: 개별 오차의 크기에 덜 민감한 상황에서 사용합니다.
    from sklearn.metrics import mean_absolute_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    mae = mean_absolute_error(y_true, y_pred)

    2. 평균 제곱근 오차 (Root Mean Squared Error, RMSE)
    특성: 오차를 제곱하여 평균을 낸 후 제곱근을 취한 것입니다. 큰 오차에 더 큰 가중치를 줍니다.
    사용 상황: 큰 오차를 특히 피하고자 할 때 사용합니다.
    from sklearn.metrics import mean_squared_error
    import numpy as np
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    3. 평균 절대 백분율 오차 (Mean Absolute Percentage Error, MAPE)
    특성: 각 예측 오차의 절대값을 실제 값으로 나눈 뒤 평균을 내어 백분율로 나타낸 것입니다. 오차를 상대적인 비율로 표현합니다.
    사용 상황: 오차를 상대적인 비율로 비교하고자 할 때, 특히 여러 단위의 데이터를 비교할 때 유용합니다.
    def mean_absolute_percentage_error(y_true, y_pred): 
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = mean_absolute_percentage_error(y_true, y_pred)

    4. MASE (Mean Absolute Scaled Error)
    특성: 시계열 데이터의 정확도를 평가하는데 적합한 측도로, 단순 예측(no-change forecast)의 오차로 표준화된 오차의 평균입니다.
    사용 상황: 시계열 데이터에서 다른 시계열 데이터와의 비교가 필요할 때 사용합니다. 특히 시즌성이나 추세 등을 고려해야 할 때 유용합니다.

    def mean_absolute_scaled_error(y_true, y_pred, y_train):
        n = len(y_train)
        d = np.abs(np.diff(y_train)).sum() / (n-1)
        errors = np.abs(y_true - y_pred)
        return errors.mean() / d
    # y_train은 모델 훈련에 사용된 시계열 데이터입니다.
    mase = mean_absolute_scaled_error(y_true, y_pred, y_train)

    """
    return 0