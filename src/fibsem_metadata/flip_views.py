# flip views to compensate for flipped raw data

from pathlib import Path
from fibsem_tools.io import read
import os
from fibsem_metadata.models.index import DatasetViewCollection, DatasetView

bucket = "s3://janelia-cosem-datasets"
flip_axis = "y"
path = "/home/dvb/dev/fibsem-metadata/metadata/datasets/jrc_hela-2"
if __name__ == "__main__":
    dataset_name = Path(path).name
    views_file = Path(path) / "views.json"
    s3_path = os.path.join(
        bucket, dataset_name, f"{dataset_name}.n5", "em", "fibsem-uint16", "s0"
    )
    dataset = read(s3_path)
    y_extent = dataset.attrs["transform"]["scale"][1] * dataset.shape[1]

    old_views = DatasetViewCollection.parse_file(views_file)
    new_views = old_views.copy()
    new_views.views = []

    for v in old_views.views:
        new_view = v.dict()
        if v.position is not None:
            new_position = [v.position[0], y_extent - v.position[1], v.position[2]]
            new_view["position"] = new_position
        new_views.views.append(DatasetView(**new_view))

    with open(views_file, "w") as fh:
        fh.write(new_views.json(indent=2))
