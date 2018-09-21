import data
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
