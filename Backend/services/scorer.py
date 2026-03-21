def calculate_score(data):

    score = 100

    rules = [
        ("glucose", 140, 10),
        ("hba1c", 6.5, 10),
        ("ldl", 130, 10),
        ("triglycerides", 150, 10),
        ("creatinine", 1.3, 10),
        ("alt", 55, 5),
        ("ast", 48, 5),
        ("hemoglobin", 12, 10)
    ]

    for param, limit, penalty in rules:
        val = data.get(param, None)

        if val is not None:
            if param == "hemoglobin":
                if val < limit:
                    score -= penalty
            else:
                if val > limit:
                    score -= penalty

    return max(score, 0)