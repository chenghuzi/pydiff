from io import StringIO
import tokenize
import difflib
import black


def remove_comments(source):
    """

    Returns 'source' minus comments and docstrings.
    Adopted from from https://stackoverflow.com/questions/1769332/script-to-remove-python-comments-docstrings
    """
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        # ltext = tok[4]
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
        pass
    return out


def remove_empty(source):
    source_lines = source.split('\n')
    clean_source_lines = []
    for line in source_lines:
        if line.strip() == '':
            continue
        if line.strip('\t') == '':
            continue
        elif line.strip() == 'pass':
            continue
        else:
            clean_source_lines.append(line)
    clean_source = '\n'.join(clean_source_lines)

    return clean_source


def snippets2cleansnippets(lines):
    source_a = '\n'.join(lines)
    source_a = remove_comments(source_a)
    source_a = remove_empty(source_a)
    return source_a.split('\n')


def resolve_diff_un(snippet_a, snippet_b):
    diff = list(difflib.ndiff(snippet_a, snippet_b))
    result = '\n'.join(
        (line for line in diff if line.startswith('- ') or line.startswith('+ ')))
    return result


def resolve_diff_basic(snippet_a, snippet_b):
    snippet_a = snippets2cleansnippets(snippet_a)
    snippet_b = snippets2cleansnippets(snippet_b)

    return resolve_diff_un(snippet_a, snippet_b)


def blackformat(snippet):
    lines = black.format_str('\n'.join(snippet), mode=black.Mode())
    snippet = lines.split('\n')
    return snippet


def resolve_diff_style(snippet_a, snippet_b):
    snippet_a = snippets2cleansnippets(snippet_a)
    snippet_b = snippets2cleansnippets(snippet_b)
    snippet_a = blackformat(snippet_a)
    snippet_b = blackformat(snippet_b)

    return resolve_diff_un(snippet_a, snippet_b)


def resolve_diff(snippet_a, snippet_b, format='black'):
    if format == 'black':
        return resolve_diff_style(snippet_a, snippet_b)
    elif format is None:
        resolve_diff_basic(snippet_a, snippet_b)
    else:
        raise ValueError('No such format options')


if __name__ == '__main__':
    snippet_a = (
        "# Router definition",
        "api_router = APIRouter()"
    )
    snippet_b = (
        "# Make sure endpoint are immune to missing trailing slashes",
        "api_router = APIRouter(redirect_slashes=True)"
    )
    print(resolve_diff(snippet_a, snippet_b))