#!/bin/sh

### Setup the following variables to configure cluster MR1/MR2 ###

# Topology
MASTER=localhost
NAMENODE=$MASTER
JOB_TRACKER=$MASTER
RESOURCE_MANAGER=$MASTER
SLAVES_FILE=slaves

# Java
CLUSTER_JAVA_HOME=/home/kasha/toolchain/sun-jdk-64bit-1.6.0.31

# Ports
HADOOP_BASE_PORT=23000 # DFS: +70, JT: +30

# Directories
HADOOP_TMP_DIR=/tmp/
HADOOP_LOG_DIR=/home/kasha/install/hadoop-logs

HDFS_BASE_DIR=/home/kasha/install/hdfs
DFS_NAME_DIR=$HDFS_BASE_DIR/name
DFS_DATA_DIR=$HDFS_BASE_DIR/data
MAPRED_LOCAL_DIR=$HDFS_BASE_DIR/mrlocal

# MR1 confs
TT_MAP_TASKS_MAX=4
TT_REDUCE_TASKS_MAX=2
MAPRED_CHILD_JAVA_OPTS="-Xmx1024m"
IO_SORT_MB=320
IO_SORT_RECORD_PERCENT=0.17
TT_HTTP_THREADS=8
REDUCE_PARALLEL_COPIES=4

