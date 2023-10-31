def round_grade(grade: float) -> float:
    '''
    Round a grade based on the UFSC grades round model: 0, 0.5, 1.0
    '''
    integer_part, decimal_part = divmod(grade, 1)
    if decimal_part >= 0.75:
        return float(integer_part) + 1.0
    elif decimal_part >= 0.25:
        return float(integer_part) + 0.5
    else:
        return float(integer_part)
    

def normalize(value, max, min):
        return (value - min)/(max - min)

def rescale_to_0_10_scale(value_to_rescale, max):
    if max > 0:
        return (10 * value_to_rescale / max)
    else:
        return 0