import data
import numpy as np
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
