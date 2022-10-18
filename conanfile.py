from conans import ConanFile, CMake, tools


class Ogre3dConan(ConanFile):
    name = "ogre3d"
    license = "MIT"
    # version = "13.4.0"  # uncomment to "enable package development flow"
    author = "SINTEF Ocean"
    url = "https://github.com/sintef-ocean/conan-ogre3d"
    description = "3D graphics rendering engine"
    topics = ("graphics", "3D rendering", "3D", "ogre3d")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ['patches/*']
    generators = ("cmake", "cmake_find_package")
    _cmake = None

    options = {
        "with_freetype": [True, False],
        "with_sdl": [True, False],
        "with_qt": [True, False],
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
        "build_tests": [True, False],
        }

    default_options = {
        "with_freetype": False,
        "with_sdl": False,
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
        "rendersystem_vulkan": True,
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
        "build_tests": False,
        }

    def requirements(self):
        deps = self.conan_data["dependencies"][self.version]
        if self.options.install_tools:
            self.requires(f"pugixml/{deps['pugixml']}")
        if self.options.with_sdl:
            self.requires(f"sdl/{deps['sdl']}", private=True)
        if self.options.with_qt:
            self.output.warn("Qt dependency handling may not work")
            # Qt 6 not working on linux, but when it do: remember to set correct QT_VERSION_MAJOR in patch
            self.requires(f"qt/{deps['qt']}", private=True)
        if self.options.rendersystem_opengl:
            self.requires(f"opengl/{deps['opengl']}")
            if self.settings.os != "Windows":
                self.requires(f"egl/{deps['egl']}")
        if self.options.rendersystem_opengl3:
            self.requires(f"opengl/{deps['opengl']}")
            if self.settings.os != "Windows":
                self.requires(f"egl/{deps['egl']}")
        if self.options.rendersystem_opengles:
            self.output.warn("OpenGL ES requirement not handled by conan")
            # debian: libgles2-mesa-dev
            if self.settings.os != "Windows":
                self.requires(f"egl/{deps['egl']}")
        if self.options.rendersystem_tiny and self.settings.os != "Windows":
            self.requires(f"llvm-openmp/{deps['llvm-openmp']}", private=True)
        if self.options.rendersystem_vulkan:
            self.requires(f"vulkan-loader/{deps['vulkan-loader']}", private=True)

        if self.options.plugin_assimp:
            self.requires(f"assimp/{deps['assimp']}", private=False)
        if self.options.plugin_exrcodec:
            self.requires(f"openexr/{deps['openexr']}", private=False)
        if self.options.plugin_freeimage:
            self.requires(f"freeimage/{deps['freeimage']}", private=False)
        if self.options.with_freetype:
            self.requires(f"freetype/{deps['freetype']}", private=True)
        if self.options.plugin_glslang:
            self.requires(f"glslang/{deps['glslang']}", private=False)

        if self.options.get_safe("component_bullet", False):
            self.requires(f"bullet3/{deps['bullet3']}", private=False)

        if self.settings.os == "Linux":
            self.requires(f"xorg/{deps['xorg']}")  # X11 dependencies

        # with_sdl a conflict arises for zlib..
        if self.options.with_sdl or self.options.plugin_assimp:
            self.requires(f"zlib/{deps['zlib']}", override=True, private=True)

        if self.options.with_qt:
            self.requires(f"openssl/{deps['openssl']}", override=True)
            if self.settings.os == "Linux":
                self.requires(f"xkbcommon/{deps['xkbcommon']}", override=True)

    def build_requirements(self):
        deps = self.conan_data["dependencies"][self.version]
        if self.options.bindings_csharp or self.options.bindings_java \
           or self.options.bindings_python:
            self.tool_requires(f"swig/{deps['swig']}")

        if self.options.build_tests:
            self.tool_requires(f"gtest/{deps['gtest']}")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.rendersystem_direct3d9
            del self.options.rendersystem_direct3d11
        if tools.Version(self.version) < "13.4.0":
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

        if self.options.install_samples:
            if not self.options.with_qt or not self.options.with_sdl:
                self.output.info("Samples requires with_qt or with_sdl, selecting with_sdl=True")
                self.options.with_sdl = True

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            defs = dict()

            defs['CMAKE_POSITION_INDEPENDENT_CODE'] = True
            defs["OGRE_BUILD_DEPENDENCIES"] = False  # Use conan libs instead
            defs["OGRE_COPY_DEPENDENCIES"] = False
            defs["OGRE_INSTALL_DEPENDENCIES"] = False
            defs["CMAKE_INSTALL_RPATH"] = "$ORIGIN;$ORIGIN/OGRE"  # subject to change
            defs["OGRE_WITH_FREETYPE"] = self.options.with_freetype
            defs["OGRE_WITH_QT"] = self.options.with_qt
            # defs["OGRE_WITH_SDL"] = self.options.with_sdl # Todo: include this

            renderers = "OGRE_BUILD_RENDERSYSTEM"
            if self.settings.os == "Windows":
                defs[f"{renderers}_D3D9"] = self.options.rendersystem_direct3d9
                defs[f"{renderers}_D3D11"] = self.options.rendersystem_direct3d11
            defs[f"{renderers}_GL"] = self.options.rendersystem_opengl
            defs[f"{renderers}_GL3PLUS"] = self.options.rendersystem_opengl3
            defs[f"{renderers}_GLES2"] = self.options.rendersystem_opengles
            defs[f"{renderers}_TINY"] = self.options.rendersystem_tiny
            defs[f"{renderers}_VULKAN"] = self.options.rendersystem_vulkan
            defs[f"{renderers}_METAL"] = self.options.rendersystem_metal

            plugins = "OGRE_BUILD_PLUGIN"
            defs[f"{plugins}_CG"] = False
            defs[f"{plugins}_ASSIMP"] = self.options.plugin_assimp
            defs[f"{plugins}_BSP"] = self.options.plugin_bsp
            defs[f"{plugins}_DOT_SCENE"] = self.options.plugin_dotscene
            defs[f"{plugins}_EXRCODEC"] = self.options.plugin_exrcodec
            defs[f"{plugins}_FREEIMAGE"] = self.options.plugin_freeimage
            defs[f"{plugins}_GLSLANG"] = self.options.plugin_glslang
            defs[f"{plugins}_OCTREE"] = self.options.plugin_octree
            defs[f"{plugins}_PCZ"] = self.options.plugin_pcz
            defs[f"{plugins}_PFX"] = self.options.plugin_particlefx
            defs[f"{plugins}_STBI"] = self.options.plugin_stbi

            comp = "OGRE_BUILD_COMPONENT"
            defs[f"{comp}_CSHARP"] = self.options.bindings_csharp
            defs[f"{comp}_JAVA"] = self.options.bindings_java
            defs[f"{comp}_PYTHON"] = self.options.bindings_python
            defs[f"{comp}_BITES"] = self.options.component_bites
            defs[f"{comp}_MESHLODGENERATOR"] = self.options.component_meshlodgenerator
            defs[f"{comp}_OVERLAY"] = self.options.component_overlay
            defs[f"{comp}_OVERLAY_IMGUI"] = self.options.component_overlay_imgui
            defs[f"{comp}_PAGING"] = self.options.component_paging
            defs[f"{comp}_PROPERTY"] = self.options.component_property
            defs[f"{comp}_RTSHADERSYSTEM"] = self.options.component_rtshadersystem
            defs[f"{comp}_TERRAIN"] = self.options.component_terrain
            defs[f"{comp}_VOLUME"] = self.options.component_volume
            if tools.Version(self.version) >= "13.4.0":
                defs[f"{comp}_BULLET"] = self.options.component_bullet

            defs["OGRE_BUILD_RTSHADERSYSTEM_SHADERS"] = \
                self.options.component_rtshadersystem

            defs["OGRE_BUILD_SAMPLES"] = self.options.install_samples
            defs["OGRE_INSTALL_SAMPLES"] = self.options.install_samples
            defs["OGRE_BUILD_TOOLS"] = self.options.install_tools
            defs["OGRE_INSTALL_TOOLS"] = self.options.install_tools

            defs["OGRE_CONFIG_DOUBLE"] = self.options.enable_double
            defs["OGRE_CONFIG_NODE_INHERIT_TRANSFORM"] = \
                self.options.enable_node_inherit_transform

            config = "OGRE_CONFIG_ENABLE"
            defs[f"{config}_ASTC"] = self.options.enable_astc
            defs[f"{config}_DDS"] = self.options.enable_dds
            defs[f"{config}_ETC"] = self.options.enable_etc
            defs[f"{config}_GL_STATE_CACHE_SUPPORT"] = \
                self.options.enable_gl_state_cache_support
            defs[f"{config}_GLES2_GLSL_OPTIMISER"] = \
                self.options.enable_gles2_glsl_optimiser
            defs[f"{config}_MESHLOD"] = self.options.enable_meshlod
            defs[f"{config}_PVRTC"] = self.options.enable_pvrtc
            defs[f"{config}_QUAD_BUFFER_STEREO"] = \
                self.options.enable_quad_buffer_stereo
            defs[f"{config}_VIEWPORT_ORIENTATIONMODE"] = \
                self.options.enable_viewport_orientationmode
            defs[f"{config}_ZIP"] = self.options.enable_zip

            defs["OGRE_BUILD_TESTS"] = self.options.build_tests

            self._cmake.definitions.update(defs)
            self._cmake.configure(source_folder=self._source_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("LICENSE*", dst="licenses", src=self._source_subfolder,
                  ignore_case=True, keep_path=True)

    def package_info(self):
        self.cpp_info.name = 'Ogre3D'
        libdirs = ['lib']
        if self.settings.os == "Windows": # For Windows, static plugin, codec, and render system libraries are in bin-folder
            libdirs.append('bin')
        self.cpp_info.libdirs = libdirs
        libs = ["OgreMain"]

        # TODO: support components and closer mirror Ogre's cmake configure script
        self.cpp_info.includedirs.append("include/OGRE")
        self.cpp_info.includedirs.append("include/OGRE/Threading")

        include = "include/OGRE"
        if self.options.component_bites:
            self.cpp_info.includedirs.append(f"{include}/Bites")
            libs.append("OgreBites")
            if self.options.with_qt:
                libs.append("OgreBitesQt")

        if self.options.get_safe("component_bullet", False):
            self.cpp_info.includedirs.append(f"{include}/Bullet")
            libs.append("OgreBullet")
        if self.options.component_meshlodgenerator:
            self.cpp_info.includedirs.append(f"{include}/MeshLodGenerator")
            libs.append("OgreMeshLodGenerator")
        if self.options.component_overlay:
            self.cpp_info.includedirs.append(f"{include}/Overlay")
            libs.append("OgreOverlay")
        if self.options.component_overlay_imgui:
            self.cpp_info.defines.append("IMGUI_DISABLE_OBSOLETE_KEYIO")
        if self.options.component_paging:
            self.cpp_info.includedirs.append(f"{include}/Paging")
            libs.append("OgrePaging")
        if self.options.component_property:
            self.cpp_info.includedirs.append(f"{include}/Property")
            libs.append("OgreProperty")
        if self.options.component_rtshadersystem:
            self.cpp_info.includedirs.append(f"{include}/RTShaderSystem")
            libs.append("OgreRTShaderSystem")
        if self.options.component_terrain:
            self.cpp_info.includedirs.append(f"{include}/Terrain")
            libs.append("OgreTerrain")
        if self.options.component_volume:
            self.cpp_info.includedirs.append(f"{include}/Volume")
            libs.append("OgreVolume")

        include_RS = "include/OGRE/RenderSystems"
        if self.settings.os == "Windows":
            if self.options.rendersystem_direct3d9:
                self.cpp_info.includedirs.append(f"{include_RS}/Direct3D9")
                libs.append("RenderSystem_Direct3D9")
            if self.options.rendersystem_direct3d11:
                self.cpp_info.includedirs.append(f"{include_RS}/Direct3D11")
                libs.append("RenderSystem_Direct3D11")
        if self.options.rendersystem_opengl:
            self.cpp_info.includedirs.append(f"{include_RS}/GL")
            self.cpp_info.includedirs.append(f"{include_RS}/GL/GL")
            if self.settings.os == "Windows": 
                libs.append("RenderSystem_GL")
        if self.options.rendersystem_opengl3:
            self.cpp_info.includedirs.append(f"{include_RS}/GL3Plus")
            if self.settings.os == "Windows": 
                libs.append("RenderSystem_GL3Plus")
        if self.options.rendersystem_opengles:
            self.cpp_info.includedirs.append(f"{include_RS}/GLES2")
            if self.settings.os == "Windows": 
                libs.append("RenderSystem_GLES2")
        if self.options.rendersystem_vulkan:
            self.cpp_info.includedirs.append(f"{include_RS}/Vulkan")
            if self.settings.os == "Windows": 
                libs.append("RenderSystem_Vulkan")

        include_P = "include/OGRE/Plugins"
        if self.options.plugin_assimp:
            self.cpp_info.includedirs.append(f"{include_P}/Assimp")
            if self.settings.os == "Windows": 
                libs.append("Codec_Assimp")
        if self.options.plugin_bsp:
            self.cpp_info.includedirs.append(f"{include_P}/BSPSceneManager")
            if self.settings.os == "Windows": 
                libs.append("Plugin_BSPSceneManager")
        if self.options.plugin_dotscene:
            self.cpp_info.includedirs.append(f"{include_P}/DotScene")
            if self.settings.os == "Windows": 
                libs.append("Codec_EXR")
        if self.options.plugin_exrcodec:
            self.cpp_info.includedirs.append(f"{include_P}/EXRCodec")
            if self.settings.os == "Windows": 
                libs.append("Codec_EXR")
        if self.options.plugin_freeimage:
            self.cpp_info.includedirs.append(f"{include_P}/FreeImageCodec")
            if self.settings.os == "Windows": 
                libs.append("Codec_FreeImage")
        if self.options.plugin_glslang:
            self.cpp_info.includedirs.append(f"{include_P}/GLSLang")
            if self.settings.os == "Windows": 
                libs.append("Plugin_GLSLang")
        if self.options.plugin_octree:
            self.cpp_info.includedirs.append(f"{include_P}/OctreeSceneManager")
            self.cpp_info.includedirs.append(f"{include_P}/OctreeZone")
            if self.settings.os == "Windows": 
                libs.append("Plugin_OctreeSceneManager")
                libs.append("Plugin_OctreeZone")
        if self.options.plugin_pcz:
            self.cpp_info.includedirs.append(f"{include_P}/PCZSceneManager")
            if self.settings.os == "Windows": 
                libs.append("Plugin_PCZSceneManager")
        if self.options.plugin_particlefx:
            self.cpp_info.includedirs.append(f"{include_P}/ParticleFX")
            if self.settings.os == "Windows": 
                libs.append("Plugin_ParticleFX")
        if self.options.plugin_stbi:
            self.cpp_info.includedirs.append(f"{include_P}/STBICodec")
            if self.settings.os == "Windows": 
                libs.append("Codec_STBI")

        if self.settings.compiler == "Visual Studio" \
           and self.settings.build_type == "Debug":
            self.cpp_info.libs = [lib + "_d" for lib in libs]
        else:
            self.cpp_info.libs = libs
