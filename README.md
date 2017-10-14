# beacon

Instructions and files to set up an Elixir-based beacon connected to a MySQL database.

## What is a Beacon?
Beacons are web-based discovery services for genetic variants. They are useful to know if the dataset present at any institution connected to the beacon network contains a given allele (or genetic variant). Beacons are an efficient way to share valuable genetic information without overly expose genomic data, due to privacy or security issues.

You can find more info on the Beacon Network at this page: [https://beacon-network.org/#/about](https://beacon-network.org/#/about). <br>
Beacon API v.0.3 can be found at this link: [https://github.com/ga4gh/beacon-team/releases/tag/v0.3.0](https://github.com/ga4gh/beacon-team/releases/tag/v0.3.0)   

## Purpose
This document illustrates how to set up a beacon based on the [Elixir beacon v.0.3](https://github.com/elixirhub/human-data-beacon) on a Linux server. This beacon is meant to work with variants stored in a **MySQL database**.

## Backend
These instructions follow those present on the Elixir Beacon's ones but differ from them for the setup of a MySQL database instead.

### Requirements:
* MySQL server
* Java 8 JDK
* Apache Maven 3

### Database setup:
Download the database containing the test data from [here](db/elixir_beacon_dev.sql), then restore it on your local machine:

<pre>
mysql -u [root] -p[root_password] elixir_beacon_dev < [path/to/downloaded/db.sql]
</pre>

From inside a MySQL shell, as root, create a new user named "microaccounts_dev", identified by a standard password 'r783qjkldDsiu', and grant it privileges over the newly-created database:

<pre>
CREATE USER 'microaccounts_dev'@'localhost' IDENTIFIED BY 'r783qjkldDsiu';
GRANT ALL ON elixir_beacon_dev TO 'microaccounts_dev'@'localhost';
FLUSH PRIVILEGES;
</pre>

### Java Beacon setup:
