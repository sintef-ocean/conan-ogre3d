[![Linux GCC](https://github.com/sintef-ocean/conan-ogre3d/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A"Linux+GCC")
[![Linux Clang](https://github.com/sintef-ocean/conan-ogre3d/workflows/Linux%20Clang/badge.svg)](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A"Linux+Clang")
[![Windows MSVC](https://github.com/sintef-ocean/conan-ogre3d/workflows/Windows%20MSVC/badge.svg)](https://github.com/sintef-ocean/conan-ogre3d/actions?query=workflow%3A"Windows+MSVC")

[Conan.io](https://conan.io) recipe for [Ogre3D](https://www.ogre3d.org).

*Note* We are refactoring to support conan v2. The consequence of this is that the recipe
no longer supports old generators such as `cmake_paths` and `cmake_find_package`. Use
`CMakeToolchain` and `CMakeDeps` instead.


## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:
   ```
   [requires]
   ogre3d/[~13.5.0]@sintef/stable

   [options]
   ogre3d:with_sdl=True
   ogre3d:install_samples=True

   [tool_requires]
   cmake/[>=3.25.0]

   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv

   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.15)
   project(TheProject CXX)

   find_package(Ogre3D REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor Ogre3D::Ogre3D)
   ```
   Install and build e.g. a Release configuration (linux):
   ```bash
   $ conan install . -s build_type=Release -pr:b=default
   $ source build/Release/generators/conanbuild.sh
   $ cmake --preset conan-release
   $ cmake --build build/Release
   $ source build/Release/generators/deactivate_conanbuild.sh
   ```

## Package components

We have added support for component targets [EXPERIMENTAL]:

 - `Ogre3D::Ogre3D` - Depends on all components below
 - `Ogre3D::Components` - All built component libraries, including core libraries
 - `Ogre3D::Plugins` - All built plugin and codec libraries, depends on `Ogre3D::Components`
 - `Ogre3D::RenderSystems` - All built rendersystem libraries, depends on `Ogre3D::Components`

 Typically, you only need to link `Ogre3D::Components`, but if you include headers from
 any of the other features in your code, you need to link the corresponding targets.

## Package options

| Option                          | Allowed values    | Default |
|---------------------------------|-------------------|---------|
| with_freetype                   | [True, False]     | False   |
| with_sdl                        | [True, False]     | True    |
| with_qt                         | [False, "5", "6"] | False   |
| install_samples                 | [True, False]     | False   |
| install_tools                   | [True, False]     | True    |
| bindings_csharp                 | [True, False]     | False   |
| bindings_java                   | [True, False]     | False   |
| bindings_python                 | [True, False]     | False   |
| rendersystem_direct3d11         | [True, False]     | True    |
| rendersystem_direct3d9          | [True, False]     | False   |
| rendersystem_metal              | [True, False]     | False   |
| rendersystem_opengl             | [True, False]     | False   |
| rendersystem_opengl3            | [True, False]     | True    |
| rendersystem_opengles           | [True, False]     | False   |
| rendersystem_tiny               | [True, False]     | False   |
| rendersystem_vulkan             | [True, False]     | False   |
| plugin_assimp                   | [True, False]     | True    |
| plugin_bsp                      | [True, False]     | True    |
| plugin_dotscene                 | [True, False]     | True    |
| plugin_exrcodec                 | [True, False]     | True    |
| plugin_freeimage                | [True, False]     | False   |
| plugin_glslang                  | [True, False]     | True    |
| plugin_octree                   | [True, False]     | True    |
| plugin_particlefx               | [True, False]     | True    |
| plugin_pcz                      | [True, False]     | True    |
| plugin_stbi                     | [True, False]     | True    |
| plugin_rsimage                  | [True, False]     | False   |
| component_bites                 | [True, False]     | True    |
| component_bullet                | [True, False]     | True    |
| component_meshlodgenerator      | [True, False]     | True    |
| component_overlay               | [True, False]     | True    |
| component_overlay_imgui         | [True, False]     | True    |
| component_paging                | [True, False]     | True    |
| component_property              | [True, False]     | True    |
| component_rtshadersystem        | [True, False]     | True    |
| component_terrain               | [True, False]     | True    |
| component_volume                | [True, False]     | True    |
| enable_astc                     | [True, False]     | True    |
| enable_dds                      | [True, False]     | True    |
| enable_double                   | [True, False]     | False   |
| enable_etc                      | [True, False]     | True    |
| enable_gl_state_cache_support   | [True, False]     | False   |
| enable_gles2_glsl_optimiser     | [True, False]     | False   |
| enable_meshlod                  | [True, False]     | True    |
| enable_node_inherit_transform   | [True, False]     | False   |
| enable_pvrtc                    | [True, False]     | False   |
| enable_quad_buffer_stereo       | [True, False]     | False   |
| enable_viewport_orientationmode | [True, False]     | False   |
| enable_zip                      | [True, False]     | True    |

To build and run tests, set `tools.build:skip_test=False` in `global.conf`, in `[conf]` or
`--conf` as part of `conan install`. *Note:* Since `13.6.4` you need to set option
`install_samples=True` in addition to the default options to actually to build and run
tests. For simplicity, we require this option to be enabled for older versions too.


## Known recipe issues

  The recipe is only tested on Windows and Linux. It will yet not work for Macos,
  Emscripten and Android, or other platforms for that matter.
  - OpenGL ES dependency are system installed for Debian-based linux only
  - Currently, migration to conan v2 causes SWIG to not work: `bindings_*` options are not
    functional yet. A workaround is to install swig on your system and set modify recipe
    by setting `_need_swig(self): return False`

## Non-exposed Ogre configuration

  The conan recipe does not expose all options of the Ogre build script. The following
  variables currently use their default values as defined by the Ogre build system.
  ```
    OGRE_STATIC
    OGRE_PROFILING
    OGRE_RESOURCEMANAGER_STRICT         # Default (2)
    OGRE_NODELESS_POSITIONING           # Deprecated
    OGRE_BITES_STATIC_PLUGINS           # TODO
    OGRE_BUILD_PLUGIN_CG                # Deprecated
    OGRE_BUILD_XSIEXPORTER              # Needs SoftImage (unsupported)
    OGRE_BUILD_RENDERSYSTEM_METAL       # TODO for macos
    OGRE_BUILD_MSVC_MP
    OGRE_BUILD_MSVC_ZM
    OGRE_BUILD_LIBS_AS_FRAMEWORKS
    OGRE_CONFIG_STATIC_LINK_CRT
    OGRE_CONFIG_FILESYSTEM_UNICODE
    OGRE_CONFIG_THREADS                 # Default (3)
    OGRE_CONFIG_THREAD_PROVIDER         # Default (std)
    OGRE_CONFIG_ENABLE_TBB_SCHEDULER
    OGRE_CONFIG_ENABLE_GLES2_CG_SUPPORT
    OGRE_INSTALL_DOCS                   # Forced to false
    OGRE_INSTALL_PDB
    OGRE_INSTALL_VSPROPS
  ```

## Future recipe work:

  The following tasks are on the horizon for this recipe
  - [ ] Allow static build and add option fPIC
  - [ ] Ensure package info to follow native ogre's cmake and pkgconfig find scripts
  - [ ] Add support for Macos, Emscripten, Android, and other platforms
  - [ ] Rename package name to ogre and move to conan center?

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
