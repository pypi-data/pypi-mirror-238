def m2():
    """
    2  EDA
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 

    2.1 분석 전 준비작업
    2.1.1 Data description
    데이터는 ADP 21회, 24, 28회 머신러닝 파트에 나왔던 데이터입니다. 해당 데이터로 실습을 진행해보겠습니다. 실제 시험장에서는 아래 데이터 설명에 관한 자료를 프린트로 제공해줍니다.

    school - 학교 유형 (binary: “GP” or “MS”)

    sex - 학생들의 성별 (binary: “F” - female or “M” - male)

    paid - 과목(Math or Portuguese)에 대한 추가 유료 수업 수강 여부 (binary: yes or no)

    famrel - 가족관계 (numeric: from 1 - very bad to 5 - excellent)

    freetime - 방과 후 자유시간 (numeric: from 1 - very low to 5 - very high)

    goout - 친구들과의 외출 빈도 (numeric: from 1 - very low to 5 - very high)

    Dalc - 주중 알코올 소비량 (numeric: from 1 - very low to 5 - very high)

    Walc - 주말 알코올 소비량 (numeric: from 1 - very low to 5 - very high)

    health - 현재 건강 상태 (numeric: from 1 - very bad to 5 - very good)

    absences - 결석 횟수 (numeric: from 0 to 93)

    G3 - 성적 등급 (numeric: from 1 to 11, output target)

    2.1.2 데이터 불러오기
    dat = pd.read_csv('./data/ex_data/adp1.csv')

    데이터를 불러왔을 때 가장 먼저 해야할 일은 데이터를 재대로 불러왔는지 확인하는 것입니다. 변수명이 한글이거나 특수문자가 올 경우 글자가 깨질 수 있습니다. 값에 한글이 있을 경우 인코딩 문제로 글자가 깨질 수 있습니다. 한글로 데이터가 깨질 경우 encoding = ‘utf-8’ or ‘CP949’옵션을 이용하면 됩니다.

    dat = pd.read_csv('./data/ex_data/adp1.csv', encoding = "utf-8")

    2.1.3 데이터의 형태 확인
    dat.head()

      school sex paid  famrel  freetime  goout  Dalc  Walc  health  absences  grade
    0     GP   F   no       4         3    4.0     1     1       3         6      1
    1     GP   F   no       5         3    3.0     1     1       3         4      1
    2     GP   F  yes       4         3    2.0     2     3       3        10      4
    3     GP   F  yes       3         2    2.0     1     1       5         2      9
    4     GP   F  yes       4         3    2.0     1     2       5         4      4
    2.1.4 변수명 간결하게 변경
    2.1.4.1 janitor 패키지 이용
    import janitor

    변수명에 대·소문자가 섞여있을 경우 데이터 전처리를 할 때 번거로울 수 있습니다. 따라서 변수명을 간결하게 변경해줍니다.

    .clean_names()

    변수명이 영문일 경우 : 소문자로 변경

    변수명에 띄어쓰기가 있을 경우 : _생성

    remove_special = True : 특수문자가 있을 경우 제거

    dat = dat.clean_names()

    Dalc, Walc 변수의 경우 dalc, walc로 변경된 것을 확인할 수 있습니다. 다음으로 특수문자와 한글이 있는 경우를 살펴보겠습니다.

    Example

    df = pd.DataFrame(
        {"시험": range(2),
        "Bell Chart": range(2),
        "Animals@#$%^": range(2)})

    df

       시험  Bell Chart  Animals@#$%^
    0   0           0             0
    1   1           1             1
    df.clean_names().columns

    Index(['시험', 'bell_chart', 'animals@#$%^'], dtype='object')
    한글의 경우 한글 그대로 인식하는 것을 볼수 있습니다. 띄어쓰기의 경우 _를 생성해주었습니다. 특수문자의 경우 변환되지 않은 것을 확인할 수 있습니다. 특수 문자를 제거하기 위해 remove_special = True 옵션을 추가해보겠습니다.

    df.clean_names(remove_special = True)

       시험  bell_chart  animals
    0      0           0        0
    1      1           1        1
    특수문자가 깔끔하게 제거된 것을 볼 수 있습니다. 변수가 많을 경우 janitor 패키지를 사용하는 것을 고려해볼 수 있습니다.

    Caution
    janitor 패키지는 진흥원에서 제공하는 패키지 지원 리스트에 없으므로, 시험 시작 전 미리 패키지를 사전 설치해보시기 바랍니다.

    2.1.4.2 pandas 패키지 이용
    pandas에서 지원하는 .rename() 함수를 이용해서 변수명을 하나씩 변경할 수 있습니다.

    (dat 
        .rename(columns = {'school' : '학교'})
        .columns
    )

    Index(['학교', 'sex', 'paid', 'famrel', 'freetime', 'goout', 'dalc', 'walc',
           'health', 'absences', 'grade'],
          dtype='object')
    2.1.5 변수 속성 확인
    EDA, 모델링을 진행할 때 적절하게 변수 속성을 변경하는 것이 중요합니다. 변수 속성을 확인하는 함수는 다음과 같습니다.

    #dat.dtypes
    dat.info()

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 366 entries, 0 to 365
    Data columns (total 11 columns):
     #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
     0   school    366 non-null    object 
     1   sex       366 non-null    object 
     2   paid      366 non-null    object 
     3   famrel    366 non-null    int64  
     4   freetime  366 non-null    int64  
     5   goout     356 non-null    float64
     6   dalc      366 non-null    int64  
     7   walc      366 non-null    int64  
     8   health    366 non-null    int64  
     9   absences  366 non-null    int64  
     10  grade     366 non-null    int64  
    dtypes: float64(1), int64(7), object(3)
    memory usage: 31.6+ KB
    .info() 함수를 이용해서 변수 속성을 확인하고 data description 내용과 매칭해서 변환해야할 변수를 정리해주어야 합니다. 총 데이터 행 개수는 366이며, 12개 칼럼이 존재하는 것을 알 수 있습니다. school, sex, paid 변수는 objec형(문자형)을 의미합니다. 다른 변수들은 int64(정수형), float64(실수형)인 것을 확인할 수 있습니다. goout 변수의 경우 non-null인 행이 356이므로, 결측치가 10개 존재하는 것을 확인할 수 있습니다.

    2.2 EDA(탐색적 자료분석)
    2.2.1 변수 속성 변환
    변수별 그래프를 그리기 전에 변수별 속성을 확인하고 바꿔주어야 합니다. .astype() 함수를 이용해서 변수 속성을 변환해볼 수 있습니다.

    Example

    (dat
        .astype({'famrel' : 'int32', 'dalc' : 'float64'})
        .info()
    )

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 366 entries, 0 to 365
    Data columns (total 11 columns):
     #   Column    Non-Null Count  Dtype  
    ---  ------    --------------  -----  
     0   school    366 non-null    object 
     1   sex       366 non-null    object 
     2   paid      366 non-null    object 
     3   famrel    366 non-null    int32  
     4   freetime  366 non-null    int64  
     5   goout     356 non-null    float64
     6   dalc      366 non-null    float64
     7   walc      366 non-null    int64  
     8   health    366 non-null    int64  
     9   absences  366 non-null    int64  
     10  grade     366 non-null    int64  
    dtypes: float64(2), int32(1), int64(5), object(3)
    memory usage: 30.1+ KB
    float or int에 붙는 숫자는 비트를 의미합니다. 64비트는 32비트에 비해서 더 큰 숫자를 저장하지만, 용량을 많이 차지합니다. ADP 시험에서는 크게 중요하지 않습니다.

    2.2.2 변수 생성 or 변수 변경
    새로운 변수를 생성하거나 특정 변수를 변경하고 싶을 경우 .assign() 함수를 이용할 수 있습니다. 또한 종종 사용되는 lambda 함수도 함께 이용해볼 수 있습니다.

    Example famrel 변수를 표준화해보겠습니다.

    (dat
        .assign(famrel = lambda x: x.famrel - np.nanmean(x.famrel)/np.std(x.famrel))
        .head(2)
    )

      school sex paid   famrel  freetime  ...  dalc  walc  health  absences  grade
    0     GP   F   no -0.41557         3  ...     1     1       3         6      1
    1     GP   F   no  0.58443         3  ...     1     1       3         4      1

    [2 rows x 11 columns]
    (dat
        .assign(famrel = lambda x: x['famrel'] - np.nanmean(x['famrel'])/np.std(x['famrel']))
        .head(2)
    )

      school sex paid   famrel  freetime  ...  dalc  walc  health  absences  grade
    0     GP   F   no -0.41557         3  ...     1     1       3         6      1
    1     GP   F   no  0.58443         3  ...     1     1       3         4      1

    [2 rows x 11 columns]
    lambda 함수에서 x는 assign 함수가 적용된 dat를 의미합니다. lambda 함수를 이용해서 원하는 형태로 변수를 변경해볼 수 있습니다. lambda 함수 내에서는 x[‘famrel’] 형태와 x.famrel 형태 둘다 동일한 결과를 산출합니다.

    하나의 칼럼이 아닌 다수의 칼럼에 특정 함수를 적용해야할 경우도 있습니다. 이 경우 .apply() 함수를 이용해볼 수 있습니다. 특정 칼럼을 지정한 후 .apply(원하는 함수) 형태로 활용해볼 수 있습니다.

    Example

    먼저 표준화 함수를 정의해주었습니다.

    def standardize(x):
        return (x - np.nanmean(x)/np.std(x))

    famrel, freetime 변수에 표준화 함수를 동시에 적용해보겠습니다.

    (dat[['famrel', 'freetime']]
        .apply(standardize)
        .head(2)
    )

        famrel  freetime
    0 -0.41557 -0.242302
    1  0.58443 -0.242302
    standardize() 함수를 정의한 후 .apply() 함수를 적용했을 때, famrel, freetime가 표준화된 것을 확인할 수 있습니다.

    2.2.3 변수 선택
    변환해야 하는 변수가 많을 경우, 코드가 길어질 수 있습니다. 따라서 특정 패턴이 존재하는 경우 패턴에 따라 변수를 선택해볼 수 있습니다.

    Example1

    ’f’로 시작하는 변수에 표준화 함수를 적용해보겠습니다. str.startwith() 함수를 이용해서 칼럼명이 ’f’로 시작하는 경우 true, 아닐 경우 false로 필터링해줬습니다. 필터링한 칼럼명에 .apply() 함수를 이용해서 표준화 함수를 적용해줬습니다.

    (dat
        .loc[:, dat.columns.str.startswith('f')]
        .apply(standardize)
        .head(2)
    )

        famrel  freetime
    0 -0.41557 -0.242302
    1  0.58443 -0.242302
    Example2

    ’c’로 시작하는 변수에 표준화 함수를 적용해보겠습니다. str.endswith() 함수를 이용해서 칼럼명이 ’c’로 시작하는 경우 true, 아닐 경우 false로 필터링해줬습니다. 필터링한 칼럼명에 .apply() 함수를 이용해서 표준화 함수를 적용해줬습니다.

    (dat
        .loc[:, dat.columns.str.endswith('c')]
        .apply(standardize)
        .head(2)
    )

           dalc      walc
    0 -0.677095 -0.789321
    1 -0.677095 -0.789321
    Example3

    ’f’를 포함하는 변수에 표준화 함수를 적용해보겠습니다. str.contains() 함수를 이용해서 칼럼명이 ’f’를 포함하는 경우 true, 아닐 경우 false로 필터링해줬습니다. 필터링한 칼럼명에 .apply() 함수를 이용해서 표준화 함수를 적용해줬습니다.

    (dat
        .loc[:, dat.columns.str.contains('f')]
        .apply(standardize)
        .head(2)
    )

        famrel  freetime
    0 -0.41557 -0.242302
    1  0.58443 -0.242302
    .select_dtypes() 함수를 이용해서 특정 변수를 모두 선택한 후 .apply() 함수를 적용해볼 수 있습니다.

    .select_dtypes(include = ’’)

    숫자형 : ‘number’

    문자형 : ‘object’

    날짜, 시간 : ‘datetime’, ‘timedelta’

    Example

    .select_dtypes('number')를 통해 수치형 변수만 선택해줬습니다. 선택된 칼럼명에 .apply() 함수를 이용해서 표준화 함수를 적용해줬습니다.

    (dat
        .select_dtypes('number')
        .apply(standardize)
        .head(2)
    )

        famrel  freetime     goout  ...    health  absences     grade
    0 -0.41557 -0.242302  1.192457  ...  0.408977  5.310415 -0.639516
    1  0.58443 -0.242302  0.192457  ...  0.408977  3.310415 -0.639516

    [2 rows x 8 columns]
    .select_dtypes('object')를 통해 범주형 변수만 선택해줬습니다.

    (dat
        .select_dtypes('object')
        .head(2)
    )

      school sex paid
    0     GP   F   no
    1     GP   F   no
    2.2.4 데이터 재구조화
    데이터를 재구조화하는 것은 데이터 전처리를 할 때 중요한 부분입니다. 특히 long form으로 바꾸는 것은 꼭 필요한 부분이므로, 숙지하시길 바랍니다.



    예시를 보면 왼쪽이 wide form 형태이고, 오른쪽이 long form 형태입니다. wide form에서 long form으로, long form에서 wide form으로 자유자재로 바꾸는 것이 중요합니다.

    pd.melt() : wide form에서 long form으로 바꾸는 함수

    id_vars : 기준 칼럼
    value_vars : long form으로 바꾸고 싶은 칼럼
    var_name : long form으로 바꿨을 때 생성되는 변수의 변수명(default : variable)
    value_name : long form으로 쌓은 값(default : value)
    ignore_index = False : 기존 index 사용 여부
    Note
    id_vars 옵션을 지정하지 않고, ignore_index = True 옵션을 지정할 경우 .pivot() 함수를 통해 wide form으로 역변환할 때, 잘못된 결과가 산출될 수 있습니다.

    Example

    먼저 범주형 변수를 cat_columns로 저장했습니다. pd.melt() 함수를 통해서 데이터를 long form으로 변경해줬습니다.

    cat_columns = dat.select_dtypes('object').columns

    long_df = pd.melt(dat,
            value_vars = cat_columns, 
            var_name = 'cat_variable', 
            value_name = 'value', 
            ignore_index = False)

    long_df.head(2)

      cat_variable value
    0       school    GP
    1       school    GP

    # long_df = pd.melt(dat.reset_index(), 
    #         id_vars = 'index',
    #         value_vars = cat_columns, 
    #         var_name = 'cat_variable', 
    #         value_name = 'value')
    #         
    # long_df.head(2)

    long form으로 변환된 데이터는.pivot() 함수를 통해 다시 wide form으로 재변환할 수 있습니다.

    .pivot()

    index : 인덱스로 사용될 칼럼

    columns : wide form으로 바꿀 칼럼

    values : 값으로 입력될 칼럼

    (long_df
        .pivot(columns = 'cat_variable', values = 'value')
        .head(2)
    )

    cat_variable paid school sex
    0              no     GP   F
    1              no     GP   F
    2.2.5 요약통계량
    변수 속성을 변경한 후에 가장 처음 확인해야 하는 것이 변수별 요약통계량입니다. 변수별 요약통계량에서 확인해야될 사항은 다음과 같습니다.

    결측치 및 이상치 확인

    goout에 결측치 10개 존재

    absences의 경우 max 값이 75로 이상치로 의심됨

    변수별 요약통계량은 .describe() 함수를 통해 확인해볼 수 있습니다.

    pd.options.display.max_columns = None # full 출력 옵션 
    dat.describe()

               famrel    freetime       goout        dalc        walc      health   
    count  366.000000  366.000000  356.000000  366.000000  366.000000  366.000000  \
    mean     3.942623    3.207650    3.098315    1.469945    2.278689    3.576503   
    std      0.894113    0.990667    1.105121    0.877683    1.275237    1.382234   
    min      1.000000    1.000000    1.000000    1.000000    1.000000    1.000000   
    25%      4.000000    3.000000    2.000000    1.000000    1.000000    3.000000   
    50%      4.000000    3.000000    3.000000    1.000000    2.000000    4.000000   
    75%      5.000000    4.000000    4.000000    2.000000    3.000000    5.000000   
    max      5.000000    5.000000    5.000000    5.000000    5.000000    5.000000   

             absences       grade  
    count  366.000000  366.000000  
    mean     5.587432    5.000000  
    std      8.113696    3.053855  
    min      0.000000    0.000000  
    25%      0.000000    3.000000  
    50%      4.000000    5.000000  
    75%      8.000000    7.000000  
    max     75.000000   11.000000  
    2.2.6 시각화
    시각화는 EDA에 포함되는 문제입니다. 시각화에서 확인해야할 내용은 다음과 같습니다.

    반응변수 vs 설명변수 상관계수 확인

    설명변수 vs 설명변수 상관계수 확인

    변수별 분포 확인(연속형 변수의 분포의 치우침, 범주형 변수의 class 불균형 확인)

    범주형 설명변수와 반응변수 boxplot 그리기

    여기서 주의해야할 점은 시각화에 많은 시간을 소요하면 안됩니다. 시각화 배점은 5점 정도이고, 문제에서 요구하는 것이 모호하기 때문에 필요 이상으로 쓰지 않아도 점수가 깍이지 않습니다. 따라서 형식적인 시각화 및 짧은 해석을 하고 넘어갑니다. 대신 EDA 과정에서 데이터에 함정이 있지 않은지 유의하면서 진행해줘야 합니다.

    pandas는 간단한 시각화 툴을 제공합니다. 대표적인 시각화툴인 matplotlib을 불러와서 사용하므로, matplotlib 패키지를 import해야 합니다. pandas를 이용하여 시각화를 해보겠습니다.

    2.2.7 변수별 분포 확인
    # import matplotlib
    # matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    import seaborn as sns

    연속형 변수에 대해서 .hist() method를 통해 변수별 histogram을 간단하게 그려볼 수 있습니다.

    dat.select_dtypes('number').hist();
    plt.show();



    히스토그램을 통해 각 변수의 분포 특징 및 이상치 등을 확인해볼 수 있습니다. 예를 들어 absences 변수의 경우 우측으로 긴꼬리를 갖는 분포 형태로, 결석 횟수는 0인 경우가 가장 많고, 결석 횟수가 75번 이상인 케이스가 존재하며, 이상치로 의심됩니다.

    범주형 변수의 경우 seaborn 패키지를 이용해보겠습니다. .countplot()을 이용하면 간단하게 막대그래프를 그려볼 수 있습니다.

    f, axes = plt.subplots(ncols = 3, figsize = (20,4))
    sns.countplot(dat['school'], ax = axes[0])
    sns.countplot(dat['sex'], ax = axes[1])
    sns.countplot(dat['paid'], ax = axes[2])
    plt.show();



    school 유형이 GP인 경우 MS인 경우에 비해 약 8배 이상 많은 것을 볼 수 있으며, school 변수의 경우 클래스 불균형이 존재합니다.

    2.2.8 변수 분포 및 상관관계 확인
    연속형 변수 간의 관계는 산점도와 상관계수를 통해 확인해볼 수 있습니다.

    sns.pairplot(dat.select_dtypes('number'));
    plt.show();



    Correlation plot

    #plt.clf() # 초기화 
    corr = dat.select_dtypes('number').corr()
    sns.heatmap(corr, annot = True)
    plt.show();



    grade와 다른 설명변수 사이에는 상관관계가 낮으며, walc와 dalc, walc와 goout의 경우 다른 변수에 비해서 상대적으로 높은 상관관계를 보이는 것을 확인할 수 있습니다.

    순서형 변수 간의 관계는 spearman 상관계수를 통해 확인해볼 수 있습니다. famrel, goout,..etc 등의 변수는 very low 1 : - very high : 5로 구분되며, 리커트 척도로 볼 수 있습니다. very low가 very high에 비해 5배 높다로 볼 수 있을까요? 리커트 척도 혹은 그와 유사한 형태는 순서형으로 볼 수도 있고, 연속형으로 볼 수도 있습니다(분석가 주관). 다만 순서형 변수로 볼 경우 평균을 계산한다거나, 평균을 이용한 가설 검정을 하는 것은 적절하지 않으므로 주의가 필요합니다.

    #plt.clf() # 초기화 
    corr = dat.loc[:, ['famrel', 'freetime', 'goout', 'dalc', 'walc', 'health']].corr(method = 'spearman')
    sns.heatmap(corr, annot = True)
    plt.show();



    2.2.9 Boxplot
    범주형 변수와 연속형 변수의 관계는 boxplot을 통해 시각화해볼 수 있습니다. 각 범주형 변수와 타겟인 grade와의 관계를 살펴보겠습니다.

    f, axes = plt.subplots(ncols = 3, figsize = (20,4))

    sns.boxplot(x = "school", y = "grade", data = dat, ax = axes[0])
    axes[0].set_title('school vs grade boxplot')

    sns.boxplot(x = "sex", y = "grade", data = dat, ax = axes[1])
    axes[1].set_title('sex vs grade boxplot')

    sns.boxplot(x = "paid", y = "grade", data = dat, ax = axes[2])
    axes[2].set_title('sex vs grade boxplot')

    plt.show();



    학교 유형, 유료 강의 수강 여부에 따른 성적 등급은 큰 차이가 없는 것을 확인할 수 있습니다. 성별에 따른 성적 등급을 보면 남성의 경우 여성에 비해 성적 등급이 높은 경향이 있는 것을 확인해볼 수 있습니다.

    from scipy.stats import ttest_ind
    male = dat.loc[dat.sex == 'M']['grade']
    female = dat.loc[dat.sex == 'F']['grade']

    res = ttest_ind(male, female, 
                          equal_var=False)

    2.2.10 mosaic plot
    범주형 변수 간의 관계는 mosaic plot을 통해 시각화해볼 수 있습니다. statsmodels의 mosaic() 함수를 불러오겠습니다.

    from statsmodels.graphics.mosaicplot import mosaic

    tt = pd.crosstab(dat['sex'], dat['school'])
    tt

    school   GP  MS
    sex            
    F       172  23
    M       153  18
    mosaic(dat, ['school', 'sex'], title='school vs sex')

    (<Figure size 1400x1000 with 3 Axes>, {('GP', 'F'): (0.0, 0.0, 0.8835603403746297, 0.5274725274725275), ('GP', 'M'): (0.0, 0.53079478660874, 0.8835603403746297, 0.4692052133912598), ('MS', 'F'): (0.8885354647527391, 0.0, 0.11146453524726099, 0.5591119034113929), ('MS', 'M'): (0.8885354647527391, 0.5624341625476055, 0.11146453524726099, 0.43756583745239436)})
    plt.show();



    학교 유형에 따른 성별의 관계를 확인해본 결과 대체로 큰 차이가 없어보입니다.

    from scipy.stats import fisher_exact
    oddsr, p = fisher_exact(table=tt.to_numpy(), alternative='two-sided')
    oddsr, p

    (0.8797953964194374, 0.741976356513386)
    fisher exact test 결과를 보면 유의수준 5%에서 p-value = 0.74로 매우 크기 때문에 귀무가설을 기각할 수 없습니다. 따라서 학교 유형과 성별은 유의미한 연관성이 없다고 볼 수 있습니다.

    from scipy.stats import fisher_exact
    oddsr, p = fisher_exact(table=tt.to_numpy(), alternative='two-sided')
    oddsr, p

    (0.8797953964194374, 0.741976356513386)

    # from scipy.stats import chi2_contingency
    # c, p, dof, expected = chi2_contingency(tt)
    # p
    """
