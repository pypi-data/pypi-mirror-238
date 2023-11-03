def s3():
    """
    제 3 장
    t 검정 파헤치기
    여러 상황에서의 t 검정
    자료구조 파악하기
    데이터가 어떻게 주어졌는지에 따라서 t 검정의 형태가 바뀝니다. 따라서 주어진 데이터가 어떠한
    형태인지 파악하는 것이 중요합니다.
    기본적인 자료형
    t 검정의 기본적인 자료 형태는 데이터가 벡터 형태로 모든 표본이 같은 그룹으로 묶일 수 있는 형태입
    니다.
    표 3.1: 학생들의 점수 조사표 (기본형태)
    학생 ID 성적
    1 9.76
    2 11.10
    3 10.70
    4 10.72
    5 11.80
    6 6.15
    7 10.52
    8 14.83
    9 13.03
    10 16.46
    11 10.84
    12 12.45
    다른 변수들이 추가 된 데이터
    기본 데이터 형태에서 변형이 된 데이터의 경우 기본 자료형과 다르게 그룹을 나눌 수 있는 변수들이
    들어있는 형태가 있습니다.
    • 표 3.2의 경우 성별 변수로서 데이터가 두 그룹으로 나뉠 수 있습니다.
    t 검정 파헤치기 | 59
    • 표 3.3의 구조는 전체 관찰 대상은 학생 6명으로 바라볼 수 있습니다.
    표 3.2: 학생들의 성별 점수 조사 결과
    학생 ID 성적 성별
    1 9.76 female
    2 11.10 female
    3 10.70 female
    4 10.72 female
    5 11.80 female
    6 6.15 female
    7 10.52 female
    8 14.83 male
    9 13.03 male
    10 16.46 male
    11 10.84 male
    12 12.45 male
    표 3.3: 교육 프로그램 수료 후 점수 변화 조사 결과
    학생 ID 성적 전/후
    1 9.76 before
    2 11.10 before
    3 10.70 before
    4 10.72 before
    5 11.80 before
    6 6.15 before
    1 10.52 after
    2 14.83 after
    3 13.03 after
    4 16.46 after
    5 10.84 after
    6 12.45 after
    통계 검정 선택 시 판단 요소
    t 검정의 형태를 결정 할 때, 다음 두 가지를 고려 후 판단합니다.
    1. 그룹 변수가 존재하는가?
    2. 표본들을 짝지을 수 있는 특정 변수가 존재하는가?
    그룹 변수가 존재하는 경우, 데이터의 집단을 그룹 변수의 값에 따라서 2개로 나누어 생각할 수
    있는지 판단하고, 그렇다면 2 표본 t 검정을 선택합니다. 특정 데이터의 경우 주어진 표본들이 짝을
    지을 수 있는 경우가 존재하는데, 이 경우, 짝지을 수 있는 데이터들을 사용하여 데이터를 변형한 후, t
    검정을 진행합니다.
    60 | t 검정 파헤치기
    3
    검정 할 수 있는 형태들
    위의 각 데이터는 다음과 같은 형태의 검정에 적합한 데이터이다.
    • 학생들의 점수의 평균이 특정 값과 같은가?
    𝐻0
    ∶ 𝜇 = 10 𝑣𝑠. 𝐻𝐴 ∶ 𝜇 ≠ 10
    • 남학생과 여학생 두 그룹의 평균은 같을까?
    𝐻0
    ∶ 𝜇𝑀 = 𝜇𝐹 𝑣𝑠. 𝐻𝐴 ∶ 𝜇𝑀 ≠ 𝜇𝐹
    • 교육 프로그램은 효과가 있었을까?
    𝐻0
    ∶ 𝜇𝑏𝑒𝑓𝑜𝑟𝑒 = 𝜇𝑎𝑓𝑡𝑒𝑟 𝐻𝐴 ∶ 𝜇𝑏𝑒𝑓𝑜𝑟𝑒 < 𝜇𝑎𝑓𝑡𝑒𝑟
    t 검정을 위한 분산 가정 체크 방법
    그룹이 2개 이상인 데이터를 t‑검정하기 위해서는 한가지 가정을 추가적으로 체크해야 합니다.
    • 그룹별 데이터가 동일한 분산을 갖는가?
    F‑test를 사용한 두 그룹의 등분산 체크하는 방법 (그룹 2개)
    • 핵심 idea: F 검정은 추정한 분산의 비율로 두 그룹의 분산이 같은지 검정한다.
    F 분포
    확률변수 𝑋 가 자유도 𝑑1
    , 𝑑2 인 𝐹 분포를 따른다고 하면, 𝑋 는 다음과 같이 분수꼴로 표현되는 두
    개의 확률변수𝑌1
    , 𝑌2가 존재한다.
    𝑋 = 𝑌1/𝑑1
    𝑌2/𝑑2
    𝑌1과 𝑌2는 카이제곱분포 자유도 𝑑1과 𝑑2를 따르는 확률변수
    스튜던트 정리 revisit
    (𝑛 − 1) 𝑆2
    𝜎
    2
    ∼ 𝜒2
    (𝑛−1)
    • 앞에서 배운 스튜던트 정리에 따르면 정규분포를 따르는 표본 크기 𝑛로 구한 위의 통계량은
    카이제곱분포 자유도 𝑛 − 1을 따른다.
    • 그룹 1 (표본 𝑛개)과 그룹 2 (표본 𝑚개) 데이터로 위 통계량을 구하게 된다면?
    (𝑛 − 1) 𝑆2
    1
    𝜎
    2
    1
    ∼ 𝜒2
    (𝑛−1)
    (𝑚 − 1) 𝑆2
    2
    𝜎
    2
    2
    ∼ 𝜒2
    (𝑚−1)
    여기서 𝜎
    2
    1 과 𝜎
    2
    2 는 각 그룹 데이터의 모분산이다.
    t 검정 파헤치기 | 61
    귀무가설이 참이라면?
    두 그룹의 분산이 𝜎
    2
    0 로 같다면 다음은 자유도 𝑛, 𝑚인 F분포를 따르게 된다.
    (𝑛−1)𝑆2
    1
    𝜎
    2
    0
    / (𝑛 − 1)
    (𝑚−1)𝑆2
    2
    𝜎
    2
    0
    / (𝑚 − 1)
    =
    𝑆
    2
    1
    𝑆
    2
    2
    ∼ 𝐹𝑛−1,𝑚−1
    F 통계량 값에 따른 해석
    • 두 그룹의 분산이 동일하다면, 𝐹 값은 1이 나와야 함.
    • 두 그룹의 분산이 다르다면, 𝐹 값은 1보다 작거나 큰 값으로 나옴.
    F‑검정의 가설
    𝐻0
    : 𝜎
    2
    𝐴 = 𝜎2
    𝐵 vs. 𝐻𝐴: 𝜎
    2
    𝐴 ≠ 𝜎2
    𝐵
    • 귀무가설: A와 B 그룹의 분산은 같다.
    • 대립가설: A와 B 그룹의 분산은 같지 않다.
    Python에서 F‑test 하기
    데이터가 데이터 프레임에 들어있는지, 벡터 형식으로 들어있는지에 대하여 구문이 달라진다.
    데이터
    총 관찰 데이터는 30개이며 자료 구조는 다음과 같다.
    import pandas as pd
    import numpy as np
    # Set seed for reproducibility
    mydata = pd.read_csv('./data/tooth_growth.csv')
    mydata.head()
    ^༈ len supp dose
    ^༈ 0 11.2 VC 0.5
    ^༈ 1 9.4 OJ 0.5
    ^༈ 2 25.2 OJ 1.0
    ^༈ 3 16.5 OJ 0.5
    ^༈ 4 16.5 VC 1.0
    Python code
    oj = mydata[mydata['supp'] ^༰'OJ']
    s1 = oj['len'].std(ddof=1) #oj의 표본표준편차
    62 | t 검정 파헤치기
    3
    vc = mydata[mydata['supp'] ^༰'VC']
    s2 = vc['len'].std(ddof=1) #vc의 표본표준편차
    ratio_of_variances = s1^*2/s2^*2 # s1^2/s2^2
    print('ratio_of_variances:',round(ratio_of_variances,4))
    ^༈ ratio_of_variances: 0.6701
    𝐹 검정이 파이썬에서는 현재 지원되지 않는 상태이므로 다음과 같이 f_test() 함수를 정의하도록
    하자.
    import numpy as np
    import scipy.stats as stats
    def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    f = np.var(x, ddof=1) / np.var(y, ddof=1) # 검정통계량
    dfn = x.size-1
    dfd = y.size-1
    p = stats.f.cdf(f, dfn, dfd)
    p = 2*min(p, 1-p) # two sided p༡value
    return f, p
    # F 검정 수행하기
    f_value, p_value = f_test(oj['len'], vc['len'])
    print("Test statistic: ", f_value)
    ^༈ Test statistic: 0.6701284713415635
    print("p༡value: ", p_value)
    ^༈ p༡value: 0.4438335690639984
    t‑검정 가정 체크 예시
    앞에서 살펴 본 3가지 데이터 셋에 대하여, t 검정을 진행 할 경우, 가정 체크 과정에 대하여 알아보도록
    하겠습니다.
    t 검정 파헤치기 | 63
    첫번째 자료에 대한 가정 체크
    주어진 데이터를 sample 변수에 저장하도록 하겠습니다.
    sample = [9.76, 11.1, 10.7, 10.72, 11.8,
    6.15, 10.52, 14.83, 13.03,
    16.46, 10.84, 12.45]
    정규성 체크
    데이터의 정규성을 체크하기 위하여, QQ plot과 Shapiro Wilk 검정을 수행합니다.
    • Q‑Q plot
    import pingouin as pg
    import matplotlib.pyplot as plt
    ax = pg.qqplot(sample, dist='norm', confidence=0.95)
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
    2 = 0.914
    • Shapiro Wilk 검정
    64 | t 검정 파헤치기
    3
    import scipy.stats as sp
    print(sp.shapiro(sample))
    ^༈ ShapiroResult(statistic=0.9387352466583252, pvalue=0.48186349868774414)
    1표본 t‑test 함수 옵션 설정
    대립가설의 형태에 따라서 alternative 옵션을 조정해줘야 합니다.
    • two.sided
    • less
    • greater
    주어진 유의 수준에 따라서 conf.level 옵션을 조정해줘야 합니다.
    • conf.level=0.95
    from scipy.stats import ttest_1samp
    t_statistic, p_value = ttest_1samp(sample, popmean=10, alternative='two༡sided')
    print("t༡statistic:", t_statistic)
    ^༈ t༡statistic: 2.050833816777307
    print("p༡value:", p_value)
    ^༈ p༡value: 0.06488240727465693
    두번째 자료에 대한 가정 체크
    주어진 데이터를 판다스 데이터 프레임으로 만들어 봅시다.
    import pandas as pd
    sample = [9.76, 11.1, 10.7, 10.72, 11.8, 6.15, 10.52,
    14.83, 13.03, 16.46, 10.84, 12.45]
    gender = ["Female"]*7 + ["Male"]*5
    my_tab2 = pd.DataFrame({"score": sample, "gender": gender})
    my_tab2
    ^༈ score gender
    ^༈ 0 9.76 Female
    t 검정 파헤치기 | 65
    ^༈ 1 11.10 Female
    ^༈ 2 10.70 Female
    ^༈ 3 10.72 Female
    ^༈ 4 11.80 Female
    ^༈ 5 6.15 Female
    ^༈ 6 10.52 Female
    ^༈ 7 14.83 Male
    ^༈ 8 13.03 Male
    ^༈ 9 16.46 Male
    ^༈ 10 10.84 Male
    ^༈ 11 12.45 Male
    두 집단 각각에 대하여 정규성을 체크하고, 등분산 가정 체크를 실시합니다.
    정규성 체크 ‑ 여학생 집단
    • Q‑Q plot
    ax = pg.qqplot(sample[:7], dist='norm', confidence=.95)
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
    2 = 0.732
    • Shapiro Wilk 검정
    66 | t 검정 파헤치기
    3
    result = sp.shapiro(sample[:7])
    print(result)
    ^༈ ShapiroResult(statistic=0.7618962526321411, pvalue=0.016863727942109108)
    정규성 체크 ‑ 남학생 집단
    • Q‑Q plot
    ax = pg.qqplot(sample[7:12], dist='norm', confidence=.95)
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
    2 = 0.984
    • Shapiro Wilk 검정
    result = sp.shapiro(sample[7:12])
    print(result)
    ^༈ ShapiroResult(statistic=0.9813238382339478, pvalue=0.9415760636329651)
    t 검정 파헤치기 | 67
    등분산성 체크
    • F‑test
    # F 검정 수행하기
    female = my_tab2[my_tab2['gender'] ^༰ 'Female']['score']
    male = my_tab2[my_tab2['gender'] ^༰ 'Male']['score']
    f_value, p_value = f_test(female, male)
    print("Test statistic: ", f_value)
    ^༈ Test statistic: 0.7230748344750079
    print("p༡value: ", p_value)
    ^༈ p༡value: 0.6870845918240329
    두번째 자료에 대한 검정 실시
    귀무가설 vs. 대립가설
    귀무가설은 “두 그룹의 모평균이 동일하다” 이며, 대립가설은 “두 그룹의 모평균이 동일하지 않다”
    라고 설정되어 있습니다.
    • 𝐻0
    : 𝜇𝑚𝑎𝑙𝑒 = 𝜇𝑓𝑒𝑚𝑎𝑙𝑒
    • 𝐻𝐴: 𝜇𝑚𝑎𝑙𝑒 ≠ 𝜇𝑓𝑒𝑚𝑎𝑙𝑒
    alternative 옵션 설정하는 방법
    • two.sided
    • less
    • greater
    alternative = "greater" 로 설정한다는 의미는 첫 번째 입력값에 해당하는 그룹 (x 자리) 의 평균이
    두 번째 입력값에 해당하는 그룹 (y 자리)의 평균보다 크다는 의미입니다.
    Unpaired two sample t test
    Unpaired two sample t test는 데이터의 정규성과 등분산성이 보장 된 경우 적용할 수 있는 t 검정
    입니다. ttest_ind 함수에 equal_var=True를 적용해 줍니다.
    • 정규성 통과 등분산성 통과
    from scipy.stats import ttest_ind
    male = my_tab2[my_tab2['gender'] ^༰ 'Male']
    68 | t 검정 파헤치기
    3
    female = my_tab2[my_tab2['gender'] ^༰ 'Female']
    t_statistic, p_value = ttest_ind(female['score'], male['score'], equal_var=True)
    print("t༡statistic: ",t_statistic)
    ^༈ t༡statistic: -2.9360367510416165
    print("p༡value: ",p_value)
    ^༈ p༡value: 0.01488614765791557
    Welch (or Satterthwaite) two sample t test
    Welch (or Satterthwaite) two sample t test는 데이터의 정규성은 보장되나, 등분산성이 보장 되지
    않는 경우 적용할 수 있는 t 검정입니다. ttest_ind 함수에 equal_var=False을 적용해 줍니다.
    • 정규성 통과 등분산성 불만족
    from scipy.stats import ttest_ind
    male = my_tab2[my_tab2['gender'] ^༰ 'Male']
    female = my_tab2[my_tab2['gender'] ^༰ 'Female']
    t_statistic, p_value = ttest_ind(female['score'], male['score'], equal_var=False)
    print("t༡statistic: ",t_statistic)
    ^༈ t༡statistic: -2.850539711551644
    print("p༡value: ", p_value)
    ^༈ p༡value: 0.02199712977900471
    무엇이 다를까?
    등분산성 가정을 만족하는지 만족하지 않는지에 따라서 t 검정의 검정통계량 값을 계산 할 때, 분산을
    추정하는 방법과 검정통계량이 따르는 t분포의 자유도 값이 달라집니다. 하지만, 검정통계량의 형태는
    동일합니다.
    https://academic.oup.com/beheco/article/17/4/688/215960?login=false
    t 검정 파헤치기 | 69
    Unpaired two sample t test
    • 검정 통계량
    𝑡 =
    (𝑋1 − 𝑋2
    ) − (𝜇1 − 𝜇2
    )
    0
    𝑠
    2
    𝑝√(
    1
    𝑛1
    +
    1
    𝑛2
    )
    ∼ 𝑡𝑛1+𝑛2−2
    여기서 𝑥은 표본평균, 𝑛은 표본크기를 나타내고, (𝜇1 − 𝜇2
    )
    0 은 귀무가설에서 주장하는 두
    집단 모평균의 차이를 나타낸다. 보통은 0으로 설정 됨.
    • 검정 통계량의 분포는 자유도가 𝑛1 + 𝑛2 − 2인 𝑡 분포를 따른다.
    • 𝑠
    2
    𝑝는 두 모집단의 분산을 추정하기 위한 통계량으로 쓰임.
    𝑠
    2
    𝑝 =
    (𝑛1 − 1) 𝑆2
    1 + (𝑛2 − 1) 𝑆2
    2
    𝑛1 + 𝑛2 − 2
    𝑛1
    , 𝑠1
    , 𝑛2
    , 𝑠2는 각각 그룹 1과 2의 표본 크기와 표본 표준편차를 나타낸다.
    Welch’s t‑test statistic
    • 검정 통계량
    𝑡 =
    (𝑋1 − 𝑋2
    ) − (𝜇1 − 𝜇2
    )
    0
    √𝑆2
    2
    𝑛1
    +
    𝑆2
    2
    𝑛2
    ∼ 𝑡𝜈
    자유도 𝜈 는 다음 Satterthwaite’s approximation을 사용하여 계산한다.
    𝜈 ≈
    (
    𝑠
    2
    1
    𝑛1
    +
    𝑠
    2
    2
    𝑛2
    )
    2
    𝑠
    4
    1
    𝑛2
    1
    (𝑛1−1) +
    𝑠
    4
    2
    𝑛2
    2
    (𝑛2−1)
    세번째 자료에 대한 가설 체크
    세번째 자료는 데이터가 짝지어 질 수 있는 데이터 (대응 표본) 였습니다. 주어진 자료를 입력 받은 후,
    대응되는 표본들끼리의 차을 이용하여 하나의 그룹 데이터로 변형시켜 보겠습니다.
    import pandas as pd
    tab3 = pd.read_csv('./data/tab3.csv')
    tab3_data = tab3.pivot_table(index='id',columns='group',values='score')
    tab3_data['score_diff'] = tab3_data['after'] - tab3_data['before']
    test3_data = tab3_data[['score_diff']]
    test3_data
    ^༈ group score_diff
    ^༈ id
    70 | t 검정 파헤치기
    3
    ^༈ 1 0.76
    ^༈ 2 3.73
    ^༈ 3 2.33
    ^༈ 4 5.74
    ^༈ 5 -0.96
    ^༈ 6 6.30
    주어진 표본 크기가 반절로 줄어들었지만, 변형 결과 첫번째 유형의 데이터와 형태가 동일해 졌습
    니다. 따라서, 1표본 t‑test 검정을 위한 가정 체크를 실시한다.
    • Q‑Q plot
    ax = pg.qqplot(test3_data, dist='norm',confidence=.95)
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
    2 = 0.975
    • Shapiro test
    result = sp.shapiro(test3_data)
    print(result)
    ^༈ ShapiroResult(statistic=0.9559008479118347, pvalue=0.7876578569412231)
    t 검정 파헤치기 | 71
    세번째 자료에 대한 검정 실시
    • 교육 프로그램은 효과가 있었을까?
    𝐻0
    ∶𝜇𝑏𝑒𝑓𝑜𝑟𝑒 = 𝜇𝑎𝑓𝑡𝑒𝑟 𝑣𝑠. 𝐻𝐴 ∶ 𝜇𝑏𝑒𝑓𝑜𝑟𝑒 < 𝜇𝑎𝑓𝑡𝑒𝑟
    𝐻0
    ∶𝜇𝑑 ≤ 0 𝑣𝑠. 𝐻𝐴 ∶ 𝜇𝑑 > 0
    • 𝜇𝑑
    ∶= 𝜇𝑎𝑓𝑡𝑒𝑟 − 𝜇𝑏𝑒𝑓𝑜𝑟𝑒
    • 새로운 모수에 대한 표본 평균을 관찰하는 것으로 생각할 수 있음.
    귀무가설 vs. 대립가설
    귀무가설은 “교육 프로그램의 점수 향상 효과가 없음.” 이며, 대립가설은 “교육 프로그램의 점수 향상
    효과가 있음.” 라고 설정.
    • 𝐻0
    : 𝜇𝑑 = 0
    • 𝐻𝐴: 𝜇𝑑 > 0
    Paired t test
    • 검정통계량
    𝑡 =
    𝐷 − 𝜇0
    𝑑
    𝑆𝑑/
    √𝑛𝑑
    ∼ 𝑡𝑛𝑑−1
    • 표본 크기 𝑛𝑑가 원래 자료의 반으로 줄어든다는 것에 주의하자.
    • 이후 내용은 1표본 𝑡 검정과 동일.
    • 데이터 프레임 형식일 때 1표본 𝑡 검정하는 방법
    from scipy.stats import ttest_1samp
    t_statistic, p_value = ttest_1samp(test3_data, 0, alternative='greater')
    print("t༡statistic:", t_statistic)
    ^༈ t༡statistic: [2.58116143]
    print("p༡value:", p_value)
    ^༈ p༡value: [0.02468128]
    앞에서는 두 그룹의 값의 차를 사용하여 score_diff를 계산하여 1 표본 t‑test를 사용하였다. 하지만,
    ttest_rel()를 사용하면, 두 그룹의 값을 따로따로 입력하여 paired t test를 수행할 수 있다.
    72 | t 검정 파헤치기
    3
    t_statistic, p_value = stats.ttest_rel(tab3_data['after'],
    tab3_data['before'],
    alternative='greater')
    print("t༡statistic:", t_statistic)
    ^༈ t༡statistic: 2.5811614301011883
    print("p༡value:", p_value)
    ^༈ p༡value: 0.02468128345546597
    주의사항!
    여기서 주의할 점은, alternative 옵션을 첫번째 그룹을 기준으로 대립가설의 부등호를 입력한다는
    것이다. 따라서, 다음과 같이 순서를 바꿔서 입력하면 엉뚱한 p‑value값이 도출 됨에 주의합니다.
    t_statistic, p_value = stats.ttest_rel(tab3_data['before'],
    tab3_data['after'],
    alternative='greater')
    print("t༡statistic:", t_statistic)
    ^༈ t༡statistic: -2.5811614301011883
    print("p༡value:", p_value)
    ^༈ p༡value: 0.9753187165445341
    3.1 참고 내용
    데이터가 특정 분산값을 따르는지 체크하는 방법 (23회 기출문제)
    정규분포를 따르는 확률변수에서 관찰한 표본들의 표본표준편차 𝑆
    2은 다음과 같이 카이제곱분포를
    따름.
    • 앞에서 배운 스튜던트 정리와 관련이 있음.
    (𝑛 − 1) 𝑆2
    𝜎
    2
    ∼ 𝜒2
    (𝑛−1)
    귀무가설 vs. 대립가설
    • 𝐻0
    : 모분산 𝜎
    2이 𝜎
    2
    0 와 같다.
    • 𝐻𝐴: 모분산 𝜎
    2이 𝜎
    2
    0 같지 않다.
    참고 내용 | 73
    검정순서
    • 데이터가 정규성을 따르는지 체크
    • 검정통계량 값을 계산해서 대응하는 카이제곱 분포에서 관찰할 수 있는 확률을 구함.
    Python에서 구현하기
    표 3.1 의 성적 데이터의 표준편차가 3보다 큰 지 검정하고자 한다면 다음과 같이 할 수 있다.
    import numpy as np
    from scipy.stats import chi2
    sample_data = np.array([9.76, 11.10, 10.70, 10.72,
    11.80, 6.15, 10.52, 14.83,
    13.03, 16.46, 10.84, 12.45])
    s = np.std(sample_data, ddof=1)
    sigma = 3
    n = 12
    chi = ((n-1)*(s^*2)) / sigma^*2
    p_value = 1 - chi2.cdf(chi, df=n-1)
    print('Chi-Squared:',chi)
    ^༈ Chi-Squared: 8.16306666666667
    print('p_value:',p_value)
    ^༈ p_value: 0.6986263615554091
    연습문제
    신약 효과 분석
    새로 제안된 혈압약에 대한 효과 분석을 위하여 무작위로 배정된 두 그룹에 대한 혈압 측정 데이터입
    니다. Treated 그룹의 경우 혈압약을 일정기간 복용하였으며, Control 그룹은 평상시 활동을 그대로
    유지하였습니다. 표 3.4는 두 그룹의 혈압을 측정한 데이터입니다.
    혈압약의 사용이 혈압을 떨어뜨리는 효과가 있는지 유의수준 5%하에서 검정해보세요.
    • 귀무가설 vs. 대립가설
    • 가정 체크 및 검정 방법 설정
    74 | t 검정 파헤치기
    3
    표 3.4: 혈압약 효과 측정 데이터
    ID Score Group
    1 3.81 control
    2 4.47 control
    3 4.81 control
    4 4.79 control
    5 4.25 control
    6 3.93 treated
    7 4.26 treated
    8 3.74 treated
    9 3.61 treated
    10 3.93 treated
    11 4.36 treated
    12 3.93 treated
    13 3.89 treated
    14 4.03 treated
    15 3.85 treated
    16 4.06 treated
    고양이 소변의 효과
    고양의 소변이 식물의 성장을 저해한다는 명제를 확인하기 위하여 무작위로 선정된 두 식물 그룹을
    가지고 실험을 진행하였습니다.
    Treated 그룹의 경우 고양이 소변을 체취하여 일정 간격으로 뿌려주었으며, 이외 다른 조건은
    Treated, Control 그룹 모두 동일하게 유지하였습니다. 표 3.5는 한달 후 두 그룹의 성장 높이 데이터
    를 기록한 것입니다.
    고양의 소변이 식물의 성장을 저해한다는 것에 대한 검정을 유의수준 5%하에서 수행해보세요.
    표 3.5: 식물 성장 측정 데이터
    ID Score Group
    1 45 control
    2 87 control
    3 123 control
    4 120 control
    5 70 control
    6 51 treated
    7 71 treated
    8 42 treated
    9 37 treated
    10 51 treated
    11 78 treated
    12 51 treated
    13 49 treated
    14 56 treated
    15 47 treated
    16 58 treated
    참고 내용 | 75
    """