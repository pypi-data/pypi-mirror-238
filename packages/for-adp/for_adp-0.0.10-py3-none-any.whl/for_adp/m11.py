def m11():
    """
    11  일반화선형모형(Generalized Linear Model)
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    왜 “일반화” 선형 모형인가?

    반응변수의 분포가 정규분포가 아닌 데이터에 대해 모델링하기 위해 모형을 확장했으므로, “일반화” 선형 모형이라고 함

    일반화선형모형 안에는 다중회귀모형도 포함됨

    ex) 특정 실험의 성공 여부, 특정 도로를 이용하는 자동차 대수(count data), 0 과잉 데이터 etc..

    일반화선형모형은 총 세 가지로 규정됨

    random component
    반응변수에 대한 확률분포를 규정함

    반응변수의 분포가 지수분포족(분포의 집합군)에 속한다고 가정

    우리가 들어본 분포는 다 지수분포족..
    systematic component
    설명변수를 선형 예측식으로 규정함 —> 
    link function

    random component와 systematic component와의 함수관계를 표현

    link function의 형태는 지수분포족의 일반식에서 유도할 수 있음
    ink function은 범위만 동일하면 다른 함수도 가능, 일반적으로 많이 쓰는 link function은 정해져있음
    Random component	Link	Model
    normal	identity	linear regression
    poisson	log	poisson regression
    negative binomial	log	negative binomial regression
    …etc	…etc	…etc
    11.1 Model
    11.1.1 단순선형회귀

    random component : 
    의 분포가 정규분포(
    )

    systematic component : 

    link function : 

    11.1.2 로지스틱회귀


    random component : 
    의 분포가 이항분포, 

    systematic component : 

    link function : 


    11.1.3 포아송 회귀

    random component : 
    의 분포가 포아송분포, 

    systematic component : 

    link function : 

    과대산포(over dispersion) 되어 있지 않은 count data에 적용 가능한 모형

    과대산포 : 분산이 평균에 비해 크게 나타나는 현상

    과대산포가 존재할 경우 poisson regression 추정량의 SE에 영향을 줌


    , se값이 커짐에 따라 검정통계량 값이 커지고, H0 쉽게 기각

    11.1.4 음이항 회귀모형
    random component : 
    의 분포가 음이항 분포

    systematic component : 

    link function : 

    과대산포가 존재할 경우 대안모형으로 음이항회귀 고려

    포아송 분포의 분산은 평균의 함수이므로, 파라미터를 추가해서 통제

    분산을 통제할 수 있는 모수가 있는 음이항분포 고려

    11.1.5 특수한 일반화선형모형
    zero inflated model

    zero inflation : 가정된 분포에 비해 0값이 많은 경우

    zero inflation을 반영할 수 있는 모형 필요

    zero-inflated poisson model

    zero inflation을 고려한 poisson 모형
    zero-inflated negative binomial model

    zero-inflation과 over dispersion을 동시에 고려한 모형
    11.2 Example
    colab link : https://colab.research.google.com/drive/1h2z39FcpoR8Mn5pnN7pqKw4dzRRelnzp?usp=sharing

    import pandas as pd
    import numpy as np
    import time
    from datetime import datetime
    from sklearn.preprocessing import KBinsDiscretizer
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GridSearchCV, KFold
    from sklearn import set_config
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import BaggingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score
    import matplotlib.pyplot as plt
    import seaborn as sns

    dat = pd.read_csv('./data/ex_data/bikesharingdata/train2.csv')
    y = dat['count']
    X = dat.drop(['count'], axis = 1)

    dat = dat.astype({'datetime' : 'datetime64[ns]', 'weather' : 'int64', 'season' : 'object', 'workingday' : 'object', 'holiday' : 'object'})
    dat['year'] = dat['datetime'].dt.year
    dat['month'] = dat['datetime'].dt.month
    dat['day'] = dat['datetime'].dt.day
    dat['wday'] = dat['datetime'].dt.day_name()
    dat['hour'] = dat['datetime'].dt.hour
    dat = dat.drop(['datetime'], axis = 1)

    freq = dat['weather'].value_counts(normalize = True)
    prob_columns = dat['weather'].map(freq)
    dat['weather'] = dat['weather'].mask(prob_columns < 0.1, '3')
    dat['weather'].value_counts()

    weather
    1    7192
    2    2834
    3     860
    Name: count, dtype: int64

    dat['weather'] = dat['weather'].astype(int)

    num_columns = dat.select_dtypes('number').columns.tolist()
    cat_columns = dat.select_dtypes('object').columns.tolist()
    num_columns.remove('count')

    cat_preprocess = make_pipeline(
        #SimpleImputer(strategy="constant", fill_value="NA"),
        OneHotEncoder(handle_unknown="error", sparse=False, drop = 'first')
    )

    num_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5),
        StandardScaler()
    )

    preprocess = ColumnTransformer(
        [("num", num_preprocess, num_columns),
        ("cat", cat_preprocess, cat_columns)],
        remainder='passthrough'
    )

    pre_dat = preprocess.fit_transform(dat)

    cat_encoder = preprocess.named_transformers_["cat"]["onehotencoder"]
    cat_names = list(cat_encoder.get_feature_names())
    full_name = num_columns + cat_names + ['count']
    dat = pd.DataFrame(pre_dat, columns = full_name)

    y = dat['count']
    X = dat.drop(['count'], axis = 1)

    bins = np.nanquantile(y, np.arange(0, 1, 0.1))
    y_binned = np.digitize(y, bins)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = y_binned, random_state = 0)

    train_y = train_y.astype(int)
    test_y = test_y.astype(int)

    np.mean(train_y)

    191.31637574644006
    np.var(train_y)

    32702.739708867543
    np.min(train_y)

    1
    11.2.1 Poisson regression
    poisson regression의 경우 sklearn에서 지원합니다. 다만 sklearn의 경우 summary table option을 지원하지 않습니다. 따라서 예측이 아닌 추론이 목적이라면 statsmodels 패키지를 이용하는 것이 바람직합니다.

    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    exog = sm.add_constant(train_X)
    poission_model = sm.GLM(train_y, exog, family=sm.families.Poisson())
    result = poission_model.fit()
    result.summary()

    Generalized Linear Model Regression Results
    Dep. Variable:	count	No. Observations:	8708
    Model:	GLM	Df Residuals:	8686
    Model Family:	Poisson	Df Model:	21
    Link Function:	Log	Scale:	1.0000
    Method:	IRLS	Log-Likelihood:	-1.5700e+05
    Date:	Mon, 30 Oct 2023	Deviance:	2.5828e+05
    Time:	01:06:20	Pearson chi2:	2.16e+05
    No. Iterations:	9	Pseudo R-squ. (CS):	1.000
    Covariance Type:	nonrobust		
    coef	std err	z	P>|z|	[0.025	0.975]
    const	4.0180	0.004	971.032	0.000	4.010	4.026
    weather	0.0011	0.001	1.113	0.266	-0.001	0.003
    temp	-0.0312	0.004	-7.269	0.000	-0.040	-0.023
    atemp	0.0962	0.004	23.240	0.000	0.088	0.104
    humidity	-0.0336	0.001	-31.374	0.000	-0.036	-0.031
    windspeed	0.0124	0.001	15.118	0.000	0.011	0.014
    casual	0.1775	0.001	195.844	0.000	0.176	0.179
    registered	0.4833	0.001	650.658	0.000	0.482	0.485
    year	0.0013	0.001	1.444	0.149	-0.000	0.003
    month	0.0742	0.003	22.274	0.000	0.068	0.081
    day	-0.0012	0.001	-1.494	0.135	-0.003	0.000
    hour	0.1742	0.001	168.225	0.000	0.172	0.176
    x0_2	-0.0089	0.004	-2.135	0.033	-0.017	-0.001
    x0_3	-0.0965	0.007	-14.367	0.000	-0.110	-0.083
    x0_4	-0.0458	0.009	-5.211	0.000	-0.063	-0.029
    x1_1	1.0618	0.005	231.957	0.000	1.053	1.071
    x2_1	1.0082	0.002	472.605	0.000	1.004	1.012
    x3_Monday	-0.0535	0.003	-17.839	0.000	-0.059	-0.048
    x3_Saturday	0.9589	0.002	401.479	0.000	0.954	0.964
    x3_Sunday	0.9892	0.002	419.960	0.000	0.985	0.994
    x3_Thursday	-0.0463	0.003	-15.982	0.000	-0.052	-0.041
    x3_Tuesday	-0.0702	0.003	-23.914	0.000	-0.076	-0.064
    x3_Wednesday	-0.0891	0.003	-30.332	0.000	-0.095	-0.083
    log_result = pd.DataFrame(
        {
            "OR": result.params,
            "Lower CI": result.conf_int()[0],
            "Upper CI": result.conf_int()[1],
        }
    )
    exp_result = np.exp(log_result)

    print(exp_result)

                         OR   Lower CI   Upper CI
    const         55.591941  55.142905  56.044633
    weather        1.001059   0.999195   1.002926
    temp           0.969255   0.961128   0.977451
    atemp          1.100966   1.092071   1.109933
    humidity       0.966961   0.964934   0.968993
    windspeed      1.012518   1.010886   1.014152
    casual         1.194242   1.192122   1.196366
    registered     1.621409   1.619050   1.623771
    year           1.001286   0.999541   1.003035
    month          1.077058   1.070045   1.084116
    day            0.998829   0.997294   1.000366
    hour           1.190325   1.187912   1.192744
    x0_2           0.991179   0.983149   0.999275
    x0_3           0.908022   0.896148   0.920052
    x0_4           0.955251   0.938943   0.971843
    x1_1           2.891697   2.865868   2.917758
    x2_1           2.740532   2.729098   2.752014
    x3_Monday      0.947909   0.942353   0.953497
    x3_Saturday    2.608759   2.596576   2.621000
    x3_Sunday      2.688996   2.676611   2.701439
    x3_Thursday    0.954760   0.949355   0.960196
    x3_Tuesday     0.932170   0.926819   0.937551
    x3_Wednesday   0.914715   0.909461   0.919999
    exog2 = sm.add_constant(test_X)
    ypred = result.predict(exog2)

    from sklearn.metrics import mean_squared_error
    print('RMSE : ', np.sqrt(mean_squared_error(ypred, test_y)))

    RMSE :  90.89929658535766
    11.2.2 Negative binomial regression
    계수 해석은 poisson과 같이 link function이 log() 일 경우 
     취해서 해석
    exog = sm.add_constant(train_X)
    negbin_model = sm.GLM(train_y, exog, family=sm.families.NegativeBinomial())
    result2 = negbin_model.fit()
    result2.summary()

    Generalized Linear Model Regression Results
    Dep. Variable:	count	No. Observations:	8708
    Model:	GLM	Df Residuals:	8686
    Model Family:	NegativeBinomial	Df Model:	21
    Link Function:	Log	Scale:	1.0000
    Method:	IRLS	Log-Likelihood:	-50319.
    Date:	Mon, 30 Oct 2023	Deviance:	3578.6
    Time:	01:06:22	Pearson chi2:	2.32e+03
    No. Iterations:	100	Pseudo R-squ. (CS):	0.6156
    Covariance Type:	nonrobust		
    coef	std err	z	P>|z|	[0.025	0.975]
    const	3.9108	0.057	69.113	0.000	3.800	4.022
    weather	0.0172	0.012	1.412	0.158	-0.007	0.041
    temp	0.0390	0.070	0.554	0.580	-0.099	0.177
    atemp	0.0566	0.067	0.843	0.399	-0.075	0.188
    humidity	-0.0678	0.014	-4.724	0.000	-0.096	-0.040
    windspeed	0.0123	0.012	1.046	0.296	-0.011	0.035
    casual	0.1813	0.016	11.248	0.000	0.150	0.213
    registered	0.8544	0.014	59.258	0.000	0.826	0.883
    year	-0.0045	0.011	-0.398	0.690	-0.027	0.018
    month	0.0553	0.046	1.194	0.232	-0.035	0.146
    day	0.0009	0.011	0.085	0.932	-0.020	0.022
    hour	0.2834	0.012	23.215	0.000	0.260	0.307
    x0_2	-0.0291	0.055	-0.530	0.596	-0.137	0.079
    x0_3	-0.0957	0.092	-1.034	0.301	-0.277	0.086
    x0_4	-0.0472	0.124	-0.381	0.704	-0.290	0.196
    x1_1	1.0225	0.061	16.636	0.000	0.902	1.143
    x2_1	0.9332	0.028	33.419	0.000	0.878	0.988
    x3_Monday	-0.0599	0.042	-1.434	0.151	-0.142	0.022
    x3_Saturday	0.9639	0.032	30.232	0.000	0.901	1.026
    x3_Sunday	0.9912	0.032	31.078	0.000	0.929	1.054
    x3_Thursday	-0.0570	0.041	-1.394	0.163	-0.137	0.023
    x3_Tuesday	-0.0938	0.041	-2.286	0.022	-0.174	-0.013
    x3_Wednesday	-0.0885	0.041	-2.170	0.030	-0.168	-0.009
    exog2 = sm.add_constant(test_X)
    ypred = result2.predict(exog2)
    from sklearn.metrics import mean_squared_error
    print('RMSE : ', np.sqrt(mean_squared_error(ypred, test_y)))

    RMSE :  613.9017403642823
    11.2.3 Zero-inflated poisson model
    알고리즘 수렴성의 문제가 발생할 경우

    fit(max_iter = 1000, method=‘nm’)
    iteration 횟수 추가, 학습 방법 변경
    fit_regularized() : penalty term 추가
    train_y = train_y - 1 # 0부터 시작하도록
    test_y = test_y - 1

    exog = sm.add_constant(train_X)
    result3 = sm.ZeroInflatedPoisson(endog=train_y, exog=exog, inflation='logit').fit(max_iter = 1000, method='nm')

    Warning: Maximum number of iterations has been exceeded.
    result3.summary()

    ZeroInflatedPoisson Regression Results
    Dep. Variable:	count	No. Observations:	8708
    Model:	ZeroInflatedPoisson	Df Residuals:	8686
    Method:	MLE	Df Model:	21
    Date:	Mon, 30 Oct 2023	Pseudo R-squ.:	-0.001449
    Time:	01:06:22	Log-Likelihood:	-7.3883e+05
    converged:	False	LL-Null:	-7.3777e+05
    Covariance Type:	nonrobust	LLR p-value:	1.000
    coef	std err	z	P>|z|	[0.025	0.975]
    inflate_const	0.0972	0.021	4.530	0.000	0.055	0.139
    const	5.2574	1.59e+04	0.000	1.000	-3.12e+04	3.12e+04
    weather	0.0010	0.001	1.195	0.232	-0.001	0.003
    temp	0.0010	0.005	0.205	0.837	-0.009	0.011
    atemp	0.0010	0.005	0.215	0.830	-0.008	0.010
    humidity	0.0009	0.001	0.907	0.365	-0.001	0.003
    windspeed	0.0010	0.001	1.204	0.229	-0.001	0.003
    casual	0.0011	0.001	0.913	0.361	-0.001	0.003
    registered	0.0011	0.001	1.036	0.300	-0.001	0.003
    year	0.0010	0.001	1.265	0.206	-0.001	0.003
    month	0.0010	0.003	0.308	0.758	-0.006	0.008
    day	0.0010	0.001	1.255	0.210	-0.001	0.003
    hour	0.0010	0.001	1.186	0.236	-0.001	0.003
    x0_2	0.0010	0.004	0.256	0.798	-0.007	0.009
    x0_3	0.0010	0.007	0.153	0.878	-0.012	0.014
    x0_4	0.0010	0.009	0.112	0.911	-0.016	0.018
    x1_1	0.0009	1.59e+04	5.97e-08	1.000	-3.12e+04	3.12e+04
    x2_1	0.0010	1.59e+04	6.21e-08	1.000	-3.12e+04	3.12e+04
    x3_Monday	0.0009	0.003	0.315	0.753	-0.005	0.007
    x3_Saturday	0.0010	1.59e+04	6.23e-08	1.000	-3.12e+04	3.12e+04
    x3_Sunday	0.0010	1.59e+04	6.11e-08	1.000	-3.12e+04	3.12e+04
    x3_Thursday	0.0010	0.003	0.335	0.738	-0.005	0.007
    x3_Tuesday	0.0010	0.003	0.326	0.744	-0.005	0.007
    x3_Wednesday	0.0011	0.003	0.361	0.718	-0.005	0.007
    exog3 = sm.add_constant(test_X)
    ypred = result3.predict(exog3)
    from sklearn.metrics import mean_squared_error
    print('RMSE : ', np.sqrt(mean_squared_error(ypred, test_y)))

    RMSE :  207.7052046594193
    11.2.4 Zero-inflated negative binomial model
    exog = sm.add_constant(train_X)
    result4 = sm.ZeroInflatedNegativeBinomialP(endog=train_y, exog=exog, inflation='logit').fit_regularized()

    Optimization terminated successfully    (Exit mode 0)
                Current function value: 5.581333364459855
                Iterations: 40
                Function evaluations: 43
                Gradient evaluations: 40
    result4.summary()

    ZeroInflatedNegativeBinomialP Regression Results
    Dep. Variable:	count	No. Observations:	8708
    Model:	ZeroInflatedNegativeBinomialP	Df Residuals:	8685
    Method:	MLE	Df Model:	22
    Date:	Mon, 30 Oct 2023	Pseudo R-squ.:	0.1050
    Time:	01:06:24	Log-Likelihood:	-48602.
    converged:	True	LL-Null:	-54303.
    Covariance Type:	nonrobust	LLR p-value:	0.000
    coef	std err	z	P>|z|	[0.025	0.975]
    inflate_const	-4.8282	0.131	-36.981	0.000	-5.084	-4.572
    const	4.1904	28.023	0.150	0.881	-50.734	59.115
    weather	0.0176	0.008	2.337	0.019	0.003	0.032
    temp	0.0315	0.043	0.733	0.464	-0.053	0.116
    atemp	0.0545	0.041	1.329	0.184	-0.026	0.135
    humidity	-0.0684	0.009	-7.808	0.000	-0.086	-0.051
    windspeed	0.0137	0.007	1.922	0.055	-0.000	0.028
    casual	0.1889	0.011	17.650	0.000	0.168	0.210
    registered	0.8461	0.011	79.301	0.000	0.825	0.867
    year	-0.0080	0.007	-1.174	0.240	-0.021	0.005
    month	0.0539	0.028	1.917	0.055	-0.001	0.109
    day	0.0001	0.007	0.019	0.985	-0.013	0.013
    hour	0.2768	0.008	35.552	0.000	0.262	0.292
    x0_2	-0.0354	0.033	-1.063	0.288	-0.101	0.030
    x0_3	-0.0952	0.056	-1.696	0.090	-0.205	0.015
    x0_4	-0.0555	0.075	-0.737	0.461	-0.203	0.092
    x1_1	0.7344	28.023	0.026	0.979	-54.189	55.658
    x2_1	0.6567	28.023	0.023	0.981	-54.267	55.580
    x3_Monday	-0.0571	0.025	-2.264	0.024	-0.107	-0.008
    x3_Saturday	0.6767	28.023	0.024	0.981	-54.247	55.600
    x3_Sunday	0.7061	28.023	0.025	0.980	-54.217	55.630
    x3_Thursday	-0.0555	0.025	-2.253	0.024	-0.104	-0.007
    x3_Tuesday	-0.0919	0.025	-3.712	0.000	-0.140	-0.043
    x3_Wednesday	-0.0863	0.025	-3.503	0.000	-0.135	-0.038
    alpha	0.3532	0.006	60.186	0.000	0.342	0.365
    exog4 = sm.add_constant(test_X)
    ypred = result4.predict(exog4)
    from sklearn.metrics import mean_squared_error
    print('RMSE : ', np.sqrt(mean_squared_error(ypred, test_y)))

    RMSE :  581.4325747121763
    """