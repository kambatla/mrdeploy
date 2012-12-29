#!/bin/bash

#usage mr1-setup-conf.sh <master> <base_port>

USER=kasha
MASTER=$1
HADOOP_BASE_PORT=$2
JAVA_HOME=$3

#####################################################################################################

# DFS WebUI 23070
# JT WebUI 23030

NAMENODE=$MASTER
JOB_TRACKER=$MASTER

NAMENODE_PORT=$(($HADOOP_BASE_PORT + 10))
DFS_DATANODE_PORT=$(($HADOOP_BASE_PORT + 20))
DFS_DATANODE_IPC_PORT=$(($HADOOP_BASE_PORT + 21))
DFS_HTTP_PORT=$(($HADOOP_BASE_PORT + 70))

JOB_TRACKER_PORT=$(($HADOOP_BASE_PORT + 11))
JOB_TRACKER_HTTP_PORT=$((HADOOP_BASE_PORT + 30))

XML_CONFIGS='core-site.xml hdfs-site.xml mapred-site.xml'

for FILE in $XML_CONFIGS; do
  sed -i -e "s|@NAMENODE@|$NAMENODE|" $FILE
  sed -i -e "s|@NAMENODE_PORT@|$NAMENODE_PORT|" $FILE
  sed -i -e "s|@DFS_DATANODE_PORT@|$DFS_DATANODE_PORT|" $FILE
  sed -i -e "s|@DFS_DATANODE_IPC_PORT@|$DFS_DATANODE_IPC_PORT|" $FILE
  sed -i -e "s|@DFS_HTTP_PORT@|$DFS_HTTP_PORT|" $FILE
  sed -i -e "s|@JOB_TRACKER@|$JOB_TRACKER|" $FILE
  sed -i -e "s|@JOB_TRACKER_PORT@|$JOB_TRACKER_PORT|" $FILE
  sed -i -e "s|@JOB_TRACKER_HTTP_PORT@|$JOB_TRACKER_HTTP_PORT|" $FILE
  sed -i -e "s|@USER@|$USER|" $FILE
done

sed -i -e "s|@JAVA_HOME@|$JAVA_HOME|" 'hadoop-env.sh'

echo $MASTER > masters
