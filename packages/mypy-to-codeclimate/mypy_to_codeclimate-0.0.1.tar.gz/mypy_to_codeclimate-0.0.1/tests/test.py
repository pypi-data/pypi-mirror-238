# Valid issues to be parsed
"""dir/module.py:2: error: Description"""
"module.py:2: error: Description"
"module.py:2: error: Description"
"module.py:2: note: Description"
"module.py:2: egg: Description"
"module.py:2: error: Description"
'module.py:2: error: Description "abc" [123] (eee)'
"module.py:2: error: Description  [error-code]"
"module.py:2:5: error: Description"
"""long/path.py:513: error: Return type "Test" of "get_metadata" incompatible with return type "None" in supertype "TotoTest"  [override]"""

# COmplete with no errors
"Success: no issues found in 1 source file"
"Success: no issues found in 360 source files"
# Complete with errors
"Found 5 errors in 1 file (checked 1 source file)"
"Found 5 errors in 3 files (checked 360 source files)"
# Fatal error (code 2)
"mypy: can't read file 'doesnotexist.py': No such file or directory"
"fatal error because mypy is a teapot"
