import difflib


def generate_diff(
    original_code,
    updated_code
):

    diff = difflib.unified_diff(
        original_code.splitlines(),
        updated_code.splitlines(),
        lineterm=""
    )

    final_diff = "\n".join(diff)

    return final_diff