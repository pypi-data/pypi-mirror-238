def m4():
    """
    4  데이터 분할
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor

    dat = pd.read_csv('./data/ex_data/adp1.csv')

    y = dat.grade
    X = dat.drop(['grade'], axis = 1)

    4.1 데이터 분할 이유
    머신러닝의 목적은 미래를 정확히 예측하는 최적의 알고리즘을 찾는 것입니다. 즉, 과거 데이터를 이용해서 학습한 결과를 미래 데이터에 적용했을 때에도 정확히 예측하는 알고리즘을 찾는 것입니다. 이를 위해서 전체 데이터셋을 훈련 데이터(train)와 검증 데이터(test)로 분할합니다.

    훈련 데이터는 우리가 알고 있는 데이터(과거 데이터)로 알고리즘 학습, 초매개변수 조정 등에 사용됩니다. 검증 데이터는 우리가 모르는 데이터(미래 데이터)로 훈련 데이터로 학습한 모델이 미래 데이터에 적용했을 때에도 잘 작동하는지 평가하는데 사용됩니다. 즉, 일반화 가능성을 평가하는데 사용됩니다.

    데이터 분할 방법은 크게 단순 무작위 샘플링, 층화 샘플링 두 가지로 볼 수 있습니다. 다른 방법도 있지만 ADP 시험에서는 한 개념에 대해 최대 두 가지를 제시하라고 나오기 때문에 다른 방법론은 생략했습니다.

    Tip
    시험에서는 데이터 분할 방법을 두 가지 제시하고, 적절한 분할 방법을 선택 후 데이터를 분할하고, 분할 방법을 선택한 이유에 대해 설명하라고 나옵니다. 따라서 대표적인 분할 방법 두 가지에 대한 간략한 개념을 이해하고 방법론을 선택한 이유를 적절하게 제시할 수 있으면 됩니다.

    4.1.1 Simple random sampling
    데이터를 무작위로 특정 비율로 분할하는 방법입니다. 보통 train/test 비율은 
    , 
    로 분할합니다. 표본의 크기가 클 경우 일반적으로 훈련 데이터와 검증 데이터는 유사한 분포를 갖습니다.

    단점

    범주형 변수의 각 범주의 빈도가 불균형일 때 단순 무작위 샘플링을 할 경우 훈련 데이터와 검증 데이터의 분포가 달라질 수 있음

    연속형 변수의 경우 분포가 치우쳐져 있을 때 단순 무작위 샘플링을 할 경우 훈련 데이터와 검증 데이터의 분포가 달라질 수 있음

    train_test_split()

    test_size : 테스트 데이터의 비율

    random_state : 난수 발생값(train/test 데이터 재현을 하기 위해서는 고정 필요)

    shuffle = True(default) : 데이터 분할 전 데이터를 섞을지 여부

    stratify = None(default) : 층화추출 여부

    Caution
    shuffle = False일 경우 stratify = None이어야 합니다.

    from sklearn.model_selection import train_test_split

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    print('trainX shape : ',  train_X.shape)

    trainX shape :  (292, 10)
    print('trainy shape : ',  train_y.shape)

    trainy shape :  (292,)
    print('testX shape : ',  test_X.shape)

    testX shape :  (74, 10)
    print('testy shape : ',  test_y.shape)

    testy shape :  (74,)
    4.1.2 strata sampling
    strata sampling은 범주 불균형 문제에 대한 해결 방안으로 범주의 빈도를 고려해서 샘플링을 진행합니다. 각 범주에 해당하는 하위 샘플에 별도로 simple random sampling을 수행한 후 데이터를 분할하고, 이후 결합하는 방식으로 데이터셋을 분할하는 방법입니다. 연속형 변수의 경우 quantile을 기준으로 비닝을 함으로써 범주형 변수에서 시행하는 것과 같은 방식으로 진행됩니다.

    범주형 일 때



    그림을 보면 빨간색이 여자, 파란색이 남자라고 해보겠습니다. 성별에 따라 각 층을 나누고, random sampling을 진행합니다. 이렇게 진행할 경우 여성 혹은 남성의 빈도가 적을 경우 random sampling의 문제인 훈련 데이터셋에 소수 범주가 뽑힐 확률이 적어지는 문제를 해결할 수 있습니다.

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = X['school'], random_state = 0)

    import matplotlib.pyplot as plt
    test_y.hist()
    plt.show()



    연속형일 때



    그림을 보면 양쪽 끝에 가격이 싸거나 비싼 값이 있습니다. 상대적으로 가격이 비싼 경우 랜덤샘플링을 진행할 때 훈련 데이터에 포함되지 않을 수 있습니다. 따라서 quantile을 기준으로 비닝을 하고, strata sampling을 진행함으로써 이러한 문제를 해결합니다.

    비닝

    연속형 변수를 이산형 변수로 변환하는 방법입니다. 보통 분위수(quantile)를 기준으로 이산화를 진행합니다. 아래 코드에서는 10분위수를 기준으로 비닝을 했습니다.

    bins = np.nanquantile(y, np.arange(0, 1, 0.1))
    y_binned = np.digitize(y, bins)
    y_binned[0:10]

    array([ 2,  2,  5, 10,  5, 10,  6,  2, 10,  4])
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, stratify = y_binned, random_state = 0)

    import matplotlib.pyplot as plt
    test_y.hist()
    plt.show()

    """