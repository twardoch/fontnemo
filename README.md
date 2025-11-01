# fontnemo

Python CLI tool that uses `fire` and `fonttools`, which modifies the font family portion only. 

## Name strings operation

The tool identifies the font's "Family Name" and "Family Slug". 

- Reference: @./vendors/fonttools/Snippets/rename-fonts.py
- Reference: @./vendors/fonttools/Lib/fontTools/varLib/instancer/names.py
- Reference: @./vendors/fonttools/ is a code snapshot of the `fonttools` package, but in our code we don’t use the `vendors` subfolder but simply the PyPI `fonttools` package

### `family_name`

#### Reading

Tool reads `family_name` from font nameID 16 (Typographic Family name). If doesn’t exist, from nameID 21 (WWS Family Name). If doesn’t exist, from nameID 1 (Font Family name). 

#### Editing

When the tool writes `new_family_name`, it replaces the old `family_name` in these nameID fields: 1, 4, 16, 18, 21

### `family_slug`

#### Reading

Tool reads `family_slug` from nameID 25 (Variations PostScript Name Prefix). If doesn’t exist, from nameID 6 (PostScript name) up to the first hyphen (if hyphen exists in string). 

#### Editing

When the tool writes `new_family_slug`, it replaces the old `family_slug` in these nameID fields: 6, 20, 25

SLUG_RULE: `new_family_slug` must be restricted to the printable ASCII subset, codes 33 to 126, except for the 10 characters '[', ']', '(', ')', '{', '}', '<', '>', '/', '%'. 

## CLI

### CLI command `view` (short synonym `v`)

Mandatory parameter: 

- `--input_path INPUTPATH`: input font file

Optional parameters: 

- `--long`: optional bool (default: False) 

Outputs: 

If not long: 

f"{family_name}"

If long: 

f"{input_path}:{family_name}"

### CLI command `new` (short synonym: `n`)

Mandatory parameter: 

- `--input_path INPUTPATH`: input font file
- `--new_family`: new family name

Optional parameters: 

- `--output_path OUTPUTPATH`: output font file
    - if not provided or equal `0`, replaces input file (see below)
    - if --output_path is `1`, then it replaces input file but before it does, we make a backup copy of the input file in such a way that we use the same base filename and we append `--TIMESTAMP` to it where TIMESTAMP is made according to TIME_RULE
    - if --output_path is `2`, then the output path is the input path with the `--TIMESTAMP` suffix added to the basename. 

TIME_RULE: current Unix timestamp expressed in lowercase base-36

Replacing input file is done safely: the fontTools library must write into a temporary file, and once this is done, we optionally produce the backup copy of the input file, and then finally we move the temporary file to the input path. 

Operation: 

1. Tool identifies `family_name` and `family_slug`
2. `new_family_name` = `new_family`
3. `new_family_slug` is built from `new_family_name` using SLUG_RULE
4. Tool replaces `family_name` with `new_family_name` and `family_slug` with `new_family_slug` in all nameIDs as described above. 

### CLI command `replace` (short synonym: `r`)

(`--input_path` and `--output_path` as previously)

Mandatory parameters: 

- `--find`: find string
- `--replace`: replace string

Operation: 

Analogical to `new` operation, except that: 

- `new_family_name` is made so that we take `family_name` and in there we replace `find` string with `replace_string`
- from `find` we build `find_slug` using SLUG_RULE, from `replace` we build `replace_slug` using SLUG_RULE, and `new_family_slug` is made so that we take `family_slug` and in there we replace `find_slug` with `replace_slug`

### CLI command `suffix` (short synonym: `s`)

(`--input_path` and `--output_path` as previously)

Mandatory parameters: 

- `--suffix`: suffix string

Operation: 

Analogical to `replace` operation, except that: 

- `new_family_name` is made so that we take `family_name` and append `suffix` to it
- from `suffix` we build `suffix_slug` using SLUG_RULE, and `new_family_slug` is made so that we take `family_slug` and append `suffix_slug`

### CLI command `prefix` (short synonym: `p`)

(`--input_path` and `--output_path` as previously)

Mandatory parameters: 

- `--prefix`: prefix string

Operation: 

Analogical to `suffix` operation, except that: 

- `new_family_name` is made so that we take `family_name` and prepend `prefix` to it
- from `prefix` we build `prefix_slug` using SLUG_RULE, and `new_family_slug` is made so that we take `family_slug` and prepend `prefix_slug`

### CLI command `timestamp` (short synonym: `t`)

(`--input_path` and `--output_path` as previously)

Optional parameter

- `--separator`: string, defaults to ` ` (space)

Operation: 

Specialized `suffix` operation in which we build suffix as follows: 

- it starts with the separator
- then it’s the timestamp build according to TIME_RULE 

---

