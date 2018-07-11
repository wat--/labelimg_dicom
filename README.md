# LabelImg

Forked from [labelImg](https://github.com/tzutalin/labelImg/blob/master/labelImg.py), updated to work with DICOMs.


## Installation


### Mac OS X

```text
brew install qt  # will install qt-5.x.x
brew install libxml2
make qt5py3
python labelImg.py
python  labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
```

### Linux (Ubuntu)

```text
sudo apt-get install pyqt5-dev-tools
sudo pip3 install lxml
make qt5py3
python3 labelImg.py
python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
```

### Windows

Download and install [Anaconda](https://www.anaconda.com/download/#download).

Open the Anaconda Prompt and go to the `labelImg` directory.

```text
conda install pyqt=5
pyrcc5 -o resources.py resources.qrc
python labelImg.py
python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
```


## Usage

### Annotate

1. Build and launch using the instructions above.
2. Click 'Change default saved annotation folder' in Menu/File
3. Click 'Open Dir'
4. Click 'Create RectBox'
5. Click and release left mouse to select a region to annotate the rect
   box
6. You can use right mouse to drag the rect box to copy or move it

The annotation will be saved to the folder you specify.

Make sure PascalVOC (not YOLO) is selected in the toolbar on the left-hand side.

You can refer to the below hotkeys to speed up your workflow.


### Create pre-defined classes

You can edit the
`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__
to load pre-defined classes

### Keyboard Shortcuts

| Keys      | Description                              |
|-----------|------------------------------------------|
| `cmd + u` | Load all of the images from a directory  |
| `cmd + r` | Change the default annotation target dir |
| `cmd + s` | Save                                     |
| `cmd + d` | Copy the current label and rect box      |
| `space`   | Flag the current image as verified       |
| `w`       | Create a rect box                        |
| `d`       | Next image                               |
| `a`       | Previous image                           |
| `del`     | Delete the selected rect box             |
| `cmd + +` | Zoom in                                  |
| `cmd + -` | Zoom out                                 |
| `↑→↓←`    | Move selected rect box                  |


## License

Free software: [MIT license](https://github.com/tzutalin/labelImg/blob/master/LICENSE)

Citation: Tzutalin. LabelImg. Git code (2015). https://github.com/tzutalin/labelImg
