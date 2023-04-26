import pytest
from experiment_scheduler.task_manager.task_manager_server import ResourceManager


class TestResourceManager:
    @pytest.fixture(autouse=True)
    def init(self):
        """
        initialize test
        contruct ResourceManager and set attributes which are required for tests below repeatedly
        """
        num_resource = 4
        self.ResourceManager = ResourceManager(num_resource)
        self.test_task_id0, self.test_task_id1 = "test0", "test1"
        self.ResourceManager._resource_rental_history[self.test_task_id0] = 0
        self.ResourceManager._resource_rental_history[self.test_task_id1] = 1
        self.ResourceManager._available_resources[0] = False
        self.ResourceManager._available_resources[1] = False

    def test_set_resource_as_idle(self):
        """
        test target: set_resource_as_idle()
        """
        test_idx = 0
        assert self.ResourceManager._available_resources[test_idx] == False

        self.ResourceManager.set_resource_as_idle(test_idx)
        assert self.ResourceManager._available_resources[test_idx] == True

    def test_set_resource_as_used(self):
        """
        test target: set_resource_as_used()
        """

        test_idx = 2
        assert self.ResourceManager._available_resources[test_idx] == True

        self.ResourceManager.set_resource_as_used(test_idx)
        assert self.ResourceManager._available_resources[test_idx] == False

    def test_test_release_resource(self):
        """
        test target: test_release_resource()
        """

        self.ResourceManager.release_resource(self.test_task_id0)

        assert self.test_task_id0 not in self.ResourceManager._resource_rental_history
        assert self.ResourceManager._available_resources[0] == True
        assert self.test_task_id1 in self.ResourceManager._resource_rental_history
        assert self.ResourceManager._available_resources[1] == False

    def test_get_resource(self):
        """
        test target: test_get_resource()
        """
        new_test_task_id0, new_test_task_id1, new_test_task_id2 = (
            "new_test0",
            "new_test1",
            "new_test2",
        )
        new_resource_idx0 = self.ResourceManager.get_resource(new_test_task_id0)
        new_resource_idx1 = self.ResourceManager.get_resource(new_test_task_id1)

        assert (
            self.ResourceManager._resource_rental_history[new_test_task_id0]
            == new_resource_idx0
        )
        assert self.ResourceManager._available_resources[new_resource_idx0] == False
        assert self.ResourceManager.get_resource(new_test_task_id2) == None

    def test_has_availabe_resource(self):
        """
        test target: test_has_available_resource()
        """
        assert self.ResourceManager.has_available_resource() == True

        new_test_task_id0, new_test_task_id1 = "new_test0", "new_test1"
        self.ResourceManager.get_resource(new_test_task_id0)
        self.ResourceManager.get_resource(new_test_task_id1)

        assert self.ResourceManager.has_available_resource() == False

    def test_get_tasks_using_resource(self):
        """
        test target: test_get_tasks_using_resource
        """

        assert self.ResourceManager.get_tasks_using_resource() == [
            self.test_task_id0,
            self.test_task_id1,
        ]
