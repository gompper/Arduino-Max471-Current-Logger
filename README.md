# Arduino MAX471 Current Logger
This project uses the MAX471 IC to log the current used by a in series connected consumer.

## How it's done
Acquired data is averaged over 64 samples and sent via serial connection to PC. Averaging is done to increase the sample rate, because serial connection is slower than sampling rate.

## Wiring
Wiring is done analog to this [diagram](https://wolles-elektronikkiste.de/wp-content/uploads/2020/08/max471___Basic-1024x609.png)

## Plot
Data gets plotted after receiving it via serial connection using the main client [`./py/serial_read.py`](./py/serial_read.py):
```
$python3 ./py/serial_read.py
```
, but can separately be read using the the script [`./py/plot_amps.py`](./py/plot_amps.py):
```
$ python3 ./py/serial_read.py <./path/to/data.npy>
```