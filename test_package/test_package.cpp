#include <memory>
#include "OGRE/OgreRoot.h"
#ifdef TEST_IMGUI
#include <cstring>
#include <imgui.h>
#include <imgui_internal.h>
#endif

int main()
{
	Ogre::String empty1, empty2, log("log.log");
	std::unique_ptr<Ogre::Root> root = std::make_unique<Ogre::Root>(empty1, empty2, log);
#ifdef TEST_IMGUI
	// ImGui is exported by OgreOverlay
	if (std::strcmp(ImGui::GetVersion(), IMGUI_VERSION) != 0)
		return 1;
#endif
	return 0;
}
