[app]
title = PavPlay
project_dir = .
input_file = src/main.py
exec_directory = ./dist
project_file = 
icon = /home/harsh/Desktop/Programs/Pav-Play/.venv/lib/python3.12/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[python]
python_path = /home/harsh/Desktop/Programs/Pav-Play/.venv/bin/python3
packages = Nuitka==4.2.1,ordered_set,zstandard

[qt]
qml_files = 
excluded_qml_plugins = 
modules = Concurrent,Core,DBus,Gui,Multimedia,MultimediaWidgets,Network,Widgets
plugins = accessiblebridge,egldeviceintegrations,generic,iconengines,imageformats,multimedia,networkaccess,networkinformation,platforminputcontexts,platforms,platforms/darwin,platformthemes,styles,tls,wayland-decoration-client,wayland-graphics-integration-client,wayland-shell-integration,xcbglintegrations

[nuitka]
mode = onefile
extra_args = --include-data-dir=assets=assets --linux-onefile-icon=assets/nav/appicon.png --product-name=PavPlay --file-description=Pav Play media player

