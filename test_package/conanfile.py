import os

from conans import ConanFile, CMake, tools


class Ogre3dTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            target_name = "test_package"
            if self.settings.os == "Windows":
                tester_exe = target_name + ".exe"
                tester_path = os.path.join(self.build_folder,
                                           str(self.settings.build_type))
            else:
                tester_exe = target_name
                tester_path = "." + os.sep
            self.run(os.path.join(tester_path, tester_exe),
                     run_environment=True)
