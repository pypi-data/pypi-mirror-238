def m7():
    """
    7  Pipeline
    파이프라인은 sklearn에서 머신러닝 모델링을 쉽게 구축해주는 클래스입니다. 간단한 tabular 데이터의 경우 데이터 전처리, 모델링 과정은 유사한 경향이 있습니다. 따라서 반복적으로 많이 사용되는 클래스는 간단하게 pipeline을 이용해서 간단하게 구현해볼 수 있습니다. 또한 pipeline을 이용하면 교차검증시 validation leakage를 방지할 수 있습니다.

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

    데이터 전처리 전 data leakage 방지를 위해 데이터를 train/test로 분할합니다.

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 0)

    7.1 Pipeline example
    먼저 얼마나 코드가 간소화되는지 예시를 살펴보겠습니다. 이전 전처리 코드를 보면 데이터 전처리 함수를 불러와서 반복하는 과정을 거쳤습니다. 범주형 변수와 연속형 변수가 혼합되어 있는 데이터의 경우 코드가 길어지고, 비효율적입니다. pipeline을 이용해서 코드를 간소화해보겠습니다.

    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer, SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer, make_column_transformer
    from sklearn.pipeline import Pipeline, make_pipeline
    from sklearn.linear_model import LinearRegression

    먼저 범주형 변수와 연속형 변수에 각각 다른 전처리를 적용하기 위해 범주형 변수와 연속형 변수를 지정해주었습니다.

    num_columns = train_X.select_dtypes('number').columns.tolist()
    cat_columns = train_X.select_dtypes('object').columns.tolist()

    다음으로 make_pipeline() 함수를 이용해서 간단한 pipeline을 구축해주었습니다. 먼저 범주형 변수의 경우 간단하게 one-hot enocoding을 적용해주었습니다.

    cat_preprocess = make_pipeline(
        #SimpleImputer(strategy="constant", fill_value="NA"),
        OneHotEncoder(handle_unknown="ignore", sparse=False)
    )

    수치형 변수의 경우 goout에 결측치가 존재하므로, 평균대치법을 이용해서 결측치를 대치하고, 변수의 스케일을 맞추기 위해서 표준화를 진행해주었습니다.

    num_preprocess = make_pipeline(
        SimpleImputer(strategy="mean"), 
        StandardScaler()
    )

    마지막으로 ColumnTransformer()를 통해 두 개의 전처리 pipeline을 결합해주었습니다.

    preprocess = ColumnTransformer(
        [("num", num_preprocess, num_columns),
        ("cat", cat_preprocess, cat_columns)]
    )

    preprocess

    ColumnTransformer(transformers=[('num',
                                     Pipeline(steps=[('simpleimputer',
                                                      SimpleImputer()),
                                                     ('standardscaler',
                                                      StandardScaler())]),
                                     ['famrel', 'freetime', 'goout', 'Dalc', 'Walc',
                                      'health', 'absences']),
                                    ('cat',
                                     Pipeline(steps=[('onehotencoder',
                                                      OneHotEncoder(handle_unknown='ignore',
                                                                    sparse=False))]),
                                     ['school', 'sex', 'paid'])])
    train/test에 대해서 전처리 결과를 뽑아볼 수 있습니다. 다만 출력 결과는 numpy array이며, 칼럼명이 없습니다.

    pre_train_X = preprocess.fit_transform(train_X)
    pre_test_X = preprocess.transform(test_X)

    print('train dim : ', pre_train_X.shape)

    train dim :  (292, 13)
    print('test dim : ', pre_test_X.shape)

    test dim :  (74, 13)
    따라서 데이터 프레임으로 변환하고 싶다면, 따로 변수명을 넣어주어야 합니다. 연속형 변수와 범주형 변수가 혼합되어있는 ColumnTransformer()의 경우 .get_feature_names() 옵션이 작동하지 않습니다. 따라서 수동으로 지정해주어야 합니다.

    pd.DataFrame(pre_train_X, columns = preprocess.get_feature_names())

    Transformer num (type Pipeline) does not provide get_feature_names.
    .named_transformers_ 옵션을 이용하면 각 전처리 step 별로 지정된 별칭을 통해, 각 전처리 단계에 접근할 수 있습니다.

    preprocess.named_transformers_

    {'num': Pipeline(steps=[('simpleimputer', SimpleImputer()),
                    ('standardscaler', StandardScaler())]), 'cat': Pipeline(steps=[('onehotencoder',
                     OneHotEncoder(handle_unknown='ignore', sparse=False))])}
    “cat”으로 저장된 별칭 안에 존재하는 one-hot encoder 클래스에 접근했습니다.

    cat_encoder = preprocess.named_transformers_["cat"]["onehotencoder"]
    cat_encoder

    OneHotEncoder(handle_unknown='ignore', sparse=False)
    one-hot encoder의 경우 이전처럼 .get_feature_names() 옵션을 통해 변수명을 불러올 수 있습니다.

    cat_names = list(cat_encoder.get_feature_names())
    print(cat_names)

    ['x0_GP', 'x0_MS', 'x1_F', 'x1_M', 'x2_no', 'x2_yes']
    수치형 변수와 범주형 변수의 각 변수명을 합쳐주었습니다. 마지막으로 해당 칼럼명을 이용해서 데이터프레임으로 변경해주면 됩니다.

    full_name = num_columns + cat_names
    pd.DataFrame(pre_train_X, columns = full_name).head()

         famrel  freetime     goout      Dalc  ...  x1_F  x1_M  x2_no  x2_yes
    0  0.087029 -2.303087 -0.084149 -0.526353  ...   1.0   0.0    0.0     1.0
    1  1.191925 -0.237030 -1.003311 -0.526353  ...   0.0   1.0    1.0     0.0
    2  0.087029 -0.237030 -0.084149 -0.526353  ...   1.0   0.0    0.0     1.0
    3  0.087029 -0.237030 -0.084149  0.579367  ...   0.0   1.0    1.0     0.0
    4  0.087029 -0.237030  0.835014  0.579367  ...   1.0   0.0    0.0     1.0

    [5 rows x 13 columns]
    Note
    sklearn 1.0부터 get_feature_names_out()을 이용하면 칼럼명을 쉽게 출력할 수 있습니다.

    pipepline은 전처리뿐만 아니라 모델링까지 이어서 진행할 수 있습니다. 이전에 구현한 전처리 pipeline을 이용해서 random forest 모형을 적합시켜보겠습니다.

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import cross_val_score

    먼저 사전에 정의한 전처리 pipeline과 함께 RandomForestRegressor()를 불러와서 pipeline을 생성해주었습니다.

    full_pipe = Pipeline(
        [
            ("preprocess", preprocess),
            ("regressor", RandomForestRegressor(random_state=42))
        ]
    )

    pipeline의 경우 set_config()를 이용하면 정의한 pipeline을 다이어그램으로 도식화할 수 있습니다.

    from sklearn import set_config # sklearn version 0.23 이상, adp sklearn 버전 : 0.23.2

    set_config(display="diagram")
    full_pipe

    Pipeline
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    RandomForestRegressor
    pipeline의 각 단계는 .named_steps를 통해 접근할 수 있습니다.

    #full_pipe.named_steps['preprocess']
    full_pipe.named_steps['regressor']


    RandomForestRegressor
    RandomForestRegressor(random_state=42)
    정의한 pipeline을 이용해서 train 데이터를 fitting한 후 모델 성능을 확인해보겠습니다. .fit()을 통해 데이터를 fitting할 수 있습니다. fitting된 결과를 바탕으로 test 데이터를 이용해서 모형 성능을 평가해보겠습니다.

    full_pipe.fit(train_X, train_y)

    Pipeline
    preprocess: ColumnTransformer
    num

    SimpleImputer

    StandardScaler
    cat

    OneHotEncoder

    RandomForestRegressor
    y_preds = full_pipe.predict(test_X)

    RMSE로 모형 성능을 평가하기 위해 sklearn에 내장된 mean_squared_error 함수를 불러왔습니다.

    from sklearn.metrics import mean_squared_error

    모형 성능을 확인해보면 약 3.2정도인 것을 확인할 수 있습니다.

    print('RMSE : ', np.sqrt(mean_squared_error(y_preds, test_y)))

    RMSE :  3.2026054896905527
    이전 챕터의 교차검증을 그대로 적용해볼 수도 있습니다.

    from sklearn.model_selection import KFold

    cv = KFold(n_splits = 5, shuffle = True, random_state = 0)
    cv_score = cross_val_score(full_pipe, train_X, train_y, scoring='neg_mean_squared_error', cv = cv)
    rmse_score = np.sqrt(np.absolute(cv_score))
    mean_rmse_score = np.mean(rmse_score)

    5-fold 교차검증 결과를 보면 평균 RMSE는 약 3.09정도인 것을 확인할 수 있습니다.

    print('RMSE :', rmse_score)

    RMSE : [2.9152386  3.07995068 3.05774098 3.20002822 3.2321638 ]
    print('mean RMSE :', mean_rmse_score)

    mean RMSE : 3.0970244581609894
    """