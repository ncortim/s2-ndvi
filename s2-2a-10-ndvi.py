import glob
import numpy as np
from osgeo import gdal


def find_band(directory, pattern):
    """
    Find the file path for a specific band (e.g., B04, B08)
    within the R10m folder.
    """
    file_path = glob.glob(f"{directory}/**/*{pattern}", recursive=True)
    if file_path:
        return file_path
    else:
        raise FileNotFoundError(f"Band {pattern} not found in {directory}")


def read_band(band_path):
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


def compute_ndvi(red_band, nir_band):
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


def write_cog(ndvi, transform, projection, output_cog_path):
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


def main(safe_folder, output_cog_path):
    """
    Main function to read bands, compute NDVI, and write the output COG.

    Args:
        red_band_path (str): Path to the red band file.
        nir_band_path (str): Path to the NIR band file.
        output_cog_path (str): Path where the COG will be saved.
    """

    red_band_path = find_band(safe_folder, "B04_10m.jp2")
    nir_band_path = find_band(safe_folder, "B08_10m.jp2")

    red_band_path = red_band_path[0]
    nir_band_path = nir_band_path[0]

    red_band, transform, projection = read_band(red_band_path)
    nir_band, _, _ = read_band(nir_band_path)

    ndvi = compute_ndvi(red_band, nir_band)

    write_cog(ndvi, transform, projection, output_cog_path)


# Example usage
if __name__ == "__main__":
    safe_folder = "/path/to/sentinel/SAFE/directory"
    output_cog_path = "path/to/output/ndvi_cog.tif"

    main(safe_folder, output_cog_path)
