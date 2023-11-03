from IPython.display import display, Latex
import time


def print_latex(latex_string: str):
    display(Latex(latex_string))


# Wrapper (decorator) for evaluating execution time of a given function
def time_it(original_func):
    def wrapper_func(*args, **kwargs):
        start = time.perf_counter_ns()
        return_val = original_func(*args, **kwargs)
        end = time.perf_counter_ns()
        elapsed_time_millis = end - start
        print(
            f"'{original_func.__name__}' time of execution: {elapsed_time_millis} [ns]"
        )
        return return_val

    return wrapper_func
