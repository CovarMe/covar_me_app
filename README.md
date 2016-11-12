## Set up 

### Generics
Note: Require _npm_ and _pip_
```
source cvenv/bin/activate
pip install -r Requirements.txt
npm i -g bower
bower install
```

### MongoDB (Database)
[Link for MongoDB install on Ubuntu](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)

### Flask (Web Framework)
[Link for Flask Quickstart](http://flask.pocoo.org/docs/0.11/quickstart/)

### Dev Infrastructure

* Hadoop
* Hive
* OpenTSDB (on HBase)

#### Cluster Setup
1. Set up [Hadoop on Mac](https://amodernstory.com/2014/09/23/installing-hadoop-on-mac-osx-yosemite/): `brew install hadoop` 
2. Install HBase: `brew install hbase`, [set to distributed mode and correct port](https://hbase.apache.org/book.html#quickstart) (9000 if you followed 1.)
3. [Install](http://opentsdb.net/docs/build/html/installation.html) and [configure](http://opentsdb.net/docs/build/html/user_guide/configuration.html) OpenTSDB: `brew install opentsdb` (note: `HBASE_HOME` is the installation folder of HBase on the Master Node, also see [setup wiki page](http://wiki.cvrgrid.org/index.php/OpenTSDB_Cluster_Setup#Installing_OpenTSDB)) 
4. Install Hive: `brew install hive`

#### Cluster StartUp
To just run all the services, kill the processes first and start with the following commands:
```
hstart
start-hbase.sh
tsdb tsd
hive
```

#### Database Setup
1. Setup the using the Python script e.g.: `python setup_opentsdb_metrics.py -s stocktickers.csv -m "price,ask,bid"`
2. Import time-series data using _import_timeseries.py_ e.g.: `python import_timeseries.py -H "http://localhost" -p 9001 -i 50 -s stocks.csv -m 'price' -c 'PRC' -t 'date' -n 'TICKER"`

