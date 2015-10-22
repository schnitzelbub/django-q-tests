from nose_parameterized import parameterized


def custom_name_func(testcase_func, param_num, param):
    return "{}_{}".format(
        testcase_func.__name__,
        parameterized.to_safe_name("_".join("{}_{}".format(key, val) for key, val in param.kwargs.items())))


def custom_name_func_param_num(testcase_func, param_num, param):
    return "{}_{}_{}".format(
        testcase_func.__name__,
        param_num,
        parameterized.to_safe_name("_".join("{}_{}".format(key, val) for key, val in param.kwargs.items())))
