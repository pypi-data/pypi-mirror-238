"""
Defines a Skyramp client, which can be used to interact with a cluster.
"""

import ctypes
import json
import yaml

from skyramp.utils import _library, _call_function
from skyramp.scenario import _Scenario
from skyramp.endpoint import _Endpoint

class _Client:
    """
    Skyramp client object which can be used to interact with a cluster.
    """

    def __init__(
        self,
        kubeconfig_path: str = "",
        cluster_name: str = "",
        context: str = "",
    ) -> None:
        """
        Initializes a Skyramp Client.

        kubeconfig_path: The filesystem path of a kubeconfig
        cluster_name: The name of the cluster.
        context: The Kubernetes context within a kubeconfig
        """
        self.kubeconfig_path = kubeconfig_path
        self.cluster_name = cluster_name
        self.context = context
        self.project_path = ""
        self._namespace_set = set()

    def apply_local(self) -> None:
        """
        Creates a local cluster.
        """
        apply_local_function = _library.applyLocalWrapper
        argtypes = []
        restype = ctypes.c_char_p

        _call_function(apply_local_function, argtypes, restype, [])

        self.kubeconfig_path = self._get_kubeconfig_path()
        if not self.kubeconfig_path:
            raise Exception("no kubeconfig found")

    def remove_local(self) -> None:
        """
        Removes a local cluster.
        """
        func = _library.removeLocalWrapper
        argtypes = []
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [])

    def add_kubeconfig(
        self,
        context: str,
        cluster_name: str,
        kubeconfig_path: str,
    ) -> None:
        """
        Adds a preexisting Kubeconfig file to Skyramp.

        context: The kubeconfig context to use
        cluster_name: Name of the cluster
        kubeconfig_path: filepath of the kubeconfig
        """
        func = _library.addKubeconfigWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [
                context.encode(),
                cluster_name.encode(),
                kubeconfig_path.encode(),
            ],
        )

        self.kubeconfig_path = kubeconfig_path

    def remove_cluster(self, cluster_name: str) -> None:
        """
        Removes a cluster, corresponding to the name, from Skyramp
        """
        func = _library.removeClusterFromConfigWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [cluster_name.encode()])

    def deploy_skyramp_worker(
        self, namespace: str, worker_image: str, local_image: bool
    ) -> None:
        """
        Installs a Skyramp worker onto a cluster if one is registered with Skyramp
        """
        if not self.kubeconfig_path:
            raise Exception("no cluster to deploy worker to")

        func = _library.deploySkyrampWorkerWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [namespace.encode(), worker_image.encode(), local_image],
        )

        self._namespace_set.add(namespace)

    def delete_skyramp_worker(self, namespace: str) -> None:
        """
        Removes the Skyramp worker, if a Skyramp worker is installed on a registered Skyramp cluster
        """
        if not self.kubeconfig_path:
            raise Exception("no cluster to delete worker from")

        if namespace not in self._namespace_set:
            raise Exception(f"no worker to delete from {namespace} namespace")

        func = _library.deleteSkyrampWorkerWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        _call_function(func, argtypes, restype, [namespace.encode()])

        self._namespace_set.remove(namespace)

    def mocker_apply(self, namespace: str, address: str, endpoint) -> None:
        """
        Applies a configuration to mocker.
        namespace: The namespace where Mocker resides
        address: The address of Mocker
        endpoint: The Skyramp enpdoint object
        """
        yaml_string = yaml.dump(endpoint.mock_description)

        func = _library.applyMockDescriptionWrapper
        argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        restype = ctypes.c_char_p  # pylint: disable=duplicate-code

        _call_function(
            func,
            argtypes,
            restype,
            [
                namespace.encode(),
                address.encode(),
                yaml_string.encode(),
            ],
        )

    def tester_start(self, namespace: str, address: str, scenario: _Scenario, blocked=False):
        """
        Runs testers. If namespace is provided, connects with the worker instance running
        on the specified namespace in the registered Kubernetes cluster. If address is provided,
        connects to the worker directly using the network address.
        namespace: The namespace where mocker resides
        address: The address to reach mocker
        scenario: Scenario object for the test to run
        """
        test_description = scenario.get_test_description()
        test_yaml = yaml.dump(test_description)

        func = _library.runTesterStartWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
        restype = ctypes.c_char_p

        _call_function(
            func,
            argtypes,
            restype,
            [
                namespace.encode(),
                address.encode(),
                test_yaml.encode(),
                True,
            ],
        )

        if blocked:
            # Wait until the test is done
            func = _library.runTesterStatusWrapper
            argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            restype = ctypes.c_char_p

            tester_status_raw = _call_function(
                func,
                argtypes,
                restype,
                [namespace.encode(), address.encode()],
                return_output=True,
            )

            tester_status = ""
            try:
                tester_status = json.loads(tester_status_raw)
            except ValueError as error:
                raise Exception(f"Could not parse tester status: {error}")

            if "status" not in tester_status:
                raise Exception(f"Could not parse tester status: {tester_status}")

            if tester_status["status"] == "finished":
                return

            if "error" in tester_status:
                raise Exception(f"Test failed: {tester_status['error']}")

            if "message" in tester_status:
                raise Exception(f"Test failed: {tester_status['message']}")

            raise Exception("Test failed")

    def _get_kubeconfig_path(self) -> str:
        func = _library.getKubeConfigPath
        argtypes = []
        restype = ctypes.c_char_p

        return _call_function(func, argtypes, restype, [], True)

    def set_project_directory(self, path: str) -> None:
        """
        Sets the project directory for the client.
        """
        self.project_path = path
        func = _library.setProjectDirectoryWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        return _call_function(func, argtypes, restype, [path.encode()])

    def load_endpoint(self, name: str) -> _Endpoint:
        """
        Loads an endpoint from a file.
        """
        if not self.project_path:
            raise Exception("project path not set")
        func = _library.getEndpointFromProjectWrapper
        argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        restype = ctypes.c_char_p

        endpoint_data = _call_function(
            func,
            argtypes,
            restype,
            [
                name.encode(),
                self.project_path.encode(),
            ],
            True,
        )
        if not endpoint_data:
            raise Exception(f"endpoint {name} not found")
        try:
            endpoint = json.loads(endpoint_data)
        except json.JSONDecodeError:
            raise ValueError(f"Endpoint data for {name} is not valid JSON")
        return _Endpoint(json.dumps(endpoint))


    # pylint: disable=unused-argument
    # pylint: disable=line-too-long
    def tester_start_v1(self, scenario: _Scenario, global_headers: map=None, namespace: str='',address: str='', blocked=False) -> str:
        """
        Runs testers. If namespace is provided, connects with the worker instance running
        on the specified namespace in the registered Kubernetes cluster. If address is provided,
        connects to the worker directly using the network address.
        namespace: The namespace where mocker resides
        address: The address to reach mocker
        scenario: Scenario object for the test to run
        """
        if scenario is None:
            raise Exception("no scenario provided")

        scenario.set_global_headers(global_headers)
        test_description = scenario.get_test_description_v1()

        test_yaml = yaml.dump(test_description)
        # global_headers_json = json.dumps(global_headers)

        # combine all the scenarios into one test_description
        if blocked:
            func = _library.runTesterStartWrapper
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
            restype = ctypes.c_char_p

            _call_function(
                func,
                argtypes,
                restype,
                [
                    namespace.encode(),
                    address.encode(),
                    test_yaml.encode(),
                    True,
                ],
            )

            func = _library.runTesterStatusWrapper
            argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            restype = ctypes.c_char_p

            tester_status_raw = _call_function(
                func,
                argtypes,
                restype,
                [namespace.encode(), address.encode()],
                return_output=True,
            )

            tester_status = ""
            try:
                tester_status = json.loads(tester_status_raw)
            except ValueError as error:
                raise Exception(f"Could not parse tester status: {error}")

            if "status" not in tester_status:
                raise Exception(f"Could not parse tester status: {tester_status}")

            if tester_status["status"] == "finished":
                return

            if "error" in tester_status:
                raise Exception(f"Test failed: {tester_status['error']}")

            if "message" in tester_status:
                raise Exception(f"Test failed: {tester_status['message']}")

            raise Exception("Test failed")



def _new_client(kubeconfig_path: str) -> _Client:
    return _Client(
        kubeconfig_path=kubeconfig_path,
        context="kind-skyramp-local-kind-cluster",
        cluster_name="kind-cluster",
    )
