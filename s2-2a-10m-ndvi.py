import glob
import click
import numpy as np
from osgeo import gdal
from typing import Tuple


def find_band(directory: str, pattern: str) -> str:
    """Find the file path for a specific band
    (e.g., B04, B08) within the R10m folder.


    Args:
        directory (str): path to Sentine SAFE directory
        pattern (str): filename pattern used for searchin

    Raises:
        FileNotFoundError: Error if file was not found

    Returns:
        str: path to Sentinel 2 file according to defined pattern
    """
    file_path = glob.glob(f"{directory}/**/*{pattern}", recursive=True)
    if file_path:
        return file_path
    else:
        raise FileNotFoundError(f"Band {pattern} not found in {directory}")


def read_band(
    band_path: str,
) -> Tuple[np.ndarray, Tuple[float, float, float, float, float, float], str]:
    """
    Read a raster band from the given path and return as a numpy array.

    Args:
        band_path (str): Path to the raster band file.

    Returns:
        tuple: (numpy array of raster data, geotransform, projection)
    """
    ds = gdal.Open(band_path)
    band_array = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    transform = ds.GetGeoTransform()
    projection = ds.GetProjection()
    ds = None  # Close the dataset
    return band_array, transform, projection


def compute_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """
    Compute the NDVI from Red and NIR bands.

    Args:
        red_band (numpy array): Array of red band data.
        nir_band (numpy array): Array of NIR band data.

    Returns:
        numpy array: Array of NDVI values.
    """
    np.seterr(divide="ignore", invalid="ignore")  # Handle division by zero
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi


def write_cog(
    ndvi: np.ndarray,
    transform: Tuple[float, float, float, float, float, float],
    projection: str,
    output_cog_path: str,
):
    """
    Write the NDVI array to a Cloud Optimized GeoTIFF (COG).

    Args:
        ndvi (numpy array): Array of NDVI values.
        transform (tuple): Geotransform of the raster.
        projection (str): Projection of the raster.
        output_cog_path (str): Path where the COG will be saved.
    """
    driver = gdal.GetDriverByName("GTiff")
    if driver is None:
        raise RuntimeError("GDAL driver for GTiff not found")

    rows, cols = ndvi.shape
    options = ["TILED=YES", "COMPRESS=LZW", "BLOCKXSIZE=512", "BLOCKYSIZE=512"]

    # Create a new dataset
    output_ds = driver.Create(
        output_cog_path, cols, rows, 1, gdal.GDT_Float32, options=options
    )
    output_ds.SetGeoTransform(transform)
    output_ds.SetProjection(projection)

    # Write the NDVI array
    output_band = output_ds.GetRasterBand(1)
    output_band.WriteArray(ndvi)
    output_band.SetDescription("NDVI")
    output_band.SetNoDataValue(-9999)

    output_band.FlushCache()
    output_ds.FlushCache()
    output_ds = None  # Close the dataset

    print(f"NDVI calculation complete. COG saved to {output_cog_path}")


@click.command()
@click.argument("path_to_s2_folder", type=click.Path(exists=True))
@click.argument("output_cog_path", type=click.Path(exists=True))
# def main(**kwargs):
def main(path_to_s2_folder: str, output_cog_path: str):
    """
    Main function to read bands, compute NDVI, and write the output COG.

    Args:
        path_to_s2_folder (str): Path to the Sentinel2 SAFE folder. Do not
            use a trailing slash (e.g. /path/to/dir)
        output_cog_path (str): Path where the COG will be saved. Do not
            use a trailing slash (e.g. /path/to/dir)
    """

    # path_to_s2_folder = (kwargs["path_to_s2_folder"],)
    # output_cog_path = (kwargs["output_cog_path"],)
    output_cog_path = f"{output_cog_path}/s2-2a-10m-ndvi.tif"

    red_band_path = find_band(path_to_s2_folder, "B04_10m.jp2")
    nir_band_path = find_band(path_to_s2_folder, "B08_10m.jp2")

    red_band_path = red_band_path[0]
    nir_band_path = nir_band_path[0]

    red_band, transform, projection = read_band(red_band_path)
    nir_band, _, _ = read_band(nir_band_path)

    ndvi = compute_ndvi(red_band, nir_band)

    write_cog(ndvi, transform, projection, output_cog_path)


if __name__ == "__main__":
    main()
