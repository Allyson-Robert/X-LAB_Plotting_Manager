def is_monotonic(seq, *, strict=False, increasing=None):
    """
       Check if a sequence is monotonic.

       Parameters
       ----------
       seq : sequence
           A list or tuple of comparable elements.
       strict : bool, optional
           If True, requires strictly increasing/decreasing (no equal elements allowed).
       increasing : bool or None, optional
           - True  → check only increasing
           - False → check only decreasing
           - None  → check either increasing or decreasing

       Keyword-only arguments
       ----------------------
       The asterisk (*) in the function signature means that all parameters
       after it must be passed by name. This prevents mistakes like
       `is_monotonic(data, True, False)` where it’s unclear what each value
       means, and enforces readable calls such as
       `is_monotonic(data, strict=True, increasing=False)`.

       Returns
       -------
       bool
           True if the sequence satisfies the monotonicity condition.

       Notes
       -----
       - Sequences of length < 2 are considered monotonic by definition.
       - Non-strict allows equal consecutive elements.
       """
    if len(seq) < 2:
        return True

    if increasing is True:
        op = (lambda a, b: a < b) if strict else (lambda a, b: a <= b)
        return all(op(seq[i], seq[i + 1]) for i in range(len(seq) - 1))
    elif increasing is False:
        op = (lambda a, b: a > b) if strict else (lambda a, b: a >= b)
        return all(op(seq[i], seq[i + 1]) for i in range(len(seq) - 1))
    else:
        # Check either direction
        return (
            all((a < b) if strict else (a <= b) for a, b in zip(seq, seq[1:])) or
            all((a > b) if strict else (a >= b) for a, b in zip(seq, seq[1:]))
        )
