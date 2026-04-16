"""
Template engine for static site generation.

Syntax:
  {{ expr }}                          Output expression
  {{ expr | filter1 | filter2 }}      Output with filters
  {% for x in expr %}...{% endfor %}  Loop (with {% else %} for empty)
  {% if expr %}...{% endif %}         Conditional (elif, else supported)
  {% set x = expr %}                  Assign variable
  {# comment #}                       Comment (stripped)

Expressions:
  variable, obj.field                 Variable / dotted path
  "string", 42, true, false, none     Literals
  a == b, a != b, a < b              Comparisons
  a and b, a or b, not a             Boolean logic

Filters:
  | ruby              bracket notation to <ruby> HTML
  | strip_furigana    remove bracket notation
  | strip_html        remove HTML tags
  | where: field=val  filter list by field value
  | sort: "field"     sort list by field
  | default: "val"    fallback if falsy
  | join: ", "        join list
  | first / last      first/last item
  | length            collection length
  | int               convert to integer
"""

import re


# ── Errors ──────────────────────────────────────────────────────────

class TemplateError(Exception):
    pass


# ── Context ─────────────────────────────────────────────────────────

class Context:
    __slots__ = ('_data', '_parent')

    def __init__(self, data, parent=None):
        self._data = data if isinstance(data, dict) else {}
        self._parent = parent

    def get(self, key):
        if key in self._data:
            return self._data[key]
        if self._parent:
            return self._parent.get(key)
        return None

    def set(self, key, value):
        self._data[key] = value

    def child(self, data):
        return Context(data, self)


# ── AST Nodes ───────────────────────────────────────────────────────

class TextNode:
    __slots__ = ('text',)
    def __init__(self, text):
        self.text = text

class ExprNode:
    __slots__ = ('raw',)
    def __init__(self, raw):
        self.raw = raw

class ForNode:
    __slots__ = ('var_names', 'iter_raw', 'body', 'else_body')
    def __init__(self, var_names, iter_raw, body, else_body):
        self.var_names = var_names
        self.iter_raw = iter_raw
        self.body = body
        self.else_body = else_body

class IfNode:
    __slots__ = ('branches', 'else_body')
    def __init__(self, branches, else_body):
        self.branches = branches  # [(condition_raw, body), ...]
        self.else_body = else_body

class SetNode:
    __slots__ = ('name', 'expr_raw')
    def __init__(self, name, expr_raw):
        self.name = name
        self.expr_raw = expr_raw

class IncludeNode:
    __slots__ = ('path',)
    def __init__(self, path):
        self.path = path


# ── Tokenizer ──────────────────────────────────────────────────────

_TAG_RE = re.compile(r'(\{%.*?%\}|\{\{.*?\}\}|\{#.*?#\})', re.DOTALL)

def _tokenize(source):
    """Split template into (kind, content) tokens."""
    tokens = []
    for part in _TAG_RE.split(source):
        if not part:
            continue
        if part.startswith('{#'):
            continue
        if part.startswith('{{'):
            tokens.append(('expr', part[2:-2].strip()))
        elif part.startswith('{%'):
            tokens.append(('tag', part[2:-2].strip()))
        else:
            tokens.append(('text', part))
    return tokens


# ── Parser ─────────────────────────────────────────────────────────

def _parse(tokens):
    nodes, pos = _parse_block(tokens, 0, set())
    if pos < len(tokens):
        _, content = tokens[pos]
        raise TemplateError(f"Unexpected tag: {{% {content} %}}")
    return nodes


def _parse_block(tokens, pos, end_tags):
    nodes = []
    while pos < len(tokens):
        kind, content = tokens[pos]

        if kind == 'text':
            nodes.append(TextNode(content))
            pos += 1

        elif kind == 'expr':
            nodes.append(ExprNode(content))
            pos += 1

        elif kind == 'tag':
            keyword = content.split(None, 1)[0] if content.strip() else ''

            if keyword in end_tags:
                return nodes, pos

            if keyword == 'for':
                node, pos = _parse_for(tokens, pos)
                nodes.append(node)
            elif keyword == 'if':
                node, pos = _parse_if(tokens, pos)
                nodes.append(node)
            elif keyword == 'set':
                m = re.match(r'set\s+(\w+)\s*=\s*(.+)', content)
                if not m:
                    raise TemplateError(f"Invalid set: {{% {content} %}}")
                nodes.append(SetNode(m.group(1), m.group(2).strip()))
                pos += 1
            elif keyword == 'include':
                m = re.match(r'include\s+["\']([^"\']+)["\']', content)
                if not m:
                    raise TemplateError(f"Invalid include: {{% {content} %}}")
                nodes.append(IncludeNode(m.group(1)))
                pos += 1
            else:
                raise TemplateError(f"Unknown tag: {{% {content} %}}")

    if end_tags:
        raise TemplateError(f"Missing closing tag, expected: {end_tags}")
    return nodes, pos


