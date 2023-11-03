def m13():
    """
    13  Anomaly detection
    Sys.setenv(RETICULATE_PYTHON = "/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")
    library(reticulate)
    use_python("/opt/homebrew/Caskroom/miniconda/base/envs/python_adp/bin/python")

    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from sklearn.preprocessing import StandardScaler

    13.1 Anomaly detection이란?
    anomaly detection은 outlier detection, novelty detection으로 표현되며, 이상 탐지로 표현할 수 있습니다.

    Anomalies are patterns in data that do not conform to a well defined notion of normal behavior.


    그림을 통해 보면 
    는 다수의 관측치들과 다른 패턴을 보이므로, 이상치로 볼 수 있습니다.

    13.2 Anomaly detecion 구분
    이상 탐지는 label이 있는 데이터와 없는 데이터를 생각해볼 수 있습니다.

    Supervised anomaly detection : label이 존재하는 경우

    보험회사의 사기 탐지 모형 개발 : 사기라는 것을 감독관과 현업 구성원들이 규정하고 데이터를 수집한 경우
    Unsupervised anomaly detection : label이 존재하지 않는 경우

    실제로는 label이 없는 경우가 많습니다. 이상이라는 것이 사전에 정의가 되어있고, 데이터로 정의되어 있을 경우 해당 label을 이용해서 모형 성능을 평가할 수 있지만, 이상이 정의가 되어있지 않은 경우에는 이를 이용하기 어렵습니다. 따라서 적정 threshold를 정한 후 threshold 이상 넘어갈 경우 전부 이상치로 볼 수 있습니다.

    13.3 Local Outlier Factor(LOF)
    LOF는 주변 이웃들의 밀도를 고려하여 이상치를 탐지하는 알고리즘입니다. 그림을 통해 보겠습니다.



    그림을 보면 C1영역은 밀도가 높은 영역을 의미하며, C2는 밀도가 낮은 영역을 의미합니다. C1과 C2 관점에서 보면 O3는 전역 이상치(혼자 떨어져 있으므로)인 것을 알 수 있습니다. O1과 O2의 경우 밀도가 높은 C1 영역에서 멀리 떨어져있는 관측치이므로 이상치로 분류할 수 있습니다. 반면 O4의 경우 밀도가 낮은 C2 영역에서 떨어져있는 관측치 이므로, 이상치로 분류될 수 없습니다. 즉, LOF는 주변 이웃들의 밀도 정보를 활용해서 이상치를 분류하는 알고리즘으로 정리해볼 수 있습니다.

    LOF를 정의하는 방식은 다음과 같습니다.

    k-distance of an object p



    local 정보를 반영하기 위해서는 주변 이웃에 대한 거리를 측정해야 함

    k-distance of an object p는 임의의 관측치 
    에 대해 k번째 이웃의 거리를 측정하는 것으로 볼 수 있음

    ex) 
    이면 임의의 P와 주변 이웃 3개의 거리 중 최대값을 의미함
    k-distance neighborhood of an object 


    k-distance boundary 내에 위치한 관측치의 수를 의미함
    가 크면, k-distance boundary 내에 관측치의 수가 많으므로, 밀도가 높음
    ex) 
    이면 
    번째 이웃까지의 거리를 기준으로 boundary를 생성했을 때, boundary 내에 존재하는 관측치의 수로 볼 수 있음

    Reachability distance of an object p w.r.t object o


    o에 대한 k-distance와 o와 p 사이의 거리 중에 큰 값을 reachability distance로 정의함


    (o와 p가 멀리 떨어져있을 경우) reach-dist는 o와 
     사이의 실제 거리로 계산됨

    o와 
     사이의 실제 거리가 크다면 이상치로 분류될 가능성이 높음
    (o와 p가 상대적으로 가까운 경우) reach-dist는 o의 k-distance로 계산됨

    은 o 주변에 위치하므로 정상 관측치로 분류될 가능성이 높음

    k값에 따라서 k-distance는 유동적이며, 따라서 boundary의 크기는 조정될 수 있음

    k가 클 경우, boundary는 커짐

    k가 작을 경우, boundary는 작아짐

    local reachability density of an object p



    정상관측치의 경우 
    는 커짐

    는 커짐(k-distance boundary 내에 관측치의 수가 많으므로, 밀도가 높음(정상))$$

    는 작아짐

    이상 관측치의 경우 
    는 작아짐

    는 작아짐(k-distance boundary 내에 관측치의 수가 적으므로, 밀도가 낮음(이상))

    는 커짐

    local outlier factor of an object p




    p가 이상치일 경우, 
     는 작아지고, 
     는 커짐

     는 커짐
    p가 정상치일 경우 
     는 커지고, 
     는 상대적으로 커짐

    는 작아짐
    Example

    train = pd.read_csv("data/credit_fraud/train.csv")
    valid = pd.read_csv("data/credit_fraud/val.csv")

    train = train.clean_names()
    valid = valid.clean_names()

    train = train.drop(['id'], axis = 1)
    valid_x = valid.drop(['id', 'class'], axis = 1)
    valid_y = valid['class']

    from sklearn.neighbors import LocalOutlierFactor

    LocalOutlierFactor의 minpts은 int형이어야 합니다. .negative_outlier_factor_는 lof score를 의미합니다. 값이 작을수록 이상치로 판정됩니다. new_data에 대해서 lof를 적용할 경우 novelty = True 옵션을 적용합니다. novelty = True로 설정할 경우 .fit_predict가 아닌 predict()를 이용합니다.

    contamination = 0.001은 데이터 내에 이상치의 비율을 의미합니다.

    minpts = np.round(np.log(train.shape[0])).astype(int)
    clf = LocalOutlierFactor(n_neighbors = minpts, contamination = 0.001, novelty = True)
    clf.fit(train)

    LocalOutlierFactor(contamination=0.001, n_neighbors=12, novelty=True)
    (1:정상, -1:불량(사기))

    from sklearn.metrics import confusion_matrix, classification_report
    from sklearn import set_config

    pred_val = clf.predict(valid_x)
    valid_y.replace(1, -1, inplace = True)
    valid_y.replace(0, 1, inplace = True)

    result = pd.DataFrame({'real' : valid_y, 'pred' : pred_val})

    confusion_matrix(result.real, result.pred)

    array([[    0,    30],
           [   29, 28403]])
    print(classification_report(result.real, result.pred))

                  precision    recall  f1-score   support

              -1       0.00      0.00      0.00        30
               1       1.00      1.00      1.00     28432

        accuracy                           1.00     28462
       macro avg       0.50      0.50      0.50     28462
    weighted avg       1.00      1.00      1.00     28462
    13.4 Isolation forest
    Motivation

    Isolation-based Anomaly Detection

    (a) 그림의 
    의 경우 normal 관측치 사이에 위치해있으므로, isolated 하는데 많은 split이 필요합니다. 반면 (b) 그림의 
    의 경우 abnormal 관측치이므로, isolated 하는데 적은 split이 필요합니다. 따라서 isolated되기 위한(terminal node까지 도달하기 위한 거리) edge의 수를 이용해서 anomaly score를 정의할 수 있습니다.

    Isolation tree

    데이터를 subsampling 하여 
     을 생성
    split에 사용하기 위한 변수 
    를 임의로 선택
    변수 
     의 min, max value 사이에 값 
     를 임의로 선택
    보다 작을 경우 
    에 할당
    보다 클 경우 
    에 할당
    isolated(관측치가 완벽하게 분리될 때까지)될 때까지 재귀적 반복
    Path length

     : isolated될 때까지의 edge의 수


    은 
    의 평균을 의미하므로, 이 값을 이용해서 
    를 normalize 할 수 있고, 이를 통해 anomaly score를 유도할 수 있음
    anomaly score


    집합으로부터의평균




    즉, 
    가 
    에 가까울수록, 이상치에 가까우므로, anomaly score는 커짐

    데이터 출처 : https://dacon.io/competitions/official/235930/overview/description

    train = pd.read_csv("data/credit_fraud/train.csv")
    valid = pd.read_csv("data/credit_fraud/val.csv")

    train = train.clean_names()
    valid = valid.clean_names()

    train = train.drop(['id'], axis = 1)
    valid_x = valid.drop(['id', 'class'], axis = 1)
    valid_y = valid['class']

    from sklearn.ensemble import IsolationForest

    clf = IsolationForest(random_state=0, contamination = 0.001)
    clf.fit(train)

    IsolationForest(contamination=0.001, random_state=0)
    (1:정상, -1:불량(사기))

    pred_val = clf.predict(valid_x)
    valid_y.replace(1, -1, inplace = True)
    valid_y.replace(0, 1, inplace = True)

    result = pd.DataFrame({'real' : valid_y, 'pred' : pred_val})

    confusion_matrix(result.real, result.pred)

    array([[   11,    19],
           [   13, 28419]])
    print(classification_report(result.real, result.pred))

                  precision    recall  f1-score   support

              -1       0.46      0.37      0.41        30
               1       1.00      1.00      1.00     28432

        accuracy                           1.00     28462
       macro avg       0.73      0.68      0.70     28462
    weighted avg       1.00      1.00      1.00     28462
    13.4.1 참고자료
    isolation forest

    isolation-based anomaly detection

    isotree

    Anomaly detection : A survey

    """
