"""Entry point.

Mostly following this example:
https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

Use config.py to hold arguments to be accessed by imported scripts.

TODO: Argument parsing can be better structured, maybe by using parents. help
looks a bit messy as is.

"""

import sys
import argparse
import config


def main(args=None):
    """Command line call argument parsing."""
    if args is None:
        args = sys.argv[1:]
    # Main arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename', metavar='path',
        help="Path to input. Mostly a nifti file with image data."
        )
    parser.add_argument(
        "--gramag", metavar='path', required=False,
        help="Path to gradient magnitude (useful for deriche)"
        )
    parser.add_argument(
        "--ncut",  metavar='path', required=False,
        help="Path to nyp file with ncut labels"
        )
    parser.add_argument(
        "--scale", metavar='500', required=False, type=float,
        default=config.scale,
        help="Data is scaled from 0 to this number."
        )
    parser.add_argument(
        "--percmin", metavar='0.25', required=False, type=float,
        default=config.perc_min,
        help="Minimum percentile used in truncation."
        )
    parser.add_argument(
        "--percmax",  metavar='99.75', required=False,  type=float,
        default=config.perc_max,
        help="Maximum percentile used in truncation."
        )
    parser.add_argument(
        "--nogui", action='store_true',
        help="Only save 2D histogram image without showing GUI."
        )

    # used in Deriche filter gradient magnitude computation
    parser.add_argument(
        "--deriche_prepare", action='store_true',
        help=("------------------(utility feature)------------------ \
              Use this flag with the following arguments:")
        )
    parser.add_argument(
        "--der_alpha", required=False, type=float,
        default=2, metavar='2',
        help="Alpha controls smoothing, lower -> smoother"
        )

    # used in ncut preparation  (TODO: not yet tested after restructuring.)
    parser.add_argument(
        "--ncut_prepare", action='store_true',
        help=("------------------(utility feature)------------------ \
              Use this flag with the following arguments:")
        )
    parser.add_argument(
        "--ncut_maxRec", required=False, type=int,
        default=config.max_rec, metavar=config.max_rec,
        help="Maximum number of recursions."
        )
    parser.add_argument(
        "--ncut_nrSupPix", required=False, type=int,
        default=config.nr_sup_pix, metavar=config.nr_sup_pix,
        help="Number of regions/superpixels."
        )
    parser.add_argument(
        "--ncut_compactness", required=False, type=float,
        default=config.compactness, metavar=config.compactness,
        help="Compactness balances intensity proximity and space \
        proximity of the superpixels. \
        Higher values give more weight to space proximity, making \
        superpixel shapes more square/cubic. This parameter \
        depends strongly on image contrast and on the shapes of \
        objects in the image."
        )

    # set config file variables to be accessed from other scripts
    args = parser.parse_args()
    # used in all
    config.filename = args.filename
    # used in segmentator GUI (main and ncut)
    config.gramag = args.gramag
    config.scale = args.scale
    config.perc_min = args.percmin
    config.perc_max = args.percmax
    # used in deriche filter
    config.deriche_alpha = args.der_alpha
    # used in ncut preparation
    config.max_rec = args.ncut_maxRec
    config.nr_sup_pix = args.ncut_nrSupPix
    config.compactness = args.ncut_compactness
    # used in ncut
    config.ncut = args.ncut

    print("===========\nSegmentator\n===========")

    # Call other scripts with import method (couldn't find a better way).
    if args.nogui:
        print '--No GUI option is selected. Saving 2D histogram image...'
        import hist2d_counts
    elif args.deriche_prepare:
        import deriche
    elif args.ncut_prepare:
        print '--Preparing n-cut related files...'
        import ncut_prepare
    elif args.ncut:
        print '--Experimental N-cut feature is selected.'
        import segmentator_ncut
    else:
        import segmentator_main


if __name__ == "__main__":
    main()