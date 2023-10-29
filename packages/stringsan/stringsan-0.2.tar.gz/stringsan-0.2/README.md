# Stringsan : String manipulation package
This package contains functions related to strings and regex so that I do not have to type them every time. 

# Getting Started
```py
from stringsan.strings import occurrences

MESSAGE = "This is a string which contains a string which contains another string and string? Is it a string?"

print(occurrences(MESSAGE, "string"))
```

Or, compress a string!

```py
from stringsann.strings import compress_string
MESSAGE = "aaaaaaaaaaaaaaaaaabbbbeeebeeeeeeeeeeeeeeeeccccccccccccccccccc"

print(compress_string(MESSAGE))
```

Check out more functions in the `/stringsan`
