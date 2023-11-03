def s11_1():
    """
    제 11 장
    챕터별 연습문제 풀이
    Chapter 1. 통계적 검정의 근본 원리
    문제 1. 농구, 축구 경기 선호도 확률
    슬통 마을의 많은 사람들이 농구와 축구 관람을 좋아한다고 한다. 마을의 40%는 농구 경기를 좋아하고,
    70%는 축구 경기를 좋아하며, 농구와 축구 관람을 모두 좋아하는 비율이 20%라고 한다.
    • 사건 Basket: 특정 사람이 농구를 좋아할 확률
    • 사건 Soccer: 특정 사람이 축구를 좋아할 확률
    𝑃 (𝐵𝑎𝑠𝑘𝑒𝑡) = 0.4
    𝑃(𝑆𝑜𝑐𝑐𝑒𝑟) = 0.7
    𝑃 (𝐵𝑎𝑠𝑘𝑒𝑡 ∩ 𝑆𝑜𝑐𝑐𝑒𝑟) = 0.2
    1) 마을 사람을 무작위로 한 명 선택했을 때, 그 사람이 농구와 축구 둘 다 좋아하지 않는 사람일
    확률을 구하세요.
    구하고자 하는 것: 𝑃 (𝐵𝑐 ∩ 𝑆𝑐
    )
    𝑃 (𝐵𝑐 ∩ 𝑆𝑐
    ) = 𝑃 ((𝐵 ∪ 𝑆)𝑐
    ) = 1 − 𝑃 (𝐵 ∪ 𝑆)
    확률의 덧셈법칙에 의하여 다음이 성립한다.
    𝑃(𝐵 ∪ 𝑆) = 𝑃 (𝐵) + 𝑃 (𝑆) − 𝑃 (𝐵 ∩ 𝑆) = 0.4 + 0.7 − 0.2 = 0.9
    따라서 농구와 축구 둘 다 좋아하지 않는 사람일 확률은 1 − 0.9 = 0.1
    2) 마을 사람을 무작위로 한 명 선택해서, 농구를 좋아하냐고 물어보았다. 그 사람이 농구를 좋아하
    지 않는다고 대답했다면, 축구를 좋아할 확률을 구하세요.
    구하고자 하는 것: 𝑃 (𝑆|𝐵𝑐
    )
    위 확률은 조건부 확률에 의하여 다음과 같이 쓸 수 있다.
    챕터별 연습문제 풀이 | 203
    𝑃 (𝑆|𝐵𝑐
    ) = 𝑃(𝑆 ∩ 𝐵𝑐
    )
    𝑃 (𝐵𝑐)
    =
    𝑃 (𝑆) − 𝑃 (𝑆 ∩ 𝐵)
    1 − 𝑃 (𝐵) =
    0.7 − 0.2
    0.6
    =
    5
    6
    round(5/6, 2)
    ^༈ 0.83
    문제 2. 빨간공, 파란공
    두 개의 상자 A, B가 놓여있다. A 상자에는 빨간색 공이 3개, 파란색 공이 3개 들어있고, B 상자에는
    빨간색 공이 4개, 파란색 공이 6개 들어있다고 한다.
    1) 각각의 상자에서 하나씩 공을 꺼낼 때, 두 공이 같은 색깔일 확률을 구하세요.
    • 사건 AR: 상자 A에서 빨간공을 꺼내는 사건
    • 사건 AB: 상자 A에서 파란공을 꺼내는 사건
    • 사건 BR: 상자 B에서 빨간공을 꺼내는 사건
    • 사건 BB: 상자 B에서 파란공을 꺼내는 사건
    • 두 공이 같은 색깔
    – 상자 A에서 빨간공을 꺼내고, 상자 B에서 빨간공을 꺼내거나
    – 상자 A에서 파란공을 꺼내고, 상자 B에서 파란공을 꺼내는 경우
    • 구하고자 하는 것: 𝑃 ((𝐴𝑅 ∩ 𝐵𝑅) ∪ (𝐴𝐵 ∩ 𝐵𝐵))
    모두 빨간공을 꺼내는 사건과 모두 파란공을 꺼내는 사건은 동시에 일어날 수 없으므로 각각 사건의
    확률의 합으로 나눠쓸 수 있음.
    𝑃 ((𝐴𝑅 ∩ 𝐵𝑅) ∪ (𝐴𝐵 ∩ 𝐵𝐵)) = 𝑃 (𝐴𝑅 ∩ 𝐵𝑅) + 𝑃 (𝐴𝐵 ∩ 𝐵𝐵)
    각 상자에서 공을 꺼내는 사건은 독립이므로 독립사건 곱셈법칙 적용
    𝑃 (𝐴𝑅 ∩ 𝐵𝑅) + 𝑃 (𝐴𝐵 ∩ 𝐵𝐵) = 𝑃 (𝐴𝑅)𝑃 (𝐵𝑅) + 𝑃 (𝐴𝐵)𝑃 (𝐵𝐵)
    = 0.5 ∗ 0.4 + 0.5 ∗ 0.6
    204 | 챕터별 연습문제 풀이
    11
    0.5 * 0.4 + 0.5 * 0.6
    ^༈ 0.5
    2) 이번에는 슬통이가 두 개 상자 중 하나에서 공을 하나 꺼내왔다고 한다. 뽑힌 공의 색깔을 보니
    빨간색이었다. 슬통이가 이 공을 상자 A에서 꺼냈을 확률을 구하세요.
    • 사건 A: 상자 A를 선택하는 사건
    • 사건 B: 상자 B를 선택하는 사건
    • 사건 R: 빨간공을 꺼내는 사건
    • 구하는 것: 𝑃(𝐴|𝑅)
    베이즈 정리에 의하여 다음이 성립한다.
    𝑃(𝐴|𝑅) = 𝑃 (𝐴)𝑃 (𝑅|𝐴)
    𝑃(𝑅)
    =
    𝑃(𝐴)𝑃 (𝑅|𝐴)
    𝑃 (𝐴)𝑃 (𝑅|𝐴) + 𝑃 (𝐵)𝑃 (𝑅|𝐵)
    =
    0.5 ∗ 0.5
    0.5 ∗ 0.5 + 0.5 ∗ 0.4
    p_a_bar_r = (0.5 * 0.5)/(0.5 * 0.5 + 0.5 * 0.4)
    round(p_a_bar_r,3)
    ^༈ 0.556
    문제 3. ADP 실기시험 성적 분포
    2022년에 실시 된 ADP 실기 시험의 통계파트 표준점수는 평균이 30, 표준편차가 5인 정규분포를
    따른다고 한다.
    𝑋 ∼ 𝒩(30, 52
    )
    1) ADP 실기 시험의 통계파트 표준점수의 밀도함수를 그려보세요.
    import numpy as np
    from scipy.stats import norm
    import matplotlib.pyplot as plt
    x = np.arange(15,45,0.1)
    y = norm.pdf(x, loc=30, scale=5)
    plt.plot(x, y)
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA2504A88>]
    챕터별 연습문제 풀이 | 205
    plt.show()
    20 30 40
    0.00
    0.02
    0.04
    0.06
    0.08
    2) ADP 수험생을 임의로 1명을 선택하여 통계 점수를 조회했을때 45점 보다 높은 점수를 받았을
    확률을 구하세요.
    구하는 것: 𝑃(𝑋 > 45)
    1 - norm.cdf(45, 30, 5)
    ^༈ 0.0013498980316301035
    3) 슬통이는 상위 10%에 해당하는 점수를 얻었다고 한다면, 슬통이의 점수는 얼마인지 계산해보
    세요.
    구하는 것: 𝑃(𝑋 > 𝑘) = 0.1 에서 𝑘 값
    Quantile 을 구해주는 qnorm 함수를 사용하여 계산
    norm.ppf(0.9, 30, 5)
    ^༈ 36.407757827723
    4) 슬기로운 통계생활의 해당 회차 수강생은 16명이었다고 한다. 16명의 통계 파트 점수를 평균
    내었을 때, 이 평균값이 따르는 분포의 확률밀도 함수를 1번의 그래프와 겹쳐 그려보세요.
    중심극한정리에 의하여, 표본평균 확률변수는 다음과 같은 정규분포를 따른다.
    𝑋 ∼ 𝒩(30, 5
    2
    16
    )
    따라서 개별 점수의 정규분포보다 훨씬 좁은 종모양의 분포를 띄게 된다.
    206 | 챕터별 연습문제 풀이
    11
    x = np.arange(15,45,0.1)
    y = norm.pdf(x, loc=30, scale=5)
    plt.plot(x, y)
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA26FD248>]
    y2 = norm.pdf(x,loc=30,scale=5/np.sqrt(16))
    plt.plot(x,y2,color='red')
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA2710CC8>]
    plt.show()
    20 30 40
    0.0
    0.1
    0.2
    0.3
    5) 슬기로운 통계생활 ADP 반 수강생들의 통계점수를 평균내었다고 할 때, 이 값이 38점보다 높게
    나올 확률을 구하세요.
    구하고자 하는 것: 𝑃 (𝑋 > 38) 여기서 𝑋 ∼ 𝒩(30, 5
    2
    16 )
    1 - norm.cdf(38, 30, 5/np.sqrt(16))
    ^༈ 7.76885222819601e-11
    따라서 슬기로운 통계생활 ADP 반 수강생들의 통계점수를 평균내었다고 할 때, 이 값이 38점보다
    높게 나올 사건은 거의 일어나기 불가능하다.
    문제 4. 코비드 19 발병률
    Covid‑19의 발병률은 1%라고 한다. 다음은 이번 코로나 사태로 인하여 코로나 의심 환자들 1,085
    명을 대상으로 슬통 회사의 “다잡아” 키트를 사용하여 양성 반응을 체크한 결과이다.
    챕터별 연습문제 풀이 | 207
    키트 \ 실제 양성 음성 합계
    양성 370 10 380
    음성 15 690 705 ⸻—– ⸺ ⸺ ⸺
    합계 385 700 1085
    • 사건 DP: 키트가 양성으로 판단하는 사건
    • 사건 TP: 실제상태가 양성인 사건
    • 사건 DN: 키트가 음성으로 판단하는 사건
    • 사건 TN: 실제상태가 음성인 사건
    1) 다잡아 키트가 코로나 바이러스에 걸린 사람을 양성으로 잡아낼 확률을 계산하세요.
    • 구하는 것: 𝑃(𝐷𝑃 |𝑇 𝑃 )
    𝑃(𝐷𝑃 |𝑇 𝑃 ) = 370/385
    370 / 385
    ^༈ 0.961038961038961
    2) 슬통 회사에서 다잡아 키트를 사용해 양성으로 나온 사람이 실제로는 코로나 바이러스에 걸려
    있을 확률을 97%라며, 키트의 우수성을 주장했다. 이 주장이 옳지 않은 이유를 서술하세요.
    표본으로 뽑힌 집단의 유병률과 모집단의 유병률의 차이가 크다.
    3) Covid‑19 발병률을 사용하여, 키트의 결과값이 양성으로 나온 사람이 실제로 코로나 바이러스에
    걸려있을 확률을 구하세요.
    • Covid‑19 발병률의 의미: 𝑃(𝑇 𝑃 ) = 0.01
    구하고자 하는 것: 𝑃 (𝑇 𝑃 |𝐷𝑃 )
    위 확률은 베이즈 정리에 의하여 다음과 같이 계산 할 수 있다.
    𝑃 (𝑇 𝑃 |𝐷𝑃 ) = 𝑃(𝑇 𝑃 ∩ 𝐷𝑃 )
    𝑃(𝐷𝑃 )
    =
    𝑃 (𝑇 𝑃 )𝑃 (𝐷𝑃 |𝑇 𝑃 )
    𝑃(𝑇 𝑃 )𝑃 (𝐷𝑃 |𝑇 𝑃 ) + 𝑃 (𝑇 𝑁)𝑃 (𝐷𝑃 |𝑇 𝑁)
    테이블에서 얻을 수 있는 정보 중 𝑃 (𝐷𝑃 |𝑇 𝑃 )와 𝑃 (𝐷𝑃 |𝑇 𝑁)의 정보는 상대적으로 믿을 수 있는
    정보이므로, 발병률 정보와 같이 대입해서 계산한다.
    𝑃 (𝑇 𝑃 )𝑃 (𝐷𝑃 |𝑇 𝑃 )
    𝑃(𝑇 𝑃 )𝑃 (𝐷𝑃 |𝑇 𝑃 ) + 𝑃 (𝑇 𝑁)𝑃 (𝐷𝑃 |𝑇 𝑁)
    =
    0.01 ∗ (370/385)
    0.01 ∗ (370/385) + 0.99 ∗ (10/700)
    208 | 챕터별 연습문제 풀이
    11
    sol = (0.01 * (370 / 385)) / (0.01 * (370 / 385) + 0.99 * (10 / 700))
    round(sol,3)
    ^༈ 0.405
    따라서, 키트의 결과값이 양성으로 나온 사람이 실제로 코로나 바이러스에 걸려있을 확률은 40.5%
    로 추정하는게 합리적이다.
    문제 5. 카이제곱분포와 표본분산
    자유도가 𝑘인 카이제곱분포를 따르는 확률변수 𝑋를
    𝑋 ∼ 𝜒2
    (𝑘)
    과 같이 나타내고, 이 확률변수의 확률밀도함수는 다음과 같습니다.
    𝑓𝑋(𝑥; 𝑘) = 1
    2
    𝑘/2Γ(𝑘/2) 𝑥
    𝑘/2−1𝑒
    −𝑥/2
    다음의 물음에 답하세요.
    1) 자유도가 4인 카이제곱분포의 확률밀도함수를 그려보세요.
    • 관련 패키지
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import chi2, norm
    x = np.linspace(0, 20, 1000)
    pdf = chi2.pdf(x, 4)
    plt.plot(x, pdf)
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA26ED908>]
    plt.xlabel("x")
    ^༈ Text(0.5, 0, 'x')
    plt.ylabel("f_X(x; k)")
    ^༈ Text(0, 0.5, 'f_X(x; k)')
    챕터별 연습문제 풀이 | 209
    plt.show()
    0 5 10 15 20
    x
    0.00
    0.05
    0.10
    0.15
    f_X(x; k)
    그림 11.1: 자유도 4인 카이제곱분포 pdf
    2) 다음의 확률을 구해보세요.
    𝑃 (3 ≤ 𝑋 ≤ 5)
    chi2.cdf(5, 4) - chi2.cdf(3, 4)
    ^༈ 0.27052790518742903
    3) 자유도가 4인 카이제곱분포에서 크기가 1000인 표본을 뽑은 후, 히스토그램을 그려보세요.
    np.random.seed(2023)
    sample_size = 1000
    sample_data = chi2.rvs(4, size=sample_size)
    plt.hist(sample_data, bins=50, density=True,
    color="lightblue", edgecolor="black");
    plt.xlabel("sample")
    ^༈ Text(0.5, 0, 'sample')
    plt.ylabel("density")
    ^༈ Text(0, 0.5, 'density')
    210 | 챕터별 연습문제 풀이
    11
    plt.show()
    0 5 10 15
    sample
    0.00
    0.05
    0.10
    0.15
    0.20
    density
    그림 11.2: 자유도가 4인 카이제곱분포에서 추출된 표본의 히스토그램
    4) 자유도가 4인 카이제곱분포를 따르는 확률변수에서 나올 수 있는 값 중 상위 5%에 해당하는
    값은 얼마인지 계산해보세요.
    chi2.ppf(0.95, 4)
    ^༈ 9.487729036781154
    5) 3번에서 뽑힌 표본값들 중 상위 5%에 위치한 표본의 값은 얼마인가요?
    np.percentile(sample_data, 95)
    ^༈ 9.079466124811068
    6) 평균이 3, 표준편차가 2인 정규분포를 따르는 확률변수에서 크기가 20인 표본, 𝑥1
    , ..., 𝑥20,을
    뽑은 후 표본분산을 계산한 것을 𝑠
    2
    1이라 생각해보죠. 다음을 수행해보세요!
    • 같은 방법으로 500개의 𝑠
    2들, 𝑠
    2
    1
    , 𝑠2
    2
    , ..., 𝑠2
    500 발생시킵니다.
    • 발생한 500개의 𝑠
    2들 각각에 4.75를 곱하고, 그것들의 히스토그램을 그려보세요. (히스토그램
    을 그릴 때 density = True 옵션을 사용해서 그릴 것)
    • 위에서 그린 히스토그램에 자유도가 19인 카이제곱분포 확률밀도함수를 겹쳐그려보세요.
    np.random.seed(2023)
    n = 20
    num_samples = 500
    var_samples = []
    챕터별 연습문제 풀이 | 211
    for i in range(num_samples):
    x = norm.rvs(3, 2, size=n)
    var_samples.append(np.var(x, ddof=1))
    scaled_var_samples = np.array(var_samples) * 4.75
    plt.hist(scaled_var_samples,
    bins=50, density=True, color="lightblue",
    edgecolor="black");
    plt.xlabel("4.75 * s^2");
    plt.ylabel("density");
    x = np.linspace(0, max(scaled_var_samples), 1000)
    pdf_chi19 = chi2.pdf(x, df=19)
    plt.plot(x, pdf_chi19, 'r--', linewidth=2);
    plt.legend(["histogram", "df 19 chisquare dist"], loc="upper right");
    plt.show()
    0 10 20 30 40
    4.75 * s^2
    0.00
    0.02
    0.04
    0.06
    0.08
    density
    histogram
    df 19 chisquare dist 그림 11.3: 500개의 scale 된 표본분산의 히스토그램
    Chapter 2. 통계적 검정의 근본 원리
    문제 1. 신뢰구간 구하기
    다음은 한 고등학교의 3학년 학생들 중 16명을 무작위로 선별하여 몸무게를 측정한 데이터이다. 이
    데이터를 이용하여 해당 고등학교 3학년 전체 남학생들의 몸무게 평균을 예측하고자 한다.
    212 | 챕터별 연습문제 풀이
    11
    79.1, 68.8, 62.0, 74.4, 71.0, 60.6, 98.5, 86.4, 73.0, 40.8, 61.2, 68.7, 61.6, 67.7, 61.7, 66.8
    단, 해당 고등학교 3학년 남학생들의 몸무게 분포는 정규분포를 따른다고 가정한다.
    1) 모평균에 대한 95% 신뢰구간을 구하세요.
    2) 작년 남학생 3학년 전체 분포의 표준편차는 6kg 이었다고 합니다. 이 정보를 이번 년도 남학생
    분포의 표준편차로 대체하여 모평균에 대한 90% 신뢰구간을 구하세요.
    데이터 입력
    import numpy as np
    from scipy.stats import t, norm
    sample_data = np.array([79.1, 68.8, 62.0, 74.4, 71.0, 60.6, 98.5, 86.4,
    73.0, 40.8, 61.2, 68.7, 61.6, 67.7, 61.7, 66.8])
    sample_data
    ^༈ array([79.1, 68.8, 62. , 74.4, 71. , 60.6, 98.5, 86.4, 73. , 40.8, 61.2,
    ^༈ 68.7, 61.6, 67.7, 61.7, 66.8])
    표본에서의 정보 추출하기
    다음은 표본 평균과 표본 표준편차를 계산하는 파이썬 코드 입니다.
    sample_mean = np.mean(sample_data)
    sample_sd = np.std(sample_data, ddof=1) # ddof=1로 설정하여 표본 표준편차를 계산
    n = len(sample_data) # 표본 크기
    last_year_sd = 6 # 작년 표준편차
    1) 모평균에 대한 95% 신뢰구간을 구하기 위해, 표본 평균과 표본 표준편차를 사용하고, 표본 크
    기는 16명이므로 자유도는 15입니다.
    # 모평균에 대한 95% 신뢰구간 계산 (작년의 표준편차를 사용)
    ci_95 = t.interval(0.95, df=n-1, loc=sample_mean,
    scale=sample_sd/np.sqrt(n))
    print("모평균에 대한 95% 신뢰구간: ", np.round(ci_95, 2))
    ^༈ 모평균에 대한 95% 신뢰구간: [62.13 75.65]
    위의 계산을 stats.t.interval()을 사용하지 않고, 구하면 다음과 같습니다.
    t_critical = t.ppf(1 - 0.05/2, df=n-1) # t 분포의 분위수 계산
    mg_of_error = t_critical * sample_sd / np.sqrt(n) # margin of error 계산
    ci_95 = (sample_mean - mg_of_error, sample_mean + mg_of_error)
    np.round(ci_95, 2)
    챕터별 연습문제 풀이 | 213
    ^༈ array([62.13, 75.65])
    2) 모평균에 대한 90% 신뢰구간을 구하기 위해, 표본 평균을 사용하고, 표준 편차는 작년의 값인
    6kg을 사용합니다. 표본 크기는 여전히 16명이므로 z 분포의 90% 신뢰구간을 계산하겠습니다.
    # 모평균에 대한 90% 신뢰구간 계산 (작년의 표준편차를 사용)
    ci_90 = norm.interval(0.90, loc=sample_mean,
    scale=last_year_sd/np.sqrt(n))
    print("모평균에 대한 90% 신뢰구간 (작년의 표준편차를 사용): ", np.round(ci_90, 2))
    ^༈ 모평균에 대한 90% 신뢰구간 (작년의 표준편차를 사용): [66.43 71.36]
    위의 계산을 stats.norm.interval()을 사용하지 않고, 구하면 다음과 같습니다.
    z_critical = norm.ppf(1 - 0.10/2) # z 분포의 분위수 계산
    mg_of_error = z_critical * last_year_sd / np.sqrt(n)
    ci_90 = (sample_mean - mg_of_error, sample_mean + mg_of_error)
    np.round(ci_90, 2)
    ^༈ array([66.43, 71.36])
    문제 2. 신형 자동차의 에너지 소비효율 등급
    슬통 자동자는 매해 출시되는 신형 자동차의 에너지 소비효율 등급을 1등급으로 유지하고 있다. 22
    년 개발된 신형 모델이 한국 자동차 평가원에서 설정한 에너지 소비 효율등급 1등급을 받을 수 있을지
    검정하려한다. 평가원에 따르면 1등급의 기준은 평균 복합 에너지 소비효율이 16.0 이상인 경우 부여
    한다고 한다.
    다음은 신형 자동차 15대의 복합 에너지소비효율 측정한 결과이다.
    15.078, 15.752, 15.549, 15.56, 16.098, 13.277, 15.462, 16.116, 15.214, 16.93, 14.118, 14.927,
    15.382, 16.709, 16.804
    표본에 의하여 판단해볼때, 현대자동차의 신형 모델은 에너지 효율 1등급으로 판단할 수 있을지
    유의수준 1% 하에서 판단해보시오.
    데이터 입력
    import numpy as np
    sample_data = np.array([15.078, 15.752, 15.549, 15.56, 16.098,
    13.277, 15.462, 16.116, 15.214, 16.93,
    14.118, 14.927, 15.382, 16.709, 16.804])
    sample_data
    ^༈ array([15.078, 15.752, 15.549, 15.56 , 16.098, 13.277, 15.462, 16.116,
    ^༈ 15.214, 16.93 , 14.118, 14.927, 15.382, 16.709, 16.804])
    214 | 챕터별 연습문제 풀이
    11
    귀무가설 vs. 대립가설
    귀무가설: 22년 개발된 현대 자동차 신형 모델의 평균 에너지 소비 효율등급은 1등급 기준을 만족한다.
    𝜇 ≥ 16
    대립가설: 22년 개발된 현대 자동차 신형 모델의 평균 에너지 소비 효율등급은 1등급 기준을 만족
    하지 않는다.
    𝜇 < 16
    가정 체크 및 검정 방법 설정
    1표본 t 검정은 데이터가 정규성을 만족해야 한다는 전제를 만족해야 하므로 데이터의 정규성 가정을
    체크한다.
    정규성 검정 데이터에 대한 정규성 검정을 시각화 기법과 Shapiro‑wilk 검정을 사용하여 시행한다.
    import pingouin as pg
    import matplotlib.pyplot as plt
    ax = pg.qqplot(sample_data, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.show()
    2 0 2
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
    2 = 0.941
    1 개의 표본을 제외하면정규성을 띄는 것으로 판단된다. 정확한 검정을 위하여 S‑W 검정을 시행한다.
    S‑W 검정의 유의수준은 정해진 값이 없으므로 5%를 기준으로 진행한다.
    • Shapiro‑Wilk 검정
    – 귀무가설: 데이터가 정규분포를 따른다.
    챕터별 연습문제 풀이 | 215
    – 대립가설: 데이터가 정규분포를 따르지 않는다.
    from scipy.stats import shapiro
    shapiro(sample_data)
    ^༈ ShapiroResult(statistic=0.9448551535606384, pvalue=0.4473438858985901)
    p‑value 값 0.4473이 유의수준인 5%보다 크므로 귀무가설을 기각할 수 없다. 따라서 데이터는
    정규성을 만족한다고 판단한다.
    t 검정
    표본이 정규성을 만족하므로 t‑test를 실시한다.
    from scipy.stats import ttest_1samp
    ttest_1samp(sample_data, 16,alternative='less')
    ^༈ Ttest_1sampResult(statistic=-1.8500447456376756, pvalue=0.042762417664207845)
    표본의 평균 복합 에너지 효율은 15.53173이고, 검정통계량값은 ‑1.85이다. t 검정통계량에 대응
    하는 p‑value값 0.04276가 유의수준인 1%보다 크므로, 귀무가설을 기각하지 못한다. 따라서 22년
    현대 자동차 신형 모델 그룹의 평균 에너지 소비효율은 1등급을 만족한다고 판단한다.
    기각역
    𝑡 통계량은 귀무가설하에서 자유도가 14인 𝑡 분포를 따르며, 유의수준 1%에 해당하는 기각역은 다음을
    만족하는 ̄𝑥의 범위를 역산하면 된다.
    𝑡 =
    ̄𝑥 − 𝜇0
    𝑠/√
    𝑛
    =
    ̄𝑥 − 16
    𝑠/√
    15
    ≤ −2.624
    result = 16 - 2.624 * (sample_data.std(ddof=1) / np.sqrt(15))
    result.round(3)
    ^༈ 15.336
    따라서 기각역은 𝑥가 15.336보다 작은 영역이다.
    검정력
    검정력을 구하기 위해서 실제 평균 복합 에너지 평균값을 15이라고 가정할 때, 표본 평균이 15.335
    보다 크거나 같게 관찰될 확률을 구한다.
    𝑃 (𝑋 ≤ 15.335|𝜇 ̄
    𝑎 = 15) = 𝑃 (𝑧 ≤ 15.335 − 15
    1/√
    15 )
    = 𝑃 (𝑡 ≤ 1.324)
    216 | 챕터별 연습문제 풀이
    11
    따라서, 검정력은 다음과 같이 90.28%로 계산할 수 있다.
    from scipy.stats import norm
    norm.cdf(1.297449)
    ^༈ 0.9027616289304574
    문제 3. 검정력을 만족하는 표본 개수
    귀무가설과 대립가설 설정
    해당 검정을 위해 귀무가설과 대립가설을 다음과 같이 수립할 수 있다.
    𝐻0
    ∶ 𝜇 = 16 𝑣𝑠. 𝐻𝑎
    ∶ 𝜇 ≠ 16
    기각역 구하기
    모 표준편차를 알고있다는 가정하에서 다음의 𝑍 통계량은 귀무가설하에서 표준정규분포를 따르며,
    유의수준 5%에 해당하는 기각역은 다음을 만족하는 ̄𝑥의 범위를 역산하면 된다.
    𝑧 =
    ̄𝑥 − 𝜇0
    𝜎/√
    𝑛
    =
    ̄𝑥 − 16
    2/√
    15
    ≥ 1.96
    𝑧 =
    ̄𝑥 − 𝜇0
    𝜎/√
    𝑛
    =
    ̄𝑥 − 16
    2/√
    15
    ≤ −1.96
    따라서, R에서는 다음의 함수를 사용해서 구할 수 있다.
    from scipy.stats import norm
    norm.ppf(0.025, 16, 2/np.sqrt(15))
    ^༈ 14.987878950494672
    norm.ppf(0.975, 16, 2/np.sqrt(15))
    ^༈ 17.01212104950533
    즉, 기각역은 표본평균이 14.987보다 작은 영역과 17.012보다 큰 영역이다.
    평균값 15일때의 검정력
    검정력을 구하기 위해서 실제 평균 복합 에너지 평균값을 15이라고 가정할 때, 다음의 영역에 속할
    확률을 구한다.
    𝑃 (𝑋 ≥ 17.012|𝜇 ̄
    𝑎 = 15) = 𝑃 (𝑍 ≥ 17.012 − 15
    2/√
    15 )
    = 𝑃 (𝑍 ≥ 3.896)
    챕터별 연습문제 풀이 | 217
    𝑃 (𝑋 ≤ 14.987|𝜇 ̄
    𝑎 = 15) = 𝑃 (𝑍 ≤ 14.987 − 15
    2/√
    15 )
    = 𝑃 (𝑍 ≤ −0.0251)
    p1 = norm.cdf(-0.0251)
    p2 = 1 - norm.cdf(3.896)
    p1 + p2
    ^༈ 0.49003649728580484
    검정력을 만족하는 표본개수
    다음의 코드를 통하여 유의수준 5%하에서 검정력 80%를 만족하는 표본크기를 구하면, 표본크기가
    32 이상인 경우에 만족하는 것을 알 수 있다.
    n = 32
    a = 16 + norm.ppf(0.975, 0, 1) * (2/np.sqrt(n))
    b = 16 - norm.ppf(0.975, 0, 1) * (2/np.sqrt(n))
    left_a = (b-15) / (2/np.sqrt(n))
    right_b = (a-15) / (2/np.sqrt(n))
    norm.cdf(left_a) + (1-norm.cdf(right_b))
    ^༈ 0.8074304194325567
    문제 4. IQR 과 상자그림
    주어진 데이터를 사용하여 다음의 물음에 답하세요.
    12, 15, 14, 10, 18, 20, 21, 15, 17, 19, 10, 13, 16, 22, 50, 70
    1. 첫 번째와 세 번째 사분위수(Q1, Q3)를 계산하세요.
    2. Interquartile Range (IQR)를 계산하세요.
    3. 이상치를 식별하고, 이들을 데이터 세트에서 찾아내세요.
    4. 데이터의 상자그림(Boxplot)을 그리세요.
    Chapter 3. t 검정 파헤치기
    문제 1. 신약 효과 분석
    새로 제안된 혈압약에 대한 효과 분석을 위하여 무작위로 배정된 두 그룹에 대한 혈압 측정 데이터
    이다. Treated 그룹의 경우 혈압약을 일정기간 복용하였으며, Control 그룹은 평상시 활동을 그대로
    유지하였다. 표 11.2는 두 그룹의 혈압을 측정한 데이터이다.
    218 | 챕터별 연습문제 풀이
    11
    혈압약의 사용이 혈압을 떨어뜨리는 효과가 있는지 유의수준 5%하에서 검정하시오.
    표 11.2: 혈압약 효과 측정 데이터
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
    데이터 입력
    import pandas as pd
    import numpy as np
    prac_group = ["control"]*5 + ["treated"]*11
    id = list(range(1,17))
    score = np.array([3.81, 4.47, 4.81, 4.79, 4.25, 3.93, 4.26, 3.74,
    3.61, 3.93, 4.36, 3.93, 3.89, 4.03, 3.85, 4.06])
    prac1 = pd.DataFrame({"id":id, "score":score, "group":prac_group})
    prac1
    ^༈ id score group
    ^༈ 0 1 3.81 control
    ^༈ 1 2 4.47 control
    ^༈ 2 3 4.81 control
    ^༈ 3 4 4.79 control
    ^༈ 4 5 4.25 control
    ^༈ 5 6 3.93 treated
    ^༈ 6 7 4.26 treated
    ^༈ 7 8 3.74 treated
    ^༈ 8 9 3.61 treated
    ^༈ 9 10 3.93 treated
    챕터별 연습문제 풀이 | 219
    ^༈ 10 11 4.36 treated
    ^༈ 11 12 3.93 treated
    ^༈ 12 13 3.89 treated
    ^༈ 13 14 4.03 treated
    ^༈ 14 15 3.85 treated
    ^༈ 15 16 4.06 treated
    control = prac1[prac1['group']^༰'control']['score']
    treated = prac1[prac1['group']^༰'treated']['score']
    귀무가설 vs. 대립가설
    • 귀무가설: 혈압약의 사용은 혈압을 떨어뜨리는 효과가 없다. 𝜇𝑐𝑜𝑛𝑡𝑟𝑜𝑙 = 𝜇𝑡𝑟𝑒𝑎𝑡𝑒𝑑
    • 대립가설: 혈압약의 사용은 혈압을 떨어뜨리는 효과가 있다. 𝜇𝑐𝑜𝑛𝑡𝑟𝑜𝑙 > 𝜇𝑡𝑟𝑒𝑎𝑡𝑒𝑑
    가정 체크 및 검정 방법 설정
    2표본 t 검정은 데이터가 정규성을 만족하고, 등분산성의 만족 유무에 따라서 선택할 수 있는 검정
    방법이 달라지므로 검정의 가정을 체크한다.
    정규성 검정 각 그룹에 대한 정규성 검정을 시각화 기법과 Shapiro‑wilk 검정을 사용하여 시행한다.
    import pingouin as pg
    import matplotlib.pyplot as plt
    plt.subplot(1,2,1);
    ax = pg.qqplot(control, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.subplot(1,2,2);
    ax = pg.qqplot(treated, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.show()
    220 | 챕터별 연습문제 풀이
    11
    2 0 2
    Theoretical quantiles
    2
    0
    2
    Ordered quantiles
    R
    2 = 0.925
    2 0 2
    Theoretical quantiles
    2
    0
    2
    Ordered quantiles
    R
    2 = 0.949
    몇 개의 표본을 제외하면 두 그룹 모두 정규성을 띄는 것으로 판단된다. 정확한 검정을 위하여 유의
    수준 5% 하에서 Shapiro‑Wilk 검정을 시행한다.
    • 귀무가설: 데이터가 정규분포를 따른다.
    • 대립가설: 데이터가 정규분포를 따르지 않는다.
    from scipy.stats import shapiro
    shapiro(prac1.iloc[:5,1])
    ^༈ ShapiroResult(statistic=0.9128482341766357, pvalue=0.4848945438861847)
    shapiro(prac1.iloc[5:16,1])
    ^༈ ShapiroResult(statistic=0.9562556147575378, pvalue=0.7242791652679443)
    두 그룹 데이터 모두 p‑value 값이 유의수준인 5%보다 크므로 귀무가설을 기각할 수 없다. 따라서
    두 그룹 데이터 모두 정규성을 만족한다고 판단한다.
    등분산성 검정 두 그룹이 정규성을 만족한다는 것을 확인하였으므로, 유의수준 5%하에서 F 검정을
    통하여 등분산성 가정을 확인한다.
    • 귀무가설: 두 그룹의 모분산이 같다.
    • 대립가설: 두 그룹의 모분산은 같지 않다.
    import numpy as np
    import scipy.stats as stats
    def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    챕터별 연습문제 풀이 | 221
    f = np.var(x, ddof=1) / np.var(y, ddof=1) # 검정통계량
    dfn = x.size-1
    dfd = y.size-1
    p = stats.f.cdf(f, dfn, dfd)
    p = 2*min(p, 1-p) # two sided p༡value
    return f, p
    group1 = prac1[prac1["group"] ^༰ "control"]["score"]
    group2 = prac1[prac1["group"] ^༰ "treated"]["score"]
    # Perform F༡test
    f_value, p_value = f_test(group1, group2)
    print("Test statistic: {:.3f}".format(f_value))
    ^༈ Test statistic: 3.800
    print("p༡value: {:.3f}".format(p_value))
    ^༈ p༡value: 0.079
    F 검정통계량 값 3.8에 대응하는 p‑value 0.079가 유의수준인 5% 보다 크므로 귀무가설을 기각할
    수 없다. 따라서 두 그룹 데이터의 모분산은 동일하다고 판단한다.
    t 검정
    표본의 정규성과 등분산성을 만족하므로 독립 2표본 t‑test를 실시한다.
    from scipy.stats import ttest_ind
    t_value, p_value = ttest_ind(group1, group2, equal_var = True, alternative='greater')
    print("Test statistic: ", t_value.round(3))
    ^༈ Test statistic: 3.0
    print("p༡value: ", p_value.round(3))
    ^༈ p༡value: 0.005
    컨트롤 그룹의 표본 평균 혈압은 4.426이고, 혈압약을 복용한 그룹의 표본 평균 혈압은 3.96을
    나타냈다.
    t 검정의 p‑value 0.005가 유의수준인 5%보다 작으므로, 귀무가설을 기각한다. 즉, 혈압약 복용/
    미복용 두 그룹의 평균 혈압 차는 통계적으로 유의미하다고 이야기 할 수 있다. 따라서 혈압약의 사용이
    혈압을 떨어뜨리는 효과가 있다고 판단한다.
    222 | 챕터별 연습문제 풀이
    11
    문제 2. 고양이 소변의 효과
    고양이의 소변이 식물의 성장을 저해한다는 명제를 확인하기 위하여 무작위로 선정된 두 식물 그룹을
    가지고 실험을 진행하였다.
    Treated 그룹의 경우 고양이 소변을 체취하여 일정 간격으로 뿌려주었으며, 이외 다른 조건은
    Treated, Control 그룹 모두 동일하게 유지하였다. 표 11.3는 한달 후 두 그룹의 성장 높이 데이터를
    기록한 것이다.
    고양이의 소변이 식물의 성장을 저해한다는 것에 대한 검정을 유의수준 5%하에서 수행해보시오.
    표 11.3: 식물 성장 측정 데이터
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
    데이터 입력
    prac_group = ["control"]*5 + ["treated"]*11
    id = list(range(1,17))
    score = [45, 87, 123, 120, 70,51, 71, 42, 37, 51, 78,51, 49, 56, 47, 58]
    prac2 = pd.DataFrame({"id":id, "score":score, "group":prac_group})
    prac2
    ^༈ id score group
    ^༈ 0 1 45 control
    ^༈ 1 2 87 control
    ^༈ 2 3 123 control
    ^༈ 3 4 120 control
    ^༈ 4 5 70 control
    ^༈ 5 6 51 treated
    ^༈ 6 7 71 treated
    챕터별 연습문제 풀이 | 223
    ^༈ 7 8 42 treated
    ^༈ 8 9 37 treated
    ^༈ 9 10 51 treated
    ^༈ 10 11 78 treated
    ^༈ 11 12 51 treated
    ^༈ 12 13 49 treated
    ^༈ 13 14 56 treated
    ^༈ 14 15 47 treated
    ^༈ 15 16 58 treated
    control = prac2[prac2['group']^༰'control']['score']
    treated = prac2[prac2['group']^༰'treated']['score']
    귀무가설 vs. 대립가설
    귀무가설: 고양이의 소변은 식물의 성장에 무해하다.
    𝜇𝑐𝑜𝑛𝑡𝑟𝑜𝑙 = 𝜇𝑡𝑟𝑒𝑎𝑡𝑒𝑑
    대립가설: 고양이의 소변은 식물의 성장에 저해한다.
    𝜇𝑐𝑜𝑛𝑡𝑟𝑜𝑙 > 𝜇𝑡𝑟𝑒𝑎𝑡𝑒𝑑
    가정 체크 및 검정 방법 설정
    2표본 t 검정은 데이터가 정규성을 만족하고, 등분산성의 만족 유무에 따라서 선택할 수 있는 검정
    방법이 달라지므로 검정의 가정을 체크한다.
    정규성 검정 각 그룹에 대한 정규성 검정을 시각화 기법과 Shapiro‑wilk 검정을 사용하여 시행한다.
    import pingouin as pg
    import matplotlib.pyplot as plt
    plt.subplot(1,2,1);
    ax = pg.qqplot(control, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.subplot(1,2,2);
    ax = pg.qqplot(treated, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.show()
    224 | 챕터별 연습문제 풀이
    11
    2 0 2
    Theoretical quantiles
    2
    0
    2
    Ordered quantiles
    R
    2 = 0.946
    2 0 2
    Theoretical quantiles
    2
    0
    2
    Ordered quantiles
    R
    2 = 0.910
    Control 그룹의 경우 정규성을 띄는 것으로 판단되나 Treated 그룹의 두 표본이 정규성을 만족하지
    않는 것으로 보인다. 정확한 검정을 위하여 유의수준 5% 하에서 Shapiro‑Wilk 검정을 시행한다.
    • 귀무가설: 데이터가 정규분포를 따른다.
    • 대립가설: 데이터가 정규분포를 따르지 않는다.
    from scipy.stats import shapiro
    shapiro(prac2.iloc[:5,1])
    ^༈ ShapiroResult(statistic=0.9245066046714783, pvalue=0.5594186186790466)
    shapiro(prac2.iloc[5:16,1])
    ^༈ ShapiroResult(statistic=0.9170808792114258, pvalue=0.2950724959373474)
    두 그룹 데이터 모두 p‑value 값, 0.55와 0.29가 이 유의수준인 5%보다 크므로 귀무가설을 기각할
    수 없다. 따라서 두 그룹 데이터 모두 정규성을 만족한다고 판단한다.
    등분산성 검정 두 그룹이 정규성을 만족한다는 것을 확인하였으므로, 유의수준 5%하에서 F 검정을
    통하여 등분산성 가정을 확인한다.
    • 귀무가설: 두 그룹의 모분산이 같다.
    • 대립가설: 두 그룹의 모분산은 같지 않다.
    import numpy as np
    import scipy.stats as stats
    group1 = prac2[prac2["group"] ^༰ "control"]["score"]
    group2 = prac2[prac2["group"] ^༰ "treated"]["score"]
    챕터별 연습문제 풀이 | 225
    #perform F༡test
    f_value, p_value = f_test(group1, group2)
    print("Test statistic: {:.3f}".format(f_value))
    ^༈ Test statistic: 7.788
    print("p༡value: {:.3f}".format(p_value))
    ^༈ p༡value: 0.008
    F 검정의 p‑value값 0.0081이 유의수준인 5% 보다 작으므로 귀무가설을 기각한다. 따라서 두 그룹
    데이터의 등분산 가정을 만족하지 않는다고 판단한다.
    t 검정
    주어진 표본은 정규성을 만족하나 등분산성을 만족하지 못하므로 Welch’s two sample t‑test를 실
    시한다.
    from scipy.stats import ttest_ind
    import math
    t_value, p_value = ttest_ind(group1, group2,
    equal_var = False,
    alternative='greater')
    print("control mean: ", np.mean(group1).round(3))
    ^༈ control mean: 89.0
    print("treated mean: ", np.mean(group2).round(3))
    ^༈ treated mean: 53.727
    print("Test statistic: ", t_value.round(3))
    ^༈ Test statistic: 2.307
    print("p༡value: ", p_value.round(3))
    ^༈ p༡value: 0.038
    226 | 챕터별 연습문제 풀이
    11
    컨트롤 그룹 식물들의 표본 평균 높이는 89.0이고, 고양이 소변을 뿌린 식물 그룹의 표본 평균 높이는
    53.727을 나타냈다.
    t 검정통계량 값 2.3069에 대응하는 p‑value값 0.03767이 유의수준인 5%보다 작으므로, 귀무가설
    을 기각한다. 즉, 고양이 소변을 뿌린 그룹과 그렇지 않은 식물 그룹의 평균 높이 차는 주어진 유의수준
    하에서 통계적으로 유의미하다고 말할 수 있다. 따라서 고양이 소변이 식물 성장을 저해하는 효과가
    있다고 판단한다.
    Chapter 4. 비모수 검정 친해지기
    문제 1. 신제품 촉매제
    슬통 회사에서는 이번에 출시한 새로운 촉매제의 효능을 검증하고 싶어한다. 신제품 촉매재는 기존
    공정에서 사용되는 화학반응 속도를 혁신적으로 줄여주는 기능이 탑재되어 있다고 한다.
    회사 제품 검증 부서에서는 기존 공정의 화학 반응속도와 촉매제를 넣은 후의 반응 속도를 측정하여
    표 4.4 데이터를 만들었다.
    1. 유의수준 5%하에서 신제품 촉매제가 기존의 화학 공정을 단축시킨다고 할 수 있는지에 대하여
    검정하시오.
    2. 촉매제로 인한 단축된 공정 시간에 대하여 90% 신뢰구간을 구하시오.
    import pandas as pd
    import numpy as np
    # 파이썬 코드
    time = [2.17, 0.86, 0.91, 3.11, 1.29, 1.25, 0.76, 2.98, 1.21,
    2.23, 0.67, 1.22, 1.23, 1.21, 1.71, 1.80, 1.41, 1.01,
    0.82, 1.03, 2.03, 0.65, 1.01, 0.45, 0.98, 1.04]
    treat = ['before']*13 + ['add_catalyst']*13
    id = list(range(1,27))
    prac4_1 = pd.DataFrame({'ID':id,
    'Time':time,
    'treat':treat})
    prac4_1.head()
    ^༈ ID Time treat
    ^༈ 0 1 2.17 before
    ^༈ 1 2 0.86 before
    ^༈ 2 3 0.91 before
    ^༈ 3 4 3.11 before
    ^༈ 4 5 1.29 before
    """