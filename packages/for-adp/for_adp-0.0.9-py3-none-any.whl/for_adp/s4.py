def s4():
    """
    제 4 장
    비모수 검정 친해지기
    4.1 비모수 검정 이해를 위한 준비운동
    이제까지의 검정들은 모두 스튜던트 정리에 기반한 모수 검정들이었습니다. 하지만 이 정리는 표본들
    이 정규분포에서 뽑혀져 나온다는 큰 가정에 기반하고 있습니다. 따라서 검정을 하기 전 가정 체크시
    정규성을 위반한 경우는 적용할 수 없습니다. 데이터가 주어졌을때, 다음과 같은 가정 체크에 따라서
    모수 검정과 비모수 검정 중 알맞은 검정을 선택하도록 합시다.
    두 그룹 이하 평균 비교 검정의 고려 순서도
    집단 1개
    • 정규성 체크
    – Yes: t‑test 시행
    – No: 대칭성 확인
    *
    Yes: Wilcoxon signed‑rank test
    *
    No: Sign test
    집단 2개
    • 정규성 체크
    – Yes
    * 등분산 체크 (F‑test)
    · Yes: 2 sample t‑test 시행
    · No: Welch’s t‑test
    – No:
    * 등분산 체크 (Levene test)
    · Yes: Mann‑Whitney‑Wilcoxon test (= Wilcoxon rank‑sum test)
    · No: Brunner‑Munzel test
    비모수 검정 친해지기 | 77
    비모수 검정의 장점
    일반적으로 비모수 검정은 다음과 같은 장점을 가지고 있습니다.
    1. 정규성 가정이 필요하지 않습니다.
    정규성 가정이 필요하지 않다는 것은 검정에 필요한 가정이 적어져, 검정을 적용할 수 있는 경우가
    많다는 의미입니다.
    2. 이상치에 민감하지 않습니다.
    검정 통계량 값이 데이터에 따라 변동하는 것이 적어서 이상치가 있더라도 검정 결과에 큰 영향을
    주지 않는다는 의미입니다.
    3. 통계량이 직관적인 경우가 많습니다.
    해당 검정 통계량을 이해하고 사용하기 쉽다는 의미입니다. 이로 인해 통계적 분석 결과를 직관적
    으로 이해하고 해석할 수 있습니다.
    비모수 검정을 매번 사용하지 않는 이유
    비모수 검정 방법은 자료가 정규분포를 따를 때에 비해 모수 검정 방법보다 파워(검정력)가 약할 수
    있습니다.
    • 검정력 (Power) ‑ 귀무가설이 참이 아닐 때, 귀무가설을 기각하는 확률
    비모수 검정시 유의 사항
    앞에서 살펴본 검정들은 t 검정 관련 함수를 사용했던 것처럼, 이번에는 상황에 맞는 비모수 검정 함수를
    사용합니다. 비모수 검정과 관련한 함수를 사용할 때 다음 사항들을 꼭 인지하고 있어야 합니다.
    • 비모수 검정은 모수의 중심점을 평균이 아닌 중앙값으로 설정하고, 중앙값에 대한 검정을 수행
    • 모 중앙값을 나타내는 그리스 문자로 𝜂사용1
    : 귀무 가설과 대립가설 설정 시 꼭 변경
    Levene 검정을 이용한 등분산 가정 체크
    비모수 검정에서 등분산 가정을 체크할 때, Levene 검정을 일반적으로 많이 사용합니다. Levene
    검정은 유료 통계프로그램 (SPSS etc.) 에서 분산 비교 시 사용하는 일반적인 검정 방법입니다.
    F 검정과의 비교
    이전 챕터에서 배운 F 검정의 경우, 스튜던트 정리의 2번째 사실인 카이제곱분포 확률변수를 분모꼴로
    나타낸 검정통계량을 사용했었습니다. 따라서 데이터가 정규분포에서 뽑혀져 나왔다는 가정이 필요
    했습니다. Levene 검정은 F 검정과 비교하여 다음과 같은 특징이 있습니다.
    • 2개 이상의 그룹에도 적용 가능 (F 검정은 2개 그룹에만 적용 가능)
    • F‑test는 태생이 정규분포와 궁합이 좋은 검정
    • 이상치에 대하여 좀 더 robust 한 검정
    1해당 문제는 위키피디아의 선형계획법 페이지에서 가져옴.
    78 | 비모수 검정 친해지기
    4
    귀무가설 vs. 대립가설
    검정의 귀무가설과 대립가설은 다음과 같습니다.
    • 귀무가설: “모든 그룹이 동일한 분산을 갖는다.”
    – 𝐻0
    : 𝜎
    2
    1 = 𝜎2
    2 = ... = 𝜎2
    𝑘
    • 대립가설: “하나라도 분산이 다른 그룹이 존재한다.”
    – 𝐻𝐴: 𝜎
    2
    𝑖 ≠ 𝜎2
    𝑗
    at least one pair
    검정통계량
    Levene 검정의 검정통계량은 다음과 같습니다.
    𝑊 = (𝑁 − 𝑘)
    (𝑘 − 1) ⋅
    ∑
    𝑘
    𝑖=1 𝑁𝑖
    (𝑍𝑖⋅ − 𝑍⋅⋅
    )
    2
    ∑
    𝑘
    𝑖=1 ∑
    𝑁𝑖
    𝑗=1(𝑍𝑖𝑗 − 𝑍𝑖⋅)
    2
    ,
    이 검정통계량의 특징은 원 데이터를 이용하는 것이 아니라 transformed 된 데이터들 𝑍𝑖𝑗 들을
    사용하여 통계량을 구함
    • 𝑘 그룹이 존재
    • 𝑍𝑖𝑗를 구하는 방법을 3가지로 선택할 수 있음
    – 𝑍𝑖𝑗 = |𝑌𝑖𝑗 − 𝑌̄
    𝑖.|: 각 그룹의 평균에서의 deviation
    – 𝑍𝑖𝑗 = |𝑌𝑖𝑗 − 𝑌̃
    𝑖.|: 각 그룹의 중앙값에서의 deviation
    – 𝑍𝑖𝑗 = |𝑌𝑖𝑗 − 𝑌 ′̄
    𝑖.|: 각 그룹의 10% 절단 평균에서의 deviation
    • mean: 대칭, median: 치우침, trimmed mean: 두터운 꼬리
    Python에서 Levene 검정 수행하기
    Python에서 Levene 검정을 수행하는 방법은 다음과 같다.
    예제 데이터 불러오기 총 관찰 데이터는 30개이며 자료 구조는 다음과 같다.
    #Levene’s test 관련 패키지 불러오기
    from scipy.stats import levene
    import pandas as pd
    import numpy as np
    mydata = pd.read_csv('./data/tooth_growth.csv')
    mydata.head()
    ^༈ len supp dose
    ^༈ 0 11.2 VC 0.5
    ^༈ 1 9.4 OJ 0.5
    비모수 검정 이해를 위한 준비운동 | 79
    ^༈ 2 25.2 OJ 1.0
    ^༈ 3 16.5 OJ 0.5
    ^༈ 4 16.5 VC 1.0
    levene() 함수 사용하기
    두 그룹으로 분리 후, levene() 함수를 사용하여 수행합니다.
    a = mydata[mydata['supp'] ^༰ 'OJ']['len']
    b = mydata[mydata['supp'] ^༰ 'VC']['len']
    levene(b, a, center='mean')
    ^༈ LeveneResult(statistic=0.06815502357191881, pvalue=0.7959528904404206)
    • Option 선택
    – center = "median" (기본) 혹은 "mean" 혹은 "trim"
    – proportiontocut = 0.05 (trim 선택 시 사용)
    4.2 비모수 검정 방법
    Wilcoxon signed rank test (1 표본 검정)
    • 가정 1: 데이터가 연속 확률분포를 따른다. (체크 불필요)
    • 가정 2: 데이터가 대칭 분포를 따른다. (체크 필요, 그래프)
    One Sample 예제 데이터
    그룹이 1개의 동일 그룹으로 이루어진 데이터에 대응하는 검정이다. 3장에서 사용한 학생들의 성별에
    따른 점수 조사 데이터를 다시 사용하자.
    표 4.1: 학생들의 점수 조사표 (기본형태)
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
    80 | 비모수 검정 친해지기
    4
    귀무가설 vs. 대립가설
    앞에서 배웠던 t 검정의 귀무가설과 대립가설 종류와 동일합니다.
    • 𝜂 = 𝜂0
    vs. 𝜂 ≠ 𝜂0
    • 𝜂 ≥ 𝜂0
    vs. 𝜂 < 𝜂0
    • 𝜂 ≤ 𝜂0
    vs. 𝜂 > 𝜂0
    자료 입력
    import numpy as np
    sample = np.array([9.76, 11.1, 10.7, 10.72, 11.8, 6.15, 10.52,
    14.83, 13.03, 16.46, 10.84, 12.45])
    검정 통계량
    모중앙값 𝜂0에 대한 검정 통계량 𝑊+은 다음과 같습니다.
    𝑊+ =
    𝑛
    ∑
    𝑖=1
    𝜓 (𝑋𝑖 − 𝜂0
    ) 𝑅𝑖
    여기서 𝜓(𝑥) 함수는 입력값 𝑥가 0보다 크면 1, 0보다 작거나 같은 경우 0을 반환합니다.
    • 코드로 직접 구해보기
    import numpy as np
    from scipy.stats import rankdata
    sample_diff = abs(np.array(sample) - 10)
    sample_rank = rankdata(sample_diff)
    sample_sign = np.sign(np.array(sample) - 10)
    sum(sample_rank[sample_sign > 0])
    ^༈ 67.0
    핵심 아이디어
    귀무가설이 참이라면 𝜂0를 중심으로 데이터가 균형을 이루며 퍼져있어야 할 것이다. 따라서 이상적인
    𝑊+인 값은 전체 순위합의 절반인 𝑛(𝑛 + 1)/4가 되어야 한다. 이 값에서 멀어질 수록 (크거나 작게
    된다면) 귀무가설을 기각하는 근거가 된다.
    • 𝑊+ 값의 이론적인 최대값은 전체 순위합인 𝑛(𝑛 + 1)/2가 된다.
    비모수 검정 방법 | 81
    가정체크 방법
    검정의 가정이 데이터의 분포가 대칭이룬다는 가정이 있으므로 확인을 해봐야 한다. 하지만 분포의
    대칭을 검정하는 방법은 현재 정확하게 정립된 것이 없는 것으로 보이므로 주어진 표본의 히스토그램을
    그려서 확인하도록 하자.
    import matplotlib.pyplot as plt
    plt.hist(sample);
    plt.show()
    6 8 10 12 14 16
    0
    1
    2
    3
    4
    5
    Python에서 검정하기
    scipy.stats의 wilcoxon() 함수를 사용합니다. 함수에서 사용할 수 있는 옵션들은 3장에서 배웠던 t
    검정 함수와 똑같으므로 설명을 생략한다. 다만, 주의점은 데이터의 입력을 귀무가설 하에서 주어진
    𝜂0 값에서 빼준 데이터를 입력해줘야 한다는 것입니다.
    from scipy.stats import wilcoxon
    eta_0=10
    statistics, pvalue = wilcoxon(sample-eta_0, alternative="two༡sided")
    print("Test statistic: ", statistics)
    ^༈ Test statistic: 11.0
    print("p༡value: ", pvalue)
    ^༈ p༡value: 0.02685546875
    5% 유의수준 하에서 p‑value 값이 작으므로, 귀무가설을 기각합니다. 해석할 때 모평균이라는 단어
    대신 분포의 중앙이라는 단어를 사용해야 함에 주의하세요!
    82 | 비모수 검정 친해지기
    4
    참고사항 위의 파이썬 코드와 R에서의 wilcox.test()함수의 검정통계량 값이 다릅니다. 이유는 R
    에서는 양수인 RANK의 합을 반환하는 반면, 파이썬에서는 양수 쪽, 음수 쪽 SUM(RANK) 중 작은 것을
    반환하기 때문입니다.
    a = np.arange(start=1, stop=13)
    print("R 결과와 같게끔 출력, Test statistic: ", sum(a)-statistics)
    ^༈ R 결과와 같게끔 출력, Test statistic: 67.0
    • R에서 결과 확인
    sample <- c(9.76, 11.1, 10.7, 10.72, 11.8, 6.15,
    10.52, 14.83, 13.03, 16.46, 10.84, 12.45)
    wilcox.test(sample, mu =10, alternative ="two.sided")
    ^༈
    ^༈ Wilcoxon signed rank exact test
    ^༈
    ^༈ data: sample
    ^༈ V = 67, p༡value = 0.02686
    ^༈ alternative hypothesis: true location is not equal to 10
    Mann‑Whitney‑Wilcoxon test (2 표본 검정)
    2 표본 독립 그룹을 가정
    2개의 독립적인 그룹에서 추출된 데이터에 대응하는 검정 방법입니다. 또한, 각 그룹의 분산이 동일
    하다는 가정을 하고 있는 검정입니다. 따라서, Levene 검정을 사용하여 각 그룹의 등분산성을 체크한
    후, 진행하도록 합시다.
    예제 데이터
    3장에서 사용된 학생들의 성별 점수 조사 데이터를 다시 사용합니다.
    자료 입력
    import pandas as pd
    sample = [9.76, 11.1, 10.7, 10.72, 11.8, 6.15, 10.52,
    14.83, 13.03, 16.46, 10.84, 12.45]
    gender = ['female']*7 + ['male']*5
    data_wilcoxon = pd.DataFrame({'id': range(1,13),
    'score': sample,
    비모수 검정 방법 | 83
    표 4.2: 학생들의 성별 점수 조사 결과
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
    'gender':gender})
    data_wilcoxon['gender'] = pd.Categorical(data_wilcoxon['gender'],
    categories=['male','female'])
    data_wilcoxon
    ^༈ id score gender
    ^༈ 0 1 9.76 female
    ^༈ 1 2 11.10 female
    ^༈ 2 3 10.70 female
    ^༈ 3 4 10.72 female
    ^༈ 4 5 11.80 female
    ^༈ 5 6 6.15 female
    ^༈ 6 7 10.52 female
    ^༈ 7 8 14.83 male
    ^༈ 8 9 13.03 male
    ^༈ 9 10 16.46 male
    ^༈ 10 11 10.84 male
    ^༈ 11 12 12.45 male
    귀무가설 vs. 대립가설
    • 𝜂1 = 𝜂2
    vs. 𝜂1 ≠ 𝜂2
    • 𝜂1 = 𝜂2
    vs. 𝜂1 < 𝜂2
    • 𝜂1 = 𝜂2
    vs. 𝜂1 > 𝜂2
    검정 통계량
    검정 통계량 𝑈 는 다음과 같이 정의된다.
    84 | 비모수 검정 친해지기
    4
    𝑈 =
    𝑛1
    ∑
    𝑖=1
    𝑛2
    ∑
    𝑗=1
    𝜓 (𝑌𝑗 − 𝑋𝑖
    )
    • 코드로 직접 구해보기
    import itertools
    sample1 = sample[:7]
    sample2 = sample[7:]
    possible_comb = list(itertools.product(sample1, sample2))
    U = sum([x[0] < x[1] for x in possible_comb])
    print(U)
    ^༈ 33
    Wilcoxon rank sum 통계량 MWW 통계량 𝑈 는 𝑋𝑖와 𝑌𝑗의 혼합표본에서 𝑌 들의 순위 𝑅𝑗들의
    합을 계산한 윌콕슨 순위합 (Wilcoxon rank sum) 통계량 𝑊 = ∑ 𝑅𝑗와 다음과 같은 관계가 있습
    니다.
    𝑊 = 𝑈 +
    𝑛
    ∑
    𝑘=1
    𝑘
    따라서 Mann‑Whitney‑Wilcoxon 검정과 Wilcoxon rank sum 검정의 동치 관계에 있다고 할
    수 있습니다.
    • 예제 데이터에서 𝑊 통계량값과 𝑈 통계량 관계 확인하기
    U + sum(range(1,6))
    ^༈ 48
    from scipy.stats import rankdata
    rank_sample = rankdata(sample)
    sum(rank_sample[7:12])
    ^༈ 48.0
    MWW 검정의 핵심 아이디어
    두 분포의 중앙이 같다면 각 그룹에서 하나씩을 뽑아 크기 비교를 하면 그중 절반은 한 그룹에서 뽑은
    표본이 더 커야합니다. 즉, 귀무가설이 참이라면 다음의 값이 0.5와 비슷하게 나와야 합니다.
    비모수 검정 방법 | 85
    U / len(possible_comb)
    ^༈ 0.9428571428571428
    이 값이 0.5에서 멀어질 수록, 귀무가설을 기각하게 되는 근거가 됩니다.
    Python에서 검정하기
    2표본의 경우 mannwhitneyu 모듈의 wilcoxon() 함수를 사용하여 수행합니다.
    from scipy.stats import mannwhitneyu
    male = data_wilcoxon[data_wilcoxon['gender'] ^༰ 'male']['score']
    female = data_wilcoxon[data_wilcoxon['gender'] ^༰ 'female']['score']
    stat, pvalue = mannwhitneyu(male, female)
    print("stat: ", stat.round(3))
    ^༈ stat: 33.0
    print("p༡value: ", pvalue.round(3))
    ^༈ p༡value: 0.01
    유의수준 5% 하에서 p‑value 값이 작으므로 귀무가설을 기각합니다.
    등분산 가정이 깨졌을 경우
    Mann‑Whitney‑Wilcoxon의 등분산 가정을 표본이 만족하지 않는 경우, 일반화 MWW 검정
    이라 불리는 Brunner Munzel 검정을 적용할 수 있습니다. 검정 관련 함수는 scipy 패키지의
    brunnermunzel()을 사용합니다.
    from scipy.stats.mstats import brunnermunzel
    female = data_wilcoxon[data_wilcoxon['gender'] ^༰ 'female']
    male = data_wilcoxon[data_wilcoxon['gender'] ^༰ 'male']
    brunnermunzel(male['score'],female['score'], alternative='two༡sided')
    ^༈ BrunnerMunzelResult(statistic=-6.511302390730245, pvalue=0.00029416889680564974)
    Two‑sample paired 예제 데이터
    특정 변수를 사용하여 1개 그룹으로 변환 가능한 짝이 존재하는 (paired) 데이터에 대응하는 검정
    방법입니다.
    86 | 비모수 검정 친해지기
    4
    표 4.3: 교육 프로그램 수료 후 점수 변화 조사 결과
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
    자료 입력 및 변환
    데이터를 입력하고, 짝이 있는 경우, 짝을 이용해서 데이터를 변환합니다.
    • 자료입력
    import pandas as pd
    id = [1, 2, 3, 4, 5, 6]
    before_after = ['before']*6 + ['after']*6
    tab3 = pd.DataFrame({'id': id*2, 'score': sample,
    'group':before_after})
    tab3['group'] = pd.Categorical(tab3['group'],
    categories=['before','after'])
    tab3
    ^༈ id score group
    ^༈ 0 1 9.76 before
    ^༈ 1 2 11.10 before
    ^༈ 2 3 10.70 before
    ^༈ 3 4 10.72 before
    ^༈ 4 5 11.80 before
    ^༈ 5 6 6.15 before
    ^༈ 6 1 10.52 after
    ^༈ 7 2 14.83 after
    ^༈ 8 3 13.03 after
    ^༈ 9 4 16.46 after
    비모수 검정 방법 | 87
    ^༈ 10 5 10.84 after
    ^༈ 11 6 12.45 after
    • 자료변환
    test3_data = tab3.pivot(index='id', columns='group', values='score')
    test3_data['score_diff'] = test3_data['after'] - test3_data['before']
    test3_data['score_diff']
    ^༈ id
    ^༈ 1 0.76
    ^༈ 2 3.73
    ^༈ 3 2.33
    ^༈ 4 5.74
    ^༈ 5 -0.96
    ^༈ 6 6.30
    ^༈ Name: score_diff, dtype: float64
    귀무가설 vs. 대립가설
    짝이 지어진 그룹간의 차이를 Δ ∶= 𝜂𝑝𝑎𝑖𝑟1
    − 𝜂𝑝𝑎𝑖𝑟2
    로 정의합니다.
    • Δ = 0 vs. Δ ≠ 0
    • Δ = 0 vs. Δ < 0
    • Δ = 0 vs. Δ > 0
    검정 통계량
    변환 된 데이터는 One sample 경우와 똑같다는 것을 알 수 있습니다.
    sample_sign = np.sign(test3_data['score_diff'])
    sum(rankdata(abs(test3_data['score_diff']))[sample_sign > 0])
    ^༈ 19.0
    Python에서 검정하기
    wilcoxon() 함수에 대한 설명은 앞에서 설명한 One Sample 경우와 같으므로 설명은 생략합니다.
    from scipy.stats import wilcoxon
    wilcoxon(test3_data['score_diff'], alternative = 'greater')
    ^༈ WilcoxonResult(statistic=19.0, pvalue=0.046875)
    88 | 비모수 검정 친해지기
    4
    4.3 부호 검정 (Sign test)
    앞에서는 부호(sign)와 순위(rank)를 사용하여 검정 통계량을 만들었습니다. Signed test 부호만을
    가지고 검정하는 부호 검정 방법에 대하여 알아봅니다. 부호 검정은 부호만을 이용한 검정이므로 적
    용할 수 있는 범위는 넓지만, 그만큼 검정력은 떨어지는 검정입니다. 따라서, 부호 검정은 제일 마지막
    선택지로 남겨두도록 하겠습니다.
    귀무가설 vs. 대립가설
    • 𝜂 = 𝜂0
    vs. 𝜂 ≠ 𝜂0
    • 𝜂 ≥ 𝜂0
    vs. 𝜂 < 𝜂0
    • 𝜂 ≤ 𝜂0
    vs. 𝜂 > 𝜂0
    검정 통계량
    모중앙값 𝜂0에 대한 검정 통계량 𝐵은 다음과 같다.
    𝐵 =
    𝑛
    ∑
    𝑖=1
    𝜓 (𝑋𝑖 − 𝜂0
    )
    윌콕슨 부호순위 검정 통계량에서 순위부분을 빼고 더한 값이 된다.
    핵심 아이디어
    만약 귀무가설이 참이라면 𝜂0를 분포의 중앙으로 데이터가 고르게 분포되어야 한다. 따라서 검정통
    계량 값 𝐵는 이항분포 𝐵(𝑛, 0.5)를 따르게 된다. 𝑛은 표본의 크기를 의미한다.
    • 이항분포 𝐵(𝑛, 0.5)에서 계산된 검정통계량 값을 관찰 할 확률로 p‑value를 계산한다.
    • 코드로 직접 구해보기
    sample_sign = np.sign(np.array(sample) - 10)
    sum(sample_sign > 0)
    ^༈ 10
    Python에서 검정하기
    statsmodels 패키지에서 제공하는 sign_test()를 이용하도록 한다.
    from statsmodels.stats.descriptivestats import sign_test
    sample = np.array([9.76, 11.1, 10.7, 10.72, 11.8, 6.15, 10.52,
    14.83, 13.03, 16.46, 10.84, 12.45])
    sign_test(sample, mu0=10)
    ^༈ (4.0, 0.03857421875)
    부호 검정 (Sign test) | 89
    다만, 이 경우 검정통계량 값이 다르게 나오는데, sign_test()의 반환값이 𝜇0보다 큰 표본의 개수
    𝑁(+)와 작은 표본의 개수𝑁(−) 차를 2로 나눈 값을 반환하기 때문이다. 이는 일반적인 검정통계량
    은 아니며, 계산된 p‑value는 동일하다.
    유의수준 5% 하에서 p‑value 값, 0.038이 작으므로 귀무가설을 기각한다.
    p‑value 값의 이해
    주어진 표본의 갯수는 12이고, 귀무가설이 참인 경우 검정통계량 값 𝐵는 이항분포 𝐵(12, 0.5)를
    따르게 되므로 p‑value는 다음과 같이 계산할 수 있다.
    from scipy.stats import binom
    (1 - binom.cdf(9, 12, 0.5)) * 2
    ^༈ 0.03857421875
    이산형 분포의 경우 검정통계량 값보다 같거나 큰 경우를 계산함에 유의하자.
    부호 검정에서의 표본 크기 계산하기
    • 만약 귀무가설에서 고려하는 𝜂0의 값과 같은 표본이 존재하는 경우 표본에서 제외시킨다.
    • 즉, 새로운 표본 갯수 𝑛
    ′는 전체 표본 𝑛에서 𝜂0인 표본 갯수 𝑘를 빼서 계산한다.
    𝑛
    ′ = 𝑛 − 𝑘
    연습문제
    신제품 촉매제
    슬통 회사에서는 이번에 출시한 새로운 촉매제의 효능을 검증하고 싶어한다. 신제품 촉매재는 기존
    공정에서 사용되는 화학반응 속도를 혁신적으로 줄여주는 기능이 탑재되어 있다고 한다.
    회사 제품 검증 부서에서는 기존 공정의 화학 반응속도와 촉매제를 넣은 후의 반응 속도를 측정하여
    데이터를 만들었다.
    1. 유의수준 5%하에서 신제품 촉매제가 기존의 화학 공정을 단축시킨다고 할 수 있는지에 대하여
    검정하시오.
    2. 촉매제로 인한 단축된 공정 시간에 대하여 90% 신뢰구간을 구하시오.
    심장 질환 약 효능
    슬통제약의 신약이 심장 질환 환자의 혈압을 낮출 수 있는지 검증하려고 한다. 표본으로 15명의 환자가
    선택되었으며, 약을 복용하기 전과 복용한 후의 혈압을 측정하였다.
    • 복용전: 130, 125, 120, 135, 140, 136, 129, 145, 150, 135, 128, 140, 139, 130, 145
    • 복용후: 125, 120, 115, 130, 135, 134, 128, 140, 145, 134, 127, 140, 138, 129, 142
    90 | 비모수 검정 친해지기
    4
    표 4.4: 촉매제 성능 비교 데이터
    ID Time Treat
    1 2.17 before
    2 0.86 before
    3 0.91 before
    4 3.11 before
    5 1.29 before
    6 1.25 before
    7 0.76 before
    8 2.98 before
    9 1.21 before
    10 2.23 before
    11 0.67 before
    12 1.22 before
    13 1.23 before
    14 1.21 add_catalyst
    15 1.71 add_catalyst
    16 1.80 add_catalyst
    17 1.41 add_catalyst
    18 1.01 add_catalyst
    19 0.82 add_catalyst
    20 1.03 add_catalyst
    21 2.03 add_catalyst
    22 0.65 add_catalyst
    23 1.01 add_catalyst
    24 0.45 add_catalyst
    25 0.98 add_catalyst
    26 1.04 add_catalyst
    약이 혈압을 실제로 낮추는 것인지 검증하기 위하여 부호 검정을 실시하라. 유의 수준은 0.05로
    하고, 양측 검정을 수행하시오.
    부호 검정 (Sign test) | 91
    """