def _parse_for(tokens, pos):
    _, content = tokens[pos]
    m = re.match(r'for\s+([\w,\s]+)\s+in\s+(.+)', content)
    if not m:
        raise TemplateError(f"Invalid for: {{% {content} %}}")
    var_names = [v.strip() for v in m.group(1).split(',')]
    iter_raw = m.group(2).strip()

    pos += 1
    body, pos = _parse_block(tokens, pos, {'endfor', 'else'})

    else_body = []
    if pos < len(tokens) and tokens[pos][1].strip() == 'else':
        pos += 1
        else_body, pos = _parse_block(tokens, pos, {'endfor'})

    if pos >= len(tokens):
        raise TemplateError("Missing {% endfor %}")
    pos += 1  # skip endfor
    return ForNode(var_names, iter_raw, body, else_body), pos


def _parse_if(tokens, pos):
    _, content = tokens[pos]
    condition = content.split(None, 1)[1].strip() if ' ' in content else ''

    pos += 1
    body, pos = _parse_block(tokens, pos, {'endif', 'else', 'elif'})
    branches = [(condition, body)]
    else_body = []

    while pos < len(tokens):
        _, tag_content = tokens[pos]
        keyword = tag_content.split(None, 1)[0]

        if keyword == 'elif':
            cond = tag_content.split(None, 1)[1].strip()
            pos += 1
            body, pos = _parse_block(tokens, pos, {'endif', 'else', 'elif'})
            branches.append((cond, body))
        elif keyword == 'else':
            pos += 1
            else_body, pos = _parse_block(tokens, pos, {'endif'})
            if pos >= len(tokens):
                raise TemplateError("Missing {% endif %}")
            pos += 1
            break
        elif keyword == 'endif':
            pos += 1
            break
        else:
            raise TemplateError(f"Unexpected in if block: {{% {tag_content} %}}")

    return IfNode(branches, else_body), pos


# ── String splitting (respects quoted strings) ─────────────────────

def _split_on(s, delim):
    """Split string on single-char delimiter, respecting quotes."""
    parts = []
    buf = []
    in_str = None
    for c in s:
        if c in ('"', "'") and not in_str:
            in_str = c
            buf.append(c)
        elif c == in_str:
            in_str = None
            buf.append(c)
        elif c == delim and not in_str:
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(c)
    parts.append(''.join(buf))
    return parts


def _split_keyword(s, kw):
    """Split on a keyword (e.g. ' and '), respecting quotes."""
    parts = []
    buf = []
    in_str = None
    i = 0
    while i < len(s):
        c = s[i]
        if c in ('"', "'") and not in_str:
            in_str = c
            buf.append(c)
            i += 1
        elif c == in_str:
            in_str = None
            buf.append(c)
            i += 1
        elif not in_str and s[i:i+len(kw)] == kw:
            parts.append(''.join(buf))
            buf = []
            i += len(kw)
        else:
            buf.append(c)
            i += 1
    parts.append(''.join(buf))
    return parts if len(parts) > 1 else [s]


# ── Expression evaluation ──────────────────────────────────────────

def _eval_full(raw, ctx, filters):
    """Evaluate expression with pipe filters."""
    parts = _split_on(raw, '|')
    val = _eval_expr(parts[0].strip(), ctx)
    for part in parts[1:]:
        val = _apply_one_filter(part.strip(), val, ctx, filters)
    return val


def _eval_expr(s, ctx):
    """Evaluate expression (comparisons, booleans, values)."""
    s = s.strip()
    if not s:
        return None

    # Boolean: or (lowest precedence)
    parts = _split_keyword(s, ' or ')
    if len(parts) > 1:
        return any(_eval_expr(p.strip(), ctx) for p in parts)

    # Boolean: and
    parts = _split_keyword(s, ' and ')
    if len(parts) > 1:
        return all(_eval_expr(p.strip(), ctx) for p in parts)

    # Boolean: not
    if s.startswith('not '):
        return not _eval_expr(s[4:], ctx)

    # Comparisons
    for op in ('==', '!=', '<=', '>=', '<', '>'):
        idx = _find_operator(s, op)
        if idx >= 0:
            left = _eval_value(s[:idx].strip(), ctx)
            right = _eval_value(s[idx+len(op):].strip(), ctx)
            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<=': return left <= right
            if op == '>=': return left >= right
            if op == '<':  return left < right
            if op == '>':  return left > right

    # in operator: "x in collection"
    parts = _split_keyword(s, ' in ')
    if len(parts) == 2:
        item = _eval_value(parts[0].strip(), ctx)
        collection = _eval_value(parts[1].strip(), ctx)
        if collection is not None:
            return item in collection
        return False

    return _eval_value(s, ctx)


