import argparse
from pathlib import Path

from evalutils.evalutils import (DEFAULT_EVALUATION_OUTPUT_FILE_PATH,
                                 DEFAULT_GROUND_TRUTH_PATH, DEFAULT_INPUT_PATH)

from dragon_eval import DragonEval

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-g", "--ground-truth-path", type=Path, default=DEFAULT_GROUND_TRUTH_PATH,
                        help="Path to the ground truth directory.")
    parser.add_argument("-i", "--predictions-path", type=Path, default=DEFAULT_INPUT_PATH,
                        help="Path to the predictions directory.")
    parser.add_argument("-o", "--output-file", type=Path, default=DEFAULT_EVALUATION_OUTPUT_FILE_PATH,
                        help="Path to the output file.")
    parser.add_argument("-f", "--folds", nargs="+", type=int, default=(0, 1, 2, 3, 4),
                        help="Folds to evaluate. Default: all folds.")
    parser.add_argument("-t", "--tasks", nargs="+", type=str, default=None,
                        help="Tasks to evaluate. Default: all tasks."),
    args = parser.parse_args()

    DragonEval(
        ground_truth_path=Path(args.ground_truth_path),
        predictions_path=Path(args.predictions_path),
        output_file=Path(args.output_file),
        folds=args.folds,
        tasks=args.tasks,
    ).evaluate()
