import io
import os
import sys
import time
import re
import subprocess

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


def find_version():
    with io.open("CMakeLists.txt", encoding="utf8") as f:
        version_file = f.read()

    version_major = re.findall(r"unitree_legged_sdk_VERSION_MAJOR (.+?)", version_file)
    version_minor = re.findall(r"unitree_legged_sdk_VERSION_MINOR (.+?)", version_file)

    if version_major and version_minor:
        unitree_legged_sdk_version = time.strftime("%Y%m%d", time.localtime())

        return version_major[0] + "." + version_minor[0] + "." + unitree_legged_sdk_version
    raise RuntimeError("Unable to find version string.")


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, "unitree_legged_sdk")

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={}".format(extdir),
            "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),  # not used on MSVC, but no harm
            "-DPYTHON_BUILD=ON",
        ]
        build_args = []

        if self.compiler.compiler_type == "msvc":
            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                build_args += ["--config", cfg]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]
            else:
                build_args += ["-j4"]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )


if sys.version_info < (3, 0):
    sys.exit("Sorry, Python < 3.0 is not supported")

requirements = ["pybind11", "auditwheel ", "twine", "wheel", "setuptools "]

with io.open("README.md", encoding="utf-8") as h:
    long_description = h.read()

setup(
    name="unitree_legged_sdk",
    version=find_version(),
    author="LJoson",
    author_email="1250377062@qq.com",
    maintainer="Unitree Robotics",
    maintainer_email="Laikago@unitree.cc",
    description="The unitree_legged_sdk is mainly used for communication between PC and Controller board.It also can be used in other PCs with UDP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unitreerobotics/unitree_legged_sdk",
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    license="BSD-3",
    python_requires=">=3.6",
    packages=find_packages("unitree_legged_sdk"),
    package_dir={"": "unitree_legged_sdk"},
    install_requires=requirements,
    ext_modules=[CMakeExtension("robot_interface")],
    cmdclass={"build_ext": CMakeBuild},
)

