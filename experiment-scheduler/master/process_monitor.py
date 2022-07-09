class ProcessMonitor:
    def __init__(self):
        self.job_list = dict()

    def add_job(self,request):
        self.job_list[request.id] = request

    def list_executing_job(self):
        """
        print job_list
        :return:
        """
        pass

    def delete_job(self,request):
        """
        delete job_list
        stop process on task_manager by request
        :param request:
        :return:
        """

        # request to task manager stop certain job
        # if stopped, delete it on job_list
        # save logs