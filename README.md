[_![MSVC Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/MSVC%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22MSVC+Conan%22)
[_![GCC Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/GCC%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22GCC+Conan%22)
[_![Clang Conan](https://github.com/sintef-ocean/conan-ogre3d/workflows/Clang%20Conan/badge.svg)_](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A%22Clang+Conan%22)

[Conan.io](https://conan.io) recipe for [Ogre3D](https://www.ogre3d.org).

The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/en/latest/reference/commands/misc/remote.html?highlight=remotes):

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local # only for freeimage [discouraged]
   $ conan config set general.revisions_enabled=1
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project.
   This file describes dependencies and your configuration of choice.
   The example below shows an example with imports only for linux:

   ```
   [requires]
   ogre3d/[~13.4.0]@sintef/stable

   [options]
   ogre3d:with_sdl=True
   ogre3d:install_samples=True

   [imports]
   licenses, * -> ./licenses @ folder=True
   bin, * -> ./bin @ root_package=ogre3d
   lib, *.so* -> ./lib @ root_package=ogre3d
   share, * -> ./share @ root_package=ogre3d

   [generators]
   cmake_paths
   cmake_find_package
   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(Ogre3D MODULE REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor Ogre3D::Ogre3D)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -b missing -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and
   compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package components

We have added support for components using `cmake` and `cmake_find_package`
generators. The following tqargets are available [EXPERIMENTAL]:

 - `Ogre3D::Ogre3D` - Depends on all components below
 - `Ogre3D::Components` - All built component libraries, including core libraries
 - `Ogre3D::Plugins` - All built plugin and codec libraries, depends on `Ogre3D::Components`
 - `Ogre3D::RenderSystems` - All built rendersystem libraries, depends on `Ogre::Components`

 Typically, you only need to link `Ogre3D::Components`, but if you include headers from
 any of the other features in you code, you need to link the corresponding targets.


## Package options

| Option                          | Allowed values | Default |
|---------------------------------|----------------|---------|
| with_freetype                   | [True, False]  | False   |
| with_sdl                        | [True, False]  | True    |
| with_qt5                        | [True, False]  | False*  |
| with_qt6                        | [True, False]  | False*  |
| install_samples                 | [True, False]  | False   |
| install_tools                   | [True, False]  | True    |
| bindings_csharp                 | [True, False]  | False   |
| bindings_java                   | [True, False]  | False   |
| bindings_python                 | [True, False]  | False   |
| rendersystem_direct3d11         | [True, False]  | True    |
| rendersystem_direct3d9          | [True, False]  | False   |
| rendersystem_metal              | [True, False]  | False   |
| rendersystem_opengl             | [True, False]  | False   |
| rendersystem_opengl3            | [True, False]  | True    |
| rendersystem_opengles           | [True, False]  | False   |
| rendersystem_tiny               | [True, False]  | False   |
| rendersystem_vulkan             | [True, False]  | True    |
| plugin_assimp                   | [True, False]  | True    |
| plugin_bsp                      | [True, False]  | True    |
| plugin_dotscene                 | [True, False]  | True    |
| plugin_exrcodec                 | [True, False]  | True    |
| plugin_freeimage                | [True, False]  | False   |
| plugin_glslang                  | [True, False]  | True    |
| plugin_octree                   | [True, False]  | True    |
| plugin_particlefx               | [True, False]  | True    |
| plugin_pcz                      | [True, False]  | True    |
| plugin_stbi                     | [True, False]  | True    |
| component_bites                 | [True, False]  | True    |
| component_bullet                | [True, False]  | True    |
| component_meshlodgenerator      | [True, False]  | True    |
| component_overlay               | [True, False]  | True    |
| component_overlay_imgui         | [True, False]  | True    |
| component_paging                | [True, False]  | True    |
| component_property              | [True, False]  | True    |
| component_rtshadersystem        | [True, False]  | True    |
| component_terrain               | [True, False]  | True    |
| component_volume                | [True, False]  | True    |
| enable_astc                     | [True, False]  | True    |
| enable_dds                      | [True, False]  | True    |
| enable_double                   | [True, False]  | False   |
| enable_etc                      | [True, False]  | True    |
| enable_gl_state_cache_support   | [True, False]  | False   |
| enable_gles2_glsl_optimiser     | [True, False]  | False   |
| enable_meshlod                  | [True, False]  | True    |
| enable_node_inherit_transform   | [True, False]  | False   |
| enable_pvrtc                    | [True, False]  | False   |
| enable_quad_buffer_stereo       | [True, False]  | False   |
| enable_viewport_orientationmode | [True, False]  | False   |
| enable_zip                      | [True, False]  | True    |
| build_tests                     | [True, False]  | False   |
|---------------------------------|----------------|---------|
| * Select with_qt5 OR with_qt6   |                |         |

## Known recipe issues

  The recipe is only tested on Windows and Linux. It will probably not work for Emscripten
  and Android and other platforms.
  - Some disabled features may detect system-installed requirements and enabled even if they are specified to be disabled in the recipe
    - This may cause downstream issues if you create a library which requires ogre3d.
  - OpenGL ES dependencies are not handled by the recipe. The need to be system installed

## Non-exposed Ogre configuration

  The conan recipe does not expose all options of the Ogre build script. The following
  variables currently use their default values as defined by the Ogre build system.
  ```
    OGRE_BUILD_MSVC_MP
    OGRE_BUILD_MSVC_ZM
    OGRE_CONFIG_STATIC_LINK_CRT
    OGRE_INSTALL_VSPROPS
    OGRE_STATIC
    OGRE_RESOURCEMANAGER_STRICT
    OGRE_NODELESS_POSITIONING
    OGRE_BUILD_PLUGIN_CG
    OGRE_CONFIG_THREADS
    OGRE_CONFIG_THREAD_PROVIDER
    OGRE_PROFILING
    OGRE_CONFIG_FILESYSTEM_UNICODE
    OGRE_INSTALL_PDB
    OGRE_BUILD_LIBS_AS_FRAMEWORKS
    OGRE_BITES_STATIC_PLUGINS
    OGRE_INSTALL_DOCS
    OGRE_BUILD_XSIEXPORTER
    OGRE_BUILD_RENDERSYSTEM_METAL
    OGRE_CONFIG_ENABLE_TBB_SCHEDULER
    OGRE_CONFIG_ENABLE_GLES2_CG_SUPPORT
  ```

## Developer Notes

  Procedure for making patch files for conanization and other fixes:
    - Clone the Ogre git repository and checkout the tagged release branch
    - Do necessary changes and create commit(s)
    - Create the patches using `git format-patch -1 --no-renames -o ../patches/`
    - The flag `-1` should coincide with the number of commits to create patch files of
    - Each patch name should be prepended with the version for which it is intended
    - Add each patch to the list of patches in `conandata.yml`
    - To add more patches to a release, you should first apply the existing patches and
      then add your fixes as additional commits.
