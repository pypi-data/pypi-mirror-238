def m5():
    """
    5  Data leakage
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor

    EDA에 이용했던 데이터를 다시 불러오겠습니다.

    dat = pd.read_csv('./data/ex_data/adp1.csv')

    위에서 설명했다시피 데이터를 훈련데이터와 검증 데이터로 분할하는 이유는 과거 데이터를 이용해서 학습한 결과를 미래 데이터에 적용했을 때에도 정확히 예측하는 알고리즘을 찾기 위해서입니다. 즉, 훈련 데이터(train)는 과거 데이터로, 우리가 알고 있는 데이터이고, 검증 데이터(test)는 미래 데이터로 우리가 모르는 데이터입니다. 따라서 실제 데이터 분석을 실시할 때에는 우리가 모르는 데이터인 검증 데이터의 정보를 이용하면 안됩니다.

    데이터 전처리 파트에서는 train/test 데이터를 묶은 all data를 이용해서 EDA, 결측치 대치 등 데이터 전처리를 진행했습니다. 이렇게 진행할 경우 all data에 test 데이터의 정보가 포함되어 있기 때문에 data leakage에 해당합니다.

    Example

    from sklearn.impute import SimpleImputer

    dat1 = dat.copy()

    imputer_mean = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    dat1['goout'] = imputer_mean.fit_transform(dat1[['goout']])
    #dat1['goout'].isna().sum()

    다만 ADP 시험 기출문제를 분석해보면 분석 절차가 data leakage에 해당하게 설계해놓은 경우가 있습니다(ADP 21회차 이전). 이 경우에는 data leakage에 해당하더라도 문제에 제시된 분석 절차에 맞게 분석하는 것이 맞습니다. 이 경우를 제외하고는 train 데이터를 기준으로 데이터 전처리를 실시해야 합니다. 따라서 먼저 전체 데이터를 train/test로 분할합니다.

    from sklearn.model_selection import train_test_split

    y = dat.grade
    X = dat.drop(['grade'], axis = 1)

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    imputer_mean = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    train_X['goout'] = imputer_mean.fit_transform(train_X[['goout']])
    test_X['goout'] = imputer_mean.transform(test_X[['goout']])

    train_X['goout'].isna().sum()

    0
    test_X['goout'].isna().sum()

    0
    train을 기준으로 만든 전처리 툴을 test 데이터에 적용하기 위해서는 transform() 함수를 이용하면 됩니다. 이 경우 train 데이터의 정보를 이용해서 test 데이터에 대한 전처리를 진행하기 때문에 data leakage가 발생하지 않습니다. 혹은 pipline을 이용하면 더 간단하게 처리할 수 있습니다.

    5.0.1 Example 1
    먼저 표준화를 해보겠습니다.

    trainX = pd.DataFrame({'x1': range(1, 9, 1), 'x2': range(15,23, 1)})
    testX = pd.DataFrame({'x1': [1, 3, 5], 'x2': [2, 4, 6]})

    from sklearn.preprocessing import StandardScaler

    stdscaler = StandardScaler()
    stdscaler.fit_transform(trainX)

    array([[-1.52752523, -1.52752523],
           [-1.09108945, -1.09108945],
           [-0.65465367, -0.65465367],
           [-0.21821789, -0.21821789],
           [ 0.21821789,  0.21821789],
           [ 0.65465367,  0.65465367],
           [ 1.09108945,  1.09108945],
           [ 1.52752523,  1.52752523]])
    stdscaler.transform(testX)

    array([[-1.52752523, -7.20119038],
           [-0.65465367, -6.32831882],
           [ 0.21821789, -5.45544726]])
    (1 - np.mean(range(1, 9, 1)))/np.std(range(1, 9, 1))

    -1.5275252316519468
    #(1 - np.mean(range(1, 9, 1)))/np.std(range(1, 9, 1), axis = 0, ddof = 1)

    train 데이터와 test 데이터에 첫 번째 인덱스에는 1이 존재합니다. 결과를 보면 train/test 모두 -1.527인 것을 확인할 수 있습니다. 즉, train 데이터의 평균과 분산으로 test 데이터가 normalize 되는 것을 볼 수 있습니다.

    Note
    R 교재의 결과와 표준화 값이 다른 이유는 표준편차를 계산할 때, np.std()의 경우 N으로 나눠주고, R의 sd()에서는 N-1로 나눠주기 때문입니다.
    """