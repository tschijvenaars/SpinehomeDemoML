# SpinehomeDemoML

This page is dedicated to the Spinehome Machine Learning Demo.
The application is very straightforward and the UI will speak for itself.

Note: The application is only for demonstrative use only and is in no means suitable for deployment on the web.

### Installing

For this project, a lot of libraries are used. Install them through the following commands:

```
pip install dash==0.21.1
pip install dash-renderer==0.12.1
pip install dash-html-components==0.10.1
pip install dash-core-components==0.22.1
pip install plotly --upgrade

pip install pandas
pip install scapy
pip install kmodes
pip install -U scikit-learn
```

### Running

To run this project, after selecting the right working directory, use the following command:

```
python main.py
```

### Docker integration
```
sudo docker build . -t spinehome:no-debug
sudo docker run -it -p 8050:8050 spinehome:no-debug
```

### Example Input

The following example input input can be used for the machine learning demo page:

Router Type:
```
‘Apple AirPort’, ‘Unknown’
```

Router Software:
```
‘Unknown’
```

Processor:
```
‘Intel Core i5’, ‘Intel Core i3’, ‘Intel Core i7’, ‘Intel Core i5-4460’, ‘Intel Pentium’, ‘Intel Celeron’, ‘Unknown’
```

Network Card:
```
‘Unknown’, ‘Apple Broadcom’, ‘Apple BCM5701’, ‘Realtek 8723BE’, ‘Realtek PCIe GBE Family Controller’, ‘TP-LINK Wireless USB Adapter’
```
