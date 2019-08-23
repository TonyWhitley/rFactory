echo git bash commands to load submodules
rem git submodule add https://github.com/TonyWhitley/ScriptedJsonEditor
rem git submodule add https://github.com/TonyWhitley/rF2_serverNotify
rem git submodule add https://github.com/TonyWhitley/rF2headlights
rem git submodule add https://github.com/TonyWhitley/gearbox

pushd rF2headlights
rem rmdir --ignore-fail-on-non-empty pyDirectInputKeySend
git submodule add -f https://github.com/TonyWhitley/pyDirectInputKeySend                                                 
rmdir --ignore-fail-on-non-empty pyRfactor2SharedMemory
rem git submodule add -f https://github.com/TonyWhitley/pyRfactor2SharedMemory                               
popd

pushd gearbox
git submodule add https://github.com/TonyWhitley/pyDirectInputKeySend                                                 
rmdir --ignore-fail-on-non-empty pyRfactor2SharedMemory
git submodule add https://github.com/TonyWhitley/pyRfactor2SharedMemory                                                  
popd

