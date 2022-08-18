<div align="center">
  <img src="./logo.png"/>
  <p>
    A CLI tool to build desktop applications with Neutralinojs and Python as backend
  <p>
</div>

<hr />

Thanks to [Neutralinojs][1]'s extension system, which allows us to spawn a process and communicate with it. `neutrapy` maintains both the app and the extension written in Python. Also thanks to [`PyOxidizer`][3] that compiles Python code to into binary so that it can be shipped with the app.

## Example

![example](./example.png)

The example is generated by `neutrapy create -n example`. It isn't the same as the offical example, called [litePy][4], from Neutralinojs. The official one saves the code into a temporary file and executes it by spawn a python process, which is just a one-way communication. `neutrapy` uses [websocket_client][5] for the extension to communicate with the Neutralino server. This enables a bi-directional communication between the frontend and backend.

## Installation

```bash
$ pip install -U neutrapy
# Installs the latest version of neutrapy
```

## Documentation

[https://pwwang.github.io/neutrapy/][6]


## Credits

- [neutralinojs][1]
- [PyOxidizer][3]
- [neutralino_python_extension_sample][2]

[1]: https://neutralino.js.org/
[2]: https://github.com/danidre14/neutralino_python_extension_sample
[3]: https://github.com/indygreg/PyOxidizer
[4]: https://github.com/codezri/litepy
[5]: https://github.com/websocket-client/websocket-client
[6]: https://pwwang.github.io/neutrapy/
