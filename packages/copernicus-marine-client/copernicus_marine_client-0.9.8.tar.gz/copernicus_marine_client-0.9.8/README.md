
<h1 align="center">Copernicus Marine Service client (CLI & Python)</h1>
<div align="center">
  <a href="https://pypi.org/project/copernicus-marine-client/"><img src="https://img.shields.io/pypi/v/copernicus-marine-client.svg?style=flat-square" alt="PyPI" /></a>
  <a href="https://pypi.org/project/copernicus-marine-client/"><img src="https://img.shields.io/pypi/pyversions/copernicus-marine-client.svg?style=flat-square" alt="PyPI Supported Versions" /></a>
  <a href="https://pypi.org/project/copernicus-marine-client/"><img src="https://img.shields.io/badge/platform-windows | linux | macos-lightgrey?style=flat-square" alt="Supported Platforms" /></a>
</div>

![Copernicus Marine Service and Mercator Ocean international logos](https://www.mercator-ocean.eu/wp-content/uploads/2022/05/Cartouche_CMEMS_poisson_MOi.png)

## Features
The `copernicus-marine-client` offers capabilities through both **Command Line Interface (CLI)** and **Python API**:
- **Metadata Information**: List and retrieve metadata information on all variables, datasets, products, and their associated documentation.
- **Subset Datasets**: Subset datasets to extract only the parts of interest, in preferred format, such as Analysis-Ready Cloud-Optimized (ARCO) Zarr or NetCDF file format.
- **Advanced Filters**: Apply simple or advanced filters to get multiple files, in original formats like NetCDF/GeoTIFF, via direct Marine Data Store connections.
- **No Quotas**: Enjoy no quotas, neither on volume size nor bandwidth.

## Installation
For installation, multiple options are available depending on your setup:

### Conda|Mamba
Though no conda package has been created yet, these steps cover the installation in a new isolated environment (safer). Replace conda by mamba if necessary.

- Create the file `copernicus-marine-client-env.yml` that contains:
```yaml
name: cmc
channels:
  - conda-forge
dependencies:
  - pip
  - pip:
    - copernicus-marine-client
```

- Use the terminal or a [Conda|Mamba] Prompt to create the `cmc` environment from the `yml` file:
```bash
conda env create --file copernicus-marine-client-env.yml
```

- Open the new `cmc` environment by running:
```bash
conda activate cmc
```

- Verify that the new `cmc` environment was installed correctly:
```bash
conda env list
```

### Pip
Otherwise, if you already have an environment (safer to clone it), the package can be installed using the `pip` command:
```bash
python -m pip install copernicus-marine-client
```

And to **upgrade the package** to the newest available version, run:
```bash
python -m pip install copernicus-marine-client --upgrade
```

## User Guide
For more comprehensive details on how to use the `copernicus-marine-client`, please refer to our [Help Center](https://help.marine.copernicus.eu/en/collections/4060068-copernicus-marine-client). It ensures a smooth migration for existing users of legacy services such as MOTU, OPeNDAP, and FTP.

## Command Line Interface (CLI)

### The `--help` option
To discover commands and their available options, consider appending `--help` on any command line.

Example:
```bash
copernicus-marine --help
```
Returns:
```bash
Usage: copernicus-marine [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  describe  Print Copernicus Marine catalog as JSON
  login     This command check the copernicus-marine credentials provided...
  get       Download originally produced data files
  subset    Downloads subsets of datasets as NetCDF files or Zarr stores
```

### Command `describe`
Retrieve metadata information about all products/datasets and display as JSON output:
```bash
copernicus-marine describe --include-datasets
```

The JSON output can also be saved like follows:
```bash
copernicus-marine describe --include-datasets > all_datasets_copernicus-marine.json
```

### Command `login`
Create a single configuration file `.copernicus-marine-credentials` allowing to access all Marine Data Store data services. By default, it saves file in user's home directory.

Example:
```bash
> copernicus-marine login
username : johndoe
password :
INFO - Configuration files stored in /Users/foo/.copernicus-marine-client
```

If `.copernicus-marine-credentials` already exists, the user is asked for confirmation to overwrite (`--overwrite`/`--overwrite-configuration-file`).

#### Access points migration and evolution

If you already have a configuration for current services (e.g. `~/motuclient/motuclient-python.ini`, `~/.netrc` or `~/_netrc`) in your home directory, it will automatically be taken into account with commands `get` and `subset` without the need for running the `login` command.
If the configuration files are already available in another directory, when running commands `subset` or `get`, you can use the `--credentials-file` option to point to the file.

### Command `subset`
Remotely subset a dataset, based on variable names, geographical and temporal parameters.

Example:
```bash
copernicus-marine subset --dataset-id cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m --variable thetao --variable so --start-datetime 2021-01-01 --end-datetime 2021-01-03 --minimum-longitude 0.0 --maximum-longitude 0.1 --minimum-latitude 28.0 --maximum-latitude 28.1
```
Returns:
```bash
INFO     - Download through S3
<xarray.Dataset>
Dimensions:    (depth: 50, latitude: 2, longitude: 1, time: 1)
Coordinates:
  * depth      (depth) float32 0.5058 1.556 2.668 ... 5.292e+03 5.698e+03
  * latitude   (latitude) float32 28.0 28.08
  * longitude  (longitude) float32 0.08333
  * time       (time) datetime64[ns] 2021-01-01
Data variables:
    thetao     (time, depth, latitude, longitude) float32 dask.array<chunksize=(1, 50, 2, 1), meta=np.ndarray>
    so         (time, depth, latitude, longitude) float32 dask.array<chunksize=(1, 50, 2, 1), meta=np.ndarray>
Attributes: (12/19)
    Conventions:    CF-1.0
    bulletin_date:  2022-11-01
    ...             ...
    title:          CMEMS IBI REANALYSIS: YEARLY PHYSICAL PRODUCTS
Do you want to proceed with download? [Y/n]:
```

By default, after the display of the summary of the dataset subset, a download confirmation is asked. To skip this user's action, call option `--force-download`.

#### Note about longitude range
Options `--minimum-longitude` and `--maximum-longitude` work as follows:
- If the result of the substraction ( `--maximum-longitude` minus `--minimum-longitude` ) is superior or equal to 360, then return the full dataset.
- If the requested longitude range:
  - **does not cross** the antemeridian, then return the dataset between range -180° and 180°.
  - **does cross** the antemeridian, then return the dataset between range 0° and 360°.

Note that you can request any longitudes you want. A modulus is applied to bring the result between -180° and 360°. For example, if you request [530°, 560°], the result dataset will be in [170°, 200°].

#### Access point migration and evolution
The copernicus marine client will download the data in the most efficient way according to your request:
- if the target dataset **is available** in ARCO version, then files are downloaded in a fresh new `data.zarr` folder in the current working directory.
- if the target dataset **is not yet available** in ARCO version, then a `data.nc` file is downloaded in the current working directory.

However, the output directory and filename can be specified using `-o`/`--output-directory` and `-f`/`--output-filename` respectively. If the later ends with `.nc`, it will be written as a NetCDF file.

You can force the use of a specific data access service with option `--force-service`.

### Command `get`
Download the dataset file(s) as originally produced, based on the datasetID or the path to files.

Example:
```bash
copernicus-marine get --dataset-url ftp://my.cmems-du.eu/Core/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m --force-service original-files
```
Returns:
```bash
INFO     - You forced selection of service: original-files
INFO     - Downloading using service original-files...
INFO     - You requested the download of the following files:
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_19930101_19931231_R20221101_RE01.nc - 8.83 MB
[... truncated for brevity..]
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20120101_20121231_R20221101_RE01.nc - 8.62 MB
Printed 20 out of 29 files

Total size of the download: 252.94 MB

Do you want to proceed with download? [Y/n]
```

You can force the use of a specific data access service with option `--force-service`.

By default:
- after the header displays a summary of the request, a download confirmation is asked. To skip this user's action, add option `--force-download`.
- files are downloaded to the current directory applying the original folder structure. To avoid this behavior, add `--no-directories` and specify a destination with the `--output-directory` option.

Option `--show-outputnames` displays the full paths of the output files, if required.

#### Note about filtering options
Option `--filter` allows to specify a Unix shell-style wildcard pattern (see [fnmatch — Unix filename pattern matching](https://docs.python.org/3/library/fnmatch.html)) and select specific files:
```bash
copernicus-marine get --dataset-id cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m --filter "*01yav_200[0-2]*"
```
Returns:
```bash
INFO     - Downloading using service files...
INFO     - You requested the download of the following files:
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20000101_20001231_R20221101_RE01.nc - 8.93 MB
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20010101_20011231_R20221101_RE01.nc - 8.91 MB
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20020101_20021231_R20221101_RE01.nc - 8.75 MB

Total size of the download: 26.59 MB
Do you want to proceed with download? [Y/n]:
```

Option `--regex` allows to specify a regular expression for more advanced files selection:
```bash
copernicus-marine get -i cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m --regex ".*01yav_20(00|01|02).*.nc"
```
Returns:
```bash
INFO     - Downloading using service files...
INFO     - You requested the download of the following files:
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20000101_20001231_R20221101_RE01.nc - 8.93 MB
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20010101_20011231_R20221101_RE01.nc - 8.91 MB
s3://mdl-native/native/IBI_MULTIYEAR_PHY_005_002/cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m_202211/CMEMS_v5r1_IBI_PHY_MY_NL_01yav_20020101_20021231_R20221101_RE01.nc - 8.75 MB

Total size of the download: 26.59 MB
Do you want to proceed with download? [Y/n]:
```

### Shared options
Both `subset` and `get` commands provide these options:

#### Option `--overwrite-output-data`

When specified, the existing files will be overwritten.
Otherwise, if the files already exist on destination, new ones with a unique index will be created once the download has been accepted (or once `--force-download` is provided).

#### Option `--request-file`

This option allows to specify CLI options but in a provided JSON file, useful for batch processing.

- Template for `subset` data request:
```json
{
	"dataset_id": "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
	"start_datetime": "2022-04-11",
	"end_datetime": "2023-08-11",
	"minimum_longitude": -182.79,
	"maximum_longitude": -179.69,
	"minimum_latitude": -40,
	"maximum_latitude": -36,
	"minimum_depth": 0,
	"maximum_depth": 0,
	"variables": ["thetao"],
	"output_directory": "./data/",
	"output_filename": "temperature_small_pacific_2022208-202308.zarr",
	"force_download": false
}
```

Example:
```bash
copernicus-marine subset --request-file template_subset_data_request.json
```

- Template for `get` data request:
```json
{
    "dataset_id": "cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m",
    "filter": "*01yav_200[0-2]*",
    "force_download": false,
    "force_service": "files",
    "log_level": "INFO",
    "no_directories": false,
    "no_metadata_cache": false,
    "output_directory": "./data/",
    "overwrite_output_data": false,
    "overwrite_metadata_cache": false,
    "show_outputnames": true
}
```

Example:
```bash
copernicus-marine get --request-file template_get_data_request.json
```

#### Option `--credentials-file`
You can use the `--credentials-file` option to point to a credentials file. The file can be either `.copernicus-marine-credentials`, `motuclient-python.ini`, `.netrc` or `_netrc`.


## Python package (API)
The `copernicus-marine-client` exposes a Python interface to allow you to [call commands as functions](https://marine.copernicus.eu/python-interface).

## Documentation
See the [Help Center](https://help.marine.copernicus.eu/en/collections/4060068-copernicus-marine-client). A detailed standalone API documentation is under construction and will come at a later stage.

## Contribution
We welcome contributions from the community to enhance this package. If you find any issues or have suggestions for improvements, please check out our [Report Template](https://help.marine.copernicus.eu/en/articles/8218546-how-to-report-a-bug-or-suggest-new-features).

## Future improvements & Roadmap
- [ ] Make available the currently not managed Analysis-Ready Cloud-Optimized (ARCO) versions of Ocean Monitoring Indicator (OMI), in situ and static datasets.
- [ ] Allow to specify the compression level when downloading your subset as NetCDF file.
- [ ] Allow to subset variables using their `standard_name(s)` and not only their `name(s)`.

To keep up to date with the most recent and planned advancements, including revisions, corrections, and feature requests generated from users' feedback, please refer to our [Roadmap](https://help.marine.copernicus.eu/en/articles/8218641-what-are-the-next-milestones).

## Join the community
Get in touch!
- Create your [Copernicus Marine Account](https://data.marine.copernicus.eu/register)
- [Log in](https://data.marine.copernicus.eu/login?redirect=%2Fproducts) and chat with us (bottom right corner of [Copernicus Marine Service](https://marine.copernicus.eu/))
- Join our [training workshops](https://marine.copernicus.eu/services/user-learning-services)
- Network y/our [Copernicus Stories](https://twitter.com/cmems_eu)
- Watch [our videos](https://www.youtube.com/channel/UC71ceOVy7WtVC7F04BKoEew)
