from os import path

from conan import ConanFile
from conan.tools.scm import Version
from conan.tools.files import get, copy, rmdir
from conan.tools.files import apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.errors import ConanInvalidConfiguration
from conan.tools.microsoft.visual import check_min_vs, is_msvc
from conan.tools.build import check_min_cppstd
from conan.tools.build import can_run
from conan.tools.system.package_manager import Apt

required_conan_version = ">=1.54"


class Ogre3dConan(ConanFile):
    name = "ogre3d"
    license = "MIT"
    author = "SINTEF Ocean"
    url = "https://github.com/sintef-ocean/conan-ogre3d"
    description = "3D graphics rendering engine"
    topics = ("graphics", "3D rendering", "3D", "ogre3d")
    settings = "os", "compiler", "build_type", "arch"
    package_type = "shared-library"

    options = {
        "with_freetype": [True, False],
        "with_sdl": [True, False],
        "with_qt": [False, "5", "6"],
        "install_samples": [True, False],
        "install_tools": [True, False],
        "bindings_csharp": [True, False],
        "bindings_java": [True, False],
        "bindings_python": [True, False],
        "rendersystem_direct3d11": [True, False],
        "rendersystem_direct3d9": [True, False],
        "rendersystem_metal": [True, False],
        "rendersystem_opengl": [True, False],
        "rendersystem_opengl3": [True, False],
        "rendersystem_opengles": [True, False],
        "rendersystem_tiny": [True, False],
        "rendersystem_vulkan": [True, False],
        "plugin_assimp": [True, False],
        "plugin_bsp": [True, False],
        "plugin_dotscene": [True, False],
        "plugin_exrcodec": [True, False],
        "plugin_freeimage": [True, False],
        "plugin_glslang": [True, False],
        "plugin_octree": [True, False],
        "plugin_particlefx": [True, False],
        "plugin_pcz": [True, False],
        "plugin_stbi": [True, False],
        "component_bites": [True, False],
        "component_bullet": [True, False],
        "component_meshlodgenerator": [True, False],
        "component_overlay": [True, False],
        "component_overlay_imgui": [True, False],
        "component_paging": [True, False],
        "component_property": [True, False],
        "component_rtshadersystem": [True, False],
        "component_terrain": [True, False],
        "component_volume": [True, False],
        "enable_astc": [True, False],
        "enable_dds": [True, False],
        "enable_double": [True, False],
        "enable_etc": [True, False],
        "enable_gl_state_cache_support": [True, False],
        "enable_gles2_glsl_optimiser": [True, False],
        "enable_meshlod": [True, False],
        "enable_node_inherit_transform": [True, False],
        "enable_pvrtc": [True, False],
        "enable_quad_buffer_stereo": [True, False],
        "enable_viewport_orientationmode": [True, False],
        "enable_zip": [True, False],
        }

    default_options = {
        "with_freetype": False,
        "with_sdl": True,
        "with_qt": False,
        "install_samples": False,
        "install_tools": True,
        "bindings_csharp": False,
        "bindings_java": False,
        "bindings_python": False,
        "rendersystem_direct3d11": True,
        "rendersystem_direct3d9": False,
        "rendersystem_metal": False,
        "rendersystem_opengl": False,
        "rendersystem_opengl3": True,
        "rendersystem_opengles": False,
        "rendersystem_tiny": False,
        "rendersystem_vulkan": False,
        "plugin_assimp": True,
        "plugin_bsp": True,
        "plugin_dotscene": True,
        "plugin_exrcodec": True,
        "plugin_freeimage": False,
        "plugin_glslang": True,
        "plugin_octree": True,
        "plugin_particlefx": True,
        "plugin_pcz": True,
        "plugin_stbi": True,
        "component_bites": True,
        "component_bullet": True,
        "component_meshlodgenerator": True,
        "component_overlay": True,
        "component_overlay_imgui": True,
        "component_paging": True,
        "component_property": True,
        "component_rtshadersystem": True,
        "component_terrain": True,
        "component_volume": True,
        "enable_astc": True,
        "enable_dds": True,
        "enable_double": False,  # does not work with tiny
        "enable_etc": True,
        "enable_gl_state_cache_support": False,
        "enable_gles2_glsl_optimiser": False,
        "enable_meshlod": True,
        "enable_node_inherit_transform": False,
        "enable_pvrtc": False,
        "enable_quad_buffer_stereo": False,
        "enable_viewport_orientationmode": False,
        "enable_zip": True,
        }

    # the minimum compiler in case of cppstd 17
    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "7",
            "clang": "7",
            "apple-clang": "10",
        }

    @property
    def _build_testing(self):
        # This seems to be the minimal configuration for successfully running tests
        # install_samples for functional resources.cfg since 13.6.
        return (not self.conf.get("tools.build:skip_test",
                                  default=True, check_type=bool)) and \
               self.options.plugin_stbi and \
               self.options.component_bites and \
               self.options.component_overlay and \
               self.options.component_rtshadersystem and \
               self.options.component_meshlodgenerator and \
               self.options.component_volume and \
               self.options.install_samples

    @property
    def _need_swig(self):
        return self.options.bindings_csharp \
            or self.options.bindings_java \
            or self.options.bindings_python

    def _cmake_new_enough(self, required_version):
        try:
            import re
            from io import StringIO
            output = StringIO()
            self.run("cmake --version", output)
            m = re.search(r"cmake version (\d+\.\d+\.\d+)", output.getvalue())
            return Version(m.group(1)) >= required_version
        except:
            return False

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.rendersystem_direct3d9
            del self.options.rendersystem_direct3d11
        if Version(self.version) < "13.4.0":
            del self.options.component_bullet

    def configure(self):
        self.options["freetype"].shared = False
        self.options["assimp"].shared = False
        self.options["pugixml"].shared = False
        self.options["openexr"].shared = False
        self.options["glslang"].shared = False
        self.options["bullet3"].shared = False
        if self.settings.os != "Windows":
            self.options["llvm-openmp"].shared = False
            self.options["llvm-openmp"].fPIC = True

        if self.options.with_qt in ["5", "6"]:
            self.output.warn("Qt required to be shared for now")
            self.options["qt"].shared = True

        if self.options.rendersystem_vulkan:
            self.options["qt"].with_vulkan = True

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        deps = self.conan_data["dependencies"][self.version]
        if self.options.install_tools or self.options.plugin_dotscene:
            self.requires(f"pugixml/{deps['pugixml']}")
        if self.options.with_sdl:
            self.requires(f"sdl/{deps['sdl']}")  # private=True
        if self.options.with_qt in ["5", "6"]:
            self.output.warn("Qt dependency handling may not work")
            if self.options.with_qt == "5":
                self.requires(f"qt/{deps['qt5']}")  # private=False
            else:
                self.requires(f"qt/{deps['qt6']}")  # private=False
        if self.options.rendersystem_opengl or \
           self.options.rendersystem_opengl3:
            self.requires(f"opengl/{deps['opengl']}")
        if (self.options.rendersystem_opengl or
           self.options.rendersystem_opengl3 or
           self.options.rendersystem_opengles) and \
           self.settings.os != "Windows":
            self.requires(f"egl/{deps['egl']}")
        if self.options.rendersystem_opengles:
            self.output.warning("OpenGL ES requirement not handled by conan")
        if self.options.rendersystem_tiny and self.settings.os != "Windows":
            self.requires(f"llvm-openmp/{deps['llvm-openmp']}")  # private=True
        if self.options.rendersystem_vulkan:
            self.requires(f"vulkan-loader/{deps['vulkan-loader']}")

        if self.options.plugin_assimp:
            self.requires(f"assimp/{deps['assimp']}")  # private=False
        if self.options.plugin_exrcodec:
            self.requires(f"openexr/{deps['openexr']}")  # private=False
            # Note: "openexr must be < 3"
        if self.options.plugin_freeimage:
            self.requires(f"freeimage/{deps['freeimage']}")  # private=False
        if self.options.with_freetype:
            self.requires(f"freetype/{deps['freetype']}")  # private=True
        if self.options.plugin_glslang:
            self.requires(f"glslang/{deps['glslang']}")  # private=False
            self.requires(f"spirv-tools/[>=2021.4]")

        if self.options.get_safe("component_bullet", False):
            self.requires(f"bullet3/{deps['bullet3']}")  # private=False

        if self.settings.os == "Linux":
            self.requires(f"xorg/{deps['xorg']}")  # X11 dependencies

        if self.options.with_sdl or self.options.plugin_assimp or \
           self.options.plugin_exrcodec or \
           self.options.plugin_stbi or self.options.plugin_freeimage:
            do_override = not (self.options.plugin_stbi or self.options.plugin_freeimage)
            self.requires(f"zlib/{deps['zlib']}", override=do_override)

        if self.options.with_qt in ["5", "6"]:
            self.requires(f"openssl/{deps['openssl']}", override=True)
        if self.settings.os == "Linux":
            self.requires(f"xkbcommon/{deps['xkbcommon']}", override=True)

        if self.options.plugin_freeimage:

            if self.options.with_qt in ["5", "6"]:
                self.requires(f"libjpeg/{deps['libjpeg']}", override=True)

            if self.options.with_freetype:
                self.requires(f"libpng/{deps['libpng']}", override=True)

    def validate(self):

        if self.settings.os not in ["Windows", "Linux"]:
            # TODO: support macos, emscripten, android, apple_ios
            raise ConanInvalidConfiguration(
                f"Recipe not yet supported for '{self.settings.os}'")

        if Version(self.version) < "13.5.0" and self.options.with_qt == "6":
            raise ConanInvalidConfiguration(
                "'with_qt' cannot be 6 for version less than 13.5.0")

        if self.options.install_samples and \
           self.options.rendersystem_vulkan and \
           not (self.options.with_qt in ["5", "6"] or self.options.with_sdl):
            raise ConanInvalidConfiguration(
                "Enabling both 'install_samples' and 'rendersystem_vulkan' "
                "require you to enable with_qt or with_sdl")

        if self.options.with_qt == "6":
            if self.settings.compiler.cppstd:
                check_min_cppstd(self, 17)
            check_min_vs(self, 191)
            if not is_msvc(self):
                minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
                if minimum_version and Version(self.settings.compiler.version) < minimum_version:
                    raise ConanInvalidConfiguration(
                        f"{self.ref} requires C++{self._min_cppstd}, "
                        "which your compiler does not support."
                    )

    def build_requirements(self):
        deps = self.conan_data["dependencies"][self.version]
        if self._need_swig:
            self.tool_requires(f"swig/{deps['swig']}")

        if self._build_testing:
            self.test_requires(f"gtest/{deps['gtest']}")

        if not self._cmake_new_enough("3.16"):
            self.tool_requires(f"cmake/{deps['cmake']}")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)

        tc.variables['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        tc.variables["OGRE_BUILD_DEPENDENCIES"] = False  # Use conan libs instead
        tc.variables["OGRE_COPY_DEPENDENCIES"] = False
        tc.variables["OGRE_INSTALL_DEPENDENCIES"] = False
        tc.variables["OGRE_INSTALL_DOCS"] = False
        tc.variables["CMAKE_INSTALL_RPATH"] = "$ORIGIN;$ORIGIN/OGRE"  # Subject to change
        tc.variables["OGRE_WITH_FREETYPE"] = self.options.with_freetype
        tc.variables["OGRE_WITH_SDL"] = self.options.with_sdl
        tc.variables["OGRE_WITH_QT"] = self.options.with_qt in ["5", "6"]
        if self.options.with_qt in ["5", "6"]:
            tc.variables["QT_VERSION_MAJOR"] = str(self.options.with_qt)

        renderers = "OGRE_BUILD_RENDERSYSTEM"
        if self.settings.os == "Windows":
            tc.variables[f"{renderers}_D3D9"] = self.options.rendersystem_direct3d9
            tc.variables[f"{renderers}_D3D11"] = self.options.rendersystem_direct3d11
        tc.variables[f"{renderers}_GL"] = self.options.rendersystem_opengl
        tc.variables[f"{renderers}_GL3PLUS"] = self.options.rendersystem_opengl3
        tc.variables[f"{renderers}_GLES2"] = self.options.rendersystem_opengles
        tc.variables[f"{renderers}_TINY"] = self.options.rendersystem_tiny
        tc.variables[f"{renderers}_VULKAN"] = self.options.rendersystem_vulkan
        tc.variables[f"{renderers}_METAL"] = self.options.rendersystem_metal

        plugins = "OGRE_BUILD_PLUGIN"
        tc.variables[f"{plugins}_CG"] = False
        tc.variables[f"{plugins}_ASSIMP"] = self.options.plugin_assimp
        tc.variables[f"{plugins}_BSP"] = self.options.plugin_bsp
        tc.variables[f"{plugins}_DOT_SCENE"] = self.options.plugin_dotscene
        tc.variables[f"{plugins}_EXRCODEC"] = self.options.plugin_exrcodec
        tc.variables[f"{plugins}_FREEIMAGE"] = self.options.plugin_freeimage
        tc.variables[f"{plugins}_GLSLANG"] = self.options.plugin_glslang
        tc.variables[f"{plugins}_OCTREE"] = self.options.plugin_octree
        tc.variables[f"{plugins}_PCZ"] = self.options.plugin_pcz
        tc.variables[f"{plugins}_PFX"] = self.options.plugin_particlefx
        tc.variables[f"{plugins}_STBI"] = self.options.plugin_stbi

        comp = "OGRE_BUILD_COMPONENT"
        tc.variables[f"{comp}_CSHARP"] = self.options.bindings_csharp
        tc.variables[f"{comp}_JAVA"] = self.options.bindings_java
        tc.variables[f"{comp}_PYTHON"] = self.options.bindings_python
        tc.variables[f"{comp}_BITES"] = self.options.component_bites
        tc.variables[f"{comp}_MESHLODGENERATOR"] = self.options.component_meshlodgenerator
        tc.variables[f"{comp}_OVERLAY"] = self.options.component_overlay
        tc.variables[f"{comp}_OVERLAY_IMGUI"] = self.options.component_overlay_imgui
        tc.variables[f"{comp}_PAGING"] = self.options.component_paging
        tc.variables[f"{comp}_PROPERTY"] = self.options.component_property
        tc.variables[f"{comp}_RTSHADERSYSTEM"] = self.options.component_rtshadersystem
        tc.variables[f"{comp}_TERRAIN"] = self.options.component_terrain
        tc.variables[f"{comp}_VOLUME"] = self.options.component_volume
        if Version(self.version) >= "13.4.0":
            tc.variables[f"{comp}_BULLET"] = self.options.component_bullet

        tc.variables["OGRE_BUILD_RTSHADERSYSTEM_SHADERS"] = \
            self.options.component_rtshadersystem

        tc.variables["OGRE_BUILD_SAMPLES"] = self.options.install_samples
        tc.variables["OGRE_INSTALL_SAMPLES"] = self.options.install_samples
        tc.variables["OGRE_BUILD_TOOLS"] = self.options.install_tools
        tc.variables["OGRE_INSTALL_TOOLS"] = self.options.install_tools

        tc.variables["OGRE_CONFIG_DOUBLE"] = self.options.enable_double
        tc.variables["OGRE_CONFIG_NODE_INHERIT_TRANSFORM"] = \
            self.options.enable_node_inherit_transform

        config = "OGRE_CONFIG_ENABLE"
        tc.variables[f"{config}_ASTC"] = self.options.enable_astc
        tc.variables[f"{config}_DDS"] = self.options.enable_dds
        tc.variables[f"{config}_ETC"] = self.options.enable_etc
        tc.variables[f"{config}_GL_STATE_CACHE_SUPPORT"] = \
            self.options.enable_gl_state_cache_support
        tc.variables[f"{config}_GLES2_GLSL_OPTIMISER"] = \
            self.options.enable_gles2_glsl_optimiser
        tc.variables[f"{config}_MESHLOD"] = self.options.enable_meshlod
        tc.variables[f"{config}_PVRTC"] = self.options.enable_pvrtc
        tc.variables[f"{config}_QUAD_BUFFER_STEREO"] = \
            self.options.enable_quad_buffer_stereo
        tc.variables[f"{config}_VIEWPORT_ORIENTATIONMODE"] = \
            self.options.enable_viewport_orientationmode
        tc.variables[f"{config}_ZIP"] = self.options.enable_zip

        tc.variables["OGRE_BUILD_TESTS"] = self._build_testing
        tc.generate()
        deps = CMakeDeps(self)
        if self._build_testing:
            deps.build_context_activated.append("gtest")
        if self._need_swig:
            deps.build_context_activated.append("swig")
        deps.generate()

    def system_requirements(self):
        if self.options.rendersystem_opengles:
            Apt(self).install(["libgles2-mesa-dev"], check=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if self._build_testing and can_run(self):
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE*", src=self.source_folder, dst="licenses",
             ignore_case=True, keep_path=True)

        rmdir(self, path.join(self.package_folder, "CMake"))
        rmdir(self, path.join(self.package_folder, "lib", "OGRE", "cmake"))
        rmdir(self, path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):

        self.cpp_info.set_property("cmake_file_name", "Ogre3D")
        self.cpp_info.set_property("cmake_target_name", "Ogre3D::Ogre3D")
        self.cpp_info.set_property("pkg_config_name", "Ogre3D")

        # TODO: Map out system_libs for windows too. ws2_32?
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("m")
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")

        # TODO: Use same component model as ogre build system (pkgconfig and cmake)
        self.cpp_info.components["components"].set_property("cmake_file_name", "Components")
        self.cpp_info.components["components"].set_property("cmake_target_name", "Ogre3D::Components")
        self.cpp_info.components["plugins"].set_property("cmake_file_name", "Plugins")
        self.cpp_info.components["plugins"].set_property("cmake_target_name", "Ogre3D::Plugins")
        self.cpp_info.components["rendersystems"].set_property("cmake_file_name", "RenderSystems")
        self.cpp_info.components["rendersystems"].set_property("cmake_target_name", "Ogre3D::RenderSystems")

        components = self.cpp_info.components
        comp = components["components"]
        plug = components["plugins"]
        rend = components["rendersystems"]

        if self.options.with_freetype:
            comp.requires.append("freetype::freetype")
        if self.options.component_bullet:
            comp.requires.append("bullet3::bullet3")
        if self.settings.os == "Linux":
            comp.requires.append("xorg::xorg")
        if self.options.with_sdl:
            comp.requires.append("sdl::sdl")
        if self.options.with_qt in ["5", "6"]:
            comp.requires.append("qt::qt")

        if self.options.rendersystem_opengl or self.options.rendersystem_opengl3:
            rend.requires.append("opengl::opengl")
        if (self.options.rendersystem_opengl or
            self.options.rendersystem_opengl3 or
            self.options.rendersystem_opengles) and \
           self.settings.os == "Linux":
            rend.requires.append("egl::egl")
        if self.options.rendersystem_tiny and self.settings.os == "Windows":
            rend.requires.append("llvm-openmpl::llvm-openmpl")
        if self.options.rendersystem_vulkan:
            rend.requires.append("vulkan-loader::vulkan-loader")

        rend.requires.append("components")

        if self.options.plugin_dotscene:
            plug.requires.append("pugixml::pugixml")
        if self.options.plugin_freeimage:
            plug.requires.append("freeimage::freeimage")
        if self.options.plugin_glslang:
            plug.requires.append("glslang::glslang")
            plug.requires.append("spirv-tools::spirv-tools")
        if self.options.plugin_assimp:
            plug.requires.append("assimp::assimp")
        if self.options.plugin_exrcodec:
            plug.requires.append("openexr::openexr")
        if self.options.plugin_stbi or self.options.plugin_freeimage:
            plug.requires.append("zlib::zlib")

        plug.requires.append("components")

        comp.bindirs = ["bin"]
        comp.libdirs = ["lib"]
        comp.libs = ["OgreMain"]

        comp.includedirs = ["include"]
        comp.includedirs.append("include/OGRE")
        comp.includedirs.append("include/OGRE/Threading")

        comp.defines = []

        include = "include/OGRE"

        # Components
        if self.options.component_bites:
            comp.includedirs.append(f"{include}/Bites")
            comp.libs.append("OgreBites")
            if self.options.with_qt in ["5", "6"]:
                comp.libs.append("OgreBitesQt")

        if self.options.get_safe("component_bullet", False):
            comp.includedirs.append(f"{include}/Bullet")
            comp.libs.append("OgreBullet")
        if self.options.component_meshlodgenerator:
            comp.includedirs.append(f"{include}/MeshLodGenerator")
            comp.libs.append("OgreMeshLodGenerator")
        if self.options.component_overlay:
            comp.includedirs.append(f"{include}/Overlay")
            comp.libs.append("OgreOverlay")
        if self.options.component_overlay_imgui:
            comp.defines.append("IMGUI_DISABLE_OBSOLETE_KEYIO")  # not needed?
        if self.options.component_paging:
            comp.includedirs.append(f"{include}/Paging")
            comp.libs.append("OgrePaging")
        if self.options.component_property:
            comp.includedirs.append(f"{include}/Property")
            comp.libs.append("OgreProperty")
        if self.options.component_rtshadersystem:
            comp.includedirs.append(f"{include}/RTShaderSystem")
            comp.libs.append("OgreRTShaderSystem")
        if self.options.component_terrain:
            comp.includedirs.append(f"{include}/Terrain")
            comp.libs.append("OgreTerrain")
        if self.options.component_volume:
            comp.includedirs.append(f"{include}/Volume")
            comp.libs.append("OgreVolume")

        rend.includedirs = []
        rend.libs = []
        if self.settings.os == "Windows":
            rend.libdirs.append("bin")
        elif self.settings.os == "Linux":
            rend.libdirs.append("lib/OGRE")
        # Render systems
        include_RS = "include/OGRE/RenderSystems"
        if self.settings.os == "Windows":
            if self.options.rendersystem_direct3d9:
                rend.includedirs.append(f"{include_RS}/Direct3D9")
                rend.libs.append("RenderSystem_Direct3D9")
            if self.options.rendersystem_direct3d11:
                rend.includedirs.append(f"{include_RS}/Direct3D11")
                rend.libs.append("RenderSystem_Direct3D11")
        if self.options.rendersystem_opengl:
            rend.includedirs.append(f"{include_RS}/GL")
            rend.includedirs.append(f"{include_RS}/GL/GL")
            rend.libs.append("RenderSystem_GL")
        if self.options.rendersystem_opengl3:
            rend.includedirs.append(f"{include_RS}/GL3Plus")
            rend.libs.append("RenderSystem_GL3Plus")
        if self.options.rendersystem_opengles:
            rend.includedirs.append(f"{include_RS}/GLES2")
            rend.libs.append("RenderSystem_GLES2")
        if self.options.rendersystem_vulkan:
            rend.includedirs.append(f"{include_RS}/Vulkan")
            rend.libs.append("RenderSystem_Vulkan")

        plug.includedirs = []
        plug.libs = []
        if self.settings.os == "Windows":
            plug.libdirs.append("bin")
        elif self.settings.os == "Linux":
            plug.libdirs.append("lib/OGRE")

        # Plugins
        include_P = "include/OGRE/Plugins"
        if self.options.plugin_bsp:
            plug.includedirs.append(f"{include_P}/BSPSceneManager")
            plug.libs.append("Plugin_BSPSceneManager")
        if self.options.plugin_dotscene:
            plug.includedirs.append(f"{include_P}/DotScene")
            plug.libs.append("Plugin_DotScene")
        if self.options.plugin_glslang:
            plug.includedirs.append(f"{include_P}/GLSLang")
            plug.libs.append("Plugin_GLSLangProgramManager")
        if self.options.plugin_octree:
            plug.includedirs.append(f"{include_P}/OctreeSceneManager")
            plug.includedirs.append(f"{include_P}/OctreeZone")
            plug.libs.append("Plugin_OctreeSceneManager")
            plug.libs.append("Plugin_OctreeZone")
        if self.options.plugin_pcz:
            plug.includedirs.append(f"{include_P}/PCZSceneManager")
            plug.libs.append("Plugin_PCZSceneManager")
        if self.options.plugin_particlefx:
            plug.includedirs.append(f"{include_P}/ParticleFX")
            plug.libs.append("Plugin_ParticleFX")

        # Codecs (Plugins)
        if self.options.plugin_assimp:
            plug.includedirs.append(f"{include_P}/Assimp")
            plug.libs.append("Codec_Assimp")
        if self.options.plugin_exrcodec:
            plug.includedirs.append(f"{include_P}/EXRCodec")
            plug.libs.append("Codec_EXR")
        if self.options.plugin_freeimage:
            plug.includedirs.append(f"{include_P}/FreeImageCodec")
            plug.libs.append("Codec_FreeImage")
        if self.options.plugin_stbi:
            plug.includedirs.append(f"{include_P}/STBICodec")
            plug.libs.append("Codec_STBI")

        if is_msvc(self) and self.settings.build_type == "Debug":
            comp.libs = [lib + "_d" for lib in comp.libs]
            rend.libs = [lib + "_d" for lib in rend.libs]
            plug.libs = [lib + "_d" for lib in plug.libs]

        if self.settings.compiler in ["gcc", "clang"] \
           and self.settings.os != "Windows":
            rend.libs = [lib + ".so" for lib in rend.libs]
            plug.libs = [lib + ".so" for lib in plug.libs]
