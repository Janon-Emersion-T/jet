from pathlib import Path
import difflib


def compare_two_patches(patch_a_path, patch_b_path):
    a = Path(patch_a_path).read_text(encoding="utf-8").splitlines()
    b = Path(patch_b_path).read_text(encoding="utf-8").splitlines()

    return "\n".join(difflib.unified_diff(
        a,
        b,
        fromfile=f"PATCH A: {patch_a_path}",
        tofile=f"PATCH B: {patch_b_path}",
        lineterm=""
    ))