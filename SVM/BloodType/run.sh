arvados-cwl-runner --name "Grid Search-dask" --api containers grid_search.cwl --script grid_search.py --x_data npy_data/data_encoded_d.npy --y_data npy_data/blood_types.npy
