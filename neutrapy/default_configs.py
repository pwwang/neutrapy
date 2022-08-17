NEU_CONFIG = {
  "applicationId": "js.neutralino.sample",
  "version": "1.0.0",
  "defaultMode": "window",
  "port": 0,
  "documentRoot": "/resources/",
  "url": "/",
  "enableNativeAPI": True,
  "enableExtensions": True,
  "exportAuthInfo": True,
  "tokenSecurity": "one-time",
  "logging": {
    "enabled": True,
    "writeToLogFile": True
  },
  "nativeAllowList": [
    "app.*",
    "os.*",
    "extensions.*",
    "debug.log"
  ],
  "globalVariables": {},
  "modes": {
    "window": {
      "title": "Neu_Python_Extension",
      "width": 800,
      "height": 500,
      "minWidth": 400,
      "minHeight": 200,
      "fullScreen": False,
      "alwaysOnTop": False,
      "icon": "/resources/icons/appIcon.png",
      "enableInspector": False,
      "borderless": False,
      "maximize": False,
      "hidden": False,
      "resizable": True,
      "exitProcessOnClose": False
    },
    "browser": {},
    "cloud": {},
    "chrome": {}
  },
  "cli": {
    "binaryName": "Neu_Python_Extension",
    "resourcesPath": "/resources/",
    "extensionsPath": "/extensions/",
    "clientLibrary": "/resources/js/neutralino.js",
    "binaryVersion": "4.4.0",
    "clientVersion": "3.3.0"
  },
  "extensions": [
      {
          "id": "js.neutralino.sample.my_python_extension",
          "command": "python extensions/my_python_extension/main.py"
      }
  ]
}
