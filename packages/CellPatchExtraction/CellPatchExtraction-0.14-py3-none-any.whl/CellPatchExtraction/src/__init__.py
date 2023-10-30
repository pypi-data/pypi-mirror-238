from pathlib import Path
import os

print(__file__)

TYPES = ('*.tiff', '*.TIF', '*.TIFF', '*.tif')
CELLPOSE_PATH = Path(__file__).resolve().parent.parent / ".cellpose_model"
AVAIL_MODELS = [p.name for p in Path(CELLPOSE_PATH).glob("*")]

print(CELLPOSE_PATH, AVAIL_MODELS)