def _find_operator(s, op):
    """Find operator position outside of quoted strings."""
    in_str = None
    i = 0
    while i < len(s) - len(op) + 1:
        c = s[i]
        if c in ('"', "'") and not in_str:
            in_str = c
        elif c == in_str:
            in_str = None
        elif not in_str and s[i:i+len(op)] == op:
            # Make sure it's not part of a longer operator (e.g. = vs ==)
            before = s[i-1] if i > 0 else ' '
            after = s[i+len(op)] if i+len(op) < len(s) else ' '
            if op in ('==', '!=', '<=', '>='):
                return i
            if op == '<' and after != '=':
                return i
            if op == '>' and after != '=' and before != '!':
                return i
        i += 1
    return -1


def _eval_value(s, ctx):
    """Evaluate a single value: literal or variable path."""
    s = s.strip()
    if not s:
        return None
    # String literal
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    # Number
    if s.lstrip('-').isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        pass
    # Boolean / None
    if s == 'true': return True
    if s == 'false': return False
    if s == 'none': return None
    # Variable path
    return _resolve(s, ctx)


def _resolve(path, ctx):
    """Resolve dotted path like 'data.words' against context."""
    parts = path.split('.')
    val = ctx.get(parts[0])
    for part in parts[1:]:
        if val is None:
            return None
        if isinstance(val, dict):
            val = val.get(part)
        elif isinstance(val, (list, tuple)):
            if part.isdigit():
                idx = int(part)
                val = val[idx] if idx < len(val) else None
            else:
                return None
        else:
            val = getattr(val, part, None)
    return val


# ── Filter application ─────────────────────────────────────────────

def _apply_one_filter(raw, value, ctx, filters):
    """Parse and apply a single filter like 'where: category_id=cat.id'."""
    parts = raw.split(':', 1)
    name = parts[0].strip()
    fn = filters.get(name)
    if not fn:
        raise TemplateError(f"Unknown filter: {name}")

    args = []
    kwargs = {}
    if len(parts) > 1:
        for arg in _split_on(parts[1], ','):
            arg = arg.strip()
            if not arg:
                continue
            eq = arg.find('=')
            if eq > 0 and not (arg[0] in ('"', "'")):
                key = arg[:eq].strip()
                val_raw = arg[eq+1:].strip()
                kwargs[key] = _eval_value(val_raw, ctx)
            else:
                args.append(_eval_value(arg, ctx))

    return fn(value, *args, **kwargs)


# ── Builtin filters ────────────────────────────────────────────────

_RUBY_RE = re.compile(r'([\u4e00-\u9fff\u3005]+)【([^】]+)】')
_FURIGANA_RE = re.compile(r'【[^】]+】')
_HTML_RE = re.compile(r'<[^>]+>')


def _f_ruby(value):
    if not isinstance(value, str): return str(value) if value is not None else ''
    return _RUBY_RE.sub(r'<ruby>\1<rt>\2</rt></ruby>', value)

def _f_strip_furigana(value):
    if not isinstance(value, str): return str(value) if value is not None else ''
    return _FURIGANA_RE.sub('', value)

def _f_strip_html(value):
    if not isinstance(value, str): return str(value) if value is not None else ''
    return _HTML_RE.sub('', value)

def _f_where(value, **kwargs):
    if not isinstance(value, list): return []
    result = value
    for field, val in kwargs.items():
        result = [item for item in result if item.get(field) == val]
    return result

def _f_sort(value, field=None):
    if not isinstance(value, list): return []
    if field:
        def key(x):
            v = x.get(field, '') if isinstance(x, dict) else getattr(x, field, '')
            try: return (0, int(v))
            except (ValueError, TypeError): return (1, str(v))
        return sorted(value, key=key)
    return sorted(value)

def _f_default(value, fallback=''):
    return value if value else fallback

def _f_join(value, sep=''):
    if isinstance(value, list):
        return sep.join(str(v) for v in value)
    return str(value) if value is not None else ''

