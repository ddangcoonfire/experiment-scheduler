import pytest
from experiment_scheduler.task_manager.task_manager_server import ResourceManager


class TestResourceManager:
    @pytest.fixture(autouse=True)
    def init(self):
        """
        initialize test
        contruct ResourceManager and set attributes which are required for tests below repeatedly
        """
        num_resource = 2
        self.ResourceManager = ResourceManager(num_resource)
        self.test_task_id0, self.test_task_id1 = "test0", "test1"
        self.ResourceManager.get_resource(self.test_task_id0)
        self.ResourceManager.get_resource(self.test_task_id1)

    def test_test_release_resource(self):
        """
        test target: test_release_resource()
        """
        assert self.ResourceManager.has_available_resource() == False

        self.ResourceManager.release_resource(self.test_task_id0)

        assert self.ResourceManager.has_available_resource() == True


    def test_get_resource(self):
        """
        test target: test_get_resource()
        """

        self.ResourceManager.release_resource(self.test_task_id0)
        resource_idx = self.ResourceManager.get_resource(self.test_task_id0)

        assert resource_idx is not None
    
    def test_get_resource_impossible(self):
        """
        test target: test_get_resource()
        """

        new_test_task_id0 = "new_test0"
        resource_idx = self.ResourceManager.get_resource(new_test_task_id0)

        assert resource_idx is None

    def test_get_resource_twice(self):
        """
        test target: test_get_resource()
        """

        with pytest.raises(RuntimeError):
            self.ResourceManager.get_resource(self.test_task_id0)

    def test_has_availabe_resource(self):
        """
        test target: test_has_available_resource()
        """
        assert not self.ResourceManager.has_available_resource()
        self.ResourceManager.release_resource(self.test_task_id0)
        assert self.ResourceManager.has_available_resource()
        self.ResourceManager.release_resource(self.test_task_id1)
        assert self.ResourceManager.has_available_resource()

    def test_get_tasks_using_resource(self):
        """
        test target: test_get_tasks_using_resource
        """

        assert self.ResourceManager.get_tasks_using_resource() == [
            self.test_task_id0,
            self.test_task_id1,
        ]
