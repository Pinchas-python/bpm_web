tear_down_tasks = []


def add_task(tear_down_object: any):
    tear_down_tasks.append(tear_down_object)


def add_task_first_index(tear_down_object: any):
    tear_down_tasks.insert(0, tear_down_object)