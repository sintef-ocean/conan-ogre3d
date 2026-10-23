from os import path
from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import cmake_layout, CMake, CMakeToolchain
from conan.tools.scm import Version


class Ogre3dTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        ogre = self.dependencies["ogre3d"]
        tc = CMakeToolchain(self)
        # imgui headers are packaged with Ogre since 14.6
        tc.variables["TEST_IMGUI"] = bool(ogre.options.component_overlay_imgui) \
            and Version(ogre.ref.version) >= "14.6"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(bin_path, env="conanrun")
