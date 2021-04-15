import argparse

from .furniture import add_argument as add_furniture_arguments
from ..util import str2bool


def create_parser(env=None):
    """
    Creates the argparser.  Use this to add additional arguments
    to the parser later.
    """
    parser = argparse.ArgumentParser(
        "IKEA Furniture Assembly Environment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # environment
    parser.add_argument(
        "--env",
        type=str,
        default=env if env is not None else "furniture-baxter-flip-v0",
        help="Environment name",
    )

    args, unparsed = parser.parse_known_args()

    # furniture config
    add_furniture_arguments(parser)

    env_arguments = get_env_specific_argument(args.env)
    if env_arguments:
        env_arguments.add_argument(parser)

    parser.add_argument("--seed", type=int, default=123, help="random seed")
    parser.add_argument("--debug", type=str2bool, default=False)

    return parser


def get_env_specific_argument(env):
    f = None
    if env == "IKEACursor-v0":
        from . import furniture_cursor as f

    elif env == "IKEASawyerGen-v0":
        from . import furniture_sawyer_gen as f

    elif env in ["IKEASawyerDense-v0", "furniture-sawyer-densereward-v0"]:
        from . import furniture_sawyer_dense as f

    return f


def argparser():
    """
    Directly parses the arguments
    """
    parser = create_parser()
    args, unparsed = parser.parse_known_args()

    return args, unparsed
