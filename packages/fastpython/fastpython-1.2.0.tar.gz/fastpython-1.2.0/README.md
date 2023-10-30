# FastPython v1.2.0

## v1.2.0 is here!!

This package allows you to use things faster, such as:
- Colored text w/ [ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)
- cls/clear command (Package chooses it automatically)
- Easy Error/Warn/Info messages
- Function debugging

## Installation

```bash
pip install fasterpython
```

# Using the package

## Class fastpython.OS

### fastpython.OS.GetOSInfo()
Gets some OS info.

Usage:
```python
from fastpython import fastpython

fastpython.OS.GetOSInfo()
```
Output (Example):
```
OS Identifier : nt
OS : Windows
```

### fastpython.OS.ClearScreen()
Clears the screen using a command thats based on your OS.
(e.g. The package chooses the command automatically [cls/clear])

Usage:
```python
from fastpython import fastpython

fastpython.OS.ClearScreen()
```

## Class fastpython.ANSI

### fastpython.ANSI.ColoredOutput(color: int, text: str {optional})
Prints text with the specified color (Uses [ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)). If you dont know any, please check fastpython.ANSI.ListColors().

Usage:
```python
from fastpython import fastpython

fastpython.ANSI.ColoredOutput(135, "Hello, World!")
```

Output:
Hello World in the color purple (\e[38;5;135mHello, World!)

### fastpython.ANSI.ListColors()
Gives a list of the ANSI colors

Usage:
```python
from fastpython import fastpython

fastpython.ANSI.ListColors()
```

Output:
All (0-255) ANSI colors.

## Class fastpython.Message

### fastpython.Message.Error(errtext: str)
Displays an error message.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Error("Error")
```

Output:
```
[X] Error
```

### fastpython.Message.Warn(warntext: str)
Displays a warning.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Warning("Warning")
```

Output:
```
[!] Warning
```

### fastpython.Message.Info(infotext: str)
Displays an information message.

Usage:
```python
from fastpython import fastpython

fastpython.Message.Info("Information")
```

Output:
```
[i] Information
```

## Class fastpython.Encoding

### Classes in fastpython.Encoding:
fastpython.Encoding.b16 (base16)
fastpython.Encoding.b32 (base32) 
fastpython.Encoding.b64 (base64) 
fastpython.Encoding.hex (hexademical) 
fastpython.Encoding.binary (binary)

### Encode/Decode:

#### Encode           
- b16.encode16(txtinput)
- b32.encode32(txtinput)
- b64.encode64(txtinput)
- hex.encodeHex(txtinput)
- bin.encodeBin(txtinput)

#### Decode
- b16.decode16(b16input)
- b32.decode32(b32input)
- b64.decode64(b64input)
- hex.decodeHex(hexinput)
- bin.decodeBin(bininput)

## Class Debugging
A class for debugging functions.

### @fastpython.Debugging.endedIn (decorator)
Once the function is finished, prints an exit message.

Example output:
```
[function my_function finished in 2.34810165s; exit code 0]
```

### @fastpython.Debugging.fullInfo (decorator)
Add some function info to an array, which can then be checked using GetFunctionInfo()

### fastpython.Debugging.GetFunctionInfo(functionName: str, raiseException=True)
Get info by the given function name.

Usage:
```python
from fastpython import *

@fastpython.Debugging.fullInfo
def helloWorld(times):
    for i in range(times):
        print("Hello, World!")
    return 100

helloWorld(50)
fastpython.Debugging.GetFunctionInfo("helloWorld")
```
Output:
```
Function Name: helloWorld
Is Running   : Exited (return code 50)
```

#### Thats It! A small update which i hope will help you!
## Hope you enjoy FastPython! =)

