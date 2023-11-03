def s910():
    """
    제 9 장
    선형계획법 문제풀이
    선형계획법 예제
    슬통이는 두 가지 종류의 빵을 판매하는데, 초코빵을 만들기 위해서는 밀가루 100g과 초콜릿 10g이
    필요하고 밀빵을 만들기 위해서는 밀가루 50g이 필요하다. 재료비를 제하고 초코빵을 팔면 100원이
    남고 밀빵를 팔면 40원이 남는다. 오늘 슬통이는 밀가루 3000g과 초콜릿 100g을 재료로 갖고 있다.
    만든 빵을 전부 팔 수 있고 더 이상 재료 공급을 받지 않는다고 가정한다면, 슬통이는 이익을 극대화
    하기 위해서 어떤 종류의 빵을 얼마나 만들어야 하는가?1
    풀이
    𝑥1 을 초코빵을 만드는 개수, 𝑥2 를 밀빵을 만드는 개수로 설정하자. 그렇다면, 𝑥1
    , 𝑥2 는 정수값을
    가져야하며, 다음과 같은 조건하에서 이익을 최대로 만드는 문제의 해가 된다.
    𝑂𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒 ∶𝑚𝑎𝑥
    𝑧
    𝑧 = 100𝑥1 + 40𝑥2
    𝐶𝑜𝑛𝑠𝑡𝑟𝑎𝑖𝑛𝑡𝑠 ∶100𝑥1 + 50𝑥2 ≤ 3000,
    10𝑥1 ≤ 100,
    𝑥1
    , 𝑥2 ≥ 0.
    위의 문제를 다음과 같은 Python코드를 통하여 풀 수 있다.
    from scipy.optimize import linprog
    # 목적함수 계수 (최소화를 위해 음수로 설정)
    c = [-100, -40]
    # 제약조건 계수
    A = [[100, 50],
    [10, 0]]
    1해당 문제는 위키피디아의 선형계획법 페이지에서 가져옴.
    선형계획법 문제풀이 | 187
    # 제약조건 우변 값
    b = [3000, 100]
    # 변수의 하한
    x0_bounds = (0, None)
    x1_bounds = (0, None)
    # 선형계획법 문제 풀이
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')
    # 결과 출력
    print('Optimal value:', -res.fun, '\nX:', res.x)
    ^༈ Optimal value: 2600.0
    ^༈ X: [10. 40.]
    위의 문제를 그림으로 풀면 다음과 같다.
    선형계획법 기출
    순현가 가치를 최대화하는 투자 계획을 세우려고 한다. 정해진 예산은 1년차 50억, 2년차 60억, 3년차
    80억을 넘지 않는 선에서 포트폴리오를 운영하려고 할 때, 현재 가능한 최대 NPV를 달성할 수 있는
    최적의 투자안을 구하시오.
    1년차 2년차 3년차 NPV
    투자안 1 23 23 15 30
    투자안 2 15 15 12 20
    투자안 3 17 25 12 31
    투자안 4 16 12 13 42
    188 | 선형계획법 문제풀이
    9
    1년차 2년차 3년차 NPV
    투자안 5 24 23 17 44
    풀이
    𝑂𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒 ∶𝑚𝑎𝑥
    𝑧
    𝑧 = 30𝑥1 + 20𝑥2 + 31𝑥3 + 42𝑥4 + 44𝑥5
    𝐶𝑜𝑛𝑠𝑡𝑟𝑎𝑖𝑛𝑡𝑠 ∶23𝑥1 + 15𝑥2 + 17𝑥3 + 16𝑥4 + 24𝑥5 ≤ 50,
    23𝑥1 + 15𝑥2 + 25𝑥3 + 12𝑥4 + 23𝑥5 ≤ 60,
    15𝑥1 + 12𝑥2 + 12𝑥3 + 13𝑥4 + 17𝑥5 ≤ 80,
    𝑥1
    , 𝑥2
    , 𝑥3
    , 𝑥4
    , 𝑥5 ≥ 0.
    위의 문제 (해가 이진수) 를 직접적으로 푸는 파이썬 패키지는 ortools에 있으나, ADP의 기본적으로
    제공되는 패키지에 속하지는 않는다.
    import numpy as np
    from ortools.linear_solver import pywraplp
    # 투자안의 비용
    costs = np.array([[23, 23, 15],
    [15, 15, 12],
    [17, 25, 12],
    [16, 12, 13],
    [24, 23, 17]])
    # 각 투자안의 NPV
    npv = np.array([30, 20, 31, 42, 44])
    # 각 해에 대한 예산 제약조건
    budgets = np.array([50, 60, 80])
    # Solver 초기화
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # 변수 설정
    x = []
    for i in range(5): # 5개 투자안
    x.append(solver.IntVar(0.0, 1.0, 'x[%i]' % i))
    # 제약조건 설정
    for i in range(3): # 3년차
    solver.Add(sum(costs[j][i] * x[j] for j in range(5)) ^ཏ budgets[i])
    선형계획법 문제풀이 | 189
    # 목적함수 설정
    ^༈ <ortools.linear_solver.pywraplp.Constraint; proxy of <Swig Object of type ↩
    'operations_research^:MPConstraint *' at 0x000001ABA1FDCE10> >
    ^༈ <ortools.linear_solver.pywraplp.Constraint; proxy of <Swig Object of type ↩
    'operations_research^:MPConstraint *' at 0x000001ABA1FF6900> >
    ^༈ <ortools.linear_solver.pywraplp.Constraint; proxy of <Swig Object of type ↩
    'operations_research^:MPConstraint *' at 0x000001ABA1FB2630> >
    objective = solver.Objective()
    for i in range(5):
    objective.SetCoefficient(x[i], float(npv[i]))
    objective.SetMaximization()
    # Solver 실행
    solver.Solve()
    # 결과 출력
    ^༈ 0
    print('Maximum NPV: ', objective.Value())
    ^༈ Maximum NPV: 93.0
    print('Investment decisions for each project:')
    ^༈ Investment decisions for each project:
    for i in range(5):
    print('x[%i] = %i' % (i, x[i].solution_value()))
    ^༈ x[0] = 0
    ^༈ x[1] = 1
    ^༈ x[2] = 1
    ^༈ x[3] = 1
    ^༈ x[4] = 0
    위와 같은 문제는 다음의 코드처럼 주어진 모든 경우의 수를 구한 후, 제약에 걸리는 경우는 제외
    시키는 방법으로 구하는 게 훨씬 빠르다.
    190 | 선형계획법 문제풀이
    9
    import numpy as np
    from itertools import product
    # 각 투자안의 연간 비용과 NPV
    costs = np.array([[23, 23, 15],
    [15, 15, 12],
    [17, 25, 12],
    [16, 12, 13],
    [24, 23, 17]])
    npv = np.array([30, 20, 31, 42, 44])
    # 연간 예산
    budgets = np.array([50, 60, 80])
    # 가능한 모든 조합 생성
    comb = list(product([0, 1], repeat=5))
    # 조건을 만족하는 조합 및 그에 따른 NPV 계산
    valid_comb = []
    valid_npv = []
    for c in comb:
    total_costs = np.dot(c, costs)
    if np.all(total_costs ^ཏ budgets):
    valid_comb.append(c)
    valid_npv.append(np.dot(c, npv))
    # 최대 NPV 찾기
    max_npv_idx = np.argmax(valid_npv)
    optimal_comb = valid_comb[max_npv_idx]
    optimal_npv = valid_npv[max_npv_idx]
    print('Optimal investment plan: ', optimal_comb)
    ^༈ Optimal investment plan: (0, 1, 1, 1, 0)
    print('Maximum NPV: ', optimal_npv)
    ^༈ Maximum NPV: 93
    선형계획법 문제풀이 | 191

    10
    제 10 장
    로지스틱 회귀분석
    이항분포와 오즈
    오즈(Odds)의 개념
    로지스틱 회귀분석은 확률의 오즈를 선형모형으로 모델링하는 개념이다. 따라서 확률의 오즈가 무엇
    인지 먼저 알아보자.
    확률의 오즈(odds)란 어떤 사건이 발생할 확률과 그 사건이 발생하지 않을 확률의 비율을 말한다.
    즉,
    Odds of Event A =
    𝑃(𝐴)
    𝑃(𝐴𝑐)
    =
    𝑃 (𝐴)
    1 − 𝑃 (𝐴)
    와 같은 형태로 표현된다.
    예를 들어, 동전 던지기에서 앞면이 나올 확률이 1/2이라면, 앞면이 나올 오즈는 1/1, 즉, 1이 된다.
    import pandas as pd
    admission_data = pd.read_csv("./data/admission.csv")
    print(admission_data.shape)
    대학교 입학 데이터
    ^༈ (400, 5)
    print(admission_data.head())
    ^༈ admit gre gpa rank gender
    ^༈ 0 0 380 3.61 3 M
    ^༈ 1 1 660 3.67 3 F
    ^༈ 2 1 800 4.00 1 F
    로지스틱 회귀분석 | 193
    ^༈ 3 1 640 3.19 4 M
    ^༈ 4 0 520 2.93 4 M
    다음은 학교 입학 데이터이다. 데이터에서 입학이 허가될 확률의 오즈를 구해보자.
    p_hat = admission_data['admit'].mean()
    p_hat / (1 - p_hat)
    ^༈ 0.4652014652014652
    입학할 확률에 대한 오즈는 0.465가 된다. 즉, 입학에 실패할 확률의 46%정도이다. 즉, 오즈가 1을
    기준으로 낮을 경우, 발생하기 어렵다는 뜻이다.
    범주형 변수를 사용한 오즈 계산 이 데이터에는 rank 변수가 존재한다. 각 범주별 입학에 대한 오즈를
    계산할 수도 있다.
    unique_ranks = admission_data['rank'].unique()
    print(unique_ranks)
    ^༈ [3 1 4 2]
    1에서부터 4등급까지 존재하는 것을 확인했다. 각 등급별 입학에 대한 오즈를 구해보자.
    grouped_data = admission_data.groupby('rank').agg(p_admit=('admit', 'mean'))
    grouped_data['odds'] = grouped_data['p_admit'] / (1 - grouped_data['p_admit'])
    print(grouped_data)
    ^༈ p_admit odds
    ^༈ rank
    ^༈ 1 0.540984 1.178571
    ^༈ 2 0.357616 0.556701
    ^༈ 3 0.231405 0.301075
    ^༈ 4 0.179104 0.218182
    1등급 학생들이 입학에 성공할 확률은 입학에 실패할 확률보다 18% 더 높으며, 나머지 등급의
    학생들은 입학할 확률이 입학에 실패할 확률보다 더 낮다는 것을 확인할 수 있다.
    오즈(Odds)를 사용한 확률 역산 Odds가 주어졌을 때, 위의 관계를 사용하여 역으로 확률을 계산할
    수 있다.
    ̂𝑝 = 𝑂𝑑𝑑𝑠
    𝑂𝑑𝑑𝑠 + 1
    앞에서 살펴본 1등급 학생들의 오즈를 사용하여 입학할 확률을 계산해보자.
    194 | 로지스틱 회귀분석
    10
    1.178 / (1.178 + 1)
    ^༈ 0.5408631772268135
    로그 오즈
    일반 회귀에서는 종속변수 𝑌 를 독립변수들의 선형결합으로 모델링하였다. 로지스틱 회귀에서는
    확률을 독립변수들의 선형결합으로 모델링하고 싶다. 하지만, 확률이라는 것은 0과 1사이의 값을
    가지게 되고, 모델링하는 선형결합은 −∞에서 ∞까지의 값을 가지므로, 이것을 그대로 종속변수로
    사용할 수는 없다. 로지스틱 회귀분석에서는 앞에서 배운 오즈에 로그를 씌운 로그 오즈를 이용하여
    −∞에서 ∞까지의 값으로 늘려준다.
    𝑙𝑜𝑔 ( 𝑝
    1 − 𝑝) = 𝛽0 + 𝛽1𝑥1 + ... + 𝛽𝑝𝑥𝑝
    확률값 𝑝에 대하여 로그 오즈값의 그래프를 그리면 다음과 같다.
    import numpy as np
    import matplotlib.pyplot as plt
    p = np.arange(0, 1.01, 0.01)
    log_odds = np.log(p / (1 - p))
    plt.plot(p, log_odds)
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA203F308>]
    plt.xlabel('p')
    ^༈ Text(0.5, 0, 'p')
    plt.ylabel('log_odds')
    ^༈ Text(0, 0.5, 'log_odds')
    plt.title('Plot of log odds')
    ^༈ Text(0.5, 1.0, 'Plot of log odds')
    plt.show()
    로지스틱 회귀분석 | 195
    0.0 0.2 0.4 0.6 0.8 1.0
    p
    4
    2
    0
    2
    4
    log_odds
    Plot of log odds
    로지스틱 회귀계수 예측 아이디어
    로지스틱 회귀분석의 계수를 구하는 내용은 MLE를 사용하여 구하는 것이다. 구하는 방식에 대한
    설명은 추후 슬기로운 통계생활 채널 영상으로 대체하겠다. 여기서는 변수의 레벨이 가장 간단한 성별
    변수를 사용하여 계수를 예측해보자.
    odds_data = admission_data.groupby('rank').agg(p_admit=('admit', 'mean')).reset_index()
    odds_data['odds'] = odds_data['p_admit'] / (1 - odds_data['p_admit'])
    odds_data['log_odds'] = np.log(odds_data['odds'])
    print(odds_data)
    ^༈ rank p_admit odds log_odds
    ^༈ 0 1 0.540984 1.178571 0.164303
    ^༈ 1 2 0.357616 0.556701 -0.585727
    ^༈ 2 3 0.231405 0.301075 -1.200395
    ^༈ 3 4 0.179104 0.218182 -1.522427
    rank 변수가 범주형이긴 하지만 순서가 있는 변수이기 때문에 수치형 변수라고 생각하고 회귀직선
    을 구해보자. 로지스틱 회귀분석의 계수를 이런식으로 추정하는 것이 아니지만, 아이디어를 충분히
    잡아내는 방식이라 생각한다.
    import statsmodels.api as sm
    model = sm.formula.ols("log_odds ~ rank", data=odds_data).fit()
    print(model.summary())
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: log_odds R༡squared: 0.972
    196 | 로지스틱 회귀분석
    10
    ^༈ Model: OLS Adj. R༡squared: 0.957
    ^༈ Method: Least Squares F༡statistic: 68.47
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 0.0143
    ^༈ Time: 14:02:22 Log-Likelihood: 3.2107
    ^༈ No. Observations: 4 AIC: -2.421
    ^༈ Df Residuals: 2 BIC: -3.649
    ^༈ Df Model: 1
    ^༈ Covariance Type: nonrobust
    ^༈ ==============================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ ------------------------------------------------------------------------------
    ^༈ Intercept 0.6327 0.188 3.368 0.078 -0.175 1.441
    ^༈ rank -0.5675 0.069 -8.275 0.014 -0.863 -0.272
    ^༈ ==============================================================================
    ^༈ Omnibus: nan Durbin-Watson: 2.037
    ^༈ Prob(Omnibus): nan Jarque-Bera (JB): 0.602
    ^༈ Skew: -0.062 Prob(JB): 0.740
    ^༈ Kurtosis: 1.103 Cond. No. 7.47
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    이 직선과 주어진 로그 오즈를 시각화해보자.
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.scatterplot(data=odds_data, x='rank', y='log_odds')
    ^༈ <AxesSubplot:xlabel='rank', ylabel='log_odds'>
    sns.regplot(data=odds_data, x='rank', y='log_odds', ci=None)
    ^༈ <AxesSubplot:xlabel='rank', ylabel='log_odds'>
    plt.show()
    로지스틱 회귀분석 | 197
    1 2 3 4
    rank
    1.5
    1.0
    0.5
    0.0
    log_odds
    로지스틱 회귀계수 해석 아이디어
    앞의 회귀모델의 경우 절편의 의미가 불분명한 모델이지만, 여기서 주의 깊게 봐야 할 것은 기울기
    계수인 -0.5675 값을 어떻게 해석할 것인가이다. 회귀분석의 경우를 떠올리면 다음과 같이 해석할 수
    있다.
    rank가 1 단위 증가하면, y변수, 즉, 로그 오즈가 0.5675 만큼 “감소”한다. 하지만, 이러한 해석은
    직관적으로 받아들이기가 어려우므로, 이 계수를 앞에서 살펴본 Odds를 구하는 방식으로 변형해보자.
    𝑙𝑜𝑔 ( 𝑝(𝑥𝑟𝑎𝑛𝑘)
    1 − 𝑝(𝑥𝑟𝑎𝑛𝑘)
    ) = 0.6327 − 0.5675𝑥𝑟𝑎𝑛𝑘
    양변에 지수를 취하여 왼쪽을 오즈로 만든다.
    𝑂𝑑𝑑𝑠(𝑥𝑟𝑎𝑛𝑘) = 𝑝(𝑥𝑟𝑎𝑛𝑘)
    1 − 𝑝(𝑥𝑟𝑎𝑛𝑘)
    = 𝑒𝑥𝑝(0.6327 − 0.5675𝑥𝑟𝑎𝑛𝑘)
    이렇게 쓰게 되면 좋은 점이 하나있는데, 지수의 성질을 이용해서 ‑0.5675라는 계수값만 딱 떨어뜨
    려놓을 수 있게 된다.
    오즈비 (Odds ratio) rank가 x일때의 오즈와, 한 단위 증가한 x+1일때의 오즈를 분수꼴로 놓아보
    자. 이러한 값을 오즈들의 비율이라는 의미로 오즈비 (Odds ratio)라고 부른다.
    𝑂𝑑𝑑𝑠(𝑥𝑟𝑎𝑛𝑘 + 1)
    𝑂𝑑𝑑𝑠(𝑥𝑟𝑎𝑛𝑘)
    =
    𝑒𝑥𝑝(0.6327 − 0.5675(𝑥𝑟𝑎𝑛𝑘 + 1))
    𝑒𝑥𝑝(0.6327 − 0.5675𝑥𝑟𝑎𝑛𝑘)
    = 𝑒𝑥𝑝(−0.5675) ≈ 0.567
    즉, rank가 한 단위 증가할 때마다, Odds가 이전 오즈의 약 절반 가량 (56%)으로 감소하는 경향을
    보인다. 이것은 앞에서 계산했던 rank별 오즈의 경향성과 일치한다.
    selected_data = odds_data[['rank', 'p_admit', 'odds']]
    selected_data['odds_frac'] = selected_data['odds'] / selected_data['odds'].shift(1, fill_value=selected_data['odds'].iloc[0])
    198 | 로지스틱 회귀분석
    10
    print(selected_data)
    ^༈ rank p_admit odds odds_frac
    ^༈ 0 1 0.540984 1.178571 1.000000
    ^༈ 1 2 0.357616 0.556701 0.472352
    ^༈ 2 3 0.231405 0.301075 0.540820
    ^༈ 3 4 0.179104 0.218182 0.724675
    오즈를 이용한 확률 역산 앞에서 오즈를 알고있다면, 이를 이용해서 확률을 역산하는 방법을 알아보
    았다. 따라서, 오즈에 대한 식을 사용하여 확률 𝑝(𝑥𝑟𝑎𝑛𝑘)는 다음과 같이 쓸 수 있다.
    𝑝(𝑥𝑟𝑎𝑛𝑘) = 𝑒𝑥𝑝(0.6327 − 0.5675𝑥𝑟𝑎𝑛𝑘)
    1 + 𝑒𝑥𝑝(0.6327 − 0.5675𝑥𝑟𝑎𝑛𝑘)
    위 식을 이용하면 각 랭크별 입학 확률을 다음과 같이 계산할 수 있다.
    rank_vec = np.array([1, 2, 3, 4])
    result = np.exp(0.6327 - 0.5675 * rank_vec) / (1 + np.exp(0.6327 - 0.5675 * rank_vec))
    print(result)
    ^༈ [0.51629423 0.37700031 0.25544112 0.16283279]
    그리고 이러한 추세를 rank변수가 −∞에서∞까지 값을 갖는 연속형 변수라고 놓았을 때는 다음과
    같이 추세선을 그려볼 수 있다.
    Python에서 로지스틱 회귀분석 하기
    앞에서 살펴본 admission 데이터를 사용하여 로지스틱 회귀분석 모델을 만들고 결과를 살펴보자.
    import statsmodels.api as sm
    admission_data['rank'] = admission_data['rank'].astype('category')
    admission_data['gender'] = admission_data['gender'].astype('category')
    model = sm.formula.logit("admit ~ gre + gpa + rank + gender", data=admission_data).fit()
    ^༈ Optimization terminated successfully.
    ^༈ Current function value: 0.573066
    ^༈ Iterations 6
    로지스틱 회귀분석 | 199
    print(model.summary())
    ^༈ Logit Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: admit No. Observations: 400
    ^༈ Model: Logit Df Residuals: 393
    ^༈ Method: MLE Df Model: 6
    ^༈ Date: 토, 28 10 2023 Pseudo R༡squ.: 0.08305
    ^༈ Time: 14:02:25 Log-Likelihood: -229.23
    ^༈ converged: True LL-Null: -249.99
    ^༈ Covariance Type: nonrobust LLR p༡value: 2.283e-07
    ^༈ ===============================================================================
    ^༈ coef std err z P>|z| [0.025 0.975]
    ^༈ -------------------------------------------------------------------------------
    ^༈ Intercept -3.9536 1.149 -3.442 0.001 -6.205 -1.702
    ^༈ rank[T.2] -0.6723 0.317 -2.123 0.034 -1.293 -0.052
    ^༈ rank[T.3] -1.3422 0.345 -3.887 0.000 -2.019 -0.665
    ^༈ rank[T.4] -1.5529 0.418 -3.717 0.000 -2.372 -0.734
    ^༈ gender[T.M] -0.0578 0.228 -0.254 0.800 -0.504 0.388
    ^༈ gre 0.0023 0.001 2.062 0.039 0.000 0.004
    ^༈ gpa 0.8032 0.332 2.420 0.016 0.153 1.454
    ^༈ ===============================================================================
    절편에 대한 계수는 일반적으로 해석하지 않는다.
    • gre (0.0023): GRE 점수가 1점 증가할 때마다 합격 로그 오즈가 0.0023만큼 증가합니다. 이는
    GRE 점수가 1점 증가할 때마다 합격에 대한 오즈가 약 0.2% 증가합니다.
    • gpa (0.8032): GPA가 1점 증가할 때마다 합격 로그 오즈가 0.8032만큼 증가합니다. 이는 GPA
    가 1점 증가할 때마다 합격에 대한 오즈가 약 123% 증가합니다
    import math
    math.exp(0.0023)
    ^༈ 1.002302647029
    math.exp(0.8032)
    ^༈ 2.232674066397348
    • gender (‑0.0578): 성별이 남성인 학생은 여성 학생에 비해 합격 로그 오즈가 0.0578만큼 낮
    습니다. 이는 여학생 그룹과 남학생 그룹의 합격에 대한 오즈비가 0.943으로 1보다 작습니다.
    그러나 p 값이 0.800으로, 이 변수의 계수는 통계적으로 유의하지 않다고 볼 수 있습니다. 즉, 이
    데이터에서 성별이 합격 여부에 큰 영향을 미치지 않는 것으로 보입니다.
    200 | 로지스틱 회귀분석
    10
    math.exp(-0.0578)
    ^༈ 0.9438386963005431
    각 계수 검정하기 with Wald test
    귀무가설: 𝛽𝑖 = 0 을 검정하기 위한 검정통계량은 다음과 같다.
    𝑧 =
    𝛽 ̂
    𝑖
    𝑆𝐸𝛽̂
    𝑖
    ∼ 𝒩(0, 12
    )
    따라서 유의수준 5%하에서 gre의 계수가 0이라는 귀무가설을 기각할 수 있다.
    import scipy.stats as stats
    result1 = 0.002256 / 0.001094
    result2 = 2 * (1 - stats.norm.cdf(result1))
    print(result1)
    ^༈ 2.0621572212065815
    print(result2)
    ^༈ 0.03919277001389343
    각 Odds ratio에 대한 신뢰구간 구하기
    앞에서 기울기 𝛽에 대한 검정이 Wald 검정을 사용하는 것을 생각해보면, 기울기에 대한 신뢰구간을
    다음과 같이 구할 수 있을 것이라 생각할 수 있다.
    𝛽𝑖 ± 𝑧∗𝑆𝐸𝑏1
    따라서 오즈비(Odds ratio)는 𝑒
    𝛽이므로 신뢰구간 을 구할 때, 기울기에 대한 신뢰구간에 지수꼴을
    취해주면 된다.
    (𝑒𝛽𝑖−𝑧∗𝑆𝐸𝑏1 , 𝑒𝛽𝑖+𝑧∗𝑆𝐸𝑏1 )
    따라서, gre 변수의 계수 0.002256에 대한 95% 신뢰구간은 다음과 같다.
    import scipy.stats as stats
    a = round(model.params[1] - stats.norm.ppf(0.975) * 0.001094, 3)
    b = round(model.params[1] + stats.norm.ppf(0.975) * 0.001094, 3)
    로지스틱 회귀분석 | 201
    glue_str = f"({a}, {b})"
    print(glue_str)
    ^༈ (-0.674, -0.67)
    추가적으로 오즈비에 대한 신뢰구간을 구해보자. 이미 계산이 다 되어있기 때문에 간단하게 구할 수
    있다.
    a = round(np.exp(a), 3)
    b = round(np.exp(b), 3)
    glue_str = f"({a}, {b})"
    print(glue_str)
    ^༈ (0.51, 0.512)
    LR test: 회귀모델이 유의한가?
    일반 선형회귀에서는 F 검정을 사용해서 모델의 유의성을 체크했는데, 로지스틱 회귀분석의 경우
    Likelihood ratio 검정을 진행한다. 이 검정의 귀무가설과 대립가설은 다음과 같다.
    귀무가설: 모든 베타 계수들이 0이다. 대립가설: 0이 아닌 베타 계수가 존재한다.
    이 검정의 검정통계량은 다음과 같다.
    Λ = −2(ℓ(𝛽)̂(0) − ℓ(𝛽)) ∼ 𝜒 ̂ 2
    𝑘−𝑟
    위 식에서 ℓ(𝛽)̂(0) 부분은 귀무가설 하에서의 로그 우도함수 값을 나타낸다. R의 결과에서는 Null
    에서의 deviance 값과 Residual deviance 값을 보여주고 있다. 이것은 위 식에서 ‑2 곱하기 각 로
    그우도 함수값을 나타낸다. 따라서 위의 Λ값은 Null deviance에서 Residual deviance 값을 빼서
    구할 수 있다. 따라서, 검정통계량 값을 계산해보면, 다음과 같다.
    𝐺2 = 499.98 − 458.45
    위의 검정통계량은 카이제곱분포 자유도가 두 모델의 자유도 차를 따르게 되므로, 다음과 같이
    p‑value를 구할 수 있다.
    계산된 p‑value 값, 2.286918e-07으로 보아 주어진 로지스틱 회귀모델은 통계적으로 유의하다라고
    판단한다.
    참고자료
    본 챕터의 데이터와 내용은 많은 부분 UCLA 로지스틱 회귀분석 자료를 참고하였음을 밝힙니다.
    """