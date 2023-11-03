def s8():
    """
    제 8 장
    회귀분석 파고들기
    8.1 Best 모델을 찾아서
    Stepwise 방법 처럼 자동으로 베스트 모델을 찾아주는 알고리즘은 현재 통계학에서는 사용하지 않는
    것을 추천하고 있다. 대표적이 이유는 다음과 같다.
    • 결과 모델의 R‑squared 값이 높게 측정되는 경향성을 띈다.
    • 결과 모델의 예측에 대한 신뢰구간이 비정상적으로 좁게 나오는 모델이 선택된다.
    • 결과 모델의 선택된 변수의 계수들이 비정상적으로 높게 나오는 경향을 띈다.
    • 다중공선성이 문제가 되는 데이터의 경우 stepwise 방법은 잘 작동하지 않는다.
    위의 문제에 대한 것은 다음의 참고 자료 를 찾아보자.
    Stepwise 방법
    • 각 단계별로 변수를 하나씩 추가해나가면서 최적의 모델을 찾는 방법
    – 모델 평가 지표들 (p‑value, AIC, BIC, Adjusted 𝑅2
    , Residual Mean Square) 중 하나
    를 선택하여 설정한 기준값을 비교하여 모델을 선택함.
    – 예를 들어 p‑value를 기준으로 한다면 𝛼𝑒𝑛𝑡𝑒𝑟와 𝛼𝑟𝑒𝑚𝑜𝑣𝑒를 먼저 설정해 놓고, 각 변수의
    p‑value와 기준을 비교해서 모델에 넣을지 뺄지 결정함.
    – 보통 𝛼𝑒𝑛𝑡𝑒𝑟와 𝛼𝑟𝑒𝑚𝑜𝑣𝑒 값으로 0.15를 선택한다. (R의 경우)
    1 단계
    • 각 변수별 회귀모델 설정 → 모델 중 𝛼𝑒𝑛𝑡𝑒𝑟 보다 낮은 p‑value 중 가장 낮은 변수를 선택
    2 단계
    • 1차 선택 변수에 나머지 변수들 끼워서 회귀모델 설정
    – 같은 방법으로 2번째 변수 선택 → 조건 불만족시 stop.
    – 이미 선택된 변수 중 𝛼𝑟𝑒𝑚𝑜𝑣𝑒 보다 높은 p‑value → 제거.
    현재 파이썬의 경우 p‑value 기반 stepwise는 구현된 것이 없고, AIC 기반 만 구현되어있다.
    회귀분석 파고들기 | 153
    AIC, BIC base stepwise method
    AIC, BIC는 무엇일까?
    • Likelihood function 기반 모델 적합도 평가 지표
    𝐴𝐼𝐶 = −2𝑙𝑜𝑔𝐿 + 2𝑝
    𝐵𝐼𝐶 = −2𝑙𝑜𝑔𝐿 + 𝑝 𝑙𝑜𝑔 𝑛
    일반적으로 Likelihood 값은 높을 수록 모델의 적합도가 높다고 판단할 수 있다. 하지만, 모델에
    사용되는 변수가 늘어날 수록 Likelihood 값이 높아지는 경향을 보인다.
    • 모델에 사용되는 변수는 적으면 적을 수록 좋다. (같은 성능이면 모델 복잡성 낮은 모델을 선호)
    • 특정 변수가 추가되었는데 늘어나는 Likelihood 값이 미미하다면 추가하지 않는 것이 좋다.
    • AIC, BIC는 Likelihood 값에 음수가 붙어있으므로 같이 낮을 수록 좋음!
    AIC stepwise in Python
    Stepwise 방법은 가능한 모든 모델의 평가지표를 비교하는 방법이 아니다.
    예를 들어 𝑝개의 독립변수가 존재하면, 2
    𝑝개의 모델에 대한 AIC값을 다 비교해야 하지만 계산량이
    너무 많아진다.
    • Stepwise 방식은 최적의 모델을 효율적으로 찾아가는 방법이라고 이해하면 된다.
    • 단, 단점은 stepwise의 결과 모델이 최적의 모델이라는 것을 장담할 수 없다.
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from mlxtend.feature_selection import SequentialFeatureSelector as SFS
    import statsmodels.api as sm
    from sklearn.datasets import load_iris
    # Load iris data
    iris = load_iris()
    X = iris.data[:, [0, 1, 3]]
    y = iris.data[:, 2]
    names = np.array(iris.feature_names)[[0, 1, 3]]
    # Define model
    lr = LinearRegression()
    # Define custom feature selector
    def aic_score(estimator, X, y):
    X = sm.add_constant(X)
    154 | 회귀분석 파고들기
    8
    model = sm.OLS(y, X).fit()
    print("Model AIC:", model.aic)
    return -model.aic
    # Perform SFS
    sfs = SFS(lr,
    k_features=(1,3),
    forward=True,
    scoring=aic_score,
    cv=0)
    sfs.fit(X, y)
    # 결과 출력
    ^༈ Model AIC: 385.1349961458542
    ^༈ Model AIC: 568.7536581517621
    ^༈ Model AIC: 206.35386357991936
    ^༈ Model AIC: 156.17922963502622
    ^༈ Model AIC: 193.9940121409602
    ^༈ Model AIC: 86.81602018114893
    ^༈ SequentialFeatureSelector(cv=0, estimator=LinearRegression(), k_features=(1, 3),
    ^༈ scoring=<function aic_score at 0x000001ABA3F9F0D8>)
    print('Selected features:', np.array(names)[list(sfs.k_feature_idx_)])
    ^༈ Selected features: ['sepal length (cm)' 'sepal width (cm)' 'petal width (cm)']
    mlxtend패키지에서 제공되는 SequentialFeatureSelector 는 순차적으로 변수를 넣어가면서 모델
    을 평가하는 기능을 제공한다. 다만 평가 지표에 AIC나 BIC같은 지표를 제공하지 않기 때문에 사용자
    가 직접 정의하여 사용해야한다.
    • 방향은 2방향이 가능: forward, backward
    – forward 옵션을 False로 설정할 경우 backward 방향이 작동한다.
    Mallows’s 𝐶𝑝
    statistic
    Mallow’s 𝐶𝑝 의 값을 이해하기 위해서 모델의 전체 모수 갯수를 𝑝, 그것들의 특정한 부분 집합인 𝑘
    개의 변수들을 생각하자. 여기서 𝑝는 각 독립변수에 딸려있는 계수 𝑝 − 1개와 절편 1개를 포함한
    값임에 주의하자.
    Mallow’s 𝐶𝑝 모델 평가 지표이며, 𝑝개의 모수를 사용한 모델로 적합된 값에 대한 MSE(mean
    square error)와 관련한 통계량이다.
    𝐶𝑘 =
    𝑆𝑆𝐸𝑘
    ̂𝜎
    2
    − (𝑛 − 2𝑘)
    Best 모델을 찾아서 | 155
    여기서 ̂𝜎
    2은 전체 모수 𝑝개를 모두 사용하여 추정된 𝜎
    2의 추정값이고, 𝑆𝑆𝐸𝑘는 모수 𝑘개를 사용
    한 모델에서 계산된 SSE 값을 의미한다. 위의 Mallow의 통계량은 기댓값을 계산하기 위해서 다음의
    사실을 받아들이도록 하자.
    𝔼 [𝑆𝑆𝐸𝑘
    ] = 𝜎2
    (𝑛 − 𝑘)
    위의 사실을 이용하면, 𝐶𝑘의 기댓값은 𝑘라는 것을 알 수 있으며, 이론적으로 𝐶𝑘의 최소값은 𝑘라는
    것이 알려져있다. 따라서, 일반적으로 𝐶𝑘 값은 작은 값이 좋다고 할 수 있으며, 𝑘 값 근처에 있는 모델을
    좋은 모델 후보로 선정한다. 또한, Full 모델의 𝐶𝑝값은 언제나 𝑝이 나오게 설계되어있다. 따라서 Full
    모델을 𝐶𝑝값으로 평가해서는 안된다.
    𝐶𝑝 값이 작게 나오는 경우
    위의 계산식에서 𝜎
    2 은 Full 모델의 MSE를 통하여 추정하게 되는데, 이 값이 잘 작동하려면 Full
    모델의 계수들이 모두 유효해야한다. 만약 Full 모델에서의 계수들이 0 근처인 변수들이 많다면, ̂𝜎
    2은
    실제 값보다 크게 추정되는 경향을 보인다. 이 경우 𝐶𝑝 값은 작아지게되고, 유용하지 않는 값이 된다.
    Mallow’s 𝐶𝑝
    in Python
    Mallow’s 𝐶𝑝를 Python에서 구현 하는 함수는 현재 존재하지 않는다. 다음과 같이 사용자 정의 함수
    를 사용하도록 하자.
    import numpy as np
    import pandas as pd
    import itertools
    from sklearn.linear_model import LinearRegression
    import statsmodels.api as sm
    def calculate_mallows_cp(X, y):
    X = sm.add_constant(X)
    lr_full = LinearRegression().fit(X, y)
    y_pred_full = lr_full.predict(X)
    k = X.shape[1]
    n = X.shape[0]
    mse_full = 1/(n-k) * np.sum((y - y_pred_full) ^* 2)
    cp_results = []
    # Loop over all possible combinations
    for p in range(1, k+1):
    for subset in itertools.combinations(range(k), p):
    X_subset = X[:, subset]
    156 | 회귀분석 파고들기
    8
    # Define and fit subset model
    lr_subset = LinearRegression().fit(X_subset, y)
    y_pred_subset = lr_subset.predict(X_subset)
    # Calculate SSE of subset model
    sse_subset = np.sum((y - y_pred_subset) ^* 2)
    # Calculate Mallow's Cp
    cp = (sse_subset / mse_full) - n + 2 * p
    # Store results
    cp_results.append((subset, cp))
    return cp_results
    iris 데이터셋을 가져와 𝐶𝑝 값을 계산해보도록 한다.
    from sklearn.datasets import load_iris
    iris = load_iris()
    # 'Petal.Width', 'Sepal.Length', 'Sepal.Width'
    X = iris.data[:, [0, 1, 3]]
    # 'Petal.Length'
    y = iris.data[:, [2]]
    cp_results = calculate_mallows_cp(X, y)
    df = pd.DataFrame(cp_results, columns=['Variables', 'Mallows Cp'])
    df[df['Mallows Cp'] ^ཏ 100]
    ^༈ Variables Mallows Cp
    ^༈ 8 (1, 3) 88.947328
    ^༈ 11 (0, 1, 3) 90.947328
    ^༈ 13 (1, 2, 3) 2.000000
    ^༈ 14 (0, 1, 2, 3) 4.000000
    예제 데이터와 모델 선택하기
    다음은 시멘트 혼합물에 따른 발열 측정 자료이다.
    • 𝑌 : heat evolved in calories per gram of cement
    • 𝑋1
    : tricalcium aluminate
    • 𝑋2
    : tricalcium silicate
    • 𝑋3
    : tetracalcium alumino ferrite
    Best 모델을 찾아서 | 157
    • 𝑋4
    : dicalcium silicate
    표 8.1: Hald cement data
    Y X1 X2 X3 X4
    78.5 7 26 6 60
    74.3 1 29 15 52
    104.3 11 56 8 20
    87.6 11 31 8 47
    95.9 7 52 6 33
    109.2 11 55 9 22
    102.7 3 71 17 6
    72.5 1 31 22 44
    93.1 2 54 18 22
    115.9 21 47 4 26
    83.8 1 40 23 34
    113.3 11 66 9 12
    109.4 10 68 8 12
    데이터를 hald_cement_data 변수에 입력한 후 Mallows 𝐶𝑝를 활용하여 모델 선택을 진행해보자.
    y = np.array([78.5, 74.3, 104.3, 87.6, 95.9, 109.2, 102.7,
    72.5, 93.1, 115.9, 83.8, 113.3, 109.4])
    X = np.array([[7, 26, 6, 60],
    [1, 29, 15, 52],
    [11, 56, 8, 20],
    [11, 31, 8, 47],
    [7, 52, 6, 33],
    [11, 55, 9, 22],
    [3, 71, 17, 6],
    [1, 31, 22, 44],
    [2, 54, 18, 22],
    [21, 47, 4, 26],
    [1, 40, 23, 34],
    [11, 66, 9, 12],
    [10, 68, 8, 12]])
    cp_results = calculate_mallows_cp(X, y)
    df = pd.DataFrame(cp_results, columns=['Variables', 'Mallows Cp'])
    df[df['Mallows Cp'] ^ཏ 20]
    ^༈ Variables Mallows Cp
    ^༈ 9 (1, 2) 0.678242
    ^༈ 11 (1, 4) 3.495851
    ^༈ 15 (0, 1, 2) 2.678242
    ^༈ 17 (0, 1, 4) 5.495851
    158 | 회귀분석 파고들기
    8
    ^༈ 21 (1, 2, 3) 1.041280
    ^༈ 22 (1, 2, 4) 1.018233
    ^༈ 23 (1, 3, 4) 1.496824
    ^༈ 24 (2, 3, 4) 5.337474
    ^༈ 25 (0, 1, 2, 3) 3.041280
    ^༈ 26 (0, 1, 2, 4) 3.018233
    ^༈ 27 (0, 1, 3, 4) 3.496824
    ^༈ 28 (0, 2, 3, 4) 7.337474
    ^༈ 29 (1, 2, 3, 4) 3.000000
    ^༈ 30 (0, 1, 2, 3, 4) 5.000000
    import matplotlib.pyplot as plt
    # Filter Cp values ^ཏ 20
    filtered_df = df[df['Mallows Cp'] ^ཏ 20]
    num_variables = [len(variables) for variables in filtered_df['Variables']]
    # Scatter plot
    plt.scatter(num_variables, filtered_df['Mallows Cp']);
    plt.plot(num_variables, num_variables,
    color='red', label='y = x');
    plt.xlabel('Num of Variables');
    plt.ylabel('Mallows Cp');
    plt.title('Scatter Plot of Cp Values');
    plt.show()
    2.0 2.5 3.0 3.5 4.0 4.5 5.0
    Num of Variables
    1
    2
    3
    4
    5
    6
    7
    Mallows Cp
    Scatter Plot of Cp Values
    Mallows’s 𝐶𝑝 값이 𝑝 직선과 가까운 모델들을 후보로 선정한다.
    • 𝑋1 + 𝑋2 모델
    • 𝑋1 + 𝑋2 + 𝑋4 모델
    Best 모델을 찾아서 | 159
    • 𝑋1 + 𝑋2 + 𝑋3 모델
    • 𝑋1 + 𝑋3 + 𝑋4 모델
    이 모델들 중에서 가장 작은 𝐶𝑝 값을 갖는 𝑋1 + 𝑋2 모델이 최적의 모델로 생각할 수 있다.
    • Adjusted 𝑅2 구하기
    from sklearn.metrics import r2_score
    def adjusted_r2_score(estimator, X, y):
    y_pred = estimator.predict(X)
    n = X.shape[0]
    p = X.shape[1]
    r2 = r2_score(y, y_pred)
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    return adjusted_r2
    # Perform SFS
    sfs = SFS(lr,
    k_features=(1,4),
    forward=True,
    scoring=adjusted_r2_score,
    cv=0)
    sfs.fit(X, y)
    # 결과 출력
    ^༈ SequentialFeatureSelector(cv=0, estimator=LinearRegression(), k_features=(1, 4),
    ^༈ scoring=<function adjusted_r2_score at 0x000001ABA4075DC8>)
    selected_indices = list(sfs.k_feature_idx_)
    print('Selected features:', selected_indices)
    ^༈ Selected features: [0, 1, 3]
    Adjusted 𝑅2 값을 기준으로 보았을 경우 최적의 모델은 𝑥1 + 𝑥2 + 𝑥4 모델로 생각할 수 있다.
    • stepwise 알고리즘을 적용한 모델 선택
    stepwise 알고리즘으로 intercept만 존재하는 모델에서 시작해서 모든 변수 조합을 기준으로 최적
    모델을 구해보면 다음과 같다.
    # Perform SFS
    sfs = SFS(lr,
    k_features=(1,4),
    160 | 회귀분석 파고들기
    8
    forward=True,
    scoring=aic_score,
    cv=0)
    sfs.fit(X, y)
    # 결과 출력
    ^༈ Model AIC: 100.41187201391966
    ^༈ Model AIC: 96.0703964203777
    ^༈ Model AIC: 105.95980439471697
    ^༈ Model AIC: 95.74404477885616
    ^༈ Model AIC: 65.63410626724041
    ^༈ Model AIC: 97.52172751297775
    ^༈ Model AIC: 76.74498580894803
    ^༈ Model AIC: 61.86628547186261
    ^༈ Model AIC: 62.619952232581554
    ^༈ Model AIC: 63.83668979165169
    ^༈ SequentialFeatureSelector(cv=0, estimator=LinearRegression(), k_features=(1, 4),
    ^༈ scoring=<function aic_score at 0x000001ABA3F9F0D8>)
    selected_indices = list(sfs.k_feature_idx_)
    print('Selected features:', selected_indices)
    ^༈ Selected features: [0, 1, 3]
    이렇게 모델을 비교하다보면 각 모델의 측정 지표에 따라서 최적의 모델이 달라지는 경우가 있다.
    이런 경우 분석가가 꼭 명심해야 하는 사실은 다음과 같다.
    • 각 측정 지표를 통해서 뽑은 최적의 모델은 정답 모델이 아니다.
    참고로 stepwise 방법은 현재 통계학에서는 거의 사용하지 않는 모델 선택 방법으로는 좋지 않은
    방법 중 하나로 꼽힌다. 따라서 결정된 최적 모델들은 분석가가 다시 면밀하게 분석하고, 최종 모델을
    결정해야 한다.
    예를 들어, Mallows’s 𝐶𝑝 기준으로 뽑힌 𝑥1 + 𝑥2 모델과 Adjusted 𝑅2 기준과 stepwise 알고리
    즘으로 선택된 𝑥1 + 𝑥2 + 𝑥4 모델을 판단 과정을 살펴보자.
    분석 시 변수 간 상관관계를 계산해본다면 𝑥2와 𝑥4가 강한 상관관계를 갖는다는 사실을 알 수 있다.
    import seaborn as sns
    df = pd.DataFrame(np.concatenate((y.reshape(-1, 1), X), axis=1), columns=['y', 'x1', 'x2', 'x3', 'x4'])
    corr_mat = df.corr().round(2)
    plt.figure(figsize=(8, 6));
    Best 모델을 찾아서 | 161
    sns.heatmap(corr_mat, annot=True, cmap='coolwarm', vmin=-1, vmax=1);
    plt.title('Correlation Matrix');
    plt.show()
    y x1 x2 x3 x4
    y x1 x2 x3 x4
    1 0.73 0.82 -0.53 -0.82
    0.73 1 0.23 -0.82 -0.25
    0.82 0.23 1 -0.14 -0.97
    -0.53 -0.82 -0.14 1 0.03
    -0.82 -0.25 -0.97 0.03 1
    Correlation Matrix
    1.00
    0.75
    0.50
    0.25
    0.00
    0.25
    0.50
    0.75
    1.00
    위의 상관계수 테이블에 의하면, 두 변수가 같이 들어간 𝑥1 + 𝑥2 + 𝑥4 모델의 경우 다중공선성
    (Multicollinearity)이 우려될 수 있으며, 이는 다음 시간에 배울 다중공선성 측정 지표인 VIF에 의
    하여도 잡아낼 수 도 있다.
    이러한 사실을 바탕으로 𝑥1+𝑥2+𝑥4 모델보다는 𝑥1+𝑥2 모델이 좀 더 좋은 판단이라고 분석가는
    최종 결정을 내릴 수 있다.
    8.2 회귀분석에서의 영향점 (influential point)
    회귀 모델을 설정함에 있어서 영향력이 있는 표본들이 존재한다. 이들을 잡아낼 수 있는 지표들을
    배워보자.
    • Cook’s distance
    • 스튜던트화 잔차
    Cook’s distance
    • PRESS 잔차: 만약 특정 포인트의 정보가 없어진다면 모델의 예측이 얼마나 바뀔 것 인가?
    𝐶𝑖 =
    ∑
    𝑛
    𝑗=1 ( ̂𝑦𝑗 − ̂𝑦𝑗(𝑖))
    ̂𝜎
    2 (𝑝 + 1)
    즉, 각 표본 별 Cook’s distance가 존재함.
    • 𝐶𝑖 값 ≥ 𝐹(𝑝+1,𝑛−𝑝−1) 분포의 중앙값을 사용하여 Influential point로 판정
    162 | 회귀분석 파고들기
    8
    from scipy.stats import f
    f.ppf(0.5, 4, 150 - 5)
    ^༈ 0.8431114434390823
    from statsmodels.formula.api import ols
    from statsmodels.stats.outliers_influence import OLSInfluence
    from sklearn.datasets import load_iris
    iris = load_iris()
    iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    #컬럼명 변경
    iris.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
    model2 = ols('Petal_Length ~ Petal_Width + Sepal_Length + Sepal_Width', data=iris).fit()
    influence = OLSInfluence(model2)
    cooks_distance = influence.cooks_distance[0]
    # Plot the Cook's distance
    plt.bar(range(len(cooks_distance)), cooks_distance, width=0.8);
    plt.ylabel("Cook's distance");
    plt.show()
    0 20 40 60 80 100 120 140
    0.00
    0.01
    0.02
    0.03
    0.04
    0.05
    0.06
    0.07
    Cook's distance
    표준화된 잔차 (Standardized Residuals)
    잔차들을 표준화 시키면 표준정규분포를 따를 것이다. 표준 정규분포의 66‑95‑99 규칙을 이용해서 3
    표준편차 영역 밖의 표본들을 걸러낸다.
    회귀분석에서의 영향점 (influential point) | 163
    std_res = influence.resid_studentized_internal
    print(std_res[np.abs(std_res) > 3])
    ^༈ 134 3.379260
    ^༈ 141 -3.151953
    ^༈ dtype: float64
    plt.hist(std_res);
    plt.show()
    3 2 1 0 1 2 3
    0
    10
    20
    30
    40
    50
    스튜던트화 잔차 (Studentized Residuals)
    그냥 잔차가 아닌 Cook’s distance 계산시의 잔차들을 표준화 한 후, 3 표준편차 영역 밖에 위치한
    표본들을 걸러낸다.
    𝑡𝑖 =
    𝑑𝑖
    𝑠𝑡𝑑 (𝑑𝑖
    )
    where 𝑑𝑖 = 𝑦𝑖 − ̂𝑦(𝑖)
    • ̂𝑦(𝑖): 𝑖 번째 표본을 제외하고 회귀 모델을 구한 후 𝑖 번째 표본에 대하여 예측한 값
    • 𝑖 번째 표본이 influential point 라면 회귀직선이 표본 𝑖 쪽으로 기울어져 있을 수 있다. 따라서
    𝑖 번째 표본을 제외 했을 때의 회귀직선을 사용해서 잔차를 구하는 것이 더 좋을 경우가 있다.
    stud_res = influence.resid_studentized_external
    stud_res[np.abs(stud_res) > 3]
    ^༈ 134 3.507635
    ^༈ 141 -3.253796
    ^༈ dtype: float64
    164 | 회귀분석 파고들기
    8
    Outliers vs. High leverage point
    영향점 (influential point)을 구성하는 표본들은 두 가지로 분류된다.
    • outlier
    • high leverage point
    회귀분석에서의 Outliers
    • 반응변수 𝑦에 대한 outlier를 의미한다.
    • Studentized __residual__을 사용한 판단
    회귀분석에서의 High leverage point
    • 독립변수 𝑋에 대한 outlier를 의미한다.
    • leverage값이 높은 관측치
    • hatvalues() 함수
    • 2(p+1)/n 보다 크면 high
    • 잔차값은 높지 않게 나올 수 있음
    그림 8.1: Image from ’https://slideplayer.com/slide/8964135/’
    회귀분석에서의 영향점 (influential point) | 165
    8.3 영향있는 표본들, Outlier에 대처하는 방법
    튀는 표본이 존재한다하여 무작정 삭제가 답이 아니다. 즉, Outlier Flag가 떳다고해서 꼭 Outlier
    라는 이야기가 아니다.
    • 의미: 내가 가진 데이터의 패턴을 벗어난 자료라는 뜻
    데이터를 자세히 살펴보고, 이상치로 판단하여 제거할 지, 영향력이 있는 표본으로 생각하여 분석에
    포함시키는 문제는 분석가의 판단이다. (합리적인 근거를 마련한다.)
    데이터 에러를 고려
    • 데이터가 잘못 기록된 것인 아닌지 살펴본다.
    • 표본이 연구 모집단을 반영하지 못한다고 생각하면 지운다. 다만, 삭제에 있어서 객관적인 이유가
    존재해야 한다.
    • Robust한 회귀분석 방법을 적용해본다.
    – 학습 시 weight를 변경: Weighted regression
    – 학습 시 손실함수를 절대거리 기반으로 변경: ltsReg or lmrob
    from statsmodels.formula.api import ols
    from statsmodels.robust.robust_linear_model import RLM
    # Fit the robust linear model
    robust_mod = RLM.from_formula(
    'Petal_Length ~ Petal_Width + Sepal_Length + Sepal_Width', data=iris).fit()
    모델 에러를 고려
    • 고려되는 현재 모델에 다른 중요한 변수가 빠진 것은 아닌지 체크한다.
    – 인터렉션 항 추가를 고려해본다.
    – 비선형 모델을 고려해본다.
    – 데이터 변환을 고려해본다.
    Scottish Hill Racing 예제
    스코틀랜드에 매해 열리는 언덕 달리기 경주 데이터를 사용하여 회귀분석 모델을 돌려보자.
    데이터 불러오기
    import pandas as pd
    race_data = pd.read_csv('./data/scottish༡hills༡races.csv')
    race_data.columns = ['hill_race', 'time', 'distance', 'climb']
    race_data.head()
    166 | 회귀분석 파고들기
    8
    그림 8.2: Image from ’www.scottishdistancerunninghistory.scot’
    ^༈ hill_race time distance climb
    ^༈ 0 Greenmantle New Year Dash 965 2.5 650
    ^༈ 1 Carnethy 2901 6.0 2500
    ^༈ 2 Craig Dunain 2019 6.0 900
    ^༈ 3 Ben Rha 2736 7.5 800
    ^༈ 4 Ben Lomond 3736 8.0 3070
    회귀분석 모델
    마지막으로 완주한 경기 시간 time을 distance 변수와 climb 변수를 사용하여 설명하는 회귀분석
    모델을 설정한다.
    reg1 = ols('time ~ distance + climb', data=race_data).fit()
    reg1.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: time R༡squared: 0.919
    ^༈ Model: OLS Adj. R༡squared: 0.914
    ^༈ Method: Least Squares F༡statistic: 181.7
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 3.40e-18
    ^༈ Time: 14:01:49 Log-Likelihood: -285.41
    ^༈ No. Observations: 35 AIC: 576.8
    ^༈ Df Residuals: 32 BIC: 581.5
    ^༈ Df Model: 2
    ^༈ Covariance Type: nonrobust
    ^༈ ==============================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ ------------------------------------------------------------------------------
    영향있는 표본들, Outlier에 대처하는 방법 | 167
    ^༈ Intercept -539.4829 258.161 -2.090 0.045 -1065.339 -13.627
    ^༈ distance 373.0727 36.068 10.343 0.000 299.604 446.542
    ^༈ climb 0.6629 0.123 5.387 0.000 0.412 0.914
    ^༈ ==============================================================================
    ^༈ Omnibus: 47.910 Durbin-Watson: 2.249
    ^༈ Prob(Omnibus): 0.000 Jarque-Bera (JB): 233.983
    ^༈ Skew: 3.026 Prob(JB): 1.55e-51
    ^༈ Kurtosis: 14.127 Cond. No. 4.20e+03
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ [2] The condition number is large, 4.2e+03. This might indicate that there are
    ^༈ strong multicollinearity or other numerical problems.
    ^༈ ""
    F‑검정 통계량과 각 변수 t 검정 통계량값을 통하여 회귀분석 모델과 사용된 모든 변수가 통계적으로
    유의한 것을 확인할 수 있다.
    잔차 그래프 분석
    적합된 모델과 잔차를 확인해보자. (앞시간에 배운 정규성 검정과 등분산 검정, 독립성 검정은 다시
    한번 연습해 볼 것.)
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(reg1.predict(), reg1.resid);
    plt.axhline(y=0, color='black', linestyle='--');
    plt.xlabel('Predicted values');
    plt.ylabel('Residuals');
    plt.show()
    168 | 회귀분석 파고들기
    8
    2000 4000 6000 8000 10000
    Predicted values
    1000
    0
    1000
    2000
    3000
    4000
    Residuals
    그래프로 보아 약간의 U 모양 그래프로 볼 수 있고, 또한 등분산 가정도 깨져보인다. (검정 필요함,
    해보세요!)
    sm.qqplot(reg1.resid, fit=True, line='45');
    plt.show()
    1 0 1 2 3 4
    Theoretical Quantiles
    1
    0
    1
    2
    3
    4
    Sample Quantiles
    Normal QQ 그래프 경우 7번와 18번 표본을 제외하고는 다들 괜찮아 보인다.
    8.4 다중공선성을 대하는 우리들의 자세
    새로운 변수가 들어왔을 경우 가능한 4가지 상황
    • 새로운 변수가 유의하지 않고, 기존 변수가 이전 값에 비해 크게 변하지 않음: 새로운 변수 추가
    해서는 안됨.
    다중공선성을 대하는 우리들의 자세 | 169
    • 새로운 변수가 유의하고, 기존 변수가 이전 값에 비해 크게 변하지 않음: 이상적 케이스
    • 새로운 변수가 유의하고, 기존 변수가 이전 값에 비해 크게 변함 : 새로운 변수 추가하고,
    collinearity 체크.
    – collinearity 증거가 없다. Add
    – collinearity 증거가 있다. Treat
    • 새로운 변수가 유의하지 않고, 기존 변수가 이전 값에 비해 크게 변함: collinearity 확실한 증거
    – 변수 넣을지 말지에 대한 것 보다 treat 먼저 선행
    Collinearity (공선성)
    • 많은 회귀분석의 경우 독립변수들은 orthogonality를 가정하지만 실제로 독립 변수들이 or‑
    thogonal 한 경우는 드물다. 이렇게 독립변수들끼리 correlation이 존재하는 상황을 공선성이
    존재한다고 한다. 하지만 독립변수 간 공선성의 존재는 실제로 분석에 영향을 줄 정도로 별 문제가
    되지 않는다.
    • 가끔 너무 심하게 orthogonal 가정이 무너져서 분석에 영향을 줄 때가 있다.
    – 데이터가 살짝만 변해도 계수가 확 바뀜
    – 변수가 더하거나 지워질 때 계수가 확 바뀜
    완전 linearly dependent한 경우
    다음의 행렬의 열 들은 완벽하게 dependent한 경우이다. 즉, 각 열을 다른 두 열을 사용하여 상수배를
    해서 더하고 빼면 만들어낼 수 있다.
    ⎛⎜⎜
    ⎝
    1 2 3
    1 2 3
    3 6 9
    ⎞⎟⎟
    ⎠
    공선성 처리 방법
    다음 사항들을 머리속에 넣고, 읽어나가기 바란다.
    170 | 회귀분석 파고들기
    8
    • 공선성은 어떻게 회귀분석 추정과 예측에 영향을 미치는가
    • 공선성을 어떻게 감지하고, 어떻게 해결할까?
    다중공선성 감지 지표
    VIF: Variance Inflation Factors
    다중공선성이 심하다는 이야기는 특정 독립변수 𝑋𝑗의 정보가 다른 독립 변수들의 정보로 모두 설명이
    가능하다는 이야기가 된다. 따라서, 𝑋𝑗를 반응변수로 놓고, 다른 독립변수를 사용해서 회귀 모델을
    적합해보면, 𝑅2이 거의 1과 비슷하게 나올 것이다. 독립변수 𝑋𝑗에 대한 VIF는 다음과 같이 계산한다.
    𝑉 𝐼𝐹𝑗 =
    1
    1 − 𝑅2
    𝑗
    • 𝑅2
    𝑗
    : 𝑗번째 독립 변수를 다른 독립변수들을 사용하여 회귀분석
    • 독립변수 𝑋𝑗가 다른 독립변수들과 선형적인 관계가 없는 이상적인 경우: VIF 값이 1
    • 독립변수 𝑋𝑗가 다른 독립변수들과 선형적인 관계가 심할 경우: VIF 값이 발산
    • 판단 기준값: 10
    왜 Variance Inflation Factors 인가?
    • VIF가 계수의 변동성 증가분을 측정하기 때문
    회귀분석에서 𝑗 번째 변수의 계수의 분산 측정값은 다음과 같이 표현할 수 있음.
    var ̂(𝛽̂
    𝑗
    ) = 𝑠
    2
    (𝑛 − 1)̂var(𝑋𝑗
    )
    ⋅
    1
    1 − 𝑅2
    𝑗
    만약 𝑗 번째 변수가 다른 변수들과 비교하여 선형 독립을 만족한다면, 𝑅2 값은 0이 나옴. 따라서
    𝑉 𝐼𝐹𝑗는 각 변수에 해당하는 계수의 분산값이 선형 독립인 경우 대비 얼마나 inflation 되었는지를
    측정하는 지표로 볼 수 있다.
    • 𝑉 𝐼𝐹𝑗
    =
    𝑉 𝑎𝑟(𝛽̂
    𝑗
    )
    𝑉 𝑎𝑟(𝛽̂
    𝑗
    )𝑙𝑖𝑛𝑒𝑎𝑟𝑙𝑦 𝑖𝑛𝑑𝑒𝑝.
    평균 VIF값의 의미
    ∑
    𝑝
    𝑗=1 𝑉 𝐼𝐹𝑗
    𝑝
    = 𝑉 𝐼𝐹
    각 변수별 측정된 VIF값의 평균은 독립변수들이 선형 독립인 경우에 비하여 회귀분석 계수 추정치가
    불안정한 정도를 나타내어 준다.
    학생 성취도 데이터
    학생 성취도 데이터를 통하여 이야기 해보자. 학생의 학업 성취도를 나타내는 achv를 가족환경 fam,
    학교 친구들 peer, 그리고 학교 환경 school을 사용하여 설명하는 회귀 모델을 적합한다.
    다중공선성을 대하는 우리들의 자세 | 171
    achieve_data = pd.read_csv('./data/student_achievement.csv')
    reg2 = ols(formula='ACHV ~ FAM + PEER + SCHOOL', data=achieve_data).fit()
    achieve_data.head()
    ^༈ ACHV FAM PEER SCHOOL
    ^༈ 0 -0.43148 0.60814 0.03509 0.16607
    ^༈ 1 0.79969 0.79369 0.47924 0.53356
    ^༈ 2 -0.92467 -0.82630 -0.61951 -0.78635
    ^༈ 3 -2.19081 -1.25310 -1.21675 -1.04076
    ^༈ 4 -2.84818 0.17399 -0.18517 0.14229
    회귀분석 결과
    회귀 모델이 유의한 지에 대한 F 검정통계량을 통하여 유의한 모델이라 말할 수 있다. 하지만 다음의
    2가지 특징을 확인 할 수 있다.
    • 각 변수들의 유의성 검정에서 p‑value값이 높게 나오고, 모두 유의하지 않은 것을 알 수 있다.
    • 𝑅2 값이 0.2로 비교적 낮다고 할 수 있다.
    reg2.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: ACHV R༡squared: 0.206
    ^༈ Model: OLS Adj. R༡squared: 0.170
    ^༈ Method: Least Squares F༡statistic: 5.717
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 0.00153
    ^༈ Time: 14:01:52 Log-Likelihood: -148.20
    ^༈ No. Observations: 70 AIC: 304.4
    ^༈ Df Residuals: 66 BIC: 313.4
    ^༈ Df Model: 3
    ^༈ Covariance Type: nonrobust
    ^༈ ==============================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ ------------------------------------------------------------------------------
    ^༈ Intercept -0.0700 0.251 -0.279 0.781 -0.570 0.430
    ^༈ FAM 1.1013 1.411 0.781 0.438 -1.715 3.918
    ^༈ PEER 2.3221 1.481 1.568 0.122 -0.635 5.280
    ^༈ SCHOOL -2.2810 2.220 -1.027 0.308 -6.714 2.152
    ^༈ ==============================================================================
    ^༈ Omnibus: 0.558 Durbin-Watson: 1.791
    172 | 회귀분석 파고들기
    8
    ^༈ Prob(Omnibus): 0.756 Jarque-Bera (JB): 0.578
    ^༈ Skew: 0.203 Prob(JB): 0.749
    ^༈ Kurtosis: 2.816 Cond. No. 19.2
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    잔차분석
    잔차 그래프를 통하여 분석을 해도 특이점이 나타나지 않을 수 있다.
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(reg2.predict(), reg2.resid);
    plt.axhline(y=0, color='black', linestyle='--');
    plt.xlabel('Predicted values');
    plt.ylabel('Residuals');
    plt.show()
    2 1 0 1 2
    Predicted values
    4
    2
    0
    2
    4
    Residuals
    QQ plot의 결과 역시 마찬가지 이다.
    sm.qqplot(reg2.resid, fit=True, line='45');
    plt.show()
    다중공선성을 대하는 우리들의 자세 | 173
    2 1 0 1 2
    Theoretical Quantiles
    2
    1
    0
    1
    2
    Sample Quantiles
    다중공선성 파악하기
    각 변수들에 대하여 상관계수를 구해보도록 하자.
    import seaborn as sns
    sns.pairplot(achieve_data, kind="scatter", diag_kind="hist")
    ^༈ <seaborn.axisgrid.PairGrid object at 0x000001ABA1F31EC8>
    6
    4
    2
    0
    2
    4
    ACHV
    2
    1
    0
    1
    2
    3
    FAM
    2
    1
    0
    1
    2
    PEER
    5 0 5
    ACHV
    2
    1
    0
    1
    2
    3
    SCHOOL
    2 0 2
    FAM
    2 1 0 1 2
    PEER
    2 0 2
    SCHOOL
    174 | 회귀분석 파고들기
    8
    • 세 변수 fam, peer, 그리고 school의 산점도가 선형적인 패턴을 보이고 있다. 이는 전형적인
    다중공선성 패턴이다.
    achieve_data.corr()
    ^༈ ACHV FAM PEER SCHOOL
    ^༈ ACHV 1.000000 0.419459 0.439846 0.418101
    ^༈ FAM 0.419459 1.000000 0.960081 0.985684
    ^༈ PEER 0.439846 0.960081 1.000000 0.982160
    ^༈ SCHOOL 0.418101 0.985684 0.982160 1.000000
    • 각 변수의 VIF는 car 패키지의 vif() 함수를 사용한다.
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    x = achieve_data.iloc[:,1:4]
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(
    x.values, i) for i in range(x.shape[1])]
    vif["features"] = x.columns
    vif
    ^༈ VIF Factor features
    ^༈ 0 37.139750 FAM
    ^༈ 1 29.782169 PEER
    ^༈ 2 81.339023 SCHOOL
    결과에서 확인 할 수 있다시피 세 변수의 VIF 값은 모두 높다.
    해결책
    • 1 차원적 해결책은 VIF가 가장 높은 변수를 제외하고 회귀분석을 돌려보는 것이다.
    – VIF값이 안정될때까지 변수를 지워나감.
    – 지우는 것 만이 능사가 아님 ‑ 지워진 변수에도 유용한 정보가 존재할 수 있기 때문이다.
    다중 공선성의 해결책으로 언급되는 방법 중 대표적인 것은 다음과 같다.
    • PCA (Principal Components Analysis)
    • Penalized Regression
    주성분 (Principal Components)의 이해
    𝑝개의 독립변수를 𝑝개의 __선형 독립인 변수들__로 바꿔주는 방법이다.
    다중공선성을 대하는 우리들의 자세 | 175
    준비단계 ‑ 변수 표준화
    주성분 분석을 적용하기 위해서 각 변수들을 scaling 해준다. (평균을 빼고, 표준편차로 나눠줌.)
    • 𝑋1
    , 𝑋2
    , ..., 𝑋𝑝의 변수를 표준화시킨 변수를 𝑋̃
    ,𝑋̃
    2
    , ..., 𝑋̃
    𝑝라고 하자.
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(achieve_data)
    scaled_data = pd.DataFrame(scaled_data, columns=achieve_data.columns)
    scaled_data.head(3)
    ^༈ ACHV FAM PEER SCHOOL
    ^༈ 0 -0.199734 0.519586 -0.012224 0.132025
    ^༈ 1 0.345912 0.692129 0.471510 0.493656
    ^༈ 2 -0.418312 -0.814296 -0.725165 -0.805211
    각 변수들은 scaling 후 평균이 0, 표준편차가 1로 맞춰지게 된다.
    • 평균 0
    scaled_data.drop(columns=['ACHV']).mean(axis=0).round()
    ^༈ FAM 0.0
    ^༈ PEER 0.0
    ^༈ SCHOOL 0.0
    ^༈ dtype: float64
    • 표준편차 1
    scaled_data.drop(columns=['ACHV']).std(axis=0).round()
    ^༈ FAM 1.0
    ^༈ PEER 1.0
    ^༈ SCHOOL 1.0
    ^༈ dtype: float64
    변환하기
    표준화된 변수들을 사용하여 새로운 변수 𝐶𝑗
    , 𝑗 = 1, ..., 𝑝을 다음과 같이 만들어낸다.
    𝐶𝑗 = 𝑣1𝑗𝑋̃
    1 + 𝑣2𝑗𝑋̃
    2 + ... + 𝑣𝑝𝑗𝑋̃
    𝑝
    계수 역할을 하는 𝑣들을 이리저리 조정하여 𝐶𝑗들이 선형독립이 되도록 계수 𝑣들을 결정하는 방법.
    • 즉, 𝐶𝑗의 공분산 행렬은 대각 행렬이 됨.
    176 | 회귀분석 파고들기
    8
    from sklearn.decomposition import PCA
    pca = PCA(n_components=3)
    scaled = scaled_data.drop(columns=['ACHV'])
    pca_array = pca.fit_transform(scaled)
    my_pca = pd.DataFrame(pca_array,
    index = scaled.index,
    columns=["pca1", "pca2", "pca3"])
    결과값 해석
    분산값 비교하기
    • 원데이터 (Scaled)
    scaled.head()
    ^༈ FAM PEER SCHOOL
    ^༈ 0 0.519586 -0.012224 0.132025
    ^༈ 1 0.692129 0.471510 0.493656
    ^༈ 2 -0.814296 -0.725165 -0.805211
    ^༈ 3 -1.211176 -1.375633 -1.055565
    ^༈ 4 0.115871 -0.252115 0.108624
    • 원 데이터의 공분산행렬
    scaled_cov = scaled.cov()
    scaled_cov
    ^༈ FAM PEER SCHOOL
    ^༈ FAM 1.014493 0.973995 0.999969
    ^༈ PEER 0.973995 1.014493 0.996394
    ^༈ SCHOOL 0.999969 0.996394 1.014493
    • 변환된 데이터
    my_pca.head()
    ^༈ pca1 pca2 pca3
    ^༈ 0 0.368955 -0.368726 0.124351
    ^༈ 1 0.956635 -0.150422 0.085339
    ^༈ 2 -1.353829 0.063735 0.019803
    ^༈ 3 -2.102111 -0.129908 -0.194383
    ^༈ 4 -0.015266 -0.268837 -0.127596
    다중공선성을 대하는 우리들의 자세 | 177
    • 변환된 데이터의 공분산행렬
    my_pca.cov().round(3)
    ^༈ pca1 pca2 pca3
    ^༈ pca1 2.995 -0.000 -0.000
    ^༈ pca2 -0.000 0.041 0.000
    ^༈ pca3 -0.000 0.000 0.008
    새로 만들어진 변수들의 분산값들은 pca.explained_variance_ 변수에 저장되어 있다.
    pca.explained_variance_.round(3)
    ^༈ array([2.995, 0.041, 0.008])
    공분산 행렬의 분해
    앞에서 살펴본 새로 만들어진 변수들의 분산 정보는 원 데이터 행렬의 공분산 행렬의 eigen values와
    동일하다는 것을 알 수 있다.
    from numpy import linalg
    eig_values, eig_vectors = linalg.eig(scaled.cov())
    eig_values
    ^༈ array([2.99477567, 0.04062791, 0.00807469])
    eig_vectors
    ^༈ array([[-0.57613845, -0.67939712, -0.45440515],
    ^༈ [-0.5754361 , 0.73197527, -0.36480886],
    ^༈ [-0.58046342, -0.05130072, 0.81266873]])
    따라서 다음의 식이 성립한다.
    𝑉 𝑎𝑟(𝐶𝑗
    ) = 𝜆𝑗
    𝜆𝑗는 원 데이터 행렬의 eigenvalues 중 𝑗번째로 큰 값을 의미
    주성분의 설명력 시각화
    각 변수 별 분산을 순서대로 계산해서 바 그래프로 그려준다.
    import matplotlib.pyplot as plt
    plt.bar(range(1, 4), pca.explained_variance_ratio_);
    plt.show()
    178 | 회귀분석 파고들기
    8
    0.5 1.0 1.5 2.0 2.5 3.0 3.5
    0.0
    0.2
    0.4
    0.6
    0.8
    1.0
    • 각 주성분의 설명력을 시각화 해준다.
    그래프를 해석해보면 첫번째 변수 𝐶1가 전체 데이터 변동성의 90퍼센트가 넘는 부분을 설명하고
    있다고 말할 수 있다.
    다중공선성의 지표로서의 eigenvalue
    Condition indices ‑ 𝜅𝑝
    eigenvalue 들 중 유독 0에 가까운 작은 값이 존재한다면, 선형 독립화 과정에서 공선성이 존재하는
    변수들의 정보가 하나의 성분으로 합쳐졌음을 의미한다.
    • 이 사실을 이용해서 원 데이터에 다중 공선성이 존재하는지를 판단하는 기준을 만들 수 있다.
    • 다중공선성이 존재해서 𝑙𝑎𝑚𝑏𝑑𝑎𝑝값이 0과 아주 가까운 값을 갖게 된다면 왼쪽항이 발산하게
    됨.
    따라서, 우리가 가진 데이터에 다중공선성이 존재한다고 판단할 수 있다. 혹은 가장 큰 eigen value
    와 가장 작은 eigen value의 비율로서 측정할 수도 있는데, 이 경우 보통 15가 다중공선성이 있다고
    판단하는 기준치가 된다.
    𝜅𝑝 = √
    𝜆1
    𝜆𝑝
    ≥ 15
    print(np.sqrt(eig_values[0] / eig_values[2]) ^༺ 15)
    ^༈ True
    eigenvectors의 의미
    앞선 공분산 행렬에 대한 eigen value decomposition의 결과에는 eigenvector들도 저장이 되어
    있다.
    다중공선성을 대하는 우리들의 자세 | 179
    eig_vectors
    ^༈ array([[-0.57613845, -0.67939712, -0.45440515],
    ^༈ [-0.5754361 , 0.73197527, -0.36480886],
    ^༈ [-0.58046342, -0.05130072, 0.81266873]])
    이 정보는 주성분 분석으로 새로 만들어진 변수 𝐶𝑗들이 어떻게 만들어졌는지에 대한 정보들을 담고
    있다.
    x_to_pc = pd.DataFrame(pca.components_,
    columns=scaled.columns,
    index=['pca1','pca2','pca3']).round(3)
    x_to_pc
    ^༈ FAM PEER SCHOOL
    ^༈ pca1 0.576 0.575 0.580
    ^༈ pca2 -0.679 0.732 -0.051
    ^༈ pca3 0.454 0.365 -0.813
    단, pca 결과와와 eigen vector 행렬이 전치 (transpose) 관계, 그리고 부호가 다르다는 것을 유
    념하자. 이는 sklearn의 구현문제로 보이며, 결과적으로는 같은 행렬이어야만 한다. 즉, 위 행렬은 각
    변수 𝐶𝑗를 만들어내기 위해 사용된 표준화된 𝑋̃에 부여된 다음과 같은 식의 가중치를 나타낸다.
    𝐶1 = 0.576𝑋̃
    1 + 0.575𝑋̃
    2 + 0.580𝑋̃
    3
    𝐶2 = −0.679𝑋̃
    1 + 0.732𝑋̃
    2 − 0.051𝑋̃
    3
    𝐶3 = 0.454𝑋̃
    1 + 0.365𝑋̃
    2 − 0.813𝑋̃
    3
    8.5 Biplot을 사용한 변수 시각화
    주성분 분석에서 각 변수의 기여도를 시각화 하는 biplot 그래프를 구현한 함수이다.
    def biplot(score, coeff, pcax, pcay, labels=None):
    pca1=pcax-1
    pca2=pcay-1
    xs = score[:,pca1]
    ys = score[:,pca2]
    n=score.shape[1]
    scalex = 1.0/(xs.max()- xs.min())
    scaley = 1.0/(ys.max()- ys.min())
    plt.scatter(xs*scalex,ys*scaley)
    for i in range(n):
    plt.arrow(0, 0, coeff[pca1, i], coeff[pca2, i],color='r',alpha=0.5)
    180 | 회귀분석 파고들기
    8
    if labels is None:
    plt.text(coeff[pca1, i]* 1.15, coeff[pca2, i] * 1.15,
    "Var"+str(i+1), color='g', ha='center', va='center')
    else:
    plt.text(coeff[pca1, i]* 1.15, coeff[pca2, i] * 1.15,
    labels[i], color='g', ha='center', va='center')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.grid()
    biplot(pca_array, pca.components_, 1, 2,
    labels=scaled.columns)
    plt.show()
    1.00 0.75 0.50 0.25 0.00 0.25 0.50 0.75 1.00
    PC 1
    1.00
    0.75
    0.50
    0.25
    0.00
    0.25
    0.50
    0.75
    1.00
    PC 2
    FAM
    PEER
    SCHOOL
    빨간선의 의미를 잘 해석할 수 있어야한다. 많이 헷갈려하고, 현직 교수님들도 헷갈려하는 부분이다.
    잘 이해하고 있도록 한다.
    • school 변수의 파란색 화살표가 가로축 (Dim 1)과 거의 일치하게 그려져있는 것을 볼 수 있
    는데, 이것은 rotation에 담겨있는 정보 중 school에 해당하는 3번째 줄 값들 중 PC1와 PC2
    에 해당하는 0.580, −0.051 값을 나타내고 있다. 다음 행렬을 보면서, 각 화살표에 대한 해석
    연습을 해보자.
    x_to_pc
    ^༈ FAM PEER SCHOOL
    ^༈ pca1 0.576 0.575 0.580
    ^༈ pca2 -0.679 0.732 -0.051
    ^༈ pca3 0.454 0.365 -0.813
    Biplot을 사용한 변수 시각화 | 181
    즉, school 변수에 담긴 정보는 PC1을 만들때 상당한 기여를 했고, 반대로 PC2를 만들 때에는
    기여도가 작았다고 해석할 수 있다.
    Eigenvalue 값을 사용한 변수 관계 파악하기
    알고 있어야 하는 상식 하나. 상수 (Constant) 의 분산은 0이다.
    • 예: 숫자 3의 분산은 0이고, 기댓값은 3이다.
    • 𝑉 𝑎𝑟(𝐶𝑗
    ) = 𝜆𝑗
    , 만약 이 값이 0에 가깝다면? 상수라는 의미.
    • 𝔼[𝐶𝑗
    ] = 0, 왜냐하면 𝑋̃들을 다 스케일링을 했기 때문이다.
    min(pca.explained_variance_).round(3)
    ^༈ 0.008
    따라서, 다음과 같이 변수들 끼리의 관계를 파악해볼 수도 있다.
    𝐶3 = 0.454𝑋̃
    1 + 0.365𝑋̃
    2 − 0.813𝑋̃
    3
    𝑠𝑒𝑡 = 0
    주성분을 이용한 회귀분석
    선형 독립을 강제로 만들었다면 회귀분석을 수행할 수 있다.
    표준화된 회귀분석
    표준화된 데이터 행렬을 사용해서 회귀분석을 수행했을 경우 구해지는 계수들을 𝜃라고 하자.
    𝑌 = 𝜃 ̃
    1𝑋̃
    1 + 𝜃2𝑋̃
    2 + 𝜃3𝑋̃
    3 + 𝜖′
    알파 계수 계산하기
    선형 독립인 주성분들 PC1, PC2, PC3들을 사용해서 회귀분석을 돌렸을때 얻어지는 계수들을 𝑎𝑙𝑝ℎ𝑎
    들이라고 하자.
    𝑌 = 𝛼 ̃
    1𝐶1 + 𝛼2𝐶2 + 𝛼3𝐶3 + 𝜖′
    우리 예제의 경우 𝛼 계수들은 다음과 같이 구할 수 있다.
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LinearRegression
    reg3 = LinearRegression(fit_intercept=False)
    reg3.fit(my_pca, scaled_data[['ACHV']])
    ^༈ LinearRegression(fit_intercept=False)
    182 | 회귀분석 파고들기
    8
    reg3.coef_
    ^༈ array([[0.2498183 , 0.38775709, 1.41806458]])
    이렇게 구해진 PC1에 대한 계수들은 주성분들의 해석이 불가능하므로 사실상 해석이 불가능하게
    된다. 물론, Biplot을 통하여 각 주성분에 대한 해석 아이디어를 얻을 수도 있겠지만, 엄밀하게 말하면
    해석력이 떨어진다.
    • 생각해 볼 거리: 왜 회귀분석 모델식에 fit_intercept=False은 왜 들어갔을까?
    𝛼 계수를 통해서 𝜃 계수 복구하기
    • 구해진 𝛼 계수들은 eigen vector들을 이용해서 𝜃 계수들로 복구 할 수 있다.
    x_to_pc
    ^༈ FAM PEER SCHOOL
    ^༈ pca1 0.576 0.575 0.580
    ^༈ pca2 -0.679 0.732 -0.051
    ^༈ pca3 0.454 0.365 -0.813
    np.dot(reg3.coef_, x_to_pc)
    ^༈ array([[ 0.52440959, 0.94507728, -1.0277675 ]])
    𝜃 계수를 통해서 𝛽 계수 복구하기
    𝛽 계수들은 표준화가 되기 전의 변수에 대한 계수들이다. 이 𝛽 계수들 역시 다음의 식을 이용하여
    구해진 𝜃 계수들로부터 다시 복구할 수 있다.
    𝛽̂
    𝑗 =
    𝑠𝑦
    𝑠𝑗
    ̂ 𝜃𝑗
    𝛽̂
    0 = 𝑦 −
    3
    ∑
    𝑗=1
    𝛽̂
    𝑗
    주성분 분석 복귀 예시
    2개의 주성분 만을 이용하여 회귀분석 모델을 적합시켰다.
    my_pca['y'] = scaled_data[['ACHV']]
    my_pca.head()
    ^༈ pca1 pca2 pca3 y
    ^༈ 0 0.368955 -0.368726 0.124351 -0.199734
    ^༈ 1 0.956635 -0.150422 0.085339 0.345912
    Biplot을 사용한 변수 시각화 | 183
    ^༈ 2 -1.353829 0.063735 0.019803 -0.418312
    ^༈ 3 -2.102111 -0.129908 -0.194383 -0.979456
    ^༈ 4 -0.015266 -0.268837 -0.127596 -1.270798
    reg_pca = ols(formula='y ~ 0 + pca1 + pca2', data=my_pca).fit()
    reg_pca.params.values
    ^༈ array([0.2498183 , 0.38775709])
    위에서 구해진 알파 계수들을 사용하여 𝜃 계수들을 구하자.
    # theta coefficients
    theta = np.dot(reg_pca.params.values, x_to_pc.iloc[:2,])
    theta
    ^༈ array([-0.11939173, 0.42748371, 0.125119 ])
    𝑌 = −0.12 ̃ 𝑋̃
    1 + 0.43𝑋̃
    2 + 0.12𝑋̃
    3 + 𝜖′
    𝜃 계수들에서 𝛽 계수들에 대한 값을 복구해보자.
    𝑌 = 𝛽0 + 𝛽1𝑋1 + 𝛽2𝑋2 + 𝛽3𝑋3 + 𝜖
    scale_info = np.array(scaler.scale_)
    center_info = np.array(scaler.mean_)
    beta = (scale_info[0] / scale_info[1:4]) * theta
    beta_0 = center_info[0] - np.dot(center_info[1:4], beta)
    beta = np.concatenate(([beta_0], beta))
    beta
    ^༈ array([-0.02595669, -0.2505051 , 1.0505191 , 0.27781196])
    원래 데이터와 대응되는 회귀식은 다음과 같다.
    ̂𝑦 = −0.026 − 0.25𝑋1 + 1.05𝑋2 + 0.28𝑋3
    참고사항
    현재 ADP 시험장에서 제공되지 않는 pca 패키지를 사용하면, 다음과 같이 biplot을 그릴 수 있다. (단,
    사용하기 위해서는 설치가 필요)
    184 | 회귀분석 파고들기
    8
    # 설치코드: !pip install pca
    from pca import pca
    model = pca(n_components=3, normalize=False);
    model.fit_transform(scaled,
    col_labels = scaled.columns);
    ^༈ [pca] >Extracting row labels from dataframe.
    ^༈ [pca] >The PCA reduction is performed on the [3] columns of the input dataframe.
    ^༈ [pca] >Fit using PCA.
    ^༈ [pca] >Compute loadings and PCs.
    ^༈ [pca] >Compute explained variance.
    ^༈ [pca] >Outlier detection using Hotelling T2 test with alpha=[0.05] and n_components=[3]
    ^༈ [pca] >Multiple test correction applied for Hotelling T2 test: [fdr_bh]
    ^༈ [pca] >Outlier detection using SPE/DmodX with n_std=[3]
    model.biplot();
    ^༈ [pca] >Plot PC1 vs PC2 with loadings.
    ^༈
    ^༈ [scatterd] >INFO> Create scatterplot
    plt.show()
    3 2 1 0 1 2 3 4
    PC1 (98.3% expl.var)
    0.8
    0.6
    0.4
    0.2
    0.0
    0.2
    0.4
    0.6
    0.8
    PC2 (1.33% expl.var)
    3 Principal Components explain [99.99%] of the variance
    SCHOOL (0.58)
    PEER (0.732)
    FAM (-0.679)
    • 위 코드에서 scaled 데이터를 사용하였기 때문에 normalize = False로 설정해주었다.
    """