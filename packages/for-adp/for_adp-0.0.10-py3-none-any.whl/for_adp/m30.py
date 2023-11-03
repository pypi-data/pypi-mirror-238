def m30():
    """
    ADP python 기출문제
    28  30회차 기출문제
    28  30회차 기출문제
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    28.1 문제 1
    Data description

    age : 나이

    gender : 성별

    bmi : bmi 수치

    fpg : 공복 혈당

    chol : 총 콜레스테롤

    tri : 트리글리세라이드

    hdl : HDL 콜레스테롤

    ldl : LDL 콜레스테롤

    alt : (혈청지오티) ALT

    dbp : 이완기 혈압

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    # import time

    dat = pd.read_csv('data/adp30_1.csv')

    dat.head(3)

       Age  Gender   BMI  DBP  FPG  Chol   Tri   HDL   LDL   ALT
    0   26       1  20.1   81  5.8  4.36  0.86  0.90  2.43  12.0
    1   40       1  17.7   54  4.6  3.70  1.02  1.50  2.04   9.2
    2   40       2  19.7   53  5.3  5.87  1.29  1.75  3.37  10.1
    dat = dat.clean_names()

    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4303 entries, 0 to 4302
    Data columns (total 10 columns):
     #   Column  Non-Null Count  Dtype  
    ---  ------  --------------  -----  
     0   age     4303 non-null   int64  
     1   gender  4303 non-null   int64  
     2   bmi     4303 non-null   float64
     3   dbp     4303 non-null   int64  
     4   fpg     4303 non-null   float64
     5   chol    4302 non-null   float64
     6   tri     4303 non-null   float64
     7   hdl     4303 non-null   float64
     8   ldl     4303 non-null   float64
     9   alt     4303 non-null   float64
    dtypes: float64(7), int64(3)
    memory usage: 336.3 KB
    dat = dat.astype({'gender' : 'object'})

    28.2 EDA를 수행하시오.
    dat.hist();
    plt.tight_layout();
    plt.show();



    corr = dat.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True);
    plt.tight_layout()
    plt.show();



    sns.countplot(dat['gender'])
    plt.show();



    28.3 데이터 전처리가 필요하다면 수행하고 이유를 작성하시오.
    chol 변수에 결측치가 1개 존재한다. 따라서 적절한 결측치 대치 방법을 통해 결측치를 대치해야 한다.

    dat.isna().sum()

    age       0
    gender    0
    bmi       0
    dbp       0
    fpg       0
    chol      1
    tri       0
    hdl       0
    ldl       0
    alt       0
    dtype: int64
    bagged tree를 이용해서 결측치를 대치함
    결측치를 처리하는 방법은 크게 대표값을 이용하는 방법과 모델을 이용하는 방법이 있다. 대표값을 이용한 방법 중 대표적으로 평균대치법이 있다. 평균대치법은 해당 변수의 대표값인 평균으로 결측치를 대치하는 방법으로 단점으로는 결측치 수가 많을 때 분포가 왜곡되는 문제가 있을 수 있다. 모델을 이용한 방법 중 대표적으로 bagged tree를 이용한 방법이 있다. bagged tree를 이용한 방법은 boostrap sample에서 개별 tree를 생성하고, 개별 tree에서 나온 예측값을 평균내서 나온 값을 이용해서 결측치를 대치하는 방법이다. bagged tree를 이용해서 결측치를 대치한 이유는 대표값을 이용하는 방법에 비해서 다른 변수의 정보를 이용해서 결측치를 대치할 수 있기 때문에 더 많은 정보를 활용해서 결측치를 대치할 수 있기 때문이다.

    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn import set_config
    set_config(display="diagram")

    num_columns = dat.select_dtypes('number').columns
    cat_columns = dat.select_dtypes('object').columns

    impute_preprocess = make_pipeline(
        IterativeImputer(estimator = RandomForestRegressor(), max_iter = 5)
    )

    preprocess = ColumnTransformer(
        [("imputation", impute_preprocess, num_columns)]
    )

    preprocess

    ColumnTransformer
    imputation
    iterativeimputer: IterativeImputer

    RandomForestRegressor
    impute_dat = preprocess.fit_transform(dat)
    num_data = pd.DataFrame(impute_dat, columns = num_columns)
    num_data.isna().sum()

    age     0
    bmi     0
    dbp     0
    fpg     0
    chol    0
    tri     0
    hdl     0
    ldl     0
    alt     0
    dtype: int64
    28.4 train test set을 DBP 컬럼 기준으로 7:3 비율로 나눈 후 잘 나뉘었는지 통계적으로 나타내시오.
    y = dat.dbp
    X = dat.drop(['dbp'], axis = 1)

    from sklearn.model_selection import train_test_split
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.3, random_state = 0)

    print('train 데이터 :', len(train_X), 'test 데이터 :', len(test_X))

    train 데이터 : 3012 test 데이터 : 1291
    데이터를 분할하는 방법은 대표적으로 simple random sampling, strata sampling이 있다. 첫 번째로, simple random sampling은 데이터를 무작위로 특정 비율로 분할하는 방법이다. 두 번째로, strata sampling은 class 불균형 문제에 대한 해결 방안으로 지정된 범주형 변수의 각 class에 해당하는 하위 샘플에 별도로 simple random sampling을 통해서 데이터를 분할하고, 이후 결합하는 방식으로 전체 데이터셋을 분할하는 방법이다. strata sampling은 연속형 변수의 경우 quantile을 기준으로 비닝을 함으로써 범주형 변수에서 시행하는 것과 같은 방식으로 진행된다.

    f, axes = plt.subplots(ncols = 2, nrows = 1, figsize = (20,4))
    train_y.hist(ax = axes[0]);
    test_y.hist(ax = axes[1]);
    plt.show()



    dbp 변수에 대해 랜덤샘플링을 적용한 결과 train/test 분포 거의 유사한 형태이며, 정규분포 형태를 띈다.

    그래프를 통해 확인했지만, dbp 변수에 대해서 train/test 분포가 같은지 통계적으로 검정해보고자 한다. 두 분포의 유사성을 검정하는 방법은 k-s test를 활용해볼 수 있다.

    from scipy import stats
    stats.ks_2samp(train_y, test_y)

    KstestResult(statistic=0.023643098661383383, pvalue=0.6816496818864761)
    유의수준 5%에서 p-value = 0.6816이므로, 귀무가설을 기각할 수 없다. 따라서 dbp의 train/test 분포는 통계적으로 동일한 분포하고 볼 수 있다.

    num_col = train_X.select_dtypes('number').columns
    result = pd.DataFrame()

    for i in range(len(num_col)):

        sample1 = train_X.loc[:, num_col[i]]
        sample2 = test_X.loc[:, num_col[i]]
        p_value = stats.ks_2samp(sample1, sample2).pvalue

        tt = pd.DataFrame({'var_name' :  num_col[i], 'P_value' : p_value}, index = [0])
        result = result._append(tt)

    result    

      var_name   P_value
    0      age  0.423309
    0      bmi  0.321328
    0      fpg  0.693973
    0     chol  0.558922
    0      tri  0.133578
    0      hdl  0.316333
    0      ldl  0.520403
    0      alt  0.268237
    설명변수에 대해서 k-s test를 동일하게 진행해본 결과 유의수준 5%에서 p-value = 0.1 ~ 0.7이므로, 귀무가설을 기각할 수 없다. 따라서 train/test 분포는 통계적으로 동일한 분포하고 볼 수 있다.

    28.5 독립변수의 차원축소의 필요성을 논하고, 필요에 따라 차원을 축소하고 불필요하다면 그 근거를 논하시오.
    차원 축소는 고려하지 않는다.
    변수 간 상관관계가 높은 고차원 데이터의 경우 모델 학습 시 과적합될 가능성이 있으며, 계산량이 많아져 모델 효율성이 떨어질 수 있다. 변수 간 상관관계가 높다는 의미는 변수 간 중복되는 정보가 있다는 의미로도 볼 수 있으므로, 적절한 차원 축소 기법을 통해 과적합을 방지하고 모델의 계산 효율성을 확보하는 것이 합리적일 수 있다. EDA 과정에서 살펴본 상관계수 그래프를 보면 변수 개수가 많지 않고, 변수 간 상관관계가 높지 않으므로, 차원 축소 고려하지 않는다.

    28.6 데이터가 회귀분석의 기본가정 따르는지 설명하시오.
    오차항 평균 0, 등분산

    오차의 분포는 정규분포

    오차항은 서로 독립

    반응변수와 설명변수 관계는 선형

    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    all_X_columns = train_X.columns.to_list()
    cols_str = " + ".join(all_X_columns)
    train = pd.concat([train_X, train_y], axis = 1)

    lm_model = smf.ols(formula = f"dbp ~ {cols_str}", data = train).fit()
    print(lm_model.summary())

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                    dbp   R-squared:                       0.161
    Model:                            OLS   Adj. R-squared:                  0.158
    Method:                 Least Squares   F-statistic:                     63.81
    Date:                Mon, 30 Oct 2023   Prob (F-statistic):          1.47e-107
    Time:                        23:58:56   Log-Likelihood:                -11229.
    No. Observations:                3012   AIC:                         2.248e+04
    Df Residuals:                    3002   BIC:                         2.254e+04
    Df Model:                           9                                         
    Covariance Type:            nonrobust                                         
    ===============================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
    -------------------------------------------------------------------------------
    Intercept      49.6349      1.898     26.150      0.000      45.913      53.357
    gender[T.2]    -3.1685      0.413     -7.680      0.000      -3.977      -2.360
    age             0.1205      0.014      8.380      0.000       0.092       0.149
    bmi             0.6622      0.062     10.597      0.000       0.540       0.785
    fpg             0.3772      0.266      1.418      0.156      -0.144       0.899
    chol            0.5084      0.335      1.517      0.129      -0.149       1.166
    tri             0.4682      0.173      2.707      0.007       0.129       0.807
    hdl            -0.1217      0.279     -0.437      0.662      -0.668       0.425
    ldl             0.2411      0.446      0.541      0.589      -0.633       1.116
    alt             0.0155      0.009      1.791      0.073      -0.001       0.033
    ==============================================================================
    Omnibus:                      122.638   Durbin-Watson:                   1.997
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):              167.866
    Skew:                           0.406   Prob(JB):                     3.54e-37
    Kurtosis:                       3.823   Cond. No.                         655.
    ==============================================================================

    Notes:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    기본 내용은 통계반에서 진행한 내용을 참고하시면 됩니다.
    잔차와 예측치(
    ) 의 산점도

    y_fit = lm_model.fittedvalues

    #  Plot
    sns.residplot(x=y_fit, y='dbp', data=train, lowess=True, 
                         scatter_kws={'alpha': 0.5}, 
                         line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plt.title('Residuals vs Fitted')
    plt.xlabel('Fitted Values')
    plt.ylabel('Residuals')
    plt.show();



    분산이 증가 or 감소하는 패턴이 없으므로, 등분산 가정을 만족한다. 또한 비선형 패턴이 없고, 0을 중심으로 무작위로 분포하는 형태이므로, 선형성 가정을 만족한다.

    QQ plot : 표준화잔차의 표본 분위수와 정규분포의 이론 분위수와의 산점도

    probplot = sm.ProbPlot(lm_model.get_influence().resid_studentized_internal, fit=True)
    fig = probplot.qqplot(line='45', color='black')
    plt.title('Normal Q-Q', fontsize=20)
    plt.show();



    양끝 꼬리 부분을 제외하면 대체로 직선 상에 위치해있으므로, 표준화잔차의 표본 분위수와 정규분포의 이론 분위수는 유사하다고 볼 수 있으며, 정규분포 가정을 만족한다.

    sns.regplot(lm_model.fittedvalues, 
               np.sqrt(np.abs(lm_model.get_influence().resid_studentized_internal)), 
                scatter=True, 
                ci=False, 
                lowess=True,
                line_kws={'color': 'blue', 'lw': 1, 'alpha': 0.8},
              scatter_kws={'facecolors':'none', 'edgecolors':'black'})

    plt.title('Scale-Location', fontsize=20)
    plt.xlabel('Fitted Values', fontsize=15)
    plt.ylabel('$\sqrt{|Standardized Residuals|}$', fontsize=15)
    plt.show();



    점들이 체계적으로 증가하거나 감소하는 패턴이 없으므로, 동일 분산 가정을 만족한다고 볼 수 있다.

    #sm.stats.durbin_watson(lm_model.resid)
    from statsmodels.stats.diagnostic import acorr_ljungbox
    ljbox_test = acorr_ljungbox(lm_model.resid, lags = [10])
    print(ljbox_test)

        lb_stat  lb_pvalue
    10  8.87988    0.54354
    ljung box test 결과 유의수준 0.05에서 Q* = 8.87, p-value = 0.54로 크기 때문에 귀무가설을 기각할 수 없다. 따라서 10시차까지 잔차 사이에 자기상관이 없다고 할 수 있다. 즉, 오차 사이에 자기상관이 없다는 가정을 만족한다.

    28.7 회귀분석 알고리즘 3개를 선택하고 선정이유와 장단점을 비교하시오.
    linear regression

    LASSO regression

    Random forest

    Linear regression 모형은 회귀계수에 대한 직관적인 해석이 용이한 장점이 있지만, 모형에 많은 가정이 있으며, 비선형 모형 대비 예측력이 떨어지는 단점이 있다.

    위 문제에서 linear regression의 가정 검토 결과 오차에 대한 가정을 만족하는 것을 볼 수 있다. Linear regression 모형을 타 모형과의 성능 비교를 위한 벤치마크 모형으로 활용하고자 한다.

    LASSO regression 모형은 제약식을 통해서 중요하지 않은 변수의 영향력을 감소시키는 특징이 있으며, 변수선택의 장점이 있다. 반면에 비선형 모형 대비 예측 성능이 떨어지는 단점이 있다.

    from patsy import dmatrices
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant
    y, X = dmatrices(f"dbp ~ {cols_str}", train, return_type='dataframe')

    vif = pd.DataFrame()
    vif["column_name"] = X.columns
    vif["vif_score"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif = vif.loc[vif.column_name != 'Intercept', :]
    vif.round(2)

       column_name  vif_score
    1  gender[T.2]       1.15
    2          age       1.30
    3          bmi       1.37
    4          fpg       1.29
    5         chol       2.88
    6          tri       1.35
    7          hdl       2.71
    8          ldl       4.66
    9          alt       1.21
    분산팽창계수를 확인해보면 ldl, chol변수의 vif > 2.5로 다중공선성이 존재하는 것을 확인할 수 있다. LASSO regression의 경우 제약식을 통해 중요하지 않은 변수의 영향력을 감소시킴에 따라 다중공선성의 효과를 완화할 수 있으므로, LASSO regression을 모형으로 활용하고자 한다.

    Random forest는 Bagging을 의사결정나무에 적용하여 의사결정나무의 단점인 예측력의 분산이 큰 단점을 보완한 모형이다. 또한 의사결정나무 생성시 변수 선택 기능을 추가하여, 개별 의사결정나무의 다양성을 확보하면서, 예측 성능을 높힌 모형이다. 단점은 boostrap sample 수에 따라서 모형 학습시 시간이 오래걸리는 문제가 있다. Ramdom forest의 경우 비선형모형이고, 사전에 설정한 모형 가정이 없으므로, Linear regression, LASSO regression 모형과의 성능 비교를 위해 활용하고자 한다.

    28.8 3개의 회귀 분석 모델링을 진행하고, 평가지표 rmse로 가장 최적화된 알고리즘 선정하시오.
    교차 검증 이용
    교차 검증 방법으로 5-fold 교차 검증 방법을 적용한다. 5-fold 교차 검증은 훈련 데이터를 임의의 거의 동일한 크기의 5개 그룹(fold)으로 나누는 리샘플링 방법이다.

    세부 방법은 다음과 같다.

    각 fold 중 
     fold는 validation셋으로 취급하고, 나머지 
    개의 fold는 훈련 데이터로 모델 적합에 이용

    이러한 절차는 
    번 반복되며, 매번 다른 그룹의 fold가 validation 셋으로 취급됨

    총 
     개의 추정치(ex. MSE)가 계산되며, 최종 CV 추정치는 
     개의 추정치를 평균내서 계산됨

    from sklearn.model_selection import GridSearchCV, KFold
    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)

    from sklearn.linear_model import LinearRegression, Lasso
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.model_selection import cross_val_score

    cat_columns = train_X.select_dtypes('object').columns.tolist()
    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer(
        [("cat", cat_preprocess, cat_columns)]
    )

    lm_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", LinearRegression())
        ]
    )

    lasso_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("scaler", StandardScaler()),
            ("regressor", Lasso())
        ]
    )

    rf_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", RandomForestRegressor(random_state=42))
        ]
    )

    lasso_param = {'regressor__alpha': np.arange(0.1, 1, 0.1)}
    RandomForest_param = {'regressor__max_features': np.arange(0.5, 1, 0.1)}

    cv_score = cross_val_score(lm_pipe, train_X, train_y, scoring='neg_root_mean_squared_error', cv = cv)
    rmse_score = np.absolute(cv_score)
    mean_rmse_score = np.mean(rmse_score)

    print('교차검증 RMSE score :', mean_rmse_score)

    교차검증 RMSE score : 10.762040736209396
    lasso_search = GridSearchCV(estimator = lasso_pipe, 
                          param_grid = lasso_param, 
                          cv = cv,
                          scoring = 'neg_root_mean_squared_error')
    lasso_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    cat

    OneHotEncoder

    StandardScaler

    Lasso
    print('best 파라미터 조합 :', lasso_search.best_params_)

    best 파라미터 조합 : {'regressor__alpha': 0.1}
    print('교차검증 RMSE score :', np.absolute(lasso_search.best_score_))

    교차검증 RMSE score : 10.759714738605052
    RandomForest_search = GridSearchCV(rf_pipe,
                                       RandomForest_param, 
                                       cv = cv,
                                       scoring = 'neg_root_mean_squared_error')
    RandomForest_search.fit(train_X, train_y)

    GridSearchCV
    preprocess: ColumnTransformer
    cat

    OneHotEncoder

    RandomForestRegressor
    print('best 파라미터 조합 :', RandomForest_search.best_params_)

    best 파라미터 조합 : {'regressor__max_features': 0.5}
    print('교차검증 RMSE score :', np.absolute(RandomForest_search.best_score_))

    교차검증 RMSE score : 10.758217155399965
    모델별로 RMSE score를 비교해보면 ramdom forest 모형의 성능이 우수한 것을 확인할 수 있다. 따라서 최종 모형으로 Random forest 모형을 선택한다.

    pred = RandomForest_search.predict(test_X)
    from sklearn.metrics import mean_squared_error
    mean_squared_error(pred, test_y, squared = False)

    10.905696789482892
    최종 검증 데이터에서의 성능은 10.90인 것을 확인할 수 있으며, 교차검증 스코어와 유사한 것을 확인할 수 있다.

    28.9 문제 2
    Tip
    한글 인코딩 이슈가 있을 경우 : read_csv 함수 이용(locale = locale('ko',encoding='CP949'로 설정)
    dat = pd.read_csv('data/adp30_2.csv')

    dat.head(2)

      사고내용 가해자성별 가해자연령 가해자차종 피해자신체상해정도        사고유형 기상상태  사망자수            발생시각
    0   경상     여   75세   자전거        경상    차대차 - 기타   맑음     0  2018-04-03 15시
    1   중상     여   26세   자전거        중상  차대차 - 측면충돌   맑음     0  2018-04-21 13시
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2410 entries, 0 to 2409
    Data columns (total 9 columns):
     #   Column     Non-Null Count  Dtype 
    ---  ------     --------------  ----- 
     0   사고내용       2410 non-null   object
     1   가해자성별      2400 non-null   object
     2   가해자연령      2406 non-null   object
     3   가해자차종      2410 non-null   object
     4   피해자신체상해정도  2410 non-null   object
     5   사고유형       2410 non-null   object
     6   기상상태       2410 non-null   object
     7   사망자수       2410 non-null   int64 
     8   발생시각       2410 non-null   object
    dtypes: int64(1), object(8)
    memory usage: 169.6+ KB
    dat.isna().sum()

    사고내용          0
    가해자성별        10
    가해자연령         4
    가해자차종         0
    피해자신체상해정도     0
    사고유형          0
    기상상태          0
    사망자수          0
    발생시각          0
    dtype: int64
    가해자성별 10개, 가해자성별 4개의 결측치가 존재하는 것을 확인할 수 있다. 해당 정보는 가해자 신상정보이므로, 결측치를 대치하는 것은 적절하지 않다. 전체 데이터 대비 결측치의 비율이 크지 않으므로 결측치를 삭제한다.

    dat = dat.dropna()

    re.sub(패턴, 바꾸고자하는 문자, 원본 문자)
    #re.sub(r'[^0-9]', '', '18세')
    import re

    def delete_text(x):
        x = re.sub(r'[^0-9]', '', str(x))
        return x

    dat['가해자연령'].apply(lambda x: delete_text(x)).head(3)

    0    75
    1    26
    2    34
    Name: 가해자연령, dtype: object
    dat['가해자연령'] = dat['가해자연령'].apply(lambda x: delete_text(x))
    dat = dat.astype({'가해자연령' : 'int64'})

    28.10 평일/주말을 구분하는 ‘주말여부’ 변수를 추가하고 데이터 분포를 확인하시오.
    def delete_text2(x):
        x = re.sub('시', '', str(x))
        return x

    dat['발생시각'].apply(lambda x: delete_text2(x)).head(3)

    0    2018-04-03 15
    1    2018-04-21 13
    2    2018-05-01 08
    Name: 발생시각, dtype: object
    from datetime import datetime
    dat['발생시각'] = dat['발생시각'].apply(lambda x: delete_text2(x))
    dat['발생시각'] = pd.to_datetime(dat['발생시각'], format='%Y-%m-%d %H')
    dat['요일'] = dat['발생시각'].dt.day_name()
    dat = dat.assign(주말여부 = np.where(dat['요일'].isin(['Saturday', 'Sunday']), 'Yes', 'No'))
    dat = dat.drop(['요일', '발생시각'], axis = 1)

    from matplotlib import font_manager, rc
    rc('font', family='AppleGothic')            ## 이 두 줄을 
    plt.rcParams['axes.unicode_minus'] = False 

    sns.countplot(dat['주말여부'])
    plt.show();



    28.11 주말여부에 따라 각 변수들(사고내용, 가해자성별, 가해자연령, 기상상태, 사고유형)이 통계적으로 유의한지 검정하시오.
    작성 방법 및 가정 확인 등은 통계반 내용 참고
    from scipy.stats import chi2_contingency
    table1 = pd.crosstab(dat['주말여부'], dat['사고내용'])

    chi2, p, df, expected = chi2_contingency(table1)
    print('statistics :', np.round(chi2, 2), 'p-value :', np.round(p, 2))

    statistics : 3.82 p-value : 0.05
    N = np.sum(table1.values) 
    minimum_dimension = min(table1.shape)-1
    Cramer_v = np.sqrt((chi2/N) / minimum_dimension) 
    print('Cramer v :', np.round(Cramer_v, 2))

    Cramer v : 0.04
    독립성 검정 결과 유의 수준 5%에서 p-value = 0.05로 귀무가설을 기각한다. 따라서 주말 여부와 사고 내용(중상, 경상) 간에는 통계적으로 유의미한 관계가 존재한다. cramer’s v = 0.04로 연관성의 강도는 크지 않다.

    table2 = pd.crosstab(dat['주말여부'], dat['가해자성별'])
    chi2, p, df, expected = chi2_contingency(table2)
    print('statistics :', np.round(chi2, 2), 'p-value :', np.round(p, 3))

    statistics : 11.96 p-value : 0.001
    N = np.sum(table2.values) 
    minimum_dimension = min(table2.shape)-1
    Cramer_v = np.sqrt((chi2/N) / minimum_dimension) 
    print('Cramer v :', np.round(Cramer_v, 2))

    Cramer v : 0.07
    독립성 검정 결과 유의 수준 5%에서 p-value = 0.001로 귀무가설을 기각한다. 따라서 주말 여부와 가해자성별(남성, 여성) 간에는 통계적으로 유의미한 관계가 존재한다. cramer’s v = 0.07로 연관성의 강도는 크지 않다.

    table3 = pd.crosstab(dat['주말여부'], dat['사고유형'])
    chi2, p, df, expected = chi2_contingency(table3)
    print('statistics :', np.round(chi2, 2), 'p-value :', np.round(p, 3))

    statistics : 1.41 p-value : 0.704
    독립성 검정 결과 유의 수준 5%에서 p-value = 0.7로 귀무가설을 기각할 수 없다. 따라서 주말 여부와 사고유형(차대차 - 기타, 차대차 - 측면충돌, 차대차 - 추돌, 차대사람 - 기타 ) 간에는 통계적으로 유의미한 관계가 존재하지 않는다.

    table4 = pd.crosstab(dat['주말여부'], dat['기상상태'])
    chi2, p, df, expected = chi2_contingency(table4)
    print('statistics :', np.round(chi2, 2), 'p-value :', np.round(p, 3))

    statistics : 5.74 p-value : 0.057
    독립성 검정 결과 유의 수준 5%에서 p-value = 0.057로 귀무가설을 기각할 수 없다. 따라서 주말 여부와 기상상태(맑음, 비, 흐림 ) 간에는 통계적으로 유의미한 관계가 존재하지 않는다.

    from scipy.stats import ttest_ind

    aa1 = dat.loc[dat['주말여부'] == 'Yes', '가해자연령']
    aa2 = dat.loc[dat['주말여부'] == 'No', '가해자연령']
    ttest_ind(aa1, aa2, equal_var = False)

    Ttest_indResult(statistic=-1.5461769343480278, pvalue=0.12239509465305189)
    welch t-test 결과 유의 수준 5%에서 p-value = 0.12로 귀무가설을 기각할 수 없다. 따라서 주말 여부와 가해자연령 간에는 통계적으로 유의미한 관계가 존재하지 않는다.

    28.12 SMOTE 오버샘플링하고 변수별 빈도를 나타내고 연속형변수의 경우 평균을 구하시오.
    SMOTE 샘플링을 하기 전에 훈련데이터와 검증 데이터를 분리한다. 데이터 분할을 하는 이유는 학습 데이터와 검증 데이터를 사전에 분할하는 이유는 최종 모형 평가에 활용되는 검증 데이터의 정보가 데이터 전처리 과정에서 활용되는 것을 방지 하기 위함이다.

    y = dat['사고내용']
    X = dat.drop(['사고내용'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = X['주말여부'], random_state = 0)

    데이터를 분할하는 방법은 대표적으로 simple random sampling, strata sampling이 있다. 첫 번째로, simple random sampling은 데이터를 무작위로 특정 비율로 분할하는 방법이다. 두 번째로, strata sampling은 class 불균형 문제에 대한 해결 방안으로 지정된 범주형 변수의 각 class에 해당하는 하위 샘플에 별도로 simple random sampling을 통해서 데이터를 분할하고, 이후 결합하는 방식으로 전체 데이터셋을 분할하는 방법이다.

    f, axes = plt.subplots(ncols = 2, nrows = 1, figsize = (20,4))
    train_y.hist(ax = axes[0]);
    sns.countplot(train_y, ax = axes[0])
    sns.countplot(test_y, ax = axes[1])
    plt.show();



    주말여부 변수에 대해 층화샘플링을 적용한 결과 train/test 분포 거의 유사한 형태인 것을 확인할 수 있다.

    SMOTE를 적용하기 위해서는 전부 numeric 이어야 하므로 변환 실시
    from sklearn.preprocessing import OrdinalEncoder
    from sklearn.compose import make_column_transformer

    cat_columns = train_X.select_dtypes('object').columns.to_list()
    num_columns = train_X.select_dtypes('number').columns.to_list()

    transformer = make_column_transformer(
        (OrdinalEncoder(), cat_columns),
        remainder='passthrough')

    encode_data = transformer.fit_transform(train_X)
    label_train_X = pd.DataFrame(encode_data, columns = train_X.columns)

    SMOTE 적용
    from collections import Counter
    from imblearn.over_sampling import SMOTE
    smote = SMOTE(random_state = 0)
    train_X_smote, train_y_smote = smote.fit_resample(label_train_X, train_y)
    print(Counter(train_y_smote))

    Counter({'경상': 1124, '중상': 1124})
    categorical variable 역변환
    aa = transformer.named_transformers_['ordinalencoder']
    invese_cat_data = aa.inverse_transform(train_X_smote[:, :6])
    invese_cat_data = pd.DataFrame(invese_cat_data, columns = cat_columns)

    역변환한 데이터 결합
    train_X_smote_sub = pd.DataFrame(train_X_smote, columns = train_X.columns)

    train_X_smote_sub = train_X_smote_sub.drop(cat_columns, axis = 1)

    train_X_smote = pd.concat([invese_cat_data, train_X_smote_sub], axis = 1)
    train_X_smote.head(2)

      가해자성별 가해자차종 피해자신체상해정도        사고유형 기상상태 주말여부  가해자연령  사망자수
    0     여   승용차        경상  차대차 - 측면충돌   맑음   No    0.0  45.0
    1     남   화물차        경상    차대차 - 기타   맑음   No    2.0  44.0
    연속형 변수 평균
    train_X_smote.loc[:, num_columns].mean()

    가해자연령     0.406093
    사망자수     49.364071
    dtype: float64
    범주형 변수 빈도
    for i in range(len(cat_columns)):
        print(train_X_smote[cat_columns[i]].value_counts())

    가해자성별
    남    1699
    여     549
    Name: count, dtype: int64
    가해자차종
    승용차    1622
    자전거     363
    화물차     263
    Name: count, dtype: int64
    피해자신체상해정도
    경상    1157
    중상    1091
    Name: count, dtype: int64
    사고유형
    차대차 - 측면충돌    1279
    차대차 - 기타       752
    차대사람 - 기타      120
    차대차 - 추돌        97
    Name: count, dtype: int64
    기상상태
    맑음    2150
    비       54
    흐림      44
    Name: count, dtype: int64
    주말여부
    No     1741
    Yes     507
    Name: count, dtype: int64
    28.13 로지스틱회귀분석, XGBoost 모형을 활용하여 분류분석을 수행하시오.
    from sklearn.linear_model import LogisticRegression
    from imblearn.pipeline import make_pipeline, Pipeline
    from sklearn.preprocessing import label_binarize

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    train_y = le.fit_transform(train_y)
    test_y = le.fit_transform(test_y)

    cat_preprocess = make_pipeline(
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    preprocess = ColumnTransformer([('cat', cat_preprocess, cat_columns)], remainder='passthrough')

    pipe_lg = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", LogisticRegression(solver='liblinear')) 
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

    Logistic regression best score :  0.9876542303827216
    Note
    logistic regression 모형의 경우 solver에 버그 이슈가 있으므로, 오류 발생시 solver='liblinear'로 설정해야 합니다.

    버그 이슈 : https://stackoverflow.com/questions/65682019/attributeerror-str-object-has-no-attribute-decode-in-fitting-logistic-regre

    import xgboost as xgb
    xgb_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("smote", SMOTE(random_state = 0)),
            ("classifier", xgb.XGBClassifier()) 
        ]
    )

    Xgb_param = {'classifier__learning_rate': np.arange(0.01, 0.3, 0.05)}

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
    print('xgboost best score : ', Xgb_search.best_score_)

    xgboost best score :  0.9867533294818207
    모델별로 성능을 비교해보면 Balanced accuracy는 대략 0.98이며, logistic regression의 성능이 가장 좋다. 따라서 최종 모형으로 logistic regression 모형을 선택한다.

    from sklearn.metrics import confusion_matrix, classification_report, balanced_accuracy_score
    pred_lg = pipe_lg.predict(test_X)
    print(classification_report(test_y, pred_lg))

                  precision    recall  f1-score   support

               0       1.00      1.00      1.00       298
               1       1.00      0.99      1.00       182

        accuracy                           1.00       480
       macro avg       1.00      1.00      1.00       480
    weighted avg       1.00      1.00      1.00       480
    balanced_accuracy_score(test_y, pred_lg)

    0.9972527472527473
    최종 검증 데이터에서의 성능은 balanced_accuracy = 0.99인 것을 확인할 수 있다.
    """