def _f_first(value):
    if isinstance(value, (list, tuple)) and value: return value[0]
    return None

def _f_last(value):
    if isinstance(value, (list, tuple)) and value: return value[-1]
    return None

def _f_length(value):
    return len(value) if hasattr(value, '__len__') else 0

def _f_int(value):
    try: return int(value)
    except (ValueError, TypeError): return 0

def _f_nl2br(value):
    if not isinstance(value, str): return str(value) if value is not None else ''
    return value.replace('\n', '<br>\n')

def _f_strip_paren(value):
    if not isinstance(value, str): return str(value) if value is not None else ''
    return re.sub(r'\s*\([^)]+\)\s*$', '', value)

def _f_slugify(value):
    if not isinstance(value, str): return ''
    s = value.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def _f_get(value, key=None):
    if isinstance(value, dict) and key:
        return value.get(key)
    return None

def _f_replace(value, old=None, new=None):
    if not isinstance(value, str): return str(value) if value is not None else ''
    if old is None: return value
    return value.replace(old, new or '')

def _f_split(value, sep=None):
    if not isinstance(value, str): return []
    return value.split(sep) if sep else value.split()


BUILTIN_FILTERS = {
    'ruby': _f_ruby,
    'strip_furigana': _f_strip_furigana,
    'strip_html': _f_strip_html,
    'where': _f_where,
    'sort': _f_sort,
    'default': _f_default,
    'join': _f_join,
    'first': _f_first,
    'last': _f_last,
    'length': _f_length,
    'int': _f_int,
    'nl2br': _f_nl2br,
    'strip_paren': _f_strip_paren,
    'slugify': _f_slugify,
    'get': _f_get,
    'replace': _f_replace,
    'split': _f_split,
}


# ── Renderer ───────────────────────────────────────────────────────

def _render(nodes, ctx, filters, loader=None):
    out = []
    for node in nodes:
        if isinstance(node, TextNode):
            out.append(node.text)
        elif isinstance(node, ExprNode):
            val = _eval_full(node.raw, ctx, filters)
            out.append(str(val) if val is not None else '')
        elif isinstance(node, ForNode):
            out.append(_render_for(node, ctx, filters, loader))
        elif isinstance(node, IfNode):
            out.append(_render_if(node, ctx, filters, loader))
        elif isinstance(node, SetNode):
            ctx.set(node.name, _eval_full(node.expr_raw, ctx, filters))
        elif isinstance(node, IncludeNode):
            if not loader:
                raise TemplateError(f"No loader for include: {node.path}")
            tpl = loader(node.path)
            inc_nodes = _parse(_tokenize(tpl))
            out.append(_render(inc_nodes, ctx, filters, loader))
    return ''.join(out)


def _render_for(node, ctx, filters, loader=None):
    iterable = _eval_full(node.iter_raw, ctx, filters)
    if not iterable:
        return _render(node.else_body, ctx, filters, loader)

    if isinstance(iterable, dict):
        iterable = list(iterable.items())
    items = list(iterable)
    if not items:
        return _render(node.else_body, ctx, filters, loader)

    out = []
    length = len(items)
    for i, item in enumerate(items):
        child = {
            'loop': {
                'index': i + 1,
                'index0': i,
                'first': i == 0,
                'last': i == length - 1,
                'length': length,
            }
        }
        if len(node.var_names) == 1:
            child[node.var_names[0]] = item
        else:
            if isinstance(item, (list, tuple)):
                for j, name in enumerate(node.var_names):
                    child[name] = item[j] if j < len(item) else None
            elif isinstance(item, dict):
                for name in node.var_names:
                    child[name] = item.get(name)
        out.append(_render(node.body, ctx.child(child), filters, loader))
    return ''.join(out)


def _render_if(node, ctx, filters, loader=None):
    for condition, body in node.branches:
        if _eval_full(condition, ctx, filters):
            return _render(body, ctx, filters, loader)
    return _render(node.else_body, ctx, filters, loader)


# ── Public API ─────────────────────────────────────────────────────

class Engine:
    def __init__(self, extra_filters=None, loader=None):
        self.filters = {**BUILTIN_FILTERS}
        if extra_filters:
            self.filters.update(extra_filters)
        self.loader = loader

    def render(self, template, context=None):
        """Render a template string with the given context dict."""
        tokens = _tokenize(template)
        nodes = _parse(tokens)
        ctx = Context(context or {})
        return _render(nodes, ctx, self.filters, self.loader)
