import os

from grader_service.autograding.kube.kube_grader import KubeAutogradeExecutor
from grader_service.autograding.local_grader import LocalAutogradeExecutor, LocalProcessAutogradeExecutor

c.GraderService.service_host = "127.0.0.1"
# existing directory to use as the base directory for the grader service
service_dir = os.path.expanduser("~/Documents/Work/grader_service_dir")
c.GraderService.grader_service_dir = service_dir

c.JupyterHubGroupAuthenticator.hub_api_url = "http://127.0.0.1:8081/hub/api"

# c.LocalAutogradeExecutor.relative_input_path = "convert_in"
# c.LocalAutogradeExecutor.relative_output_path = "convert_out"

assert issubclass(KubeAutogradeExecutor, LocalAutogradeExecutor)
c.RequestHandlerConfig.autograde_executor_class = LocalAutogradeExecutor
c.LocalAutogradeExecutor.timeout_func = lambda l: 20

c.KubeAutogradeExecutor.kube_context = "minikube"
c.KubeAutogradeExecutor.default_image_name = lambda l, a: "s210.dl.hpc.tuwien.ac.at/grader/grader-notebook-minimal:arm"

print("##########: concurrent tasks = 1")
c.GraderExecutor.n_concurrent_tasks = 1
