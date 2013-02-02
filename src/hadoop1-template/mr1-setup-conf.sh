#!/bin/sh

#usage mr1-setup-conf.sh <master> <base_port> <java_home> <HDFS_BASE_DIR>

. ./setup-env.sh

## Port configuration
# DFS
NAMENODE_PORT=$(($HADOOP_BASE_PORT + 10))
DFS_DATANODE_PORT=$(($HADOOP_BASE_PORT + 20))
DFS_DATANODE_IPC_PORT=$(($HADOOP_BASE_PORT + 21))
DFS_HTTP_PORT=$(($HADOOP_BASE_PORT + 70))

# MR1
JOB_TRACKER_PORT=$(($HADOOP_BASE_PORT + 11))
JOB_TRACKER_HTTP_PORT=$((HADOOP_BASE_PORT + 30))

XML_CONFIGS='core-site.xml hdfs-site.xml mapred-site.xml hadoop-env.sh'

for FILE in $XML_CONFIGS; do
  sed -i -e "s|@JAVA_HOME@|$CLUSTER_JAVA_HOME|" $FILE
  sed -i -e "s|@NAMENODE@|$NAMENODE|" $FILE
  sed -i -e "s|@NAMENODE_PORT@|$NAMENODE_PORT|" $FILE
  sed -i -e "s|@DFS_DATANODE_PORT@|$DFS_DATANODE_PORT|" $FILE
  sed -i -e "s|@DFS_DATANODE_IPC_PORT@|$DFS_DATANODE_IPC_PORT|" $FILE
  sed -i -e "s|@DFS_HTTP_PORT@|$DFS_HTTP_PORT|" $FILE
  sed -i -e "s|@JOB_TRACKER@|$JOB_TRACKER|" $FILE
  sed -i -e "s|@JOB_TRACKER_PORT@|$JOB_TRACKER_PORT|" $FILE
  sed -i -e "s|@JOB_TRACKER_HTTP_PORT@|$JOB_TRACKER_HTTP_PORT|" $FILE

  sed -i -e "s|@HADOOP_TMP_DIR@|$HADOOP_TMP_DIR|" $FILE
  sed -i -e "s|@HADOOP_LOG_DIR@|$HADOOP_LOG_DIR|" $FILE 
  sed -i -e "s|@DFS_DATA_DIR@|$DFS_DATA_DIR|" $FILE
  sed -i -e "s|@DFS_NAME_DIR@|$DFS_NAME_DIR|" $FILE
  sed -i -e "s|@MAPRED_LOCAL_DIR@|$MAPRED_LOCAL_DIR|" $FILE

  sed -i -e "s|@TT_MAP_TASKS_MAX@|$TT_MAP_TASKS_MAX|" $FILE
  sed -i -e "s|@TT_REDUCE_TASKS_MAX@|$TT_REDUCE_TASKS_MAX|" $FILE
  sed -i -e "s|@TT_HTTP_THREADS@|$TT_HTTP_THREADS|" $FILE
  sed -i -e "s|@REDUCE_PARALLEL_COPIES@|$REDUCE_PARALLEL_COPIES|" $FILE
  sed -i -e "s|@IO_SORT_MB@|$IO_SORT_MB|" $FILE
  sed -i -e "s|@IO_SORT_RECORD_PERCENT@|$IO_SORT_RECORD_PERCENT|" $FILE
  sed -i -e "s|@MAPRED_CHILD_JAVA_OPTS@|$MAPRED_CHILD_JAVA_OPTS|" $FILE
done

echo $MASTER > masters
