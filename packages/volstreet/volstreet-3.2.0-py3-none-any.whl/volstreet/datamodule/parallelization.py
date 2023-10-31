from joblib import Parallel, delayed


def execute_in_parallel(tasks, n_jobs=-1):
    """
    Executes tasks in parallel using joblib's Parallel and delayed functions.

    Parameters:
    tasks: List of tuples, where the first element is the function to execute,
           and the second element is a tuple containing arguments for that function.
    n_jobs: Number of jobs to run in parallel. -1 means using all processors.

    Returns:
    List of results corresponding to each task.
    """
    # Use joblib's Parallel to execute tasks in parallel
    results = Parallel(n_jobs=n_jobs)(delayed(task[0])(*task[1]) for task in tasks)
    return results
