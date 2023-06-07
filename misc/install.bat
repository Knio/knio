
mklink /H "%APPDATA%\Code\User\settings.json" %cd%\.config\Code\User\settings.json
mklink /H "%APPDATA%\Code\User\keybindings.json" %cd%\.config\Code\User\keybindings.json

mklink %USERPROFILE%\.gitconfig %cd%\.config\git\config


