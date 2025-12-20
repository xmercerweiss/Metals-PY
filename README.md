# Metals-PY
A simple script that displays the prices of various precious metals; wrote this up to help keep track of the value of my investments. Data is scraped from 
`https://www.kitco.com/api/kitco-xml/precious-metals`. Optionally accepts a file of key-value pairs representing a portfolio of metals to be
evaluated. Such a file consists of case-insensitive metal names mapped to a number of [pennyweight](https://en.wikipedia.org/wiki/Pennyweight),
such as...
```ini
GOLD=20      # 20dwt = 1oz
silver=400   # 400dwt = 20oz
PLATinum=10  # 10dwt = 0.5oz
```

Pennyweight is used in order to track amounts less than 1oz without creating the potential for floating-point arithmetic errors. Pass such
a configuration file to the script as a command-line argument.

## License
This project is licensed under the permissive Zero-Clause BSD License. Copyright 2025, Xavier Mercerweiss.
