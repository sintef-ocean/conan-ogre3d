[_![MSVC Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/MSVC%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22MSVC+Conan%22)
[_![GCC Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/GCC%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22GCC+Conan%22)
[_![Clang Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/Clang%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22Clang+Conan%22)
[ ![Download](https://api.bintray.com/packages/sintef-ocean/conan/ogre3d%3Asintef/images/download.svg) ](https://bintray.com/sintef-ocean/conan/ogre3d%3Asintef/_latestVersion)


The recipe generates library packages, which can be found at [Bintray](https://bintray.com/sintef-ocean/conan/ogre3d%3Asintef/_latestVersion).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add sintef https://api.bintray.com/conan/sintef-ocean/conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   ogre3d/[>=0.1]@sintef/stable

   [options]

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor i${CONAN_LIBS})
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -b missing -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

| Option            | Allowed values    |   Default value   |
| ----------------- | ----------------- | ----------------- |
| with_cg           | [True, False]     | False             |
| with_boost        | [True, False]     | False             |
| with_poco         | [True, False]     | False             |
| samples           | [True, False]     | False             |
| with_python       | [True, False]     | False             |
| with_csharp       | [True, False]     | False             |
| with_java         | [True, False]     | False             |
| bites             | [True, False]     | False             |
| direct3d9_renderer| [True, False]     | False             |
| opengl_renderer   | [True, False]     | False             |
| opengl3_renderer  | [True, False]     | False             |
| opengles_renderer | [True, False]     | False             |

## Known recipe issues

None
