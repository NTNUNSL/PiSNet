# PiSNet


### Usage: 

`python [scenario] [application settings] [iteration of experiments]`

- `scenario` is a python script which defined the user experiment.
- `application settings` is a configure file (`.cfg`) to the experiment script, defined the extra parameters.
- `iteration of experiments` is the number of experiment runs.

### Example:

`python example_1.py http_streaming.cfg 1` 

Above emulate `1` run of the `example_1.py` experiment with `http_streaming.cfg` configuration.


### Others:

- `machine.cfg` stores the machine information, including **IP address** and **port**.
- The folder `http_log` and `udp_log` is to **store the result of `tcpdump`**, you may want to change the setting in tcpdump section of `http_streaming.cfg` and `udp_streaming.cfg`.
- `example_1.py` runs no background traffic to `example_2.py`.