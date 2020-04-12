import os

from rosdistro import get_cached_distribution, get_index, get_index_url
from rosdistro.dependency_walker import DependencyWalker
from rosdistro.manifest_provider import get_release_tag


class Distro(object):

    def __init__(self, distro_name, python_version=None):
        index = get_index(get_index_url())
        self._distro = get_cached_distribution(index, distro_name)

        # set up ROS environments
        if python_version is None:
            python_version = index.distributions[distro_name]['python_version']
        os.environ['ROS_PYTHON_VERSION'] = '{0}'.format(
            python_version)
        os.environ['ROS_DISTRO'] = '{0}'.format(
            distro_name)
        if 'ROS_ROOT' in os.environ:
            os.environ.pop('ROS_ROOT')
        if 'ROS_PACKAGE_PATH' in os.environ:
            os.environ.pop('ROS_PACKAGE_PATH')
        self._walker = DependencyWalker(
            self._distro,
            evaluate_condition_context=os.environ)

        # cache distribution type
        self._distribution_type = index.distributions[distro_name]['distribution_type']
        self._python_version = index.distributions[distro_name]['python_version']

    def get_depends(self, pkg):
        dependencies = set()
        dependencies |= self._walker.get_recursive_depends(
            pkg,
            ['buildtool', 'buildtool_export', 'build', 'build_export',
             'run', 'test', 'exec'],
            ros_packages_only=True)
        return dependencies

    def get_released_repo(self, pkg_name):
        pkg = self._distro.release_packages[pkg_name]
        repo = self._distro.repositories[pkg.repository_name].release_repository
        release_tag = get_release_tag(repo, pkg_name)
        return repo.url, release_tag

    def check_package(self, pkg_name):
        if pkg_name in self._distro.release_packages:
            return True
        else:
            return False

    def get_version(self, pkg_name):
        pkg = self._distro.release_packages[pkg_name]
        repo = self._distro.repositories[pkg.repository_name].release_repository
        return repo.version.split('-')[0]

    def get_release_package_xml(self, pkg_name):
        return self._distro.get_release_package_xml(pkg_name)

    def check_ros1(self):
        return self._distribution_type == "ros1"

    def get_python_version(self):
        return self._python_version
