# one-time script to update individual sources based on index.json

from fibsem_metadata.models.index import DatasetIndex
import os
from glob import glob


def main():
    metadata_dir = "/home/dvb/dev/fibsem-metadata/metadata/datasets"
    datasets = glob(metadata_dir + "/*")
    for dataset in datasets:
        try:
            update_sources(metadata_dir, dataset=dataset)
        except:
            print(f"Something went wrong processing {dataset}")


def update_sources(metadata_dir, dataset):
    index_fname = os.path.join(metadata_dir, dataset, "index.json")
    sources_dir = os.path.join(metadata_dir, dataset, "sources")
    index = DatasetIndex.parse_file(index_fname)
    results = []
    for index_source in index.volumes:
        with open(os.path.join(sources_dir, f"{index_source.name}.json"), "w") as fh:
            fh.write(index_source.json(indent=2))
        results.append(True)
    return results


if __name__ == "__main__":
    main()
