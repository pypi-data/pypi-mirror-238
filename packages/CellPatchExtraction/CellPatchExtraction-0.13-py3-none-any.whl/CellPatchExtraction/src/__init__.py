from pathlib import Path


print(__file__)
TYPES = ('*.tiff', '*.TIF', '*.TIFF', '*.tif')
CELLPOSE_PATH = Path(__file__).resolve().parent / ".cellpose_model"
AVAIL_MODELS = [p.name for p in Path(CELLPOSE_PATH).glob("*")]