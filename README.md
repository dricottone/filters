# filters

## Usage

```
filter METHOD [OPTIONS]
```

Command line data filtering.

Available `METHOD`s are: `ab`, `kalman`, and `convolve`. Use `filter METHOD --help` to see available options.

```
rng DISTRIBUTION [OPTIONS]
```

Command line data generation.

Available `DISTRIBUTION`s are: `normal`, `uniform`, and `notrandom`. Use `rng DISTRIBUTION --help` to see available options.


## Example

```sh
$ rng uniform --mu 100 --delta 5 --offset 10 \
  | filter ab --report --delta 5 --initial 100
Alpha-beta filter
  α=0.0500, β=0.0050
  Initial estimate: 100.0000 changing 5.0000 per time unit
Raw:      Est.:
========  ========
109.8960  105.2448
 99.0558  109.7086
119.8484  114.9356
115.0693  119.6868
119.0251  124.3752
126.9214  129.1972
127.7748  133.8095
133.2530  138.4348
145.2687  143.4037
136.5438  147.6973
```


## Licensing

This software is distributed under the GPL license.

