from experiment_scheduler.common.logging import get_logger


logger = get_logger(name="task_manager")


class ResourceManager:
    def __init__(self, num_resource: int):
        self._resource_rental_history = {}
        self._available_resources = [True for _ in range(num_resource)]
        self.logger = get_logger(name="resource_manager")

    def set_resource_as_idle(self, resource_idx: int):
        self._available_resources[resource_idx] = True

    def set_resource_as_used(self, resource_idx: int):
        self._available_resources[resource_idx] = False

    def release_resource(self, task_id):
        if task_id not in self._resource_rental_history:
            return
        resource_idx = self._resource_rental_history[task_id]
        self._available_resources[resource_idx] = True
        del self._resource_rental_history[task_id]

    def get_resource(self, task_id):
        resource_idx = None
        for idx, resource_is_idle in enumerate(self._available_resources):
            if resource_is_idle:
                resource_idx = idx
                break
        if resource_idx is None:
            self.logger.info("There isn't any available resource.")
            return None

        self._resource_rental_history[task_id] = resource_idx
        self._available_resources[resource_idx] = False

        return resource_idx

    def has_available_resource(self):
        for resource_is_idle in self._available_resources:
            if resource_is_idle:
                return True
        return False

    def get_tasks_using_resource(self):
        return list(self._resource_rental_history.keys())

