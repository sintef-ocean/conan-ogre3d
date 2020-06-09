#include <memory>
#include "OGRE/OgreRoot.h"

int main()
{
	Ogre::String empty1, empty2, log("log.log");
	std::unique_ptr<Ogre::Root> root = std::make_unique<Ogre::Root>(empty1, empty2, log);
	return 0;
}
