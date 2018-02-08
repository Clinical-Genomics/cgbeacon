# CGbeacon

Instructions and files to set up an Elixir-based beacon connected to a MySQL database.

- [What is a Beacon?](#what-is-a-beacon-)
- [Purpose](#purpose)
- [Backend](#backend)
  * [Requirements:](#requirements-)
  * [Database setup:](#database-setup-)
  * [Java Beacon installation:](#java-beacon-installation-)
  * [Beacon setup:](#beacon-setup-)
  * [Deploying the Beacon:](#deploying-the-beacon-)
  * [Queries:](#queries-)
  * [Populate the databases with your data](#populate-the-databases-with-your-data)
    + [Installation](#installation)
    + [Database settings](#database-settings)
    + [Usage](#usage)
- [User interface](#user-interface)


## What is a Beacon?
Beacons are web-based discovery services for genetic variants. They are useful to know if the dataset present at any institution connected to the beacon network contains a given allele (or genetic variant). Beacons are an efficient way to share valuable genetic information without overly expose genomic data, due to privacy or security issues.

You can find more info on the Beacon Network at this page: [https://beacon-network.org/#/about](https://beacon-network.org/#/about). <br>
Beacon API v.0.3 can be found at this link: [https://github.com/ga4gh/beacon-team/releases/tag/v0.3.0](https://github.com/ga4gh/beacon-team/releases/tag/v0.3.0)   

## Purpose
This document illustrates how to set up a beacon based on the [Elixir beacon v.0.3](https://github.com/elixirhub/human-data-beacon) on a Linux server. This beacon is meant to work with variants stored in a **MySQL database**.

## Backend
These instructions follow those present on the Elixir Beacon's ones but differ from them for the setup of a MySQL database instead.

### Requirements:
* MySQL server 5.7
* Java 8 JDK
* Apache Maven 3<br>

### Database setup:
From inside the MySQL shell, as root, create an empty database and name it 'elixir_beacon_dev':

<pre>
create database elixir_beacon_dev;
</pre>

Download the database data structure from [here](db/elixir_beacon_dev.sql) and restore it on your local machine:

<pre>
mysql -u [root] -p[root_password] elixir_beacon_dev < [path/to/downloaded/db.sql]
</pre>

You can also set up a production MySQL database with the same data structure. 
First create it from a MySQL shell:

<pre>
create database elixir_beacon_prod;
</pre>

Then import into it the same data structure as the devel one:

<pre>
mysql -u [root] -p[root_password] elixir_beacon_prod < [path/to/downloaded/db.sql]
</pre>

From inside a MySQL shell, as root, create a new user named "microaccounts_dev", identified by a standard password 'r783qjkldDsiu', and grant it privileges over the newly-created database:

<pre>
CREATE USER 'microaccounts_dev'@'localhost' IDENTIFIED BY 'r783qjkldDsiu';
GRANT ALL ON elixir_beacon_dev.* TO 'microaccounts_dev'@'localhost';
GRANT ALL ON elixir_beacon_prod.* TO 'microaccounts_dev'@'localhost';
FLUSH PRIVILEGES;
</pre><br>

### Java Beacon installation:
To create the Beacon jar executable clone the project in you working directory. From the terminal execute the command:

<pre>
git clone https://github.com/elixirhub/human-data-beacon.git
</pre>

From terminal enter the newly created folder and the nested elixir-core folder:

<pre>
cd human-data-beacon/elixir_core
</pre>

Since the beacon is going to connect to a MySQL server it is necessary to configure the java connectore as a Maven dependency.
Open the **pom.xml file under the elixir_core directory** and, under the ```<dependencies>``` block, add the following code:

```HTML
<!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.8-dmr</version>
</dependency>
```
(Older versions of the jdbc driver can be found [here](https://mvnrepository.com/artifact/mysql/mysql-connector-java)).<br><br>

Compile the code in the **elixir_core**:
<pre>
mvn clean compile jar:jar
mvn install
</pre>

Now you should see a new folder 'target' in your current directory. This folder should contain the jar file '**elixir-core-beacon_api_v0.3-SNAPSHOT.jar**'.<br><br>

### Beacon setup:
Before running the beacon it is necessary to change some settings in the following configuration file:<br><br>
**human-data-beacon/elixir_beacon/src/main/resources/application-dev.properties**<br><br>
Specifically, the server and management **default port of the beacon is port 9075**. This might be changed into another port number.<br>
To communicate with a MySQL server it is necessary to changed the following lines:

1. datasource.elixirbeacon.url = ~~jdbc:postgresql://127.0.0.1:5432/elixir_beacon_dev~~ must be changed into:
datasource.elixirbeacon.url = jdbc:mysql://127.0.0.1:3306(or_other_mysql_port)/elixir_beacon_dev

2. datasource.elixirbeacon.driverClassName = ~~org.postgresql.Driver~~ must be changed into:
datasource.elixirbeacon.driverClassName = com.mysql.jdbc.Driver

3. spring.jpa.properties.hibernate.dialect = ~~org.hibernate.dialect.PostgreSQLDialect~~ becomes:
spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.MySQLDialect

Other information such as the beacon id, name, description etc. can be customized by modifying parameters in this file. <br>
When deploying a new beacon it is also necessary to modify the file <br> <b>human-data-beacon/elixir_beacon/src/main/resources/application-dev.yml</b>. An example of these two files can be found in the folder [elixir_beacon_settings](elixir_beacon_settings).<br><br>

### Deploying the Beacon:
Next step is to compile and test the beacon. From terminal change directory to **human-data-beacon/elixir_beacon**. Then type:
<pre>
mvn clean compile package -Dspring.profiles.active="dev" -Dmaven.test.skip=true
</pre>

Note that the command -Dmaven.test.skip=true will make compiling skip the tests, but it is necessary because tests will fail when trying to connect on a non-PostgreSQL database, like in this case.<br>
In case of successfull compilation the executable named **elixir-beacon-0.3.jar** should appear under **human-data-beacon/elixir_beacon/target/**.
To run the jar, from terminal move into the target directory and type:
<pre>
java -jar elixir-beacon-0.3.jar --spring.profiles.active=dev
</pre>

The argument --spring.profiles.active=dev specifies the profile to be used. The other profile which could be used instead is 'test'. This latter profile requires the use and connection to a different database elixir_beacon_dev, described above.<br><br>

### Queries:

Once the beacon is started it operates at the default address: **http://localhost:9075/elixirbeacon/v03/beacon/**<br>
To ask the beacon for a variant on a given chromosome, compose a query using the following base syntax:<br>

<pre>
<b>http://localhost:9075/elixirbeacon/v03/beacon/query?</b>
</pre>

And the following parameters:


|Required/Optional|   Name	          | Accepted values        |  Example                   |
|:---------------:|:----------------------|:-----------------------|:---------------------------|
|R  	          |assemblyId             |a genome assembly       | assemblyId=GRCh37          |
|R   		  |referenceName          |1-22, X, Y, MT	   | referenceName=1            |
|R                |start	          |a number                | start=1138913              |
|O                |referenceBases         |the reference base      | referenceBases=C           |
|O                |alternate              |the variant of interest | alternateBases=T           |
|O                |datasetIds             |name of a dataset       | datasetIds=EGAD00000000028 |
|O                |includeDatasetResponses|true or false(default)  |includeDatasetResponses=true|

<br>So a typical query wold look like this:

http://localhost:9075/elixirbeacon/v03/beacon/query?assemblyId=GRCh37&referenceName=1&start=1138913&alternateBases=T&includeDatasetResponses=true<br>

The possible answer to a query to the beacon would be :

1. <b>"exists" : true</b>,  if the variant of interest is present within the beacon dataset.
2. <b>"exists" : false</b>, if a variant is present at the given position, but the base(s) is different than the one present in the query.
3. <b>"exists" : false</b>, if the chromosome and position given in the query do no match any entry in the database.



### Populate the databases with your data

You can use the software from this repository to parse VCF files and insert into the databases your own data.

#### Installation
Clone this repository in a local directory using the following command:
<pre>
git clone https://github.com/Clinical-Genomics/cgbeacon.git
</pre>

Change directory to the newly created folder:
<pre>
cd cgbeacon
</pre>

Install the package:
<pre>
pip install .
</pre>

#### Database settings
Database settings are specified by the connection string passed to the program. This string should have this format:
<pre>
mysql+pymysql://db_user:db_password@db_host:db_port/db_name
</pre>
If not provided by the user the following connection string is passed to the program: mysql+pymysql://microaccounts_dev:r783qjkldDsiu@localhost:3306/elixir_beacon_dev

#### Usage
The program parses variants from a VCF file. Samples to be included in the Beacon database and variant quality threshold might be specified as optional parameters.

To execute the program:
<pre>
cgbeacon --vcf path_to_vcf_file --dataset dataset_name
</pre>

Optional parameters:

<pre>
--db_connection (mysql+pymysql://db_user:db_password@db_host:db_port/db_name)
--qual [0-99] (variant quality threshold. default=20)
--ref chr_build (reference genome build, default is grch37)
--use_panel path_to_gene_panel_bed_file (filter VCF file to use only intervals from a gene panel)
--outfile (name of the pdf output file with the results of submission to Beacon)
--customer customer_id (a text string with the name of the customer/institution owning the samples in the VCF file)
[list of samples to process separated by space] (Default is all samples found in the VCF file)
</pre>

## User interface
A simple front-end query Flask app to the Clinical Genomics Beacon is available under the [UI folder](UI). Download the compressed archive and uncompress it in the folder where you want to run the app from.
To run it, change directory to the cgbeacon_UI folder and launch it with python 3:

<pre>
cd cgbeacon_UI
python3 run.py
</pre>

Your query interface should be now available from a web browser page at the following address:
<pre>
http://127.0.0.1:5000/
</pre>

The app is designed to connect via SQL Alchemy to a default MySQL database present on the same machine as the app, but you can customize the connections parameter by modifying the parameter "SQLALCHEMY_DATABASE_URI" in the config file present in the "instance" folder.
