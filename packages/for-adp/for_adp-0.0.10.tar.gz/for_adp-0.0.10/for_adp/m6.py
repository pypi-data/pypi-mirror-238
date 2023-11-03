def m6():
    """
    6  Resampling method
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor

    EDA에 이용했던 데이터를 다시 불러오겠습니다.

    dat = pd.read_csv('./data/ex_data/adp1.csv')
    y = dat.grade
    X = dat.drop(['grade'], axis = 1)

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.compose import make_column_transformer
    from sklearn.preprocessing import OneHotEncoder

    데이터 전처리 전 data leakage 방지를 위해 데이터를 train/test로 분할합니다.

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    imputer_mean = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    train_X['goout'] = imputer_mean.fit_transform(train_X[['goout']])
    test_X['goout'] = imputer_mean.transform(test_X[['goout']])

    cat_data = train_X.select_dtypes('object')
    cat_columns = cat_data.columns

    transformer = make_column_transformer(
        (OneHotEncoder(), cat_columns),
        remainder='passthrough')


    onehot_train = transformer.fit_transform(train_X)
    #onehot_test = transformer.transform(test_X)
    train_X = pd.DataFrame(onehot_train, columns = transformer.get_feature_names())

    이전 데이터 분할 단계에서 훈련 데이터(train data)와 검증 데이터(test data)를 나눴습니다. 검증 데이터는 모델의 일반화된 성능을 측정하는데 사용됩니다. 다만 미래 데이터이므로 훈련 단계에서 우리가 사용할 수 없습니다. 따라서 훈련 단계에서 일반화된 성능을 측정하기 위해서는 훈련 데이터를 다시 한번 분할해서 validation 데이터를 이용한 test 데이터의 일반화된 성능을 간접적으로 추정할 필요가 있습니다.

    Resampling method는 크게 네 가지로 볼 수 있습니다.

    Hold out

    LOOCV

    k-fold CV

    Repeated CV

    6.1 Hold-out
    Hold-out 방법은 train, validation, test 총 세 개의 데이터셋으로 분류하는 방법입니다. train 데이터셋을 이용해서 머신러닝 모델을 학습하고, 초매개변수를 튜닝합니다. validation 데이터셋을 이용해서 각 초매개변수별 모델의 성능을 평가하고 최적의 초매개변수를 선택합니다. test 데이터셋을 이용해서 최종 모델의 일반화된 성능을 평가합니다.



    장점

    개념적으로 구현하기 쉬우며, 빠르게 계산 가능
    단점

    train 데이터셋과 test 데이터셋을 구분할 때, 어떤 관측치가 각 셋에 포함되는지에 따라 검정오차 추정치의 변동이 클 수 있음
    6.2 LOOCV
    하나의 관측치를 validation 데이터셋으로 두고, 나머지 관측치를 train 데이터셋으로 두고 검정오차 추정치 계산

    이러한 과정을 총 관측치의 개수(
    )만큼 반복해서 검정오차 추정치 계산

    개의 검정오차 추정치를 평균내서 최종 LOOCV 추정치 계산



    장점

    Hold-out 기법에 비해 CV 추정치의 편향이 작음

    개의 관측치를 사용했기 때문에 거의 편향되지 않은 CV 추정치를 구할 수 있음
    Hold-out 기법에 비해 훈련셋/검증셋 분할의 임의성에서 오는 변동성이 작음

    다중 회귀 모형을 이용하는 경우 LOOCV 계산 시간이 하나의 모델 적합과 동일하도록 하는 공식이 있음(시간이 오래 걸리는 문제 해결)

    단점

    계산량이 많음

    k-fold CV에 비해 검정오차 추정치의 분산이 클 수 있음

    sklearn에서 수행 시

    from sklearn.model_selection import LeaveOneOut
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import cross_val_score

    cv = LeaveOneOut()
    lr = LinearRegression()

    cv_score = cross_val_score(lr, train_X, train_y, scoring='neg_mean_squared_error', cv = cv)
    rmse_score = np.sqrt(np.absolute(cv_score))
    mean_rmse_score = np.mean(rmse_score)

    print('RMSE :', rmse_score[1:10])

    RMSE : [0.14658192 3.2381977  5.64481934 0.74410244 2.71588095 0.78539788
     3.02409334 3.4915811  2.87423596]
    print('mean RMSE :', mean_rmse_score)

    mean RMSE : 2.5922752937562397
    LOOCV 결과를 보면 개별 RMSE의 평균은 약 2.59 정도인 것을 확인할 수 있습니다.

    6.3 k-fold CV
    훈련 데이터를 임의의 거의 동일한 크기의 그룹(fold)으로 나누는 리샘플링 방법

    각 fold 중 
     fold는 validation셋으로 취급하고, 나머지 
    개의 fold는 훈련 데이터로 모델 적합에 이용

    이러한 절차는 
    번 반복되며, 매번 다른 그룹의 fold가 validation 셋으로 취급됨

    총 
     개의 추정치(ex. MSE)가 계산되며, 최종 CV 추정치는 
     개의 추정치를 평균내서 계산됨



    장점

    Hold-out 기법에 비해서 변동성이 작은 강건한 CV 추정치 제공

    적절한 
    를 정할 경우 LOOCV의 계산량이 너무 많은 문제 해결 가능

    LOOCV보다 CV 추정치의 편향은 크지만, 분산은 작은 추정치 제공

    LOOCV의 경우 거의 동일한 훈련 데이터가 생성되므로, 각 훈련 데이터셋은 서로 높은 상관관계가 존재함

    상관성이 높은 값들의 평균은 상관성이 낮은 값들의 평균에 비해 분산이 크므로, LOOCV의 검정오차 추정량은 k-fold CV에 비해 분산이 큼

    단점

    적절한 
    값을 정하는 것이 어려움(보통 
    )

    LOOCV에 비해 편향된 CV 추정치 제공

    sklearn에서 수행 시

    KFold()

    n_splits : fold 개수

    shuffle : fold로 나누기 전 데이터를 섞을지 여부

    random_state : seed 값

    from sklearn.model_selection import KFold

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)
    lr = LinearRegression()

    cv_score2 = cross_val_score(lr, train_X, train_y, scoring='neg_mean_squared_error', cv = cv)
    rmse_score2 = np.sqrt(np.absolute(cv_score2))
    mean_rmse_score2 = np.mean(rmse_score2)

    print('RMSE :', rmse_score2)

    RMSE : [2.91372621 2.93935557 3.17604327 3.03490742 3.20680851]
    print('mean RMSE :', mean_rmse_score2)

    mean RMSE : 3.0541681985134215
    5-fold cross validation 결과를 보면 개별 RMSE의 평균은 약 3.05 정도인 것을 확인할 수 있습니다.

    6.4 Repeated CV
    k-fold CV를 여러번 반복하는 방법입니다. 각 반복마다 데이터가 shuffle 되므로 각 반복별 fold에는 다른 데이터가 들어오게 됩니다.

    장점

    Repeated cv는 k-fold CV를 반복해서 수행함으로써 k-fold cv에 비해 더 적은 편향과 분산을 갖는 검정오차 추정치 산출
    단점

    k-fold CV에 비해 계산량이 배로 늘어나는 단점이 있음(데이터가 적을 때 사용)
    sklearn에서 수행 시

    RepeatedKFold()

    n_splits : fold 개수

    n_repeats = 10(default) : 반복 횟수

    random_state : seed 값

    from sklearn.model_selection import RepeatedKFold

    cv = RepeatedKFold(n_splits = 5, n_repeats = 2, random_state = 0)
    lr = LinearRegression()

    cv_score3 = cross_val_score(lr, train_X, train_y, scoring='neg_mean_squared_error', cv = cv)
    rmse_score3 = np.sqrt(np.absolute(cv_score3))
    mean_rmse_score3 = np.mean(rmse_score3)

    print('RMSE :', rmse_score3)

    RMSE : [2.91372621 2.93935557 3.17604327 3.03490742 3.20680851 2.92528707
     3.219225   2.95852907 3.05257393 3.1467057 ]
    print('mean RMSE :', mean_rmse_score3)

    mean RMSE : 3.057316177131306
    6.5 Validation leakage
    이전 챕터에서 설명한 data leakage 문제를 cross validation에도 적용해보겠습니다. train/test에서의 data leakage 문제는 train/valid에서도 동일하게 적용됩니다. 즉 cross validation을 적용할 때, train 데이터를 이용하여 전처리 완료된 데이터를 적용하는 것이 아니라, train/valid의 독립성을 유지하기 위해서 cross validation의 각 fold별로 적용되어야 합니다.



    위 그림을 통해 보면, 5-fold로 나눴을 때, 4개의 fold로 구성된 train 데이터로 전처리를 진행하고, 마지막 fold가 validation 데이터로 train 데이터로 생성한 전처리를 적용합니다.



    위 그림에서는 5-fold로 나눴을 때, 1~3, 5 fold로 구성된 train 데이터로 전처리를 진행하고, 4번째 fold가 validation 데이터로 train 데이터로 생성한 전처리를 적용합니다.

    이를 수행하기 위해서는 교차검증 내에 전처리 프로세스를 추가해야 합니다. 하지만 이렇게 할 경우 전처리 코드가 늘어날수록 코드가 복잡해질 수 있습니다. 이를 보완하기 위해 나온 것이 sklearn의 pipeline입니다. pipeline을 활용하면, validation leakage를 방지하면서 데이터 전처리, 모델링 등을 수행할 수 있습니다.
    """