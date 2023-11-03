def m3():
    """
    3  데이터 전처리
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt

    from sklearn import set_config
    set_config(display="diagram")

    EDA에 이용했던 데이터를 다시 불러오겠습니다.

    dat = pd.read_csv('./data/ex_data/adp1.csv')

    3.1 scikit-learn 패키지 소개
    scikit-learn 패키지는 파이썬의 대표적인 머신러닝 패키지입니다. 현재까지 계속 개발되고 있으며, 데이터 전처리, 예측 모델링, 군집분석, 이상 탐지 등 다양한 방법론과 모형을 scikit-learn의 워크플로우 안에서 이용할 수 있습니다. scikit-learn 패키지는 약자로 sklearn으로 표기하겠습니다.

    3.2 결측치 처리
    sklearn 패키지를 이용해서 결측치를 대치하는 방법에 대해 알아보겠습니다. sklearn 패키지에서 제공하는 결측치 처리 관련 함수는 대표적으로 통계량을 이용한 방법과 모형을 이용한 방법 2가지가 있습니다. 시험에서는 결측치 식별, 결측치 대치 방법에 대해 서술, 해당 방법으로 결측치를 처리한 이유 설명 등으로 문제가 나옵니다. 따라서 각 결측치 처리 방법에 대한 대략적인 이해와 장·단점에 대해 이해하고 계시는게 좋습니다.

    통계량을 이용한 결측치 처리 방법

    평균 대치법

    중앙값 대치법

    최빈값 대치법

    모형을 이용한 결측치 처리 방법

    회귀분석을 이용한 대치법

    bagged tree를 이용한 대치법

    KNN을 이용한 대치법

    3.2.1 결측치 확인
    (dat
        .isna()
        .sum(axis = 0) 
    )

    school       0
    sex          0
    paid         0
    famrel       0
    freetime     0
    goout       10
    Dalc         0
    Walc         0
    health       0
    absences     0
    grade        0
    dtype: int64
    goout에 결측치가 10개 존재하는 것을 확인할 수 있습니다. sum() 함수는 axis = 0(열 합계)가 default입니다.

    3.2.2 평균 대치법
    평균대치법은 일변량 변수의 평균으로 결측치를 대치하는 방법입니다. 장·단점은 다음과 같습니다.

    장점

    쉽고 빠르게 결측치 대치 가능
    단점

    다른 변수 간의 관계를 고려하지 못하는 문제가 있음

    대치 후 값은 평균값의 빈도수가 많아지므로 분포가 왜곡되는 문제가 있음

    sklearn의 SimpleImputer 모듈을 불러오겠습니다.

    from sklearn.impute import SimpleImputer

    dat1 = dat.copy()

    strategy = 'mean'로 설정할 경우 평균 대치법을 적용할 수 있습니다. fit_transform() 을 통해 평균 대치법을 goout 변수에 적용해주었습니다. fit_transform 은 fit() + transform()를 동시에 적용하는 메서드입니다. sklearn은 데이터 전처리 모듈을 적용할 때, fit()과 transform()을 차례로 적용합니다. 함수를 각각 적용하는 것이 번거로우므로, fit_transform()을 통해 한번에 적용할 수 있습니다.

    Note
    fit_transform()은 train 데이터에만 적용해야 합니다(data leakage 챕터에서 추가 설명).

    imputer_mean = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    dat1['goout'] = imputer_mean.fit_transform(dat1[['goout']])
    dat1['goout'].isna().sum()

    0
    goout 변수의 결측치가 대치된 것을 확인할 수 있습니다.

    3.2.3 중앙값 대치법
    중앙값 대치법은 일변량 변수의 중앙값으로 결측치를 대치하는 방법입니다. 장·단점은 다음과 같습니다.

    장점

    쉽고 빠르게 결측치 대치 가능
    단점

    다른 변수 간의 상관관계를 고려하지 못하는 문제가 있음

    대치 후 값은 중앙값의 빈도수가 많아지므로 분포가 왜곡되는 문제가 있음

    dat2 = dat.copy()

    strategy = 'median'로 설정할 경우 중앙값 대치법을 적용할 수 있습니다. fit_transform() 을 통해 평균 대치법을 goout 변수에 적용해주었습니다.

    imputer_median = SimpleImputer(missing_values = np.nan, strategy = 'median')
    dat2['goout'] = imputer_median.fit_transform(dat2[['goout']])
    #dat2['goout'].isna().sum()

    3.2.4 최빈값 대치법
    최빈값 대치법은 일변량 변수의 최빈값으로 결측치를 대치하는 방법입니다. 최빈값 대치법은 연속형 변수보다는 범주형 변수에 사용하는 것이 바람직합니다. 장·단점은 다음과 같습니다.

    장점

    쉽고 빠르게 결측치 대치 가능
    단점

    다른 변수 간의 상관관계를 고려하지 못하는 문제가 있음

    class 불균형을 더 심화시킬 수 있음

    dat3 = dat.copy()

    strategy = 'most_frequent'로 설정할 경우 최빈값 대치법을 적용할 수 있습니다. fit_transform() 을 통해 최빈값 대치법을 goout 변수에 적용해주었습니다.

    imputer_mode = SimpleImputer(missing_values = np.nan, strategy = 'most_frequent')
    dat3['goout'] = imputer_mode.fit_transform(dat3[['goout']])
    #dat3['goout'].isna().sum()

    3.3 Iterative imputer
    모형을 통한 결측치 대치를 위해 IterativeImputer를 불러오겠습니다. IterativeImputer는 MICE(Multivariate Imputation by Chained Equations) 방식을 이용하여 결측치를 대치합니다. 그림을 통해 MICE가 어떻게 작동하는지 살펴보겠습니다.

    1단계

    age, experience, salary 변수에 결측치가 1개씩 존재하는 것을 확인할 수 있습니다. 첫 단계에서는 결측치를 각 변수의 평균으로 채워넣습니다. 그 다음 왼쪽 변수부터 결측치를 채워넣을 준비를 합니다.







    age를 제외한 나머지 변수를 이용하여 linear regression 모형을 적합한 후 예측값을 age의 결측치로 대치합니다. 34.99로 대치된 것을 확인할 수 있습니다. 그 다음 experience 변수도 마찬가지로, 결측치가 채워진 age변수와 salary 변수를 이용하여 linear regression 모형을 적합한 후 예측값을 experience의 결측치로 대치합니다. 0.98로 대치된 것을 확인할 수 있습니다. 그 다음 salary 변수도 마찬가지로, 결측치가 채워진 age변수와 experience 변수를 이용하여 linear regression 모형을 적합한 후 예측값을 salary의 결측치로 대치합니다. 70로 대치된 것을 확인할 수 있습니다.









    각 변수의 결측치를 대치한 다음, 처음 각 변수별 평균을 이용해서 대치했던 것과의 차이를 구합니다. 이 차이를 0에 가깝게 수렴하도록 하는 것이 최종 목적입니다.

    2단계

    1단계를 한번 더 반복하여, 2단계 결과를 산출한 후 1단계와 2단계의 차이를 구합니다. 결과를 보면 거의 0에 가까워진 것을 확인할 수 있습니다.



    IterativeImputer를 불러올 때는 enable_iterative_imputer, IterativeImputer를 둘다 불러와야 합니다.

    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer

    Note
    IterativeImputer는 아직 실험 단계이고, 지속적으로 업데이트되고 있습니다.

    참고 : IterativeImputer 공식문서

    Example

    간단하게 예시를 코드를 통해 한번 더 보겠습니다. x3 변수에 결측치가 존재하는 것을 볼 수 있습니다.

    df = pd.DataFrame({
        'x1' : [1, 3, 5],
        'x2' : [9, 5, 3], 
        'x3' : [np.nan, 5, 4]
    })
    df

       x1  x2   x3
    0   1   9  NaN
    1   3   5  5.0
    2   5   3  4.0
    먼저 대치를 위해 train/test를 나눠주었습니다. train은 결측치가 없는 모든 행이고, test는 결측치가 있는 행입니다.

    test = df[df['x3'].isnull()==True]
    print(test)

       x1  x2  x3
    0   1   9 NaN
    train = df[df['x3'].isnull()==False]
    print(train)

       x1  x2   x3
    1   3   5  5.0
    2   5   3  4.0
    linear regression을 메서드를 불러와서 결측치를 대치해보겠습니다.

    from sklearn.linear_model import LinearRegression

    train 데이터를 이용해서 linear regression을 적합시켜주었습니다.

    lr = LinearRegression()
    y = train['x3']
    train.drop("x3", axis=1, inplace=True)
    lr.fit(train, y)


    LinearRegression
    LinearRegression()
    결측치가 존재하는 test 데이터에 linear regression을 적용하여 결측치를 6.5로 대치해주었습니다.

    test.drop("x3", axis=1, inplace=True)
    pred = lr.predict(test)
    test['x3']= pred
    print(test)

       x1  x2   x3
    0   1   9  6.5
    IterativeImputer을 이용하여 결측치 대치 결과를 확인해보겠습니다.

    imputer = IterativeImputer(estimator = lr, max_iter = 1)
    result = imputer.fit_transform(df)
    print(result)

    [[1.  9.  6.5]
     [3.  5.  5. ]
     [5.  3.  4. ]]
    동일한 결과를 산출하는 것을 확인할 수 있습니다.

    3.3.1 Linear regression을 이용한 대치법
    dat4 = dat.copy()

    먼저 수치형 변수와 범주형 변수를 선택해주었습니다.

    numeric_data = dat4.select_dtypes('number')
    cat_data = dat4.select_dtypes('object')

    estimator = LinearRegression()을 적용하여 결측치를 대치해보겠습니다. fit_transform() 함수를 이용해서 해당 모듈을 데이터에 적용해주었습니다.

    lr = LinearRegression()
    imputer = IterativeImputer(estimator = lr, max_iter = 10)
    impute_value = imputer.fit_transform(numeric_data)
    numeric_data = pd.DataFrame(impute_value, columns=numeric_data.columns)
    dat4 = pd.concat([cat_data, numeric_data], axis = 1) # cbind
    dat4.isna().sum()

    school      0
    sex         0
    paid        0
    famrel      0
    freetime    0
    goout       0
    Dalc        0
    Walc        0
    health      0
    absences    0
    grade       0
    dtype: int64
    goout 변수의 결측치가 대치된 것을 확인할 수 있습니다.

    3.3.2 Random forest을 이용한 대치법
    장점

    일변량 변수가 아닌 다변량 변수 간의 관계를 이용해서 결측치를 대치 가능
    단점

    boostrap sample의 수에 따라 계산량이 많아질 수 있음
    from sklearn.ensemble import RandomForestRegressor

    dat5 = dat.copy()

    estimator = RandomForestRegressor()을 적용하여 결측치를 대치해보겠습니다. fit_transform() 함수를 이용해서 해당 모듈을 데이터에 적용해주었습니다.

    numeric_data = dat5.select_dtypes('number')
    cat_data = dat5.select_dtypes('object')

    imputer = IterativeImputer(estimator = RandomForestRegressor(), max_iter = 10)
    impute_value = imputer.fit_transform(numeric_data)
    numeric_data = pd.DataFrame(impute_value, columns=numeric_data.columns)
    dat5 = pd.concat([cat_data, numeric_data], axis = 1)
    dat5.isna().sum()

    school      0
    sex         0
    paid        0
    famrel      0
    freetime    0
    goout       0
    Dalc        0
    Walc        0
    health      0
    absences    0
    grade       0
    dtype: int64
    goout 변수의 결측치가 대치된 것을 확인할 수 있습니다.

    Caution
    IterativeImputer는 결측치 대치에 수치형 변수만 이용할 수 있습니다. 범주형 변수의 경우 encoding 후 변수로 이용할 수 있습니다.

    3.3.3 KNN을 이용한 대치법
    knn을 이용한 대치법은 
    개의 이웃을 택한 후, 
    개의 관찰치들을 사용해서 결측치를 추정하는 방법입니다. 장·단점은 다음과 같습니다.

    장점

    데이터에 대한 가정 없이 쉽고 빠르게 결측치 대치 가능
    단점

    값에 따라 계산량이 많고, 이상치에 민감함

    변수 scale에 민감하며, 고차원 데이터의 경우 부정확할 수 있음

    KNNImputer를 불러오겠습니다.

    from sklearn.impute import KNNImputer

    dat6 = dat.copy()

    numeric_data = dat6.select_dtypes('number')
    cat_data = dat6.select_dtypes('object')

    KNNImputer()을 적용하여 결측치를 대치해보겠습니다. fit_transform() 함수를 이용해서 해당 모듈을 데이터에 적용해주었습니다.

    imputer = KNNImputer(n_neighbors = 5)
    impute_value = imputer.fit_transform(numeric_data)
    numeric_data = pd.DataFrame(impute_value, columns=numeric_data.columns)
    dat6 = pd.concat([cat_data, numeric_data], axis = 1)
    dat6.isna().sum()

    school      0
    sex         0
    paid        0
    famrel      0
    freetime    0
    goout       0
    Dalc        0
    Walc        0
    health      0
    absences    0
    grade       0
    dtype: int64
    goout 변수의 결측치가 대치된 것을 확인할 수 있습니다.

    Tip
    시험에서는 통계량을 이용한 대치 방법과 모형을 이용한 대치 방법을 제시하고, 통계량을 이용한 대치 방법 대비 모형을 이용한 대치 방법의 장점에 대해 서술하시면 됩니다.

    3.4 Encoding 방법
    sklearn 패키지를 이용해서 범주형 변수 인코딩 방법에 대해 알아보겠습니다. sklearn 패키지에서 제공하는 인코딩 방법은 크게 세 가지가 있습니다. 시험에서는 인코딩이 필요한 변수 식별, 인코딩 방법에 대해 서술, 해당 방법으로 전처리를 수행한 이유 설명 등으로 문제가 나옵니다. 따라서 각 범주형 인코딩 방법에 대한 대략적인 이해와 장·단점에 대해 이해하고 계시는게 좋습니다.

    Label encoding

    Dummy encoding

    one-hot encoding

    3.4.1 Label encoding
    label encoding 방법은 범주형 변수의 라벨에 알파벳 순서대로 고유한 정수를 할당하는 방법입니다.

    장점

    순서형 변수의 경우 순서를 반영한 인코딩이 가능함
    단점

    알파벳 순으로 번호를 매기기 때문에 수치 정보가 반영되는 문제가 있음
    LabelEncoder()를 불어오겠습니다.

    from sklearn.preprocessing import LabelEncoder

    범주형 변수를 선택한 후 LabelEncoder를 적용해주었습니다. 변환 결과를 보면 0, 1로 변환된 것을 확인할 수 있습니다.

    cat_data = dat.select_dtypes('object')
    encoder = LabelEncoder()
    cat_data.apply(encoder.fit_transform)

         school  sex  paid
    0         0    0     0
    1         0    0     0
    2         0    0     1
    3         0    0     1
    4         0    0     1
    ..      ...  ...   ...
    361       1    0     0
    362       1    1     1
    363       1    1     0
    364       1    1     0
    365       1    1     0

    [366 rows x 3 columns]
    3.4.2 one-hot encoding
    원핫인코딩은 범주형 변수의 각 범주에 대해서 각각 하나의 새로운 열을 생성하고, 
     또는 
    의 값을 부여해서 각 범주를 구분하는 방법입니다. 원핫 인코딩의 직관적인 설명은 아래 그림과 같습니다.



    원핫인코딩 vs 더미 코딩
    장점

    Label encoding의 문제점인 범주형 변수에 수치 정보가 반영되는 문제를 해결 가능
    단점

    범주형 변수 내에 다중공선성 문제가 있을 수 있음(회귀분석에서 문제가 되지만 glm 패키지에서는 factor로 처리할 경우 levels 중에 하나를 제외하기 때문에 dummy coding으로 실시됨)

    범주형 변수가 많을 경우 차원이 늘어남에 따라 계산량이 늘어나는 문제가 있음

    linear regression의 경우 dummy encoding을 수행해야 matrix 계산에 문제가 없음

    from sklearn.preprocessing import OneHotEncoder

    OneHotEncoder

    drop=None, : 칼럼 한 개를 삭제할지 여부
    drop = “first” : dummy coding
    sparse=True :
    True : sparse matrix 출력
    False : numpy array 출력
    dtype= numpy.float64, 데이터 타입 지정
    handle_unknown=‘error’ : unknown 범주가 존재할 경우 error 출력
    ‘ignore’ : unknown 범주가 존재할 경우 모두 0으로 지정
    Example

    범주형 변수만 선택한 후 OneHotEncoder()를 적용해주었습니다. 결과는 numpy array로 반환하기 때문에 데이터프레임으로 변환하기 위해서는 변수명을 추가로 할당해주어야 합니다.

    encoder = OneHotEncoder(sparse = False)
    onehot_data = encoder.fit_transform(cat_data)

    .categories_를 이용하면 OneHotEncoder()에 사용된 범주형 변수의 각 범주를 불러올 수 있습니다.

    cat_label = encoder.categories_
    print(cat_label)

    [array(['GP', 'MS'], dtype=object), array(['F', 'M'], dtype=object), array(['no', 'yes'], dtype=object)]
    데이터프레임의 칼럼으로 지정하기 위해 .flatten() 함수를 이용하여 다차원 배열로 된 범주를 1차원으로 바꿔주었습니다.

    cat_label = np.array(cat_label).flatten()
    print(cat_label)

    ['GP' 'MS' 'F' 'M' 'no' 'yes']
    원핫인코딩된 데이터프레임을 생성해주었습니다.

    onehot_data = pd.DataFrame(onehot_data, columns = cat_label)
    print(onehot_data.head(2))

        GP   MS    F    M   no  yes
    0  1.0  0.0  1.0  0.0  1.0  0.0
    1  1.0  0.0  1.0  0.0  1.0  0.0
    3.4.3 dummy encoding
    더미 인코딩은 범주형 변수의 각 범주 
    개 만큼의 새로운 열을 생성하고, 
     또는 
    의 값을 부여해서 각 범주를 구분하는 방법입니다.

    장점

    Label encoding의 문제점인 수치 정보가 반영되는 문제를 해결 가능

    one-hot encoding의 다중공선성 문제 해결

    해석시에 제외된 범주가 기준 범주가 되며, 기준범주 대비 증감으로 해석함

    단점

    범주형 변수가 많을 경우 차원이 늘어남에 따라 계산량이 늘어나는 문제가 있음
    Example

    더미 코딩을 위해 OneHotEncoder(drop = "first)를 적용해주었습니다. 결과는 numpy array로 반환하기 때문에 데이터프레임으로 변환하기 위해서는 변수명을 추가로 할당해주어야 합니다.

    encoder = OneHotEncoder(drop = "first", sparse = False)
    dummy_data = encoder.fit_transform(cat_data)

    .get_feature_names()를 이용하면 OneHotEncoder()에 사용된 범주형 변수의 각 범주를 불러올 수 있습니다.

    #cat_label = encoder.get_feature_names_out()
    cat_label = encoder.get_feature_names()
    print(cat_label)

    ['x0_MS' 'x1_M' 'x2_yes']
    더미코딩된 데이터프레임을 생성해주었습니다.

    onehot_data = pd.DataFrame(dummy_data, columns = cat_label)
    print(onehot_data.head(1))

       x0_MS  x1_M  x2_yes
    0    0.0   0.0     0.0
    3.4.4 make_column_transformer


    이전에는 범주형 변수를 따로 필터링한 다음, encoding 후 다시 합치는 단계를 진행했습니다. sklearn에서 제공하는 columnTransformer를 활용하면 조금더 간단한 방법으로 encoding을 진행할 수 있습니다. 이후 소개할 sklean pipeline에서 함께 이용가능합니다.

    Example

    from sklearn.compose import ColumnTransformer
    from sklearn.compose import make_column_transformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import OrdinalEncoder

    label encoding

    Note
    OrdinalEncoder은 2d 데이터에 적용할 수 있습니다. LabelEncoder는 1d 데이터에만 적용할 수 있습니다.

    예시 : ordinalEncoder vs LabelEncoder

    cat_data = dat.select_dtypes('object')
    cat_columns = cat_data.columns

    transformer = make_column_transformer(
        (OrdinalEncoder(), cat_columns),
        remainder='passthrough')


    encode_data = transformer.fit_transform(dat)
    mixed_data = pd.DataFrame(encode_data, columns = dat.columns)

    print(mixed_data.head(2))

       school  sex  paid  famrel  freetime  ...  Dalc  Walc  health  absences  grade
    0     0.0  0.0   0.0     4.0       3.0  ...   1.0   1.0     3.0       6.0    1.0
    1     0.0  0.0   0.0     5.0       3.0  ...   1.0   1.0     3.0       4.0    1.0

    [2 rows x 11 columns]
    one-hot encoding

    cat_data = dat.select_dtypes('object')
    cat_columns = cat_data.columns

    transformer = make_column_transformer(
        (OneHotEncoder(), cat_columns),
        remainder='passthrough')


    onehot_data = transformer.fit_transform(dat)
    mixed_data = pd.DataFrame(onehot_data, columns = transformer.get_feature_names())

    print(mixed_data.head(2))

       onehotencoder__x0_GP  onehotencoder__x0_MS  ...  absences  grade
    0                   1.0                   0.0  ...       6.0    1.0
    1                   1.0                   0.0  ...       4.0    1.0

    [2 rows x 14 columns]
    dummy encoding

    cat_data = dat.select_dtypes('object')
    cat_columns = cat_data.columns

    transformer = make_column_transformer(
        (OneHotEncoder(drop = "first"), cat_columns),
        remainder='passthrough')


    dummy_data = transformer.fit_transform(dat)
    mixed_data = pd.DataFrame(dummy_data, columns = transformer.get_feature_names())

    print(mixed_data.head(2))

       onehotencoder__x0_MS  onehotencoder__x1_M  ...  absences  grade
    0                   0.0                  0.0  ...       6.0    1.0
    1                   0.0                  0.0  ...       4.0    1.0

    [2 rows x 11 columns]
    3.5 설명변수 범주 불균형 처리 방법
    범주형 설명변수의 경우 범주의 수가 많고, 각 범주의 빈도는 불균형인 경우가 있습니다. 이 경우 더미 코딩, 원핫인코딩을 했을 때, 차원의 수(칼럼의 수)가 늘어나기 때문에, 계산량이 늘어날 수 있습니다. 그렇기 때문에, 각 범주의 의미가 퇴색되지 않는 선에서 적절히 전처리를 해주는 것이 바람직할 수 있습니다.

    주의할 점

    시험에서는 추가적인 전처리 활용방안을 제시하라고 할 때, 해당 전처리를 하는 방법과 이유, 결과를 제시해주시면 됩니다.

    Example

    bike sharing 데이터를 이용해서 해당 함수를 적용해보겠습니다.

    bike_data = pd.read_csv("./data/ex_data/bikesharingdata/train.csv")

    weather 변수의 각 범주별 빈도를 확인해보면 범주가 4인 경우 빈도가 1인 것을 볼 수 있습니다.

    bike_data['weather'].value_counts()

    weather
    1    7192
    2    2834
    3     859
    4       1
    Name: count, dtype: int64
    빈도가 1인 경우 정보가 없으므로, 범주를 통합하는 것이 바람직할 수 있습니다. 먼저 normalize = True 옵션을 통해 상대 비율을 구해주었습니다.

    freq = bike_data['weather'].value_counts(normalize = True)
    print(freq)

    weather
    1    0.660665
    2    0.260334
    3    0.078909
    4    0.000092
    Name: proportion, dtype: float64
    .map()은 series형에 데이터에 대해서 값을 변환할 때 사용합니다. .map()을 이용해서 weather 변수를 freq로 변환해준 후 prob_colums로 저장해주었습니다.

    prob_columns = bike_data['weather'].map(freq)
    prob_columns.head(2)

    0    0.660665
    1    0.660665
    Name: weather, dtype: float64
    .mask(조건, 마스킹 값)은 조건을 만족하는 데이터를 특정값으로 마스킹할 때 사용합니다. .mask()를 이용하여, 상대비율이 0.1이하인 범주를 ’other’로 처리해주었습니다.

    bike_data['weather'] = bike_data['weather'].mask(prob_columns < 0.1, 'other')

    결과를 보면 범주 4의 경우 범주 3으로 병합되고, other로 범주가 변경된 것을 볼 수 있습니다.

    bike_data['weather'].value_counts()

    weather
    1        7192
    2        2834
    other     860
    Name: count, dtype: int64
    3.6 연속형 변수 이산화 방법
    연속형 변수를 특정 그룹으로 이산화하여, 해석해볼 수 있습니다. 예를 들어 키와 체중 변수가 있을 때, 체중을 light, mid, heavy 세 그룹으로 나누고, 체중 그룹별 키의 관계를 더 직관적으로 해석해볼 수 있습니다. 연속형 변수를 이산화할 때, 이산화를 통해 나눠진 bin의 빈도가 거의 같도록 하는 방법을 고려해볼 수 있습니다.

    KBinsDiscretizer

    n_bins = 5(default) : bin 개수

    encode = ‘onehot’(default): 변환 형식(‘ordinal’, ‘onehot’, ..etc)

    strategy = ‘quantile’(default): bin을 나누는 방식

    ‘uniform’ : 각 feature는 같은 width를 가짐

    ‘quantile’ : 각 feature는 같은 데이터 수를 가짐

    Example

    from sklearn.preprocessing import KBinsDiscretizer

    strategy = 'uniform'으로 지정했을 때 결과를 살펴보겠습니다.

    X = np.array([[0, 1, 1, 2, 5, 10, 11, 14, 18]]).T
    np.shape(X)

    (9, 1)
    kbd = KBinsDiscretizer(n_bins = 3, strategy = 'uniform')
    X_bin = kbd.fit_transform(X).toarray()
    X_bin[:2, :]

    array([[1., 0., 0.],
           [1., 0., 0.]])
    print(kbd.bin_edges_)

    [array([ 0.,  6., 12., 18.])]
    각 bin의 edge는 .bin_edges_ 옵션을 통해 확인할 수 있습니다. 결과를 보면 0~6, 6~12, 12~18로 같은 width를 갖도록 분할된 것을 볼 수 있습니다.

    strategy = 'quantile'으로 설정했을 때 결과를 살펴보겠습니다.

    X = np.array([[0, 1, 1, 2, 5, 10, 11, 14, 18]]).T
    kbd = KBinsDiscretizer(n_bins = 4, strategy = 'quantile')
    kbd.fit_transform(X)

    <9x4 sparse matrix of type '<class 'numpy.float64'>'
        with 9 stored elements in Compressed Sparse Row format>
    print(kbd.bin_edges_)

    [array([ 0.,  1.,  5., 11., 18.])]
    결과를 보면 0~1, 1~5, 5~11, 11~18로 n_bins = 4이므로 4 분위수를 기준으로 분할된 것을 볼 수 있습니다. 직접 분위수를 확인 해보면 다음과 같습니다.

    print(np.quantile(X, 0.25), np.quantile(X, 0.5), np.quantile(X, 0.75), np.quantile(X, 1))

    1.0 5.0 11.0 18
    Example2

    bikesharing data를 이용해서 실습을 진행해보겠습니다. windspeed 변수에 대해서 5분위수로 이산화를 진행해주었습니다. 최종 결과는 label encoding으로 설정해주었습니다.

    kbd = KBinsDiscretizer(n_bins = 5, encode = 'ordinal')
    kbd_result = kbd.fit_transform(bike_data[['windspeed']])
    kbd_result = pd.DataFrame(kbd_result, columns = ['windspeed'])
    kbd_result.head(2)

       windspeed
    0        0.0
    1        0.0

    ## onehot
    # kbd = KBinsDiscretizer(n_bins = 5)
    # kbd_result = kbd.fit_transform(bike_data[['windspeed']])
    # kbd_result = pd.DataFrame(kbd_result.toarray())
    # kbd_result.columns = ['windspeed_{0}'.format(i) for i in range(0, len(kbd_result.columns))]
    # kbd_result.head(2)

    3.7 변수 변환 방법
    분포의 치우침이 있을 때, 변수 변환을 고려해볼 수 있습니다. 변수 변환을 통해 정규분포 형태로 변환할 수 있습니다.







    from sklearn.preprocessing import PowerTransformer
    import warnings
    np.warnings = warnings 

    numpy warning

    PowerTransformer()

    method = ‘yeo-johnson’(default), ‘box-cox’

    yeo-johnson : 모든 실수 범위에서 가능

    box-cox : 양수만 가능

    Example

    count 변수의 분포를 보면 오른쪽으로 긴꼬리를 갖는 분포인 것을 확인할 수 있습니다. 변수 변환을 진행해보겠습니다.

    #plt.clf()
    bike_data['count'].hist()
    plt.show()



    bike_data2 = bike_data.copy()
    pt = PowerTransformer(method = 'box-cox')
    bike_data2['count'] = pt.fit_transform(bike_data2[['count']])
    print('lambda : ', pt.lambdas_)

    lambda :  [0.31567024]
    boxcox 변환 후에는 정규분포와 유사한 형태로 변환된 것을 확인할 수 있습니다.

    bike_data2['count'].hist()
    plt.show()



    변환을 위한 
     값은 PowerTransformer()을 통해 계산할 수 있습니다. boxcox 변환을 
    값 그대로 변환을 할 경우 회귀모형의 경우 해석이 어려울 수 있습니다. 보통 위의 표와 같이 
     값에 가까운 정수형 변환을 실시합니다.

    일 때, 변환 전 데이터를 의미하고, 우측으로 긴꼬리를 갖는 분포일 경우 루트변환, 로그변환 등을 고려해볼 수 있습니다.

    Caution
    로그변환의 경우 0을 포함할 경우 발산하므로 주의가 필요합니다.

    np.log1p()

     : 값에 
    일 경우 
    으로 발산하기 때문에 
    을 더해줘서 해결
    bike_data3 = bike_data.copy()
    bike_data3['count'] = np.log1p(bike_data3[['count']])

    np.sqrt : 루트 변환 함수

    bike_data4 = bike_data.copy()
    bike_data4['count'] = np.sqrt(bike_data4[['count']])

    3.8 표준화, 정규화 방법
    변수별로 비교를 위해서 스케일을 통일해줘야 할 경우가 있습니다. 보통 거리 기반 알고리즘의 경우 변수의 스케일에 따라 거리의 변동이 크므로, 사전에 표준화를 진행합니다.

    StandardScaler() : 

    로 표준화

    Example

    from sklearn.preprocessing import StandardScaler

    numeric_data = dat.select_dtypes('number')
    stdscaler = StandardScaler()
    std_data = pd.DataFrame(stdscaler.fit_transform(numeric_data), columns = numeric_data.columns)

    std_data.head(2)

         famrel  freetime     goout  ...    health  absences     grade
    0  0.064260 -0.209894  0.817064  ... -0.417651  0.050918 -1.311613
    1  1.184217 -0.209894 -0.089088  ... -0.417651 -0.195916 -1.311613

    [2 rows x 8 columns]
    # stdscaler.feature_names_in_ 

    Caution
    표준화는 변수별 스케일을 통일시켜주는 목적이며, 분포의 모양을 바꾸는 것이 아닙니다. (ex. 표준화를 통해 정규분포로 바꿔준다 X)

    MinMaxScaler() : 


    Min-Max 정규화라고 하며, 값의 범위를 0 ~ 1로 통일시킵니다.

    from sklearn.preprocessing import MinMaxScaler

    numeric_data = dat.select_dtypes('number')
    mxscaler = MinMaxScaler()
    pd.DataFrame(mxscaler.fit_transform(numeric_data), columns = numeric_data.columns).head(2)

       famrel  freetime  goout  Dalc  Walc  health  absences     grade
    0    0.75       0.5   0.75   0.0   0.0     0.5  0.080000  0.090909
    1    1.00       0.5   0.50   0.0   0.0     0.5  0.053333  0.090909

    # mxscaler.feature_names_in_

    어떤 것을 사용해야 하는가?

    정답은 없음

    이상치가 존재할 경우 표준화 선호

    PCA, 거리 기반 군집분석의 경우 표준화 선호

    neural network 모형의 경우 Min-max 정규화, 표준화 둘다 사용

    3.9 추가적인 전처리 방법
    변수 간에 2차 혹은 3차 관계가 있을 때, 혹은 교호작용 효과가 있을 때, 2차항, 3차항, 교호작용항을 추가해볼 수 있습니다.

    PolynomialFeatures()

    degree = 2(default): 차수

    interaction_only = false(default) : 교호작용항만 추가할지 여부

    include_bias = True(default) : 절편항 추가 여부

    Example

    from sklearn.preprocessing import PolynomialFeatures

    numeric_data = dat1.select_dtypes('number')
    poly = PolynomialFeatures(degree=2)
    pd.DataFrame(poly.fit_transform(numeric_data), columns = poly.get_feature_names()).head(2)

         1   x0   x1   x2   x3   x4  ...  x5^2  x5 x6  x5 x7  x6^2  x6 x7  x7^2
    0  1.0  4.0  3.0  4.0  1.0  1.0  ...   9.0   18.0    3.0  36.0    6.0   1.0
    1  1.0  5.0  3.0  3.0  1.0  1.0  ...   9.0   12.0    3.0  16.0    4.0   1.0

    [2 rows x 45 columns]

    # poly.get_feature_names_out()

    Caution
    결측치가 있을 경우 에러가 발생하므로, 결측치 처리 후 파생변수를 생성해주어야 합니다.

    3.10 반응 변수 불균형 처리 방법
    일반적인 분류 문제에서는 정상을 정확히 분류하는 것보다 이상을 정확히 분류하는 것이 중요합니다. 보통 타겟변수의 빈도는 불균형한 경우가 대부분입니다. 이러한 불균형을 처리를 하지 않고 모델링을 할 경우 모델 성능에 대한 왜곡이 생길 수 있습니다. 이러한 문제에 대한 가장 간단한 해결책은 over sampling과 under sampling입니다.

    3.10.1 Random over sampling


    Upsampling vs Downsampling
    업샘플링은 소수 범주 내 관측치를 복원추출을 통해 늘리는 방법입니다.

    장점

    under sampling처럼 데이터를 잃지 않고, 소수 범주를 잘 분류할 가능성이 있음
    단점

    소수 범주를 복원추출을 통해 값을 복제하므로, 소수 범주에 과적합될 수 있음

    데이터의 크기가 증가하므로 모델 적합시 계산량이 더 많아짐

    Example

    from imblearn.over_sampling import RandomOverSampler
    from sklearn.datasets import make_classification
    from collections import Counter
    #print(imblearn.__version__)

    imblearn의 경우 불균형을 해결하기 위한 샘플링 방법을 모아놓은 패키지입니다. sklearn과 호환이 가능합니다.

    먼저 make_classification() 함수를 통해 시뮬레이션 데이터를 생성하겠습니다.

    X, y = make_classification(n_samples=1000, n_features = 10, weights=[0.9])

    target y의 경우 빈도가 9:1 정도로 불균형한 것을 확인할 수 있습니다.

    Counter(y)

    Counter({0: 896, 1: 104})
    RandomOverSampler()

    sampling_strategy = ‘minority’ : 소수범주만 리샘플링
    oversample = RandomOverSampler(sampling_strategy='minority')

    RandomOverSampler() 함수를 적용했을 때, 소수 범주를 resampling하여 target y의 경우 빈도가 5:5로 맞춰진 것을 확인할 수 있습니다.

    X_over, y_over = oversample.fit_resample(X, y)
    print(Counter(y_over))

    Counter({0: 896, 1: 896})
    3.10.2 Random under sampling
    언더 샘플링은 다수 범주의 관측치를 랜덤 샘플링을 통해 일부만 추출하므로써 다수 범주의 빈도를 줄이는 방법입니다.

    장점

    랜덤샘플링을 통해 다수 범주의 관측치를 제거하기 때문에 모델 적합시 계산 속도가 향상됨
    단점

    관측치를 제거하기 때문에 정보의 손실 발생함

    범주 불균형이 너무 심할 경우 소수 범주의 빈도가 작기 때문에 사용이 어려움

    from imblearn.under_sampling import RandomUnderSampler

    undersample = RandomUnderSampler(sampling_strategy='majority')

    RandomUnderSampler()

    sampling_strategy = ‘majority’ : 다수범주만 리샘플링
    X_under, y_under = undersample.fit_resample(X, y)
    print(Counter(y_under))

    Counter({0: 104, 1: 104})
    RandomUnderSampler() 함수를 적용했을 때, 다수 범주를 resampling하여 target y의 경우 빈도가 5:5로 맞춰진 것을 확인할 수 있습니다.

    Caution
    train/test를 나눴을 경우 upsampling/undersampling은 train 데이터에만 적용해야 합니다.

    3.11 이상치 처리 방법
    이상치 처리 방법은 간단하게 상자그림을 이용한 방법, Z-score를 이용하는 방법, 마할라노비스 거리를 이용한 방법 등이 있습니다. 이상치는 방법론을 이용해서 판단하는 경우도 있지만 주어진 변수의 의미를 보고 판단하는 경우도 있기 때문에 주의가 필요합니다. 방법론에 집착하는 것이 아니라 이상치로 판단한 근거에 대해 논리적으로 설명하고, 방법론은 부가적인 근거로 활용하는 것이 바람직합니다.

    3.11.1 Boxplot을 이용한 방법
    상자 수염 그림을 이용한 이상치 판단 방법은 아래 그림과 같습니다. 즉 울타리 밖의 관측치를 이상치로 정의합니다.

    Q3 : 제 3사분위 수

    Q1 : 제 1사분위 수

    IQR : Q3-Q1

    위 울타리(upper fence) : 

    아래 울타리(lower fence) : 



    상자그림 요약
    Example 먼저 예제 데이터를 불러오겠습니다.

    warpbreaks = pd.read_csv('./data/warpbreaks.csv')
    warpbreaks.head(2)

       breaks wool tension
    0      26    A       L
    1      30    A       L
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    warpbreaks.boxplot(column = ['breaks'])
    plt.show()



    boxplot을 보면 
    에서 이상치로 의심되는 관측치가 두 개 있는 것을 확인할 수 있습니다.

    # 1분위수 계산
    Q1 = np.quantile(warpbreaks['breaks'], 0.25)
    # 3분위수 계산
    Q3 = np.quantile(warpbreaks['breaks'], 0.75)
    IQR = Q3 - Q1

    UC = Q3 + (1.5 * IQR) # 위 울타리
    LC = Q3 - (1.5 * IQR) # 위 울타리
    warpbreaks.loc[(warpbreaks.breaks > UC) | (warpbreaks.breaks < LC), :]

        breaks wool tension
    4       70    A       L
    8       67    A       L
    22      10    A       H
    울타리 밖의 데이터를 필터링했을 때 결과를 보면 
     일 때, 인 것을 확인할 수 있습니다. 이상치로 의심되는 케이스를 제거해보겠습니다.

    plt.clf()
    warpbreaks.loc[(warpbreaks.breaks <= UC) & (warpbreaks.breaks >= LC), :].boxplot(column = ['breaks'])
    plt.show()



    인 케이스가 제거된 것을 확인할 수 있습니다.

    3.11.2 Z-score
    Z-score의 특정 값을 기준으로 이상치를 판별하는 방법입니다.

    평균표준편차


    Z-score
    upper = warpbreaks['breaks'].mean() + (3*warpbreaks['breaks'].std())
    lower = warpbreaks['breaks'].mean() - (3*warpbreaks['breaks'].std())

    warpbreaks.loc[(warpbreaks.breaks > upper) | (warpbreaks.breaks < lower), :]

       breaks wool tension
    4      70    A       L
    3sigma로 이상치를 판별했을 때, 
    인 케이스가 이상치로 판정된 것을 확인할 수 있습니다.

    3.11.3 Mahalanobis distance
    마할라노비스 거리는 Z-score 방법의 확장으로 일변량이 아닌 다변량 변수의 공분산을 고려한 거리 측도입니다.


    from scipy.spatial.distance import mahalanobis
    from scipy.stats import chi2
    #from sklearn.covariance import MinCovDet

    numeric_data = dat1.select_dtypes('number').to_numpy()
    mu = np.mean(numeric_data, axis=0)
    sigma = np.cov(numeric_data.T)
    dat1['maha_dist'] = [mahalanobis(x, mu, np.linalg.inv(sigma)) for x in numeric_data]

    마할라노비스 거리는 다변량 정규분포 가정하에 근사적으로 카이제곱분포를 따릅니다. 따라서 cutoff value를 다음과 같이 설정할 수 있습니다.

    dat1['p_value'] = 1 - chi2.cdf(dat1['maha_dist'], np.shape(numeric_data)[1])
    dat1.loc[(dat1.p_value < 0.01), :]

    Empty DataFrame
    Columns: [school, sex, paid, famrel, freetime, goout, Dalc, Walc, health, absences, grade, maha_dist, p_value]
    Index: []
    분석가의 주관에 따라 cutoff value를 지정해서 이상치를 식별해줄 수도 있습니다.

    3.12 연습문제
    런던 공유 자전거 시스템의 시간대별 총 대여량을 예측하는 문제입니다.

    Data description

    datetime : 날짜
    season : 계절 (1 = spring, 2 = summer, 3 = fall, 4 = winter)
    holiday : 공휴일
    workingday : 주말, 공휴일 제외 나머지 요일
    weather
    1: Clear, Few clouds, Partly cloudy
    2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
    temp : 섭씨 온도
    atemp : 체감온도 ( ’feels like temperature by taking into account the expected air temperature, relative humidity and the strength of the wind at around 5 feet (the typical height of an human face))
    humidity : 상대습도
    windspeed : 풍속
    casual : number of non-registered user rentals initiated
    registered : number of registered user rentals initiated
    count : number of total rentals
    1. 시각화 및 탐색적 자료분석을 수행하시오.

    2. 결측치를 식별 및 결측치 대치를 실시하고, 해당 대치방법을 선택한 이유를 작성하시오.

    3. 범주형 변수 중 변환이 필요할 경우 변환을 실시하고, 해당 변환을 실시한 이유를 서술하시오.

    4. 추가적인 전처리가 필요한 경우 실시하고, 이유를 제시하시오.

    2  EDA
    4  데이터 분할

    Copyright 2023, Don Don
    """