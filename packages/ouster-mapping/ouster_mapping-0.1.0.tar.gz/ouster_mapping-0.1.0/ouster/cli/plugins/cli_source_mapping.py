# type: ignore

import click
from ouster.cli.plugins.io_type import OusterIoType
from ouster.cli.plugins.source_osf import source
from ouster.cli.plugins.source import _source_arg_name, _output_file_arg_name
from ouster.cli.core.util import click_ro_file
from ouster.cli.plugins import cli_mapping


@click.command
@click.argument(_output_file_arg_name, required=True)
@click.option('-d', '--min_dist', default=2.0, help="Min dist (m) for points to "
              "save. Default value is 2m")
@click.option('-s', '--voxel_size', default=0.1, help="Voxel map size for down "
              "sampling. This is same with open3D voxel size. Default value is 0.1. "
              "The bigger the value, the fewer points output"
              " http://www.open3d.org/docs/0.6.0/python_api/open3d.geometry.voxel_down_sample.html")
@click.option('-f',
              '--field',
              required=False,
              type=click.Choice(['SIGNAL',
                                 'NEAR_IR',
                                 'REFLECTIVITY'],
                                case_sensitive=False),
              default="REFLECTIVITY",
              help="Chanfield for output file key value. Choose between SIGNAL, NEAR_IR, "
              "REFLECTIVITY. Default field is REFLECTIVITY")
@click.option('--print_process', required=False, type=bool,
              default=True, help="Default is On")
@click.option('--verbose_print', required=False, type=bool, default=False,
              help="Print point cloud status much frequently. Default is Off")
@click.pass_context
def convert_from_osf(ctx, *args, **kwargs):
    """
    Save point cloud from an OSF file into specific formats

    Output file format depends on output filename extension. The valid output files
    extensions are .las, .ply and .pcd. Default output format is .ply. For large point
    cloud, the output will be split into multiple files and each file is around 1G.
    Currently this tool only supports single lidar OSF files.
    """
    kwargs['input_file'] = ctx.obj.get(_source_arg_name)

    ctx.forward(cli_mapping.point_cloud_convert, *args, **kwargs)


source.commands[OusterIoType.OSF]['convert'].conversions[OusterIoType.PLY] = convert_from_osf
source.commands[OusterIoType.OSF]['convert'].conversions[OusterIoType.PCD] = convert_from_osf
source.commands[OusterIoType.OSF]['convert'].conversions[OusterIoType.LAS] = convert_from_osf


@click.command
@click.argument('viz', required=False, default="", type=str)
@click.option('-m', '--meta', required=False, default=None, type=click_ro_file,
              help="Metadata file for pcap input")
@click.option('--slam_name', default='kiss_slam', help="Slam name")
@click.option("-r", "--rate", default=1.0, help="Playback rate")
@click.option("--pause-at", default=-1, help="Lidar Scan number to pause")
@click.option('-e', '--on-eof', default='exit',
              type=click.Choice(['stop', 'exit']),
              help="Stop or exit after reaching end of file")
@click.option('-l', '--lidar_port', type=int, default=None, help="Lidar port")
@click.option('-O', '--auto_out', is_flag=True, default=False,
              help="Save SLAM results into an auto named OSF file")
@click.option('-o', '--output', required=False, type=str,
              help="Specify OSF output filename")
@click.option('-x', '--do-not-reinitialize', is_flag=True, default=False,
              help="Do not reinitialize (by default it will reinitialize if needed)")
@click.option('-y', '--no-auto-udp-dest', is_flag=True, default=False,
              help="Do not automatically set udp_dest (by default it will auto set udp_dest")
@click.option('--max_range', required=False,
              default=150.0, help="Max valid range")
@click.option('--min_range', required=False,
              default=1.0, help="Min valid range")
@click.option('-v', '--voxel_size', required=False,
              type=float, help="Voxel map size")
@click.option("--accum-num",
              default=0,
              help="Integer number of scans to accumulate")
@click.option("--accum-every",
              default=None,
              type=float,
              help="Accumulate every Nth scan")
@click.option("--accum-every-m",
              default=None,
              type=float,
              help="Accumulate scan every M meters traveled")
@click.option("--accum-map",
              is_flag=True,
              help="Enable the overall map accumulation mode")
@click.option("--accum-map-ratio",
              default=0.001,
              help="Ratio of random points of every scan to add to an overall map")
@click.pass_context
def run_slam(ctx, *args, **kwargs) -> None:
    """
    Run SLAM with a sensor or a PCAP/OSF file.\n

    To turn on the visualizer, append 'viz' to the command.
    To save the lidar data with the SLAM poses, append '-O' to the command.

    Example values for voxel_size:\n
        Outdoor: 1.4 - 2.2\n
        Large indoor: 1.0 - 1.8\n
        Small indoor: 0.4 - 0.8\n
    If voxel_size is not specifiied, the algorithm will use the first 10 scans to calculate it.\n
    Small voxel size could give more accurate results but take more memory and
    longer processing. For real-time slam, considing using a slightly larger voxel size
    and use visualizer to monitor the SLAM process.
    """
    source = ctx.obj.get(_source_arg_name)
    kwargs['source'] = source
    ctx.forward(cli_mapping.run_slam, *args, **kwargs)


source.commands[OusterIoType.SENSOR]['slam'] = run_slam
source.commands[OusterIoType.PCAP]['slam'] = run_slam
source.commands[OusterIoType.OSF]['slam'] = run_slam
