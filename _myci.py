import os
import bg_helper as bh


# Call via the following:
#   tools-py-python ~/repos/personal/packages/mongo-helper/_myci.py

this_dir = os.path.dirname(os.path.abspath(__file__))
local_package_paths = [this_dir]


def create_test_environments():
    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.5.10',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
        dep_versions_dict={
            'pymongo': '3.7.2, 3.8.0, 3.9.0, 3.10.1, 3.11.4, 3.12.3, 3.13.0',
        }
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.6.15',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4, pdbpp==0.10.3',
        dep_versions_dict={
            'pymongo': '3.7.2, 3.8.0, 3.9.0, 3.10.1, 3.11.4, 3.12.3, 3.13.0, 4.0.2, 4.1.1',
        }
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.7.17, 3.8.20, 3.9.20',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
        dep_versions_dict={
            'pymongo': '3.7.2, 3.8.0, 3.9.0',
        }
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.7.17, 3.8.20, 3.9.20, 3.10.15, 3.11.10, 3.12.7, 3.13.5',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
        dep_versions_dict={
            'pymongo': '3.10.0, 3.11.4, 3.12.3, 3.13.0, 4.0.2, 4.1.1, 4.2.0, 4.3.3, 4.4.1, 4.5.0, 4.6.3, 4.7.3',
        }
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.8.20, 3.9.20, 3.10.15, 3.11.10, 3.12.7, 3.13.5',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
        dep_versions_dict={
            'pymongo': '4.8.0, 4.9.2, 4.10.1',
        }
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.9.20, 3.10.15, 3.11.10, 3.12.7, 3.13.5',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
        dep_versions_dict={
            'pymongo': '4.11.3, 4.12.1, 4.13.2',
        }
    )

    # No-dependency environments for each Python version
    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.7.17, 3.8.20, 3.9.20, 3.10.15, 3.11.10, 3.12.7, 3.13.5',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4, pdbpp',
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.5.10',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4',
    )

    bh.tools.pyenv_create_venvs_for_py_versions_and_dep_versions(
        this_dir,
        py_versions='3.6.15',
        die=True,
        local_package_paths=local_package_paths,
        extra_packages='pytest<=7.4.4, pdbpp==0.10.3',
    )


if __name__ == '__main__':
    create_test_environments()
