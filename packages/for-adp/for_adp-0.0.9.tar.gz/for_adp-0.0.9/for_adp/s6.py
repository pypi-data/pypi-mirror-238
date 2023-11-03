def s6():
    """
    제 6 장
    ANOVA: Analysis of Variance
    6.1 Analysis of Variance
    분산 분석(ANOVA)은 이름에서 짐작할 수 있듯이 분산에 대한 검정처럼 들릴 수 있지만, 실제로는
    그렇지 않습니다. ANOVA는 주로 3개 이상의 집단에서 평균의 차이를 검정하기 위해 사용되는 통계적
    방법입니다.
    그룹을 나누는 기준이 되는 변수의 개수에 따라서 ANOVA의 종류도 다양해집니다.
    • One way ANOVA: 이 방법은 한 가지 관심 변수에 따라 그룹을 나누고 그룹 간의 평균 차이를
    검정합니다. 예를 들어, 다양한 브랜드의 제품 효과를 비교할 때 사용될 수 있습니다.
    • Two way ANOVA: 이 방법은 두 가지 관심 변수를 기준으로 그룹을 나누어 평균의 차이를 검
    정합니다. 이것은 두 가지 다른 변수가 결과에 어떤 영향을 미치는지를 동시에 알아보기 위해
    사용됩니다. 예를 들면, 제품 브랜드와 사용자의 연령대를 기준으로 제품의 효과를 비교하는
    경우에 적용될 수 있습니다.
    6.2 One‑way ANOVA
    모델 가정
    One‑way ANOVA 모델은 하나의 독립 변수에 따라 그룹 간의 평균 차이를 검정하기 위해 사용됩니다.
    이 모델에서는 데이터가 다음과 같은 원리로 발생한다고 가정합니다:
    𝑥𝑖𝑗 = 𝜇𝑖 + 𝜖𝑖𝑗
    여기서: ‑ 𝑥𝑖𝑗는 𝑖번째 집단의 𝑗번째 관찰값을 나타냅니다. ‑ 𝜇𝑖는 𝑖번째 집단의 평균을 나타냅니다.
    ‑ 𝜖𝑖𝑗는 오차항으로, 각 관찰값에 더해지는 랜덤한 변동을 나타냅니다.
    • 𝑖는 집단의 번호를 나타내며, 𝑖 = 1, ..., 𝑘로서 총 𝑘개의 집단이 있습니다.
    • 𝑗는 각 집단 내에서의 관찰값의 번호를 나타내며, 𝑗 = 1, ..., 𝑛𝑖로서 𝑖번째 집단에는 총 𝑛𝑖개의
    관찰값이 있습니다.
    • 𝜖𝑖𝑗의 분포는 정규 분포로, 평균이 0이며 분산이 𝜎
    2입니다.
    ANOVA: Analysis of Variance | 115
    이러한 가정 하에서, 각 집단 𝑖에서는 𝑛𝑖개의 표본이 관찰됩니다.
    중요한 가정
    One‑way ANOVA 모델을 사용할 때 고려해야 하는 몇 가지 중요한 가정들이 있습니다.
    정규성 모든 에러항은 정규 분포를 따라야 합니다.
    모델 적합 후 에러항의 분포를 체크하는 것은 매우 중요합니다. 이를 통해 모델의 가정이 유효한지
    확인할 수 있습니다.
    등분산성 모든 그룹에서의 에러항의 분산은 동일해야 합니다.
    독립성 각 집단 𝑖의 관찰값은 서로 독립적이며, 각 집단은 정규분포 평균 𝜇𝑖 와 분산 𝜎
    2 를 따라야
    합니다.
    귀무가설과 대립가설
    • 𝐻0
    : 모든 집단의 평균이 동일하다.
    – 𝜇1 = 𝜇2 = ... = 𝜇𝑘
    • 𝐻𝐴: 평균이 다른 집단이 적어도 하나 존재한다.
    – Not all of 𝜇1
    , 𝜇2
    , ... and 𝜇𝑘
    are equal.
    ANOVA의 핵심 아이디어
    데이터 분해
    ANOVA의 아이디어는 전체 데이터의 변동성을 분해하면 두 가지로 분리할 수 있다는 것에서부터
    시작합니다.
    그룹간 변동성과 그룹 안에서의 변동성 데이터의 변동성을 측정하는 도구로써 SS (Sums of squares)
    라는 개념을 사용합니다.
    • SST (Sums of Squares for Total): 각 데이터와 전체 평균과의 변동성
    • SSG (Sums of Squares for Groups): 각 그룹 평균과 전체 평균과의 변동성
    • SSE (Sums of Squares for Error): 각 데이터와 대응하는 그룹 평균과의 변동성
    𝑘
    ∑
    𝑖=1
    𝑛𝑗
    ∑
    𝑗=1
    (𝑋𝑖𝑗 − 𝑋..)
    2
    𝑆𝑆𝑇
    =
    𝑘
    ∑
    𝑖=1
    𝑛𝑖
    (𝑋𝑖. − 𝑋..)
    2
    𝑆𝑆𝐺
    +
    𝑘
    ∑
    𝑖=1
    𝑛𝑗
    ∑
    𝑗=1
    (𝑋𝑖𝑗 − 𝑋𝑖.)
    2
    𝑆𝑆𝐸
    • 𝑛 = ∑𝑘
    𝑖=1 𝑛𝑖
    •
    𝑆𝑆𝐺
    𝜎2 ∼ 𝜒2
    𝑘−1
    •
    𝑆𝑆𝐸
    𝜎2 ∼ 𝜒2
    𝑛−𝑘
    자세한 증명은 Hogg 책 ANOVA 파트 참조.
    116 | ANOVA: Analysis of Variance
    6
    검정 통계량
    ANOVA에서 중요한 검정 통계량은 F 값입니다. 이는 그룹 간과 그룹 내의 분산을 비교하기 위해 사용
    되며, F 분포를 따릅니다.
    𝐹 = 𝑀𝑆𝐺
    𝑀𝑆𝐸 =
    그룹 간 평균들의 분산
    그룹 안에서 분산
    여기서,
    • MSG는 그룹 간의 평균 제곱 오차로, 각 그룹의 평균과 전체 평균 간의 차이를 기반으로 계산됩
    니다.
    𝑀𝑆𝐺 = 𝑛1
    (𝑋1 − 𝑋)2 + … + 𝑛𝑘
    (𝑋𝑘 − 𝑋)2
    𝑘 − 1
    • MSE는 그룹 내의 평균 제곱 오차로, 각 그룹 내의 분산을 기반으로 계산됩니다.
    𝑀𝑆𝐸 = (𝑛1 − 1)𝑠2
    1 + … + (𝑛𝑘 − 1)𝑠2
    𝑘
    𝑛 − 𝑘
    F 값은 그룹 간의 평균 차이가 그룹 내의 변동에 비해 얼마나 큰지를 측정합니다. F 값이 크면 그룹
    간의 차이가 유의미하다는 것을 나타냅니다.
    MSE의 의미
    MSE는 여러 그룹 내의 표본 분산을 통합하여 모분산을 추정하는 방법입니다. 이를 pooled variance
    라고도 부릅니다.
    • 특징: 𝑘개의 그룹 크기를 고려하여 가중 평균을 구함
    이렇게 해서 각 그룹의 표본 수와 분산을 모두 반영하여 전체 분산을 추정하게 됩니다.
    𝑠
    2
    𝑝 =
    (𝑛1 − 1) 𝑠2
    1 + (𝑛2 − 1) 𝑠2
    2 + ... + (𝑛𝑘 − 1) 𝑠2
    𝑘
    (𝑛1 − 1) + (𝑛2 − 1) + ... + (𝑛𝑘 − 1)
    왜 작동할까?
    ANOVA의 핵심 아이디어는 각 그룹의 평균이 전체 평균에서 얼마나 움직이는지와 그룹 내의 개별
    표본이 그룹 평균에서 얼마나 움직이는지를 비교하는 것입니다.
    • 𝐹 값이 작으면: 그룹 간의 차이가 그룹 내의 차이에 비해 작다는 것을 나타냅니다. 이는 귀무가
    설이 참일 가능성이 높음을 의미합니다.
    • 𝐹 값이 크면: 그룹 간의 차이가 그룹 내의 차이에 비해 크다는 것을 나타냅니다. 이는 귀무가설이
    거짓일 가능성이 높음을 의미합니다.
    이 때, 𝐹 통계량은 𝐹𝑘−1,𝑛−𝑘 분포를 따릅니다. 여기서, 𝑘 − 1과 𝑛 − 𝑘는 각각 그룹 간과 그룹
    내의 자유도를 나타냅니다.
    One‑way ANOVA | 117
    ANOVA 예제
    데이터 불러오기
    데이터를 불러오기 위해 pandas 라이브러리를 사용하고, read_csv 함수로 데이터 파일을 불러옵니다.
    그 후, head() 함수를 사용하여 데이터의 첫 5행을 확인합니다.
    import pandas as pd
    anova_data = pd.read_csv('./data/anova_example.csv')
    anova_data.head()
    ^༈ Minutes Odor
    ^༈ 0 92 Lavender
    ^༈ 1 126 Lavender
    ^༈ 2 114 Lavender
    ^༈ 3 106 Lavender
    ^༈ 4 89 Lavender
    데이터 살펴보기
    데이터를 더 깊게 살펴보기 위해, 각 Odor 그룹에 대한 기술 통계량을 계산합니다. 이를 위해 groupby
    와 describe 함수를 사용하여 그룹별 평균, 표준편차, 최소값, 최대값 등의 통계량을 얻을 수 있습니다.
    anova_data.groupby(['Odor']).describe()
    ^༈ Minutes
    ^༈ count mean std min 25% 50% 75% max
    ^༈ Odor
    ^༈ Lavender 14.0 107.142857 17.302099 76.0 94.25 105.5 121.5 137.0
    ^༈ Lemon 14.0 88.642857 14.457402 63.0 75.75 88.5 100.0 112.0
    ^༈ No_odor 15.0 87.466667 16.282623 68.0 72.50 85.0 97.5 121.0
    ANOVA 실행하기
    ANOVA 분석을 위해 statsmodels 라이브러리를 사용합니다. ols() 함수를 사용하여 선형 회귀 모델을
    만들고, 이를 기반으로 anova_lm() 함수를 통해 ANOVA 분석을 수행합니다.
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    model = ols('Minutes ~ Odor', data=anova_data).fit()
    result = sm.stats.anova_lm(model)
    print(result)
    118 | ANOVA: Analysis of Variance
    6
    ^༈ df sum_sq mean_sq F PR(>F)
    ^༈ Odor 2.0 3457.524142 1728.762071 6.700198 0.003093
    ^༈ Residual 40.0 10320.661905 258.016548 NaN NaN
    위의 결과는 ANOVA 표라고 불리며, 검정통계량 𝐹 값 6.7에 대응하는 p‑value는 0.003이라는 것을
    알 수 있습니다.
    가정 체크
    ANOVA에서 가정을 체크하는 것은 중요합니다. 가정이 만족되지 않으면 ANOVA의 결과를 신뢰하기
    어렵습니다. 가정 중 하나는 잔차들의 정규성입니다.
    잔차들의 정규성
    모델의 잔차를 적합값에 대해 시각화하여 잔차의 분포와 패턴을 확인합니다. 주어진 그래프에서 잔차
    들은 0을 중심으로 분포되어 있으며, 어떤 특정한 패턴 없이 무작위로 분포되어 있어야 합니다.
    import matplotlib.pyplot as plt
    residuals = model.resid
    fitted_values = model.fittedvalues
    plt.scatter(fitted_values, residuals)
    plt.show()
    87.5 90.0 92.5 95.0 97.5 100.0 102.5 105.0 107.5
    30
    20
    10
    0
    10
    20
    30
    또한, 잔차들의 분포가 정규분포를 따르는지도 확인해야 합니다. pingouin 라이브러리를 사용하여
    Q‑Q 그래프를 그려 확인하도록 하겠습니다.
    import pingouin as pg
    residuals = model.resid
    One‑way ANOVA | 119
    ax = pg.qqplot(residuals, dist='norm')
    plt.ylim(-3, 3)
    ^༈ (-3.0, 3.0)
    plt.xlim(-3, 3)
    ^༈ (-3.0, 3.0)
    plt.show()
    3 2 1 0 1 2 3
    Theoretical quantiles
    3
    2
    1
    0
    1
    2
    3
    Ordered quantiles
    R
    2 = 0.977
    Shapiro‑Wilk 검정을 통하여 잔차의 정규성을 통계적으로 검정합니다.
    from scipy import stats
    W, p = stats.shapiro(residuals)
    print(round(W, 3), round(p, 3))
    ^༈ 0.971 0.353
    검정통계량 W값 0.971에 대응하는 p‑value 0.353이 유의 수준 0.05보다 크므로, 잔차가 정규분
    포를 따른다는 귀무가설을 기각할 수 없습니다. 따라서 정규성 가정을 만족한다고 판단합니다.
    등분산 가정 체크
    • 각 그룹별 상자그림 그려보기
    120 | ANOVA: Analysis of Variance
    6
    import seaborn as sns
    sns.set_palette(["#00AFBB", "#E7B800", "#FC4E07"])
    sns.boxplot(x = "Odor", y = "Minutes", data = anova_data, order = ["Lavender", "Lemon", "No_odor"])
    plt.xlabel("Odor")
    plt.ylabel("Minutes")
    plt.show()
    Lavender Lemon No_odor
    Odor
    60
    70
    80
    90
    100
    110
    120
    130
    140
    Minutes
    잔차들을 그룹별로 묶어서 Levene 검정을 실시할 수 있습니다.
    from scipy.stats import levene
    odor_groups = [anova_data[anova_data['Odor'] ^༰ odor_type]['Minutes'] for odor_type in anova_data['Odor'].unique()]
    W, p = levene(*odor_groups, center = 'mean')
    print(W, p)
    ^༈ 0.17643170248475967 0.8389048016208949
    검정통계량 값 0.132에 대응하는 p‑value가 0.87이므로 유의수준 0.05보다 큽니다. 따라서 각
    그룹별 분산이 같다는 귀무가설을 기각하지 못하므로, 등분산 가정을 만족한다고 판단합니다.
    사후 검정
    ANOVA는 여러 그룹 간의 평균 차이가 유의미한지만을 판단합니다. 만약 ANOVA 결과에서 귀무가설
    이 기각된다면, 어떤 그룹 간에 평균 차이가 유의미하게 나타났는지를 알기 위해 사후 검정 (post‑hoc
    test)을 수행해야 합니다.
    • 귀무가설 𝐻0
    : 𝜇𝐿𝑎𝑣𝑒𝑛𝑑𝑒𝑟 = 𝜇𝐿𝑒𝑚𝑜𝑛 = 𝜇𝑁𝑜 𝑜𝑑𝑜𝑟
    평균이 다른 그룹이 존재한다는 것은 판명이 났지만, 어느 그룹이 다른지 모르는 상황!
    One‑way ANOVA | 121
    추가 검정 가설
    • 𝜇𝐿𝑎𝑣𝑒𝑛𝑑𝑒𝑟 = 𝜇𝐿𝑒𝑚𝑜𝑛
    • 𝜇𝐿𝑒𝑚𝑜𝑛 = 𝜇𝑁𝑜 𝑜𝑑𝑜𝑟
    • 𝜇𝐿𝑎𝑣𝑒𝑛𝑑𝑒𝑟 = 𝜇𝑁𝑜 𝑜𝑑𝑜𝑟
    위에서 제시한 세 개의 추가 검정 가설을 각각 t‑test로 검정하려면, 여러 번의 t‑test를 수행하는
    것이므로 유의수준을 조정해야 합니다.
    Bonferrorni
    이를 위해 Bonferroni 보정 같은 방법을 사용할 수 있습니다. Bonferroni 보정은 원래의 유의수준
    (예: 0.05)을 t‑test의 수 (여기서는 3)로 나누어 각 t‑test의 유의수준을 조정합니다.
    보정된 유의수준 =
    0.05
    3
    = 0.0167
    from scipy.stats import ttest_ind
    lavender = anova_data[anova_data['Odor'] ^༰ 'Lavender']['Minutes']
    lemon = anova_data[anova_data['Odor'] ^༰ 'Lemon']['Minutes']
    no_odor = anova_data[anova_data['Odor'] ^༰ 'No_odor']['Minutes']
    t_stat1, p_val1 = ttest_ind(lavender, lemon)
    t_stat2, p_val2 = ttest_ind(lemon, no_odor)
    t_stat3, p_val3 = ttest_ind(lavender, no_odor)
    print("Lavender vs Lemon: t =", round(t_stat1, 3), ", p =", round(p_val1, 3))
    ^༈ Lavender vs Lemon: t = 3.07 , p = 0.005
    print("Lemon vs No odor: t =", round(t_stat2, 3), ", p =", round(p_val2, 3))
    ^༈ Lemon vs No odor: t = 0.205 , p = 0.839
    print("Lavender vs No odor: t =", round(t_stat3, 3), ", p =", round(p_val3, 3))
    ^༈ Lavender vs No odor: t = 3.155 , p = 0.004
    결과를 기반으로 사후 검정의 해석:
    1. Lavender vs Lemon:
    • t 값: 3.07, p‑value: 0.005
    • 해석: p 값이 0.0167보다 작으므로, 라벤더와 레몬 그룹 간의 평균에는 유의미한 차이가
    있다고 할 수 있습니다.
    122 | ANOVA: Analysis of Variance
    6
    2. Lemon vs No odor:
    • t 값: 0.205, p‑value: 0.839
    • 해석: p 값이 0.0167보다 크므로, 레몬과 무향 그룹 간의 평균에는 유의미한 차이가 없다고
    할 수 있습니다.
    3. Lavender vs No odor:
    • t 값: 3.155, p‑value: 0.004
    • 해석: p 값이 0.0167보다 작으므로, 라벤더와 무향 그룹 간의 평균에는 유의미한 차이가
    있다고 할 수 있습니다.
    정리하면, 라벤더와 레몬 그룹 간 그리고 라벤더와 무향 그룹 간에는 평균 차이가 유의미하게 나타
    났습니다. 반면, 레몬과 무향 그룹 간에는 평균 차이가 유의미하지 않았습니다.
    Tukey HSD
    Tukey HSD 검정은 ANOVA의 사후검정 중 하나입니다. 이 검정은 모든 그룹 간의 평균 차이를 비교
    하며, 이로 인한 유형 1 오류를 제어합니다. statsmodels 라이브러리의 pairwise_tukeyhsd() 함수를
    사용하여 Tukey HSD를 수행할 수 있습니다. 이러한 함수를 사용하면, 유의수준을 자동으로 보정해
    주므로 편합니다.
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    # Perform multiple comparisons
    tukey_results = pairwise_tukeyhsd(anova_data['Minutes'], anova_data['Odor'])
    print(tukey_results)
    ^༈ Multiple Comparison of Means - Tukey HSD, FWER=0.05
    ^༈ ========================================================
    ^༈ group1 group2 meandiff p༡adj lower upper reject
    ^༈ --------------------------------------------------------
    ^༈ Lavender Lemon -18.5 0.0111 -33.2768 -3.7232 True
    ^༈ Lavender No_odor -19.6762 0.0057 -34.2046 -5.1477 True
    ^༈ Lemon No_odor -1.1762 0.9788 -15.7046 13.3523 False
    ^༈ --------------------------------------------------------
    Games‑Howell test
    Games‑Howell 검정은 ANOVA의 등분산 가정이 충족되지 않을 때 선택하는 ANOVA (ANOVA with
    Welch’s correction) 검정과 같이 사용되는 사후검정입니다. 이는 각 그룹 간의 분산이 다를 때 특히
    유용합니다. pingouin 라이브러리를 사용하여 Games‑Howell 검정을 수행할 수 있습니다.
    import pingouin as pg
    pg.pairwise_gameshowell(data=anova_data, dv='Minutes', between='Odor')
    One‑way ANOVA | 123
    ^༈ A B mean(A) ^^. df pval hedges
    ^༈ 0 Lavender Lemon 107.142857 ^^. 25.203999 0.013568 1.126563
    ^༈ 1 Lavender No_odor 107.142857 ^^. 26.537150 0.010881 1.139639
    ^༈ 2 Lemon No_odor 88.642857 ^^. 26.940005 0.976900 0.074087
    ^༈
    ^༈ [3 rows x 10 columns]
    주어진 유의수준 0.05 하에서 판단하면, 앞에서와 동일한 결과(Lemon ‑ No_odor 그룹 만 유의미한
    차이 없음)를 얻게 됩니다.
    Kruskal‑Wallis Test
    Kruskal‑Wallis 검정은 비모수적인 방법으로 ANOVA의 대안으로 사용됩니다. 특히 데이터가 정규
    분포를 따르지 않을 때 유용하게 사용됩니다. 이 검정은 각 표본의 순위를 기반으로 하며, 모든 그룹의
    중앙값이 같은지를 검정합니다.
    특징
    • 정규성 가정이 필요하지 않습니다.
    • 모든 그룹의 분산이 동일하다는 가정이 필요하지 않습니다.
    • 크기가 다른 여러 그룹에 대해 중앙값의 차이를 검정합니다.
    즉, 데이터가 정규분포를 따르지 않거나, 등분산성 가정을 충족하지 못할 때 사용 가능하며, 데이터에
    이상치가 많은 경우에도 사용할 수 있습니다.
    귀무가설 vs. 대립가설
    비모수 검정이므로 모평균이 아닌 분포의 중앙(중앙값)에 대한 검정을 시행한다.
    • 귀무가설 𝐻0
    : 𝜂1 = 𝜂2 = ... = 𝜂𝑘
    • 대립가설 𝐻𝐴: Not all of 𝜂1
    , 𝜂2
    , ... and 𝜂𝑘
    are equal.
    검정통계량
    검정통계량 𝐻 는 주어진 공식에 따라 계산되며, 크기가 큰 표본에서는 카이제곱 분포를 따르게 됩니다.
    𝐻 = 12
    𝑁 (𝑁 + 1)
    𝑘
    ∑
    𝑖=1
    𝑅2
    .𝑖
    𝑛𝑖
    − 3 (𝑁 + 1)
    여기서
    • 𝑅.𝑖는 𝑖번째 그룹의 순위합입니다.
    • 𝑁 는 전체 표본의 크기입니다.
    • 𝑘는 그룹의 수입니다.
    • 𝑛𝑖는 𝑖번째 그룹의 표본 크기입니다.
    주어진 검정통계량 𝐻 는 각 그룹의 최소 표본 크기가 커지면 커질수록 자유도 𝑘 − 1인 카이제곱분
    포를 따르게 된다.
    124 | ANOVA: Analysis of Variance
    6
    Python에서 검정하기
    scipy.stats 패키지의 kruskal() 함수를 사용한다.
    from scipy.stats import kruskal
    odor_groups = [anova_data[anova_data['Odor'] ^༰ odor_type]['Minutes']
    for odor_type in anova_data['Odor'].unique()]
    H, p = kruskal(*odor_groups)
    print(H, p)
    ^༈ 10.316640217637701 0.005751353222496428
    검정통계량값 10.31에 대응하는 p‑value가 0.0057이므로 유의수준 0.05에 비하여 작습니다. 따
    라서 귀무가설을 기각하며, 각 그룹의 중앙값이 다른 그룹이 존재한다고 판단할 수 있습니다. 위의
    유의확률 값이 카이제곱 분포에서 계산된 것은 다음의 코드를 통하여 확인 할 수 있습니다.
    from scipy.stats import chi2
    1 - chi2.cdf(10.31, 2)
    ^༈ 0.005770480075096951
    Kruskal‑Wallis Test의 사후 검정
    statsmodels.stats 패키지의 multitest() 함수를 사용하여 사후 검정을 수행합니다.
    from statsmodels.stats import multitest
    odor_groups = [anova_data[anova_data['Odor'] ^༰ odor_type]['Minutes']
    for odor_type in anova_data['Odor'].unique()]
    H, p = kruskal(*odor_groups)
    reject, p_values_corrected, _, _ = multitest.multipletests(p, method='fdr_bh')
    print(kruskal(*odor_groups))
    ^༈ KruskalResult(statistic=10.316640217637701, pvalue=0.005751353222496428)
    print(p_values_corrected)
    ^༈ [0.00575135]
    One‑way ANOVA | 125
    6.3 Two‑way ANOVA
    이원 분산분석(Two‑way ANOVA)은 두 개의 독립변수가 종속변수에 미치는 영향을 동시에 분석하는
    방법입니다. 이는 실험 설계에서 두 가지 요인(독립변수)의 주효과 및 그들 간의 상호작용 효과를
    파악하기 위해 사용됩니다.
    • 주효과 (Main Effects): 각각의 독립변수가 종속변수에 미치는 평균적인 영향을 의미합니다.
    • 상호작용 효과 (Interaction Effect): 한 독립변수의 영향이 다른 독립변수의 수준에 따라 달라
    지는 경우, 이 두 변수 간에 상호작용이 있다고 말합니다.
    Two‑Way ANOVA의 모델 가정
    이원 분산분석(Two‑Way ANOVA)는 두 개의 범주형 독립변수와 하나의 연속형 종속변수 간의 관계를
    분석하는 통계적 방법입니다. 이원 분산분석의 주요 가정은 다음과 같습니다.
    𝑌𝑖𝑗𝑘 = 𝜇 + 𝛼𝑖 + 𝛽𝑗 + (𝛼𝛽)𝑖𝑗 + 𝜖𝑖𝑗𝑘
    𝑖𝑛𝑑. ∼ 𝒩(𝜇𝑖𝑗, 𝜎2
    )
    • 𝜇는 전체 평균을 나타냅니다.
    • 두 변수가 각각 𝐼 와 𝐽 레벨을 가지고 있다고 가정합니다.
    • 𝛼𝑖는 첫 번째 범주형 변수의 𝑖번째 수준의 효과를 나타냅니다. 𝑖 = 1, ..., 𝐼
    • 𝛽𝑗는 두 번째 범주형 변수의 𝑗번째 수준의 효과를 나타냅니다. 𝑗 = 1, ..., 𝐽
    • (𝛼𝛽)𝑖𝑗는 두 변수의 𝑖번째 및 𝑗번째 수준 간의 상호작용 효과를 나타냅니다.
    • 𝜖𝑖𝑗𝑘 는 𝑖번째 및 𝑗번째 수준에 속한 𝑘번째 관찰값의 잡음효과라 생각하면 되며, 정규분포
    𝒩(0, 𝜎2
    )를 따릅니다.
    이제는 모델식을 보고 관련한 가정을 추정해 볼 수 있어야 합니다. 잔차들이 정규분포를 따르고
    있으며, 분산이 𝜎
    2로 같다는 가정을 만족해야 합니다.
    귀무가설 및 대립가설
    • 주효과에 대한 귀무가설: 각 독립변수의 모든 수준들 사이에는 차이가 없다.
    • 상호작용에 대한 귀무가설: 두 독립변수의 상호작용 효과는 없다.
    Two‑Way ANOVA 예제
    TV에서 광고를 방송할 때, 광고의 길이와 노출 횟수가 광고의 효과에 어떤 영향을 미치는지 알아보기
    위해 실험을 설계했습니다.
    • 참가자 200명을 모집하여 다양한 조건의 광고에 노출시켰습니다.
    • 광고를 시청한 후에 참가자들은 물건에 대한 구매 의사를 0부터 100까지의 점수로 평가하는
    설문조사를 완료했습니다.
    2개 변수
    • 광고 길이
    • 노출 횟수
    126 | ANOVA: Analysis of Variance
    6
    데이터 구조
    표 6.1: 광고 노출횟수 효과 측정실험
    광고길이 1회 3회 5회
    30초 그룹1 그룹2 그룹3
    90초 그룹4 그룹5 그룹6
    검정 데이터에 따른 분류
    Two‑Way ANOVA를 수행할 때, 실험 설계와 데이터의 특성에 따라 분류할 수 있습니다. 우리는 다음
    과 같은 조건을 충족하고 있다고 생각합니다.
    • Crossed design: 이 디자인에서는 모든 조합의 셀(예: 광고 길이와 노출 횟수의 조합)에 대한
    정보를 모두 수집합니다.
    • CRD 혹은 RBD를 만족합니다.
    – Completely Randomized Design (CRD)
    * 각 처리 조합에 대한 관찰값은 무작위로 선택됩니다.
    * 모든 셀에 대한 표본은 독립적입니다.
    * 모든 셀의 반응변수는 동일한 분산 을 가진 정규분포를 따릅니다.
    – Randomized Block Design (RBD)
    * 실험 단위를 유사한 블록으로 그룹화하고, 각 블록 내에서 처리를 무작위로 할당합니다.
    * 블록 내에서는 모든 셀에 대한 표본이 독립적입니다.
    * 각 셀의 반응변수는 동일한 분산 𝜎
    2을 가진 정규분포를 따릅니다.
    • 균형 설계 (Balanced Design): 이 디자인에서는 각 셀에 동일한 수의 관찰값이 포함됩니다.
    이러한 설계는 통계적 검정력을 높이고, 분석을 단순화하는 데 도움이 됩니다. 각 셀마다 같은
    표본 갯수를 가진다. (최대한 노력)
    해석 방법
    Main Effects
    • 광고 길이 Main effect
    – 30 초 광고 평균 41.7
    – 90 초 광고 평균 51.7
    • 노출 횟수 Main effect
    – 1회 평균 35
    – 3회 평균 50
    – 5회 평균 55
    No interaction
    • 평행 라인이 나왔을때
    Two‑way ANOVA | 127
    표 6.2:
    광고길이 1회 3회 5회
    30초 30 45 50
    90초 40 55 60
    Main Effects with Interactions
    노출횟수 고려시 광고길이에 따른 Main effect 없음.
    • Interaction 존재시 Main effects 효과가 줄어듦.
    • 광고 길이 Main effect
    – 30 초 광고 평균 41.7
    – 90 초 광고 평균 41.7
    • 노출 횟수 Main effect
    – 1회 평균 35
    – 3회 평균 45
    – 5회 평균 45
    표 6.3:
    광고길이 1회 3회 5회
    30초 30 45 50
    90초 40 45 40
    128 | ANOVA: Analysis of Variance
    6
    Interaction
    • 평행 라인이 안나옴
    어떤 효과가 더 중요할까?
    • 같은 기울기 다른 위치
    Main effect vs. Interaction
    • 왼쪽: Interaction이 상당히 중요
    • 오른쪽: Main effect가 상당히 중요
    Two‑way ANOVA | 129
    연습문제
    • 각 그래프에 대하여 다음을 답하시오.
    용어 구분하기
    • Interaction 유무
    • Main effect 존재 유무: H 변수, V 변수
    Two‑way ANOVA 분석 전체 과정
    1. 그룹 평균과 분산을 구함
    • 그룹 평균 plot을 그린다.
    • ANOVA 가정 체크
    2. ANOVA 분석 수행 및 해석
    • 3개의 F 테스트와 p‑value가 주어짐.
    3. 검정 질문들
    • Interaction이 통계적으로 유의한가?
    • 가로 변수에 대한 main effect가 통계적으로 유의한가?
    • 세로 변수에 대한 main effect가 통계적으로 유의한가?
    연습문제
    two_anova_data = pd.read_csv('./data/ad༡two༡way༡anova.csv')
    grouped = two_anova_data.groupby(['ad_count', 'ad_length']).mean()
    grouped = grouped.unstack(level=-1)
    grouped
    ^༈ response
    130 | ANOVA: Analysis of Variance
    6
    ^༈ ad_length 30 90
    ^༈ ad_count
    ^༈ 1 12.083333 12.833333
    ^༈ 3 9.750000 8.583333
    Visualization
    • 가정 체크 해볼 것
    import seaborn as sns
    two_anova_data['ad_length'] = pd.Categorical(two_anova_data['ad_length'], categories=[30, 90], ordered=True)
    two_anova_data['ad_length'] = two_anova_data['ad_length'].cat.rename_categories(["30 초", "90 초"])
    two_anova_data['ad_count'] = pd.Categorical(two_anova_data['ad_count'], categories=[1, 3], ordered=True)
    two_anova_data['ad_count'] = two_anova_data['ad_count'].cat.rename_categories(["1회", "3회"])
    sns.boxplot(x='ad_count', y='response', data=two_anova_data, hue='ad_length')
    ^༈ <AxesSubplot:xlabel='ad_count', ylabel='response'>
    plt.show()
    1 3
    ad_count
    2.5
    5.0
    7.5
    10.0
    12.5
    15.0
    17.5
    20.0
    22.5
    response
    ad_length
    30 
    90 
    Interaction plot 해석하기
    • Main effect 유무 체크
    • Interaction 유무 체크
    Two‑way ANOVA | 131
    import seaborn as sns
    sns.pointplot(x='ad_length', y='response',
    data=two_anova_data, hue='ad_count', capsize=.2)
    ^༈ <AxesSubplot:xlabel='ad_length', ylabel='response'>
    plt.show()
    30 90 
    ad_length
    8
    10
    12
    14
    response
    ad_count
    1
    3
    Two‑way ANOVA 테이블
    F 분포 검정
    • 자유도는 해당 테이블
    Main effects 모델
    표 6.4: 상호작용 미포함 Two way ANOVA
    Source SS df Mean.Square F
    Factor A SS(A) (I‑1) SS(A)/(I‑1) MSA/MSE
    Factor B SS(B) (J‑1) SS(B)/(J‑1) MSB/MSE
    Error SSE (N‑I‑J+1) SSE/(N‑I‑J+1)
    Total SS(Total) (N‑1)
    • 자유도 예
    𝑀𝑆𝐴/𝑀𝑆𝐸 ∼ 𝐹𝐼−1,𝑁−𝐼−𝐽+1
    132 | ANOVA: Analysis of Variance
    6
    표 6.5: 상호작용 포함 Two way ANOVA
    Source SS df Mean.Square F
    Factor A SS(A) (I‑1) SS(A)/(I‑1) MSA/MSE
    Factor B SS(B) (J‑1) SS(B)/(J‑1) MSB/MSE
    Interaction SS(AB) (I‑1)(J‑1) SS(AB)/((I‑1)(J‑1)) MSAB/MSE
    Error SSE (N‑IJ) SSE/(N‑IJ)
    Total SS(Total) (N‑1)
    Interaction term 모델
    Python에서 Two‑way ANOVA 수행하기
    인터렉션이 존재하는 모델을 수식을 사용하여 넣는 방법을 주의해서 알아두자. 회귀분석이나 일반화
    선형모형에서도 같은 방식이 사용된다.
    • response ~ ad_count + ad_length
    • response ~ ad_count + ad_length + ad_count:ad_length
    • response ~ ad_count * ad_length
    위의 2번째, 3번째 방법이 동일하게 인터렉션이 존재하는 모델을 나타낸다.
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    model = ols('response ~ ad_count*ad_length', data=two_anova_data).fit()
    result = sm.stats.anova_lm(model)
    print(result)
    ^༈ df sum_sq mean_sq F PR(>F)
    ^༈ ad_count 1.0 130.020833 130.020833 10.560068 0.002218
    ^༈ ad_length 1.0 0.520833 0.520833 0.042301 0.837995
    ^༈ ad_count:ad_length 1.0 11.020833 11.020833 0.895093 0.349268
    ^༈ Residual 44.0 541.750000 12.312500 NaN NaN
    6.4 모델 검정 방법
    등분산 가정 확인
    import matplotlib.pyplot as plt
    residuals = model.resid
    fitted_values = model.fittedvalues
    plt.scatter(fitted_values, residuals)
    모델 검정 방법 | 133
    ^༈ <matplotlib.collections.PathCollection object at 0x000001AB986C0D88>
    plt.xlabel('Fitted Values')
    ^༈ Text(0.5, 0, 'Fitted Values')
    plt.ylabel('Residuals')
    ^༈ Text(0, 0.5, 'Residuals')
    plt.show()
    9 10 11 12 13
    Fitted Values
    6
    4
    2
    0
    2
    4
    6
    8
    Residuals
    from scipy.stats import levene
    two_anova_data['residuals'] = residuals
    two_anova_data['fitted_values'] = fitted_values
    x1 = two_anova_data.iloc[:12,3]
    x2 = two_anova_data.iloc[12:24,3]
    x3 = two_anova_data.iloc[24:36,3]
    x4 = two_anova_data.iloc[36:,3]
    levene(x1,x2,x3,x4)
    ^༈ LeveneResult(statistic=1.1635486527826802, pvalue=0.33441312522437444)
    Scale‑Location plot
    • 잔차들이 그룹 변수에 따라 고르게 분포 되었는가?
    134 | ANOVA: Analysis of Variance
    6
    • 등분산 가정 체크: 빨간 수평선, 잔차들이 (패턴 없이) 무작위로 퍼져있어야 함.
    • 잔차들을 표준화 후 기호를 없앰.
    1번이랑 뭐가 다른가?
    • 똑같음. 다만 잔차가 X 축을 따라서 불균형하게 분포 되어있을때, Residual vs. Fitted 보다
    이상한 점을 쉬운 경우 존재.
    정규성 가정 확인
    from scipy import stats
    residuals = model.resid
    stats.probplot(residuals, plot=plt)
    ^༈ ((array([-2.18794508, -1.81466696, -1.5940389 , -1.43152593, -1.29991017,
    ^༈ -1.18761792, -1.08858668, -0.99921942, -0.91719469, -0.84091983,
    ^༈ -0.76924975, -0.7013297 , -0.63650166, -0.57424545, -0.51414026,
    ^༈ -0.45583845, -0.39904728, -0.34351563, -0.28902427, -0.23537844,
    ^༈ -0.18240202, -0.12993297, -0.07781945, -0.02591656, 0.02591656,
    ^༈ 0.07781945, 0.12993297, 0.18240202, 0.23537844, 0.28902427,
    ^༈ 0.34351563, 0.39904728, 0.45583845, 0.51414026, 0.57424545,
    ^༈ 0.63650166, 0.7013297 , 0.76924975, 0.84091983, 0.91719469,
    ^༈ 0.99921942, 1.08858668, 1.18761792, 1.29991017, 1.43152593,
    ^༈ 1.5940389 , 1.81466696, 2.18794508]), array([-6.83333333, -6.08333333, ↩
    -5.75 , -5.75 , -5.58333333,
    ^༈ -3.83333333, -3.83333333, -3.08333333, -2.83333333, -2.58333333,
    ^༈ -2.08333333, -1.83333333, -1.83333333, -1.75 , -1.75 ,
    ^༈ -1.58333333, -1.58333333, -0.83333333, -0.75 , -0.75 ,
    ^༈ -0.58333333, -0.58333333, -0.58333333, -0.08333333, -0.08333333,
    ^༈ -0.08333333, 0.25 , 0.41666667, 0.91666667, 0.91666667,
    ^༈ 1.16666667, 1.41666667, 1.91666667, 1.91666667, 1.91666667,
    ^༈ 2.16666667, 2.16666667, 2.25 , 2.25 , 2.41666667,
    ^༈ 3.25 , 3.25 , 3.41666667, 3.91666667, 5.25 ,
    ^༈ 5.41666667, 7.16666667, 9.16666667])), (3.454475594607066, ↩
    -7.038151455032605e-15, 0.9904205983651462))
    plt.show()
    모델 검정 방법 | 135
    2 1 0 1 2
    Theoretical quantiles
    7.5
    5.0
    2.5
    0.0
    2.5
    5.0
    7.5
    10.0
    Ordered Values
    Probability Plot
    import scipy.stats as stats
    residuals = model.resid
    stats.shapiro(residuals)
    ^༈ ShapiroResult(statistic=0.9820642471313477, pvalue=0.6665181517601013)
    사후 분석 방법
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tukey = pairwise_tukeyhsd(endog=two_anova_data['response'],
    groups=two_anova_data['ad_count'],
    alpha=0.05)
    print(tukey)
    ^༈ Multiple Comparison of Means - Tukey HSD, FWER=0.05
    ^༈ ====================================================
    ^༈ group1 group2 meandiff p༡adj lower upper reject
    ^༈ ----------------------------------------------------
    ^༈ 1회 3회 -3.2917 0.0019 -5.3069 -1.2764 True
    ^༈ ----------------------------------------------------
    Unbalanced design Two‑way ANOVA
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    136 | ANOVA: Analysis of Variance
    6
    model = ols('response ~ ad_count*ad_length', data=two_anova_data).fit()
    table = sm.stats.anova_lm(model, typ=2)
    print(table)
    ^༈ sum_sq df F PR(>F)
    ^༈ ad_count 130.020833 1.0 10.560068 0.002218
    ^༈ ad_length 0.520833 1.0 0.042301 0.837995
    ^༈ ad_count:ad_length 11.020833 1.0 0.895093 0.349268
    ^༈ Residual 541.750000 44.0 NaN NaN
    .footnote[Langsrud, Ø. (2003). ANOVA for unbalanced data: Use Type II instead of Type
    III sums of squares. Statistics and Computing, 13(2), 163‑167.]
    6.5 연습문제
    자동차 연비 문제
    mpg 데이터 셋에는 자동차 연비를 나타내는 mpg 변수가 있다. 데이터 안의 차들은 cylinders 변수를
    기준으로 4개, 6개, 8개가 들어있는 그룹으로 분류할 수 있다. 자동차의 실린더 수가 늘어나면 보통
    연비가 줄어든다는 이야기가 있다. 데이터에서 이러한 경향을 보이는지 유의수준 5% 하에서 검정해
    보세요.
    import seaborn as sns
    mpg = sns.load_dataset('mpg')
    selected_mpg = mpg[['mpg', 'cylinders']]
    print(selected_mpg.head())
    ^༈ mpg cylinders
    ^༈ 0 18.0 8
    ^༈ 1 15.0 8
    ^༈ 2 18.0 8
    ^༈ 3 16.0 8
    ^༈ 4 17.0 8
    펭귄의 부리길이
    palmerpenguins 패키지의 penguins 데이터에는 펭귄 종류별 부리길이 ( bill_length_mm ) 정보가 들
    어있다. 펭귄의 종류에 따라서 부리길이가 다르다고 할 수 있는지 유의수준 1% 하에서 검정해보세요.
    연습문제 | 137
    import seaborn as sns
    penguins = sns.load_dataset('penguins')
    selected_penguins = penguins[['species', 'bill_length_mm']]
    print(selected_penguins.head())
    ^༈ species bill_length_mm
    ^༈ 0 Adelie 39.1
    ^༈ 1 Adelie 39.5
    ^༈ 2 Adelie 40.3
    ^༈ 3 Adelie NaN
    ^༈ 4 Adelie 36.7
    드릴 도구 검정 절차 (Drilling process)
    drilling༡tool༡exam.csv 데이터를 사용하여 다음 물음에 답하세요.
    슬통 철공 회사에서는 5개의 브랜드의 드릴 소재를 사용하여 철판에 구멍을 뚫은 작업을 하고 있다.
    회사 제품은 2.5cm 직경을 가진 철판인데, 브랜드 별 사용하는 소재들이 미세하게 달라, 직경에 차이
    가 발생하는지 알아보고자 한다. 품질 팀은 제품 품질을 유지하기 위하여 온도의 영향도 조사하기로
    하였다. 슬통이는 한 명의 품질 관리사에게 각기 다른 온도에서 브랜드별 드릴을 무작위로 20개씩
    선택하여 뚫은 구멍의 직경을 측정하도록 하였다.
    1) 데이터를 사용 각 브랜드별, 온도별 평균과 표준편차 정리 표를 만드세요.
    2) 브랜드별, 온도별로 ANOVA main effect & interaction plot을 그려보세요.
    3) Two‑way ANOVA 분석을 진행해 주세요.
    138 | ANOVA: Analysis of Variance
    """