# type: ignore


from typing import List, Tuple  # noqa: F401
import numpy as np
import itertools
import logging
from .slam_backend import SLAMBackend
import ouster.mapping.util as util
import ouster.client as client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class VoxelAutoSizer:

    def __init__(self, scan_source, scans_number=10) -> None:
        self.ranges = []
        # Iterate through the first 10 scans (or all values if less than 10)
        for scan in itertools.islice(scan_source, scans_number):
            sel_flag = scan.field(client.ChanField.RANGE) != 0
            scan_range = scan.field(client.ChanField.RANGE)[sel_flag]
            self.ranges.append(scan_range)

    # average highest 98% to 99% range readings and use this averaged range value
    # to calculate the voxel map size
    def get_voxel_size(self, start_pct: float = 0.98, end_pct: float = 0.99) -> float:
        # combine and flatten the ranges
        combined_ranges = np.concatenate(self.ranges, axis=0)
        sorted_ranges = np.sort(combined_ranges, axis=0)
        start_index = int(len(sorted_ranges) * start_pct)
        end_index = int(len(sorted_ranges) * end_pct)

        selected_ranges = sorted_ranges[start_index:end_index]
        # lidar range is in mm. change the unit to meter
        average = np.mean(selected_ranges) / 1000
        # use the lidar range readings and a number to land voxel size in a proper range
        voxel_size = average / 30.0

        return voxel_size


class KissBackend(SLAMBackend):
    """Wraps kiss-icp odometry to use with Ouster pipelines."""

    def __init__(
        self,
        info: client.SensorInfo,
        use_extrinsics: bool = True,
        max_range: float = 150.0,
        min_range: float = 1.0,
        voxel_size: float = None
    ):
        try:
            from kiss_icp.kiss_icp import KissICP
        except ImportError as e:
            logger.error("kiss-icp, a package required for slam, is unsupported on "
                  "yout platform. ")
            raise
        import kiss_icp.config
        super().__init__(info, use_extrinsics)
        config = kiss_icp.config.KISSConfig(config_file=None)
        config.data.deskew = True
        config.data.max_range = max_range
        config.data.min_range = min_range
        if voxel_size is not None:
            config.mapping.voxel_size = voxel_size
        else:
            config.mapping.voxel_size = max_range / 100.0
        self.kiss_icp = KissICP(config)
        # to store the middle valid timestamp of a scan and middle col pose
        self.ts_pose = list(tuple())  # type: List[Tuple[int, np.ndarray]]
        self.timestamps = np.tile(
            np.linspace(0, 1.0, self.w, endpoint=False), (self.h, 1)
        )

    """Update the pose (per_column_global_pose) variable in scan and return"""
    def update(self, scan: client.LidarScan) -> client.LidarScan:

        # filtering our zero returns makes it substantially faster for kiss-icp
        sel_flag = scan.field(client.ChanField.RANGE) != 0
        xyz = self.xyz_lut(scan.field(client.ChanField.RANGE))[sel_flag]
        self.kiss_icp.register_frame(xyz, self.timestamps[sel_flag])

        # accumulate scan timestamps in parallel list to poses
        scan_start_ts = scan.timestamp[client.core.first_valid_column(scan)]
        scan_end_ts = scan.timestamp[client.core.last_valid_column(scan)]
        scan_mid_ts = (scan_start_ts + scan_end_ts) / 2
        self.ts_pose.append((scan_mid_ts, self.kiss_icp.poses[-1]))

        if len(self.ts_pose) >= 2:
            col_global_poses = util.getScanColPose(
                self.ts_pose[-2], self.ts_pose[-1], scan
            )
            scan.pose[:] = col_global_poses
        elif len(self.ts_pose) < 2:
            # First scan pose in KISS in identity matrix. not enough poses to do
            # perturbation in every column. Juse identity matrix for col poses

            repeat_num = scan.w
            identity_matrix = np.identity(4)
            scan.pose[:] = np.array(np.tile(identity_matrix, (repeat_num, 1, 1)).tolist())

        return scan
