import data
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def compute_cases(claims):
    split_by_provider = data.split_by(claims, 'provider_id')
    num_cases = {}
    for provider in split_by_provider.keys():
        num_cases[provider]=len(split_by_provider[provider])
    return num_cases


def compute_overcharge_and_fees(claims):
    average_proc_price = data.average(claims, 'procedure', 'amount')
    split_by_provider = data.split_by(claims, 'provider_id')
    oc = {}
    fees = {}
    for provider in split_by_provider.keys():
        fees[provider] = split_by_provider[provider]['amount'].sum()
        average_price = 0
        for case in split_by_provider[provider]:
            average_price += average_proc_price[case['procedure']]['avg']
        oc[provider] = (fees[provider] - average_price)*1.0/average_price
    return oc, fees

def compute_per_patient_stats(claims):
    split_by_provider = data.split_by(claims, 'provider_id')
    mean_fees = {}
    std_fees = {}
    mean_visits = {}
    std_visits = {}
    for provider in split_by_provider.keys():
        fees = {}
        visits = {}
        for case in split_by_provider[provider]:
            key = str(case['family_id'])+str(case['member_id'])
            fees[key] = fees.get(key,0) + case['amount']
            visits [key] = visits.get(key,0) + 1
        mean_fees[provider] = np.mean(list(fees.values()))
        std_fees[provider] = np.std(list(fees.values()))
        mean_visits[provider] = np.mean(list(visits.values()))
        std_visits[provider] = np.std(list(visits.values()))
    return mean_fees, std_fees, mean_visits, std_visits


def plot_clf(clf, X, x, y, y_pred, labels, axes_calculated, pmin=-5, pmax=5, points = 10, size=(12,12)):
    n_dimensions=len(axes_calculated)
    inlier_idx = np.where(y_pred==1)[0]
    outlier_idx = np.where(y_pred==-1)[0]
    x = np.where(axes_calculated == x)[0][0]
    y = np.where(axes_calculated == y)[0][0]

    lin = np.linspace(pmin, pmax, points)
    xx, yy = np.meshgrid(lin, lin)
    grid = np.zeros((len(xx.ravel()), n_dimensions))
    grid[:, x] = xx.ravel()
    grid[:, y] = yy.ravel()
    Z = clf._decision_function(grid)
    Z = Z.reshape((points, points))
    plt.figure(figsize=size)
    plt.title("Local Outlier Factor (LOF)")
    plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

    a = plt.scatter(X[inlier_idx, x], X[inlier_idx, y], c='white',
                    edgecolor='k', s=20)
    b = plt.scatter(X[outlier_idx, x], X[outlier_idx, y], c='red',
                    edgecolor='k', s=20)
    plt.axis('tight')
    plt.xlim((pmin, pmax))
    plt.ylim((pmin, pmax))
    plt.xlabel(labels[x])
    plt.ylabel(labels[y])
    plt.axvline(0)
    plt.axhline(0)
    plt.legend([a, b],
               ["normal observations",
                "abnormal observations"],
               loc="upper left")
    plt.show()
