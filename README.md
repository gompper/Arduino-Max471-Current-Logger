# Arduino MAX471 Current Logger
This project uses the MAX471 IC to log the current used by a in series connected consumer.

## How it's done
Acquired data is averaged over 64 samples and sent via serial connection to PC. Averaging is done to increase the sample rate, because serial connection is slower than sampling rate.

## Wiring
Wiring is done analog to this [diagram](https://wolles-elektronikkiste.de/wp-content/uploads/2020/08/max471___Basic-1024x609.png)

## Usage
1. Connect the Board and Consumer according to [Wiring](#wiring).
2. Upload the Arduino Code
3. Start the [client](./py/serial_read.py) on the PC:
```
$python3 ./py/serial_read.py
```

## Plot
If you want to plot data separately use the script [`./py/plot_amps.py`](./py/plot_amps.py):
```
$ python3 ./py/plot_amps.py <./path/to/data.npy>
```