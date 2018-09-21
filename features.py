def compute_cases(claims):
    split_by_provider = data.split_by(claims, 'provider_id')
    num_cases = {}
    for provider in split_by_provider.keys():
        num_cases[provider]=len(split_by_provider[provider])
    return num_cases
    