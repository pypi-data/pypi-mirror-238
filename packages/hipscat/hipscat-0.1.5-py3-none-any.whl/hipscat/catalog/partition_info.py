"""Container class to hold per-partition metadata"""
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd

from hipscat.io import FilePointer, file_io
from hipscat.pixel_math import HealpixPixel


class PartitionInfo:
    """Container class for per-partition info."""

    METADATA_ORDER_COLUMN_NAME = "Norder"
    METADATA_DIR_COLUMN_NAME = "Dir"
    METADATA_PIXEL_COLUMN_NAME = "Npix"

    def __init__(self, pixel_list: List[HealpixPixel]) -> None:
        self.pixel_list = pixel_list

    def get_healpix_pixels(self) -> List[HealpixPixel]:
        """Get healpix pixel objects for all pixels represented as partitions.

        Returns:
            List of HealpixPixel
        """
        return self.pixel_list

    def get_highest_order(self) -> int:
        """Get the highest healpix order for the dataset.

        Returns:
            int representing highest order.
        """
        max_pixel = np.max(self.pixel_list)
        return max_pixel.order

    def write_to_file(self, partition_info_file: FilePointer):
        """Write all partition data to CSV file.

        Args:
            partition_info_file: FilePointer to where the `partition_info.csv`
                file will be written
        """
        file_io.write_dataframe_to_csv(self.as_dataframe(), partition_info_file, index=False)

    @classmethod
    def read_from_file(
        cls, partition_info_file: FilePointer, storage_options: Union[Dict[Any, Any], None] = None
    ):
        """Read partition info from a `partition_info.csv` file to create an object

        Args:
            partition_info_file: FilePointer to the `partition_info.csv` file
            storage_options: dictionary that contains abstract filesystem credentials

        Returns:
            A `PartitionInfo` object with the data from the file
        """
        if not file_io.does_file_or_directory_exist(partition_info_file, storage_options=storage_options):
            raise FileNotFoundError(f"No partition info found where expected: {str(partition_info_file)}")

        data_frame = file_io.load_csv_to_pandas(partition_info_file, storage_options=storage_options)

        pixel_list = [
            HealpixPixel(order, pixel)
            for order, pixel in zip(
                data_frame[cls.METADATA_ORDER_COLUMN_NAME],
                data_frame[cls.METADATA_PIXEL_COLUMN_NAME],
            )
        ]

        return cls(pixel_list)

    def as_dataframe(self):
        """Construct a pandas dataframe for the partition info pixels.

        Returns:
            Dataframe with order, directory, and pixel info.
        """
        partition_info_dict = {
            PartitionInfo.METADATA_ORDER_COLUMN_NAME: [],
            PartitionInfo.METADATA_PIXEL_COLUMN_NAME: [],
            PartitionInfo.METADATA_DIR_COLUMN_NAME: [],
        }
        for pixel in self.pixel_list:
            partition_info_dict[PartitionInfo.METADATA_ORDER_COLUMN_NAME].append(pixel.order)
            partition_info_dict[PartitionInfo.METADATA_PIXEL_COLUMN_NAME].append(pixel.pixel)
            partition_info_dict[PartitionInfo.METADATA_DIR_COLUMN_NAME].append(
                int(pixel.pixel / 10_000) * 10_000
            )
        return pd.DataFrame.from_dict(partition_info_dict)

    @classmethod
    def from_healpix(cls, healpix_pixels: List[HealpixPixel]):
        """Create a partition info object from a list of constituent healpix pixels.

        Args:
            healpix_pixels: list of healpix pixels
        Returns:
            A `PartitionInfo` object with the same healpix pixels
        """
        return cls(healpix_pixels)
