# LabelImg

Forked from the
[LabelImg](https://github.com/tzutalin/labelImg/blob/master/labelImg.py)
repo by [tzutalin](https://github.com/tzutalin).
Updated to work with DICOMs.


## Installation

### Mac OS X and Linux (Ubuntu 16.04)

1. Make sure you have [Anaconda](https://www.anaconda.com/download/#download) or
[Miniconda](https://conda.io/miniconda.html) installed.
2. Clone this repo and `cd` into the top-level folder.
3. Run the following
    ```text
    conda env create -f environment.yml
    conda activate label-img
    make qt4py2
    python labelImg.py
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

You can edit the file in `data/predefined_classes.txt` to define your own
classes.


### Keyboard Shortcuts

| Keys        | Description                              |
|-------------|------------------------------------------|
| `cmd + u`   | Load all of the images from a directory  |
| `cmd + r`   | Change the default annotation target dir |
| `cmd + s`   | Save                                     |
| `cmd + d`   | Copy the current label and bounding box  |
| `space`     | Flag the current image as verified       |
| `w`         | Create a bounding box                    |
| `d`         | Next image                               |
| `a`         | Previous image                           |
| `del`       | Delete the selected bounding box         |
| `cmd + '+'` | Zoom in                                  |
| `cmd + '-'` | Zoom out                                 |
| `↑ → ↓ ←`  | Move selected bounding box               |


## License

Free software: [MIT license](https://github.com/tzutalin/labelImg/blob/master/LICENSE)

Citation: Tzutalin. LabelImg. Git code (2015). https://github.com/tzutalin/labelImg
