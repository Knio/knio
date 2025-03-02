rem Run from repo root, ie ../knio> config\install\install.bat
rem Run from Administrator Command Prompt only (no PS)

mklink "%APPDATA%\Code\User\settings.json" %cd%\config\Code\User\settings.json
mklink "%APPDATA%\Code\User\keybindings.json" %cd%\config\Code\User\keybindings.json

mklink %USERPROFILE%\.gitconfig %cd%\config\dotconfig\git\config

mklink /D C:\Users\Tom\.ssh C:\Users\Tom\Desktop\Files\knio\config\dot\.ssh
