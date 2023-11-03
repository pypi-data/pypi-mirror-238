def m14():
    """
    14  시계열분석
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    library(forecast)
    library(tidyverse)
    theme_set(theme_bw())

    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    14.1 시계열 모형 소개
    14.1.1 시계열 모형 종류
    AR
    MA
    ARMA
    ARIMA
    SARIMA
    기출문제 확인 결과 ARIMA, SARIMA 모형이 주로 출제되며, 시계열 예제 데이터 수준에서 나오기 때문에 분석 프로세스 위주로 숙지하면 됩니다.

    14.1.2 시계열 기본 가정
    주어진 시계열 자료 
    은 어느 특정한 확률과정의 실현값으로 생각할 수 있으며, 가능한 시계열 모형은 무수히 많으므로 이들 중에서 일부만 고려하자는 취지에서 나온 것이 정상성 개념임

    약 정상성

     : 평균이 시점 
    에 관계 없이 일정함


     : 분산이 시점 
    에 관계없이 일정함


     : 자기공분산이 lag 
    에만 의존


    기본 가정이라고 생각하면 되고, 정상 시계열 형태가 아닐 경우 변환, 차분 등을 통해 정상시계열로 만들어줘야함

    14.1.3 확률과정의 예
    백색잡음과정(ARIMA(0, 0, 0))

    서로 독립이고 동일한 분포를 따르는(i.i.d) 확률변수로 구성된 확률과정


    평균, 분산, 공분산 등이 t 시점에 무관하므로 정상시계열임



    확률보행과정(ARIMA(0, 1, 0))

    가 백색잡음과정일 때 
    를 확률보행과정이라고 함


    평균은 일정하지만 분산과 공분산은 
     시점에 의존

    뚜렷한 추세가 존재함

    진폭이 불규칙적

    비정상 시계열의 대표적인 예시로 적절한 변환을 통해 정상시계열로 만들어줘야함



    이동평균과정(MA)(ARIMA(0, 0, q))

    현 시점의 자료는 현 시점의 오차와 과거 시점의 오차들의 선형결합으로 결정되는 모형

    가 백색잡음과정일 때 
    를 이동평균과정이라고 함

    MA(1)


    평균과 분산은 시간 
    에 무관하고, 자기공분산도 시간 
    에 무관하고 단지 
    에만 의존하므로 정상확률과정임



    자기회귀과정(AR)(ARIMA(p, 0, 0))

    현재 시점의 자료는 과거 시점의 자료와 현재 시점의 오차에 의해 결정되는 모형

    가 백색잡음과정일 때 
    를 자기회귀과정이라고 함

    AR(1)




    평균과 분산은 시간 
    에 무관하고, 자기공분산도 시간 
    에 무관하고 단지 
    에만 의존하므로 정상확률과정임



    14.1.4 모형 인식 방법
    ACF(자기상관함수)

    시계열 자료 특성상 현재의 상태가 과거의 상태는 미래의 상태와 연관되므로 시간에 따른 상관 정도를 측정하는 척도가 필요한데, 시간의 흐름에 따른 상관 정도를 나타내는 측도로 자기상관함수를 정의함

    sample version



    Example





    from statsmodels.graphics.tsaplots import plot_acf, acf

    y = pd.Series([1, 2, 5])
    plot_acf(y)
    plt.show();



    acf(y)

    array([ 1.        , -0.05128205, -0.44871795])
    frac1 = (y[1] - np.mean(y))*(y[0] - np.mean(y)) + (y[2] - np.mean(y))*(y[1] - np.mean(y))
    frac2 = np.sum((y - np.mean(y))**2)
    print(frac1/frac2)

    -0.0512820512820513
    frac1 = (y[2] - np.mean(y))*(y[0] - np.mean(y))
    frac2 = np.sum((y - np.mean(y))**2)
    print(frac1/frac2)

    -0.4487179487179487
    Sample correlogram(표본상관도표)

    ex1 = pd.read_csv('./data/ex_data/timeseries/ex1.csv')
    plot_acf(ex1.x)
    plt.show();



    X축을 시차, Y축을 표본 ACF로 표현한 그림으로 모델 인식 절차에 사용됨

    이면 표본 ACF는 점근적으로 평균은 0, 분산은 

    인 정분포를 따르며, 이 성질에 따라 신뢰구간이 점선으로 추가됨

    표본 ACF가 점선을 벗어나 있으면 
    을 기각할 수 있음

    각 시점에 대한 검정이므로 다중검정의 고질적 문제인 일종 오류가 증가하는 문제가 발생함

    따라서 엄격한 검정으로는 이용 X

    다중검정 문제 참고 : 다중검정문제

    PACF(부분자기상관함수)

    와 
     사이의 직접적인 연관성을 측정하는 함수

    가 주어졌을 때 
    와 
    에서 
    의 효과를 제거한 후 상관관계를 측정함

    가 normality 가정 하에 다음과 같이 정의됨


    from statsmodels.graphics.tsaplots import plot_pacf, pacf

    dat = pd.DataFrame({'y' : [1, 5, 15, 12, 16, 20, 21]})

    plot_pacf(dat['y'], lags = 2)
    plt.show();



    pacf(dat['y'], method = 'ywm')

    array([ 1.        ,  0.45514383, -0.23291701])
    from sklearn.preprocessing import StandardScaler
    std = StandardScaler()
    y = std.fit_transform(dat[['y']]).flatten()
    y_t = np.insert(y, 0, [0, 0], axis = 0)
    y_lag_1 = np.insert(y, 0, 0, axis = 0)
    y_lag_1 = np.append(y_lag_1, 0)
    y_lag_2 = np.append(y, [0, 0])
    dat = pd.DataFrame({'y_t' : y_t, 'y_lag_1' : y_lag_1, 'y_lag_2' : y_lag_2})

    방법 1

    fit1 = smf.ols(formula='y_t ~ y_lag_1', data=dat).fit()
    fit2 = smf.ols(formula='y_t ~ y_lag_1 + y_lag_2', data=dat).fit()
    fit1.params[1]

    0.455143832276938
    fit2.params[2]

    -0.23291701381822505
    방법 2

    fit1 = smf.ols(formula='y_t ~ y_lag_1', data=dat).fit()
    fit2 = smf.ols(formula='y_lag_2 ~ y_lag_1', data=dat).fit()
    residuals = pd.DataFrame(dict(res_fit1=fit1.resid, res_fit2=fit2.resid))
    residuals.corr()

              res_fit1  res_fit2
    res_fit1  1.000000 -0.232917
    res_fit2 -0.232917  1.000000
    partial correlation

    참고 : https://dondonkim.netlify.app/posts/2022-08-31-partial-correlation/partial_corr.html
    Sample partial correlogram(표본부분상관도표)

    plot_pacf(ex1)
    plt.show();



    X축을 시차, Y축을 표본 PACF로 표현한 그림으로 모델 인식 절차에 사용됨

    문제점 ACF와 동일

    따라서 엄격한 검정으로는 이용 X

    ACF, PACF 그래프 이용해서 모형을 인식하므로 그래프를 해석하는 것이 중요함

    14.2 AR 모형
    14.2.1 AR(1)일 때
    ACF 지수적 감소

    PACF 1차 시점 이후 절단

    이론적 그림이므로 비슷한 형태를 띄면 절단이라고 인식함. 그래프를 이용한 해석은 주관적이므로 정확한 정답은 없음

    다만 딱 봐도 절단이면 절단이라고 인식할 수 있어야 함

    ex2 = pd.read_csv('./data/ex_data/timeseries/ex2.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(ex2['x'], ax = ax1)
    plot_pacf(ex2['x'], ax = ax2, method = 'ywm')
    plt.show();



    14.2.2 AR(2)일 때
    ACF 지수적 감소

    PACF 2차 시점 이후 절단

    ex3 = pd.read_csv('./data/ex_data/timeseries/ex3.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(ex3['x'], ax = ax1)
    plot_pacf(ex3['x'], ax = ax2, method = 'ywm')
    plt.show();



    14.3 AR(P)일 때
    AR(p) 차 시점 그림 또한 ACF 지수적 감소, PACF p차 시점 이후 절단으로 동일함

    절단의 경우 3차시 이후 시점은 복잡하므로 고려 x, auto arima로 진행

    14.4 MA 모형
    14.4.1 MA(1)일 때
    ACF 1차 시점 이후 절단

    PACF 지수적 감소

    AR모형과 ACF, PACF 그림만 반대이고, 모형 인식 방법은 동일함

    ex4 = pd.read_csv('./data/ex_data/timeseries/ex4.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(ex4['x'], ax = ax1)
    plot_pacf(ex4['x'], ax = ax2, method = 'ywm')
    plt.show();



    절단의 경우 3차시 이후 시점은 복잡하므로 고려 x, auto arima로 진행
    14.5 ARMA 모형(ARIMA(p, 0, q) = ARMA(p, q))
    AR 모형과 MA모형을 합친 형태로, AR의 p와 MA의 q를 파라미터로 갖는 혼합모형

    14.5.1 ARMA(1, 1)일 때
    ACF: AR(1)모형의 영향으로 지수적 감소

    PACF: MA(1)모형의 영향으로 지수적 감소

    ACF, PACF로 차수 p, q 인식 불가능

    참고 : https://otexts.com/fppkr/non-seasonal-arima.html
    ex5 = pd.read_csv('./data/ex_data/timeseries/ex5.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(ex5['x'], ax = ax1)
    plot_pacf(ex5['x'], ax = ax2, method = 'ywm')
    plt.show();



    14.6 AR, MA, ARMA 정리
    Model	ACF	PACF
    MA(q)	q 시차 이후 0으로 절단	지수적으로 감소
    AR(p)	지수적으로 감소	p시차 이후 0으로 절단
    ARMA(p, q)	지수적으로 감소	지수적으로 감소
    보통 모수 절약의 원칙에 따라 모형 성능이 비슷할 경우 
    가 작을수록 좋음

    그래프를 보고 모형을 인식하는 것은 분석가마다 다를 수 있음

    다만 시뮬레이션 데이터처럼 누가봐도 절단으로 보이는 것은 절단으로 인식할 수 있어야 함
    14.7 ARIMA
    14.7.1 비정상 시계열 특징
    추세가 존재
    계절성 존재
    분산이 시간대에 따라 변함
    실제 자료에서 정상성을 만족하는 경우는 거의 없으므로 변환을 통해 정상시계열로 만들어줘야함

    14.7.2 비정상 시계열 정상화 방법
    분산이 일정하지 않은 경우 : 분산안정화 변환 실시

    분산 증가 : 제곱근 변환, 로그변환

    분산 감소 : 지수변환, 제곱 변환



    분산이 증가할 때

    dat = pd.read_csv("./data/ex_data/timeseries/drug.csv")

    dat.plot(x="date", y="value")
    plt.show();



    from scipy import stats
    transform_data, fitted_lambda = stats.boxcox(dat['value'])

    dat = pd.DataFrame({'trans_value' : transform_data, 'date' : dat.date})
    dat.plot(x="date", y="trans_value")
    plt.show();



    추세가 존재하는 경우 : 차분 실시

    1차 차분


    z = pd.Series([1, 3, 6, 12, 19, 21, 30, 50])
    z.diff()

    0     NaN
    1     2.0
    2     3.0
    3     6.0
    4     7.0
    5     2.0
    6     9.0
    7    20.0
    dtype: float64
    #np.diff(z)

    2차 차분



    z = pd.Series([1, 3, 6, 12, 19, 21, 30, 50])
    z.diff().diff()

    0     NaN
    1     NaN
    2     1.0
    3     3.0
    4     1.0
    5    -5.0
    6     7.0
    7    11.0
    dtype: float64
    #np.diff(z, 2)

    계절성이 존재하는 경우 : 계절 차분 실시

    계절의개수


    z = pd.Series([1, 3, 6, 12, 19, 21, 30, 50, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    z.diff(periods = 12)

    0      NaN
    1      NaN
    2      NaN
    3      NaN
    4      NaN
    5      NaN
    6      NaN
    7      NaN
    8      NaN
    9      NaN
    10     NaN
    11     NaN
    12     4.0
    13     3.0
    14     1.0
    15    -4.0
    16   -10.0
    17   -11.0
    dtype: float64
    Note
    추세만 보고 명확하지 않을 수 있으므로, ACF 그래프도 같이 확인 필요

    1차 차분으로 정상성을 만족하지 않을 경우 2차 차분까지 실시

    3차 차분은 거의 하지 않으므로 고려 X

    계절 효과가 존재하는 경우 계절 차분 실시

    Example

    추세가 존재하는 경우

    추세 + acf 천천히 감소하는 형태

    dat = pd.read_csv('./data/ex_data/timeseries/elecstock.csv')

    dat.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat['value'], ax = ax1)
    plot_pacf(dat['value'], ax = ax2, method = 'ywm')
    plt.show();



    1차 차분 실시

    추세가 사라졌으며, acf, pacf가 신뢰구간 안에 들어간 형태인 것을 볼 수 있음

    dat_diff = dat.diff()
    dat_diff.plot()
    plt.show();



    dat_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff['value'], ax = ax1)
    plot_pacf(dat_diff['value'], ax = ax2, method = 'ywm')
    plt.show();



    14.7.3 ARIMA(p, d, q)
    ARMA 모형에 차분(d)이 추가된 모형임

    추세가 있으면 차분 실시

    ACF가 천천히 감소하면 차분 실시

    통계 검정 결과를 바탕으로 차분 실시

    -   KPSS test 

    -   귀무가설 : 데이터가 정상성(stationarity)을 만족한다 

    -   P-value < 0.05 면 귀무가설을 기각하고, 데이터가 정상성을 만족하지 않으며, 차분 필요 
    과대차분을 통해 차분 차수 d 결정
    -   옵션 중에 하나
    차분을 통해 정상시계열로 만들어준 후 차수 결정

    1, 2, 3, 4(옵션) 결과가 서로 다를 수 있음 –> 종합적인 판단 결과 제시
    d차 차분된 자료의 ACF, PACF로 p, q 차수 결정(AR, MA, ARMA 차수 결정방법과 동일)

    14.7.4 Example
    데이터 생성

    ARIMA(1, 1, 0)에서 난수 발생

    dat = pd.read_csv('./data/ex_data/timeseries/ex6.csv')

    dat.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat['x'], ax = ax1)
    plot_pacf(dat['x'], ax = ax2, method = 'ywm')
    plt.show();



    from statsmodels.tsa.stattools import kpss
    #from statsmodels.tsa.stattools import adfuller

    # def kpss_test(series):    
    #     statistic, p_value, n_lags, critical_values = kpss(series)
    #     print(f'KPSS Statistic: {statistic}')
    #     print(f'p-value: {p_value}')
    #     print(f'num lags: {n_lags}')
    #     print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')

    #print(adfuller(dat)[1])
    print(kpss(dat)[1])

    0.01
    1차 차분

    dat_diff = dat.diff()
    dat_diff.plot()
    plt.show();



    모형 식별

    acf 지수적 감소
    pacf 1차 이후 절단
    ARIMA(1, 1, 0)으로 식별
    dat_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff['x'], ax = ax1)
    plot_pacf(dat_diff['x'], ax = ax2, method = 'ywm')
    plt.show();



    과대 차분했을 경우

    정상성은 만족하지만 AR(1)모형 보다는 더 복잡한 모형으로 인식함

    모수 간결성의 원칙에 따라 과대차분 모형 제외

    dat_diff2 = dat.diff().diff()
    dat_diff2.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff2['x'], ax = ax1)
    plot_pacf(dat_diff2['x'], ax = ax2, method = 'ywm')
    plt.show();



    14.8 모형 적합 절차


    14.8.1 시계열 그림, SACF 작성
    시계열 정상화 단계

    등분산 확인 및 필요시 변환

    최적의 차분 차수 결정

    ACF 형태, 단위근 검정 결과로 판단

    과대차분 여부 확인(시험에서는 생략해도 무방함)

    14.8.2 ARIMA 모형 차수 p, q 결정
    SACF를 절단으로 인식 : MA 모형

    SPACF를 절단으로 인식: AR 모형

    SACF, SPACF 모두 감소로 인식 : ARMA 모형

    후보 모형이 많을 때 AIC, BIC가 최소가 되는 모형 선택

    보통 후보 모형 1 ~ 2개 정도로 시작

    모수 간결성의 원칙에 따라 가능한 차수가 적은게 좋음

    14.8.3 절편 포함 여부 결정
    신뢰구간을 통해 절편 포함 여부 검정
    14.8.4 모수 추정
    조건부 최소제곱 추정법

    비조건부 최소제곱 추정법

    최대가능도 추정법

    대부분의 경우 추정 결과에 차이 X, 패키지 이용할 것이므로 고려 X

    14.8.5 모형 진단
    모형 식별과 모수 추정을 통해 얻어진 잠정 모형의 타당성 여부 판단

    잔차분석

    오차항이 백색잡음과정을 따르는지 확인

    정규성 확인

    14.8.6 예측
    오차 측도

    MAE : 
    RMSE : 
    MAPE : 

    MASE : 
    , 


    MAPE의 경우 자료에 0이 있을 경우 무한대로 발산하므로 지표 선택 시 주의

    MASE : 1보다 값이 클 경우 training data로 계산된 naive forecast보다 예측력이 떨어진다는 의미

    naive forecast : 

    14.9 Arima 실습
    14.9.1 데이터 불러오기
    dat = pd.read_csv('./data/ex_data/timeseries/ex_7_5d.csv')

    14.9.2 시계열 그림, SACF 작성
    추세가 있는지 확인

    추세가 있으므로 차분이 필요해보임

    acf plot을 보면 천천히 감소하므로 차분이 필요해보임

    시간에 따라 분산이 일정한지 확인

    시간에 따라 분산은 일정해보임
    dat.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat['value'], ax = ax1)
    plot_pacf(dat['value'], ax = ax2, method = 'ywm')
    plt.show();



    14.9.3 차분 차수 결정
    귀무가설 : 데이터가 정상성(stationarity)을 만족한다

    kpss test 결과 유의수준 0.05에서 p-value = 0.01 로 작기 때문에 귀무가설을 기각한다. 따라서 해당 데이터는 정상성을 만족하지 않으며, 차분이 필요해보인다.

    from statsmodels.tsa.stattools import kpss
    #from statsmodels.tsa.stattools import adfuller

    # def kpss_test(series):    
    #     statistic, p_value, n_lags, critical_values = kpss(series)
    #     print(f'KPSS Statistic: {statistic}')
    #     print(f'p-value: {p_value}')
    #     print(f'num lags: {n_lags}')
    #     print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')


    #print('p-value: %f' % adfuller(dat)[1])
    print('test statistic: %f' % kpss(dat)[0])

    test statistic: 1.716117
    print('p-value: %f' % kpss(dat)[1])

    p-value: 0.010000
    14.9.4 차분 결과 확인
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

    test statistic: 0.311144
    print('p-value: %f' % kpss(dat_diff)[1])

    p-value: 0.100000
    kpss test 결과 유의수준 0.05에서 p-value = 0.1 로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 차분한 데이터는 정상성을 만족한다.

    후보모형 : ARIMA(0, 1, 2)

    다른 모형을 고려해볼 수도 있음(주관적)
    14.9.5 ARIMA(0, 1, 2)
    신뢰구간을 통해 절편 포함 여부 및 모수 유의성 확인

    신뢰구간이 0을 포함하는 경우 해당 모수 비유의

    ma2 비유의
    trend = 't' : 차분모형에 대한 절편 포함 여부

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat.value, order=(0,1,2), trend = 't').fit()
    print(model.summary())

                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  value   No. Observations:                  100
    Model:                 ARIMA(0, 1, 2)   Log Likelihood                -341.836
    Date:                Wed, 01 Nov 2023   AIC                            691.671
    Time:                        22:47:27   BIC                            702.052
    Sample:                             0   HQIC                           695.871
                                    - 100                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    x1             1.6713      0.229      7.300      0.000       1.223       2.120
    ma.L1         -0.5276      0.091     -5.785      0.000      -0.706      -0.349
    ma.L2         -0.1896      0.098     -1.942      0.052      -0.381       0.002
    sigma2        58.0678      8.417      6.899      0.000      41.571      74.565
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.17   Jarque-Bera (JB):                 0.21
    Prob(Q):                              0.68   Prob(JB):                         0.90
    Heteroskedasticity (H):               1.07   Skew:                             0.10
    Prob(H) (two-sided):                  0.86   Kurtosis:                         3.10
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    비유의한 모수 빼고 다시 적합

    다른 모수 전부 유의
    비유의한 모수를 제외할 경우 [1, 0] : [ma1, ma2]로 지정하면 ma2 제외됨

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat.value, order=(0, 1, [1, 0]), trend = 't').fit()
    print(model.summary())

                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  value   No. Observations:                  100
    Model:                 ARIMA(0, 1, 1)   Log Likelihood                -343.050
    Date:                Wed, 01 Nov 2023   AIC                            692.100
    Time:                        22:47:27   BIC                            699.886
    Sample:                             0   HQIC                           695.250
                                    - 100                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    x1             1.6620      0.241      6.890      0.000       1.189       2.135
    ma.L1         -0.7026      0.060    -11.777      0.000      -0.819      -0.586
    sigma2        59.4747      8.469      7.022      0.000      42.875      76.074
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.88   Jarque-Bera (JB):                 0.22
    Prob(Q):                              0.35   Prob(JB):                         0.90
    Heteroskedasticity (H):               1.09   Skew:                             0.11
    Prob(H) (two-sided):                  0.81   Kurtosis:                         3.09
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 가정 확인

    오차에 대해 백색잡음과정을 가정했으므로, 잔차를 통해 백색잡음과정이 맞는지 확인하는 절차가 필요함

    가정 : 
     서로 독립이고, 평균이 0이고, 상수분산 
    을 가지며, 
    는 많은 경우 정규분포를 가정함

    잔차의 패턴이 0을 중심으로 추세가 없는 랜덤한 형태인지 확인

    잔차의 정규성 확인

    acf plot 확인 : 신뢰구간 안에 거의 대부분 포함되어 있어야함

    Ljung-box test

     : 
     시차 시까지 잔차사이에 자기상관이 없다.

    sm.stats.acorr_ljungbox(model.resid, lags=[10])

         lb_stat  lb_pvalue
    10  10.87911   0.367014
    비계절형의 경우 보통 lag 10차시까지 검정
    model.resid.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model.resid, ax = ax1)
    model.resid.hist(ax = ax2)
    plt.show();



    답안 작성 방법

    신뢰구간을 확인해본 결과, 절편 포함 ma1항 모두 신뢰구간에 0을 포함하지 않으므로 유의함

     : 
     ~ 
     시차 시까지 잔차 사이에 자기상관이 없다.

    ljung box test 결과 유의수준 0.05에서 Q* = 10.87, p-value = 0.36로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 10시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.

    잔차의 acf plot을 확인해본 결과 대체로 신뢰구간 안에 값이 포함되어 있는 것을 확인할 수 있다.

    잔차 그래프를 보면 뚜렷한 분산 증가 감소 혹은 경향성이 없고, 0을 중심으로 무작위로 분포하므로, 오차의 등분산 가정을 만족한다고 할 수 있다.

    잔차의 분포를 확인했을 때, 근사적으로 정규분포의 형태를 띄므로, 오차의 정규성을 만족한다고 할 수 있다.

     잠정 모형으로 선택

    14.9.6 Auto.arima
    ARIMA(0, 1, 3) 잠정 모형 선택
    # pmdarima==2.0.1
    #from pmdarima.pipeline import Pipeline
    import pmdarima as pm

    model2 = pm.auto_arima(dat.value, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=1,             
                       d=1,          
                       seasonal=False,   
                       start_P=0, 
                       D=None, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,1,0)(0,0,0)[0] intercept   : AIC=720.840, Time=0.00 sec
     ARIMA(1,1,0)(0,0,0)[0] intercept   : AIC=712.861, Time=0.01 sec
     ARIMA(0,1,1)(0,0,0)[0] intercept   : AIC=692.100, Time=0.05 sec
     ARIMA(0,1,0)(0,0,0)[0]             : AIC=722.230, Time=0.00 sec
     ARIMA(1,1,1)(0,0,0)[0] intercept   : AIC=692.855, Time=0.05 sec
     ARIMA(0,1,2)(0,0,0)[0] intercept   : AIC=691.671, Time=0.06 sec
     ARIMA(1,1,2)(0,0,0)[0] intercept   : AIC=690.424, Time=0.03 sec
     ARIMA(2,1,2)(0,0,0)[0] intercept   : AIC=691.155, Time=0.04 sec
     ARIMA(1,1,3)(0,0,0)[0] intercept   : AIC=687.620, Time=0.05 sec
     ARIMA(0,1,3)(0,0,0)[0] intercept   : AIC=687.428, Time=0.03 sec
     ARIMA(0,1,4)(0,0,0)[0] intercept   : AIC=688.584, Time=0.03 sec
     ARIMA(1,1,4)(0,0,0)[0] intercept   : AIC=691.079, Time=0.07 sec
     ARIMA(0,1,3)(0,0,0)[0]             : AIC=705.695, Time=0.02 sec

    Best model:  ARIMA(0,1,3)(0,0,0)[0] intercept
    Total fit time: 0.444 seconds
    14.9.7 ARIMA(0, 1, 3)
    절편 포함 여부 및 모수 유의성 확인

    모든 모수 유의
    model2.summary()

    SARIMAX Results
    Dep. Variable:	y	No. Observations:	100
    Model:	SARIMAX(0, 1, 3)	Log Likelihood	-338.714
    Date:	Wed, 01 Nov 2023	AIC	687.428
    Time:	22:47:31	BIC	700.403
    Sample:	0	HQIC	692.678
    - 100		
    Covariance Type:	opg		
    coef	std err	z	P>|z|	[0.025	0.975]
    intercept	1.6658	0.259	6.419	0.000	1.157	2.174
    ma.L1	-0.6022	0.096	-6.256	0.000	-0.791	-0.414
    ma.L2	-0.3651	0.126	-2.905	0.004	-0.611	-0.119
    ma.L3	0.2979	0.109	2.730	0.006	0.084	0.512
    sigma2	54.3188	7.750	7.009	0.000	39.129	69.509
    Ljung-Box (L1) (Q):	0.03	Jarque-Bera (JB):	0.29
    Prob(Q):	0.86	Prob(JB):	0.87
    Heteroskedasticity (H):	1.23	Skew:	0.07
    Prob(H) (two-sided):	0.55	Kurtosis:	3.23

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 검진

    가정 만족
    sm.stats.acorr_ljungbox(model2.resid(), lags=[10])

         lb_stat  lb_pvalue
    10  3.761926   0.957448
    model.resid.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model2.resid(), ax = ax1)
    model2.resid().hist(ax = ax2)
    plt.show();



    pm.tsdisplay를 이용하면 한번에 시각화 가능

    pm.tsdisplay(model2.resid(), lag_max=20, title="", show=True)



    14.9.8 aic, bic를 비교해서 최종 후보모형 선택
    ARIMA(0, 1, 3) 모형 최종 모형으로 선택
    print(model.aic)

    692.1001582481658
    print(model2.aic())

    687.4275670796609
    14.9.9 예측
    prediction, confint = model2.predict(n_periods = 20, return_conf_int=True)
    cf = pd.DataFrame(confint)

    prediction_series = pd.Series(prediction)
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    ax.plot(dat.value)
    ax.plot(prediction_series)
    plt.show();



    14.10 Seasonal-ARIMA
    ARIMA 모형에 계절 요소가 반영된 모형

    ARIMA모형과 마찬가지로 차수를 정할 때 ACF, PACF 그래프를 이용해서 확인
    계절 요소도 ACF, PACF 그래프를 이용해서 확인
    14.10.1 
     : 
    ACF : 계절 주기 12의 배수에 해당하는 시차 12, 24, 36, ..에 따라 지수적으로 감소
    PACF : 시차 12에서만 값을 갖고 그 외의 시차는 0으로 절단


    14.10.2 
    ACF : 시차 12에서만 값을 갖고 그 외의 시차는 0으로 절단
    PACF : 계절 주기 12의 배수에 해당하는 시차 12, 24, 36, ..에 따라 지수적으로 감소


    14.10.3 
    ACF : 12 시차 이후부터 계절 주기 12 배수에 해당하는 시차에 따라 지수적 감소
    PACF : 12 시차 이후부터 계절 주기 12 배수에 해당하는 시차에 따라 지수적 감소
    Note
    계절 주기는 데이터에 따라 달라지므로, data description을 통해 파악 필요

    14.10.4 
    강한 계절요소로 인해 계절 추세가 존재하는 경우

    계절 주기 s의 배수에 대해 acf가 천천히 감소

    계절 차분을 통해 정상성 회복

    14.10.5 
    비계절형 ARIMA 요소, 계절형 ARIMA 요소를 모두 갖고 있는 모형
    acf, pacf를 이용한 모형 인식 방법 동일
    14.10.6 


    모형 적합 순서

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

    14.11 Seasonal-ARIMA 실습
    1984.1부터 1988.12 백화점 매출액 arima 모형 적합하고 12 선행 시차에 대해 예측 실시

    14.11.1 시계열 그림으로 정상성 확인
    분산 증가
    로그 변환 필요
    계절성이 뚜렷함
    dat = pd.read_csv('./data/ex_data/timeseries/depart.csv')
    dat = dat.rename(columns = {'index' : 'date'})
    dat['date'] = pd.to_datetime(dat['date'], format = '%Y %b')

    import datetime
    dat['date'] = dat['date'].dt.strftime('%Y-%m')
    dat.index = dat['date']
    dat = dat.drop(['date'], axis = 1)

    dat.plot()
    plt.show();



    14.11.2 boxcox 변환
    # from scipy import stats
    # transform_data, fitted_lambda = stats.boxcox(dat['value'])
    # print('lambda :', fitted_lambda)

    # trans_dat = pd.DataFrame({'value' : transform_data})
    # trans_dat.index = dat.index
    # trans_dat.plot()
    # plt.show();

    dat['value'] = np.log(dat['value'])
    dat.plot()
    plt.show();



    14.11.3 차분 차수 확인
    시계열 그림은 차분이 필요해보임
    acf는 차분의 필요성이 명확하지 않음
    kpss test 결과는 차분 필요
    ch test : Canova-Hansen test is used (with null hypothesis of deterministic seasonality)
    from statsmodels.tsa.stattools import kpss

    print('test statistic: %f' % kpss(dat)[0])

    test statistic: 1.383651
    print('p-value: %f' % kpss(dat)[1])

    p-value: 0.010000
    from pmdarima.arima.utils import nsdiffs

    #cht = pm.arima.CHTest(m=12)
    #cht.estimate_seasonal_differencing_term(trans_dat)
    nsdiffs(dat,
                m=12, 
                max_D=12,
                test='ch')

    0
    Canova-Hansen test 결과를 바탕으로 추천된 계절 차분 차수는 0인 것을 확인할 수 있음

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat['value'], ax = ax1)
    plot_pacf(dat['value'], ax = ax2, method = 'ywm')
    plt.show();



    d=1의 경우

    추세는 제거되었지만, 추가적인 계절 차분이 필요해보임
    dat_diff = dat.diff()
    dat_diff.plot()
    plt.show();



    dat_diff.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff['value'], ax = ax1)
    plot_pacf(dat_diff['value'], ax = ax2, method = 'ywm')
    plt.show();



    print('test statistic: %f' % kpss(dat_diff)[0])

    test statistic: 0.233530
    print('p-value: %f' % kpss(dat_diff)[1])

    p-value: 0.100000
    D=1의 경우

    추세는 계절 차분만으로도 해결되는 경우가 있음

    이 경우 추세가 존재하므로 추가적으로 일반 차분 실시

    dat_diff2 = dat.diff(12)
    dat_diff2.plot()
    plt.show();



    d=1, D=1의 경우

    정상성 확보

    최적의 차분 : d = 1, D = 1

    dat_diff3 = dat_diff.diff(12)
    dat_diff3.plot()
    plt.show();



    14.11.4 모형 인식
    acf 1차 절단, pacf 감소 : p = 0, q = 1
    acf 감소, pacf 2차 절단 : p = 2, q = 0
    계절 요소 12 시차에서 모두 비유의적 : P = 0, Q = 0
    dat_diff3.dropna(inplace = True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(dat_diff3['value'], ax = ax1, lags = 24)
    plot_pacf(dat_diff3['value'].squeeze(), ax = ax2, method = 'ywm', lags = 22)
    plt.show();



    14.11.5 
    모든 모수 유의

    모형 가정 만족

    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(dat, order=(0,1,1), seasonal_order=(0, 1, 0, 12)).fit()
    print(model.summary())

                                         SARIMAX Results                                     
    =========================================================================================
    Dep. Variable:                             value   No. Observations:                   60
    Model:             ARIMA(0, 1, 1)x(0, 1, [], 12)   Log Likelihood                 108.233
    Date:                           Wed, 01 Nov 2023   AIC                           -212.465
    Time:                                   22:47:42   BIC                           -208.765
    Sample:                               01-01-1984   HQIC                          -211.073
                                        - 12-01-1988                                         
    Covariance Type:                             opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ma.L1         -0.5650      0.155     -3.649      0.000      -0.868      -0.261
    sigma2         0.0006   9.21e-05      6.357      0.000       0.000       0.001
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.12   Jarque-Bera (JB):                 9.33
    Prob(Q):                              0.73   Prob(JB):                         0.01
    Heteroskedasticity (H):               0.74   Skew:                            -0.90
    Prob(H) (two-sided):                  0.56   Kurtosis:                         4.24
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model.resid, ax = ax1)
    model.resid.hist(ax = ax2)
    plt.show();



    sm.stats.acorr_ljungbox(model.resid, lags=[12])

          lb_stat  lb_pvalue
    12  16.967024   0.150842
    14.11.6 
    모든 모수 유의

    모형 가정 만족

    from statsmodels.tsa.arima.model import ARIMA
    model2 = ARIMA(dat, order=(2,1,0), seasonal_order=(0, 1, 0, 12)).fit()
    print(model2.summary())

                                        SARIMAX Results                                     
    ========================================================================================
    Dep. Variable:                            value   No. Observations:                   60
    Model:             ARIMA(2, 1, 0)x(0, 1, 0, 12)   Log Likelihood                 108.340
    Date:                          Wed, 01 Nov 2023   AIC                           -210.681
    Time:                                  22:47:44   BIC                           -205.130
    Sample:                              01-01-1984   HQIC                          -208.592
                                       - 12-01-1988                                         
    Covariance Type:                            opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ar.L1         -0.5248      0.176     -2.975      0.003      -0.871      -0.179
    ar.L2         -0.3318      0.166     -2.002      0.045      -0.657      -0.007
    sigma2         0.0006   9.45e-05      6.118      0.000       0.000       0.001
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.01   Jarque-Bera (JB):                 9.09
    Prob(Q):                              0.91   Prob(JB):                         0.01
    Heteroskedasticity (H):               0.70   Skew:                            -0.90
    Prob(H) (two-sided):                  0.48   Kurtosis:                         4.20
    ===================================================================================

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model2.resid, ax = ax1)
    model2.resid.hist(ax = ax2)
    plt.show();



    sm.stats.acorr_ljungbox(model2.resid, lags=[12])

          lb_stat  lb_pvalue
    12  16.942806   0.151761
    14.11.7 Auto.arima
    # pmdarima==2.0.1
    #from pmdarima.pipeline import Pipeline
    import pmdarima as pm

    model3 = pm.auto_arima(dat, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=12,             
                       d=1,          
                       seasonal=True,   
                       start_P=0, 
                       D=1, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,1,0)(0,1,1)[12]             : AIC=-203.890, Time=0.19 sec
     ARIMA(0,1,0)(0,1,0)[12]             : AIC=-202.563, Time=0.02 sec
     ARIMA(1,1,0)(1,1,0)[12]             : AIC=-209.371, Time=0.18 sec
     ARIMA(0,1,1)(0,1,1)[12]             : AIC=-214.601, Time=0.21 sec
     ARIMA(0,1,1)(0,1,0)[12]             : AIC=-212.465, Time=0.03 sec
     ARIMA(0,1,1)(1,1,1)[12]             : AIC=-212.866, Time=0.27 sec
     ARIMA(0,1,1)(0,1,2)[12]             : AIC=-213.288, Time=0.70 sec
     ARIMA(0,1,1)(1,1,0)[12]             : AIC=-214.324, Time=0.12 sec
     ARIMA(0,1,1)(1,1,2)[12]             : AIC=-210.968, Time=0.77 sec
     ARIMA(1,1,1)(0,1,1)[12]             : AIC=-212.634, Time=0.18 sec
     ARIMA(0,1,2)(0,1,1)[12]             : AIC=-212.674, Time=0.19 sec
     ARIMA(1,1,0)(0,1,1)[12]             : AIC=-208.907, Time=0.13 sec
     ARIMA(1,1,2)(0,1,1)[12]             : AIC=-210.602, Time=0.29 sec
     ARIMA(0,1,1)(0,1,1)[12] intercept   : AIC=-212.582, Time=0.12 sec

    Best model:  ARIMA(0,1,1)(0,1,1)[12]          
    Total fit time: 3.403 seconds
    14.11.8 ARIMA(0,1,1)(0,1,1)[12]
    모든 모수 유의
    model3.summary()

    SARIMAX Results
    Dep. Variable:	y	No. Observations:	60
    Model:	SARIMAX(0, 1, 1)x(0, 1, 1, 12)	Log Likelihood	110.301
    Date:	Wed, 01 Nov 2023	AIC	-214.601
    Time:	22:47:49	BIC	-209.051
    Sample:	01-01-1984	HQIC	-212.512
    - 12-01-1988		
    Covariance Type:	opg		
    coef	std err	z	P>|z|	[0.025	0.975]
    ma.L1	-0.5846	0.153	-3.832	0.000	-0.884	-0.286
    ma.S.L12	-0.4162	0.210	-1.986	0.047	-0.827	-0.005
    sigma2	0.0005	9.3e-05	5.438	0.000	0.000	0.001
    Ljung-Box (L1) (Q):	0.03	Jarque-Bera (JB):	6.33
    Prob(Q):	0.87	Prob(JB):	0.04
    Heteroskedasticity (H):	0.82	Skew:	-0.64
    Prob(H) (two-sided):	0.70	Kurtosis:	4.27

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 검진

    가정 만족
    sm.stats.acorr_ljungbox(model3.resid(), lags=[12])

         lb_stat  lb_pvalue
    12  17.02342   0.148718
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    plot_acf(model3.resid(), ax = ax1)
    model3.resid().hist(ax = ax2)
    plt.show();



    14.11.9 AIC, BIC 비교
    최종 모형 : ARIMA(0,1,1)(0,1,1)[12]
    model.aic

    -212.4653096100055
    model2.aic

    -210.68050875662576
    model3.aic()

    -214.60113512182843
    model.bic

    -208.76501440658538
    model2.bic

    -205.13006595149557
    model3.bic()

    -209.05069231669825
    14.11.10 원자료에 대한 예측
    dat.index = pd.to_datetime(dat.index) # index 날짜형으로 변환

    prediction, confint = model3.predict(n_periods = 12, return_conf_int = True)
    prediction = np.exp(prediction)      # 로그 변환을 했으므로, 원래 값으로 변환
    confint = np.exp(confint)
    dat['value'] = np.exp(dat['value'])
    cf = pd.DataFrame(confint)
    prediction_series = pd.Series(prediction)

    fig, ax = plt.subplots(1, 1, figsize = (15, 5))
    ax.plot(dat.value)
    ax.plot(prediction_series)
    ax.fill_between(prediction_series.index,
                    cf[0],
                    cf[1], color = 'grey',alpha = .3)
    # ax.set_xticks(np.arange(0, total_len + 1, 10))
    plt.show();



    14.12 분기별 데이터 예제
    1996 ~ 2011년까지 분기별 유럽 소매 지수 데이터
    dat = pd.read_csv('~/Desktop/Qbook/data/ex_data/timeseries/euretail.csv')
    dat = dat.rename(columns = {'index' : 'date'})
    dat['date'] = pd.to_datetime(dat['date'].str.replace(' ', ''))
    dat['date'] = dat['date'].dt.strftime('%Y-%m')
    dat.index = dat['date']
    dat = dat.drop(['date'], axis = 1)

    dat.plot()
    plt.show();



    일반 추세 존재

    반복된 증가, 감소 패턴이 있으므로, 계절 추세도 확인 필요

    계절 차분

    dat_diff = dat.diff(4)
    dat_diff.dropna(inplace = True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    dat_diff.plot(ax = ax1)
    plot_acf(dat_diff['value'], ax = ax2)
    plt.show();



    계절 차분 결과, 일반 추세는 제거되지 않는 것으로 보임
    dat_diff2 = dat_diff.diff()
    dat_diff2.dropna(inplace = True)

    dat_diff2.plot()
    plt.show();



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,6))
    plot_acf(dat_diff2['value'], ax = ax1)
    plot_pacf(dat_diff2['value'], ax = ax2)
    plt.show();



    계절 차분과 일반 차분을 진행했을 때, 추세가 제거된 것을 볼 수 있음

    정상성을 대체로 만족하므로, 차수 인식

    계절 차수는 분기별 데이터이므로 4차수에서 모형 인식



    from statsmodels.tsa.arima.model import ARIMA
    model1 = ARIMA(dat, order=(0,1,1), seasonal_order=(0, 1, 1, 4)).fit()
    model2 = ARIMA(dat, order=(1,1,0), seasonal_order=(1, 1, 0, 4)).fit()

    model3 = pm.auto_arima(dat, 
                       start_p=0, 
                       start_q=0,
                       max_p=5, 
                       max_q=5,
                       m=4,             
                       d=1,          
                       seasonal=True,   
                       start_P=0, 
                       D=1, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    Performing stepwise search to minimize aic
     ARIMA(0,1,0)(0,1,1)[4]             : AIC=80.001, Time=0.02 sec
     ARIMA(0,1,0)(0,1,0)[4]             : AIC=95.204, Time=0.01 sec
     ARIMA(1,1,0)(1,1,0)[4]             : AIC=76.594, Time=0.02 sec
     ARIMA(0,1,1)(0,1,1)[4]             : AIC=75.360, Time=0.02 sec
     ARIMA(0,1,1)(0,1,0)[4]             : AIC=93.962, Time=0.01 sec
     ARIMA(0,1,1)(1,1,1)[4]             : AIC=77.351, Time=0.03 sec
     ARIMA(0,1,1)(0,1,2)[4]             : AIC=77.354, Time=0.06 sec
     ARIMA(0,1,1)(1,1,0)[4]             : AIC=80.370, Time=0.02 sec
     ARIMA(0,1,1)(1,1,2)[4]             : AIC=78.106, Time=0.11 sec
     ARIMA(1,1,1)(0,1,1)[4]             : AIC=inf, Time=0.05 sec
     ARIMA(0,1,2)(0,1,1)[4]             : AIC=73.618, Time=0.03 sec
     ARIMA(0,1,2)(0,1,0)[4]             : AIC=83.698, Time=0.02 sec
     ARIMA(0,1,2)(1,1,1)[4]             : AIC=75.419, Time=0.04 sec
     ARIMA(0,1,2)(0,1,2)[4]             : AIC=75.505, Time=0.05 sec
     ARIMA(0,1,2)(1,1,0)[4]             : AIC=78.682, Time=0.03 sec
     ARIMA(0,1,2)(1,1,2)[4]             : AIC=76.339, Time=0.12 sec
     ARIMA(1,1,2)(0,1,1)[4]             : AIC=69.378, Time=0.04 sec
     ARIMA(1,1,2)(0,1,0)[4]             : AIC=83.142, Time=0.02 sec
     ARIMA(1,1,2)(1,1,1)[4]             : AIC=71.355, Time=0.07 sec
     ARIMA(1,1,2)(0,1,2)[4]             : AIC=71.364, Time=0.08 sec
     ARIMA(1,1,2)(1,1,0)[4]             : AIC=75.616, Time=0.04 sec
     ARIMA(1,1,2)(1,1,2)[4]             : AIC=71.600, Time=0.16 sec
     ARIMA(2,1,2)(0,1,1)[4]             : AIC=70.723, Time=0.10 sec
     ARIMA(1,1,3)(0,1,1)[4]             : AIC=69.280, Time=0.06 sec
     ARIMA(1,1,3)(0,1,0)[4]             : AIC=inf, Time=0.10 sec
     ARIMA(1,1,3)(1,1,1)[4]             : AIC=inf, Time=0.14 sec
     ARIMA(1,1,3)(0,1,2)[4]             : AIC=70.929, Time=0.09 sec
     ARIMA(1,1,3)(1,1,0)[4]             : AIC=inf, Time=0.12 sec
     ARIMA(1,1,3)(1,1,2)[4]             : AIC=72.460, Time=0.18 sec
     ARIMA(0,1,3)(0,1,1)[4]             : AIC=67.401, Time=0.04 sec
     ARIMA(0,1,3)(0,1,0)[4]             : AIC=76.397, Time=0.03 sec
     ARIMA(0,1,3)(1,1,1)[4]             : AIC=68.410, Time=0.09 sec
     ARIMA(0,1,3)(0,1,2)[4]             : AIC=68.931, Time=0.06 sec
     ARIMA(0,1,3)(1,1,0)[4]             : AIC=71.228, Time=0.04 sec
     ARIMA(0,1,3)(1,1,2)[4]             : AIC=inf, Time=0.19 sec
     ARIMA(0,1,3)(0,1,1)[4] intercept   : AIC=inf, Time=0.13 sec

    Best model:  ARIMA(0,1,3)(0,1,1)[4]          
    Total fit time: 2.437 seconds
    model1.aic

    75.36042692171594
    model2.aic

    76.59401009669251
    model3.aic()

    67.40137406098646
    모든 모수 유의
    model3.summary()

    SARIMAX Results
    Dep. Variable:	y	No. Observations:	64
    Model:	SARIMAX(0, 1, 3)x(0, 1, [1], 4)	Log Likelihood	-28.701
    Date:	Wed, 01 Nov 2023	AIC	67.401
    Time:	22:47:58	BIC	77.789
    Sample:	01-01-1996	HQIC	71.456
    - 10-01-2011		
    Covariance Type:	opg		
    coef	std err	z	P>|z|	[0.025	0.975]
    ma.L1	0.2625	0.128	2.046	0.041	0.011	0.514
    ma.L2	0.3697	0.113	3.257	0.001	0.147	0.592
    ma.L3	0.4194	0.128	3.270	0.001	0.168	0.671
    ma.S.L4	-0.6614	0.159	-4.170	0.000	-0.972	-0.351
    sigma2	0.1451	0.029	4.997	0.000	0.088	0.202
    Ljung-Box (L1) (Q):	0.01	Jarque-Bera (JB):	0.45
    Prob(Q):	0.94	Prob(JB):	0.80
    Heteroskedasticity (H):	0.55	Skew:	0.16
    Prob(H) (two-sided):	0.19	Kurtosis:	3.28

    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    모형 검진

    모형 가정 만족(답안 작성은 기출 예시 참고)
    sm.stats.acorr_ljungbox(model3.resid(), lags=[12])

          lb_stat  lb_pvalue
    12  11.635575   0.475373
    model3.plot_diagnostics()
    plt.show();



    모형 가정 만족(답안 작성은 기출 예시 참고)
    dat.index = pd.to_datetime(dat.index) # index 날짜형으로 변환

    prediction, confint = model3.predict(n_periods = 12, return_conf_int = True)
    cf = pd.DataFrame(confint)
    prediction_series = pd.Series(prediction)

    fig, ax = plt.subplots(1, 1, figsize = (15, 5))
    ax.plot(dat.value)
    ax.plot(prediction_series)
    ax.fill_between(prediction_series.index,
                    cf[0],
                    cf[1], color = 'grey',alpha = .3)
    # ax.set_xticks(np.arange(0, total_len + 1, 10))
    plt.show();



    """
