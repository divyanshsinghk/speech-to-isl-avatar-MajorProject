def apply_isl_grammar(tokens):
    subjects = []
    objects = []
    verbs = []

    SUBJECTS = {"I", "YOU", "HE", "SHE", "WE", "THEY"}

    for token in tokens:
        if token in SUBJECTS:
            subjects.append(token)
        elif token.endswith("E") or token.endswith("ING"):
            verbs.append(token)
        else:
            objects.append(token)

    return subjects + objects + verbs
