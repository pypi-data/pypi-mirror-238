import sys
import argparse
from pathlib import Path
import os
import numpy as np
import ast

def main():
    parser = argparse.ArgumentParser("imface cli for image vector")
    parser.add_argument("--represent", help="represent image embed vector", default=False)
    parser.add_argument("-v", "--version", help="version", default=False, action="store_true")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")
    distance_command = subparsers.add_parser("distance", help="to get distance between two vector")
    distance_parser = subparsers.add_parser("distance", help="Calculate cosine distance between two vectors.")
    distance_parser.add_argument("-s", "--source", required=True, help="Source vector (space-separated)")
    distance_parser.add_argument("-t", "--target", required=True, help="Target vector (space-separated)")
    parser.add_argument("--extract", help="extract face, and only allowed to extrace one face, inset the image path", default=False)
    parser.add_argument("--treshold", help="get treshold", default=False, action="store_true")
    args = parser.parse_args()

    version =  "0.0.0.2.2"
    if args.version:
        os.environ.setdefault("DEEPFACE_HOME", "/app")
        print(version + str(os.getenv("DEEPFACE_HOME", default=str(Path.home()))))
        exit(0)
    elif args.treshold:
        treshold = utils.getTreshold()
        print(treshold)
        exit(0)

    elif args.represent:
        target_image = Path(args.represent)

        if not target_image.exists():
            print("Target image not exist")
            raise SystemExit(1)
        try:
            os.environ.setdefault("DEEPFACE_HOME", "/app")

            from imface.utils import deepface_util as utils
            embed = utils.getEmbeddingVector(str(target_image))
            print(embed)
        except Exception as e:
            print("error " + repr(e))
            raise SystemExit(1)

    elif args.extract:
        target_image = Path(args.extract)

        if not target_image.exists():
            print("image not exist")
            raise SystemExit(1)
        try:
            os.environ.setdefault("DEEPFACE_HOME", "/app")
            
            from imface.utils import deepface_util as utils
            data = utils.extractFace(str(target_image))
            if len(data) > 1:
                print("error only allowed one face")
                raise SystemExit(1)
            else:
                print(data[0]['embedding'])
        except Exception as e:
            print("error" + repr(e))
            raise SystemExit(1)

    elif args.command == "distance":
        if args.source and args.target:
            # Convert the string representation of vectors to lists of floats
            source_vector = ast.literal_eval(args.source)
            target_vector = ast.literal_eval(args.target)

            # Convert the lists to numpy arrays with the correct data type
            source_vector = np.array(source_vector, dtype=np.float32)
            target_vector = np.array(target_vector, dtype=np.float32)
            result = utils.getDistance(source_vector, target_vector)
            print(result)

    if __name__ == "__main__":
        main()