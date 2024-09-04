# s2-ndvi
This repository contains Python code for calculating the Normalized Difference Vegetation Index (NDVI) from Sentinel-2 Level 2A imagery using GDAL. The script reads the Red and Near Infrared (NIR) bands from Sentinel-2 data, computes NDVI, and outputs the result as a Cloud Optimized GeoTIFF (COG).


# Sentinel-2 NDVI Computation Tool

This Python tool calculates the Normalized Difference Vegetation Index (NDVI) from Sentinel-2 satellite imagery and outputs the result as a Cloud Optimized GeoTIFF (COG). The tool is designed to work with Sentinel-2 Level-2A data stored in a directory with the extension .SAFE, specifically targeting the 10m resolution bands.

## Features

- **Automatic Band Search:** The tool automatically searches for the red (B04) and near-infrared (B08) bands within a specified Sentinel-2 SAFE directory.
- **NDVI Calculation:** Computes NDVI using the formula:
  \[
  \text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}
  \]
- **Cloud Optimized GeoTIFF (COG) Output:** Saves the NDVI result as a Cloud Optimized GeoTIFF with efficient tiling and compression for better performance in cloud environments.

## Requirements

- Python 3.7+
- [GDAL](https://gdal.org/) (Geospatial Data Abstraction Library)
- [Click](https://click.palletsprojects.com/) (Command-line interface creation toolkit)
- [NumPy](https://numpy.org/)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/sentinel2-ndvi.git
    cd sentinel2-ndvi
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that GDAL is properly installed and configured on your system. You can refer to the [official GDAL installation guide](https://gdal.org/download.html) for assistance.

## Usage

To run the NDVI computation tool, use the following command in your terminal:

```bash
python s2-2a-10m-ndvi.py /path/to/Sentinel2_SAFE_directory /path/to/output_directory
```

### Arguments:
- `/path/to/Sentinel2_SAFE_directory`: The path to the Sentinel-2 SAFE directory containing the Level-2A data.
- `/path/to/output_directory`: The path where the output Cloud Optimized GeoTIFF will be saved.

### Example:

```bash
python s2-2a-10m-ndvi.py /data/sentinel2/SAFE /output/ndvi
```

This command will create an NDVI COG file named `s2-2a-10m-ndvi.tif` in the `/output/ndvi` directory.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact the maintainer.
