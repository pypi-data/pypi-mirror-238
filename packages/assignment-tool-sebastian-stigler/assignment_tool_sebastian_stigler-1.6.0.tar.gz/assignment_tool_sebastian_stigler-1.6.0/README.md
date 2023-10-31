# Assignment Tool

This tool is used to lead students through the assignments of the 
"Strukturierte Programmierung" course at Aalen Univerity.

# Installation Guid

Install OS dependencies (for Ubuntu 20.04), create a virtual env and activate it:

```bash
$ sudo -i 
# apt install python3.8-venv python3-wheel
# python3.8 -m venv /opt/assignment_tool_venv
# source /opt/assignment_tool_venv/bin/activate
```

Then install Kivy-Garden (0.1.4) without building a wheel, as it can't build a wheel.

```bash
(assignment_tool_venv)# pip install kivy-garden==0.1.4 --no-binary :all:
```

Now you can install the actual package

```bash
(assignment_tool_venv)# pip install assignment-tool-sebastian-stigler
```

Finally, you create a `assignment_tool.desktop` file (adapt the `Exec` and `Icon` path if your
virtual env has a different name).

```ini
[Desktop Entry]
Version=1.0
Name=Assignment Tool
Exec=/opt/assignment_tool_venv/bin/assignment_tool
Icon=/opt/assignment_tool_venv/lib/python3.8/site-packages/assignment_tool/assets/logo.png
Terminal=false
Type=Application
Categories=TextEditor;Development;IDE;
```

To integrate it into the desktop call:

```bash
# desktop-file-install assignment_tool.desktop
```