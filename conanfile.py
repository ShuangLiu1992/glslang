from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain
import os


class GLSLANGConan(ConanFile):
    name = "glslang"
    settings = "os", "compiler", "build_type", "arch"

    generators = "CMakeDeps"

    def requirements(self):
        self.requires(f"spirv_tools/{self.version}@")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.presets_prefix = f"{self.settings.os}_{self.settings.build_type}_{self.settings.arch}"
        tc.variables["ENABLE_OPT"] = True
        tc.variables["ENABLE_HLSL"] = True
        tc.generate()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        os.makedirs(f"{self.package_folder}/include/External")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "glslang"))
        self.buildenv_info.define("glslang_DIR", self.package_folder)
