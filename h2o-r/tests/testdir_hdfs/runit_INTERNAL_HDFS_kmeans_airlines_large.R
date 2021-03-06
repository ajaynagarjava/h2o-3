#----------------------------------------------------------------------
# Purpose:  This test runs k-means on the full airlines dataset.
#----------------------------------------------------------------------




#----------------------------------------------------------------------
# Parameters for the test.
#----------------------------------------------------------------------

# Check if we are running inside the H2O network by seeing if we can touch
# the namenode.
hadoop_namenode_is_accessible = hadoop.namenode.is.accessible()

if (hadoop_namenode_is_accessible) {
    hdfs_name_node = hadoop.namenode()
    hdfs_file = "/datasets/airlines_all.csv"
} else {
    stop("Not running on H2O internal network.  No access to HDFS.")
}

#----------------------------------------------------------------------

heading("BEGIN TEST")
check.kmeans_airlines <- function() {

  #----------------------------------------------------------------------
  # Single file cases.
  #----------------------------------------------------------------------

  heading("Import airlines_all.csv from HDFS")
  url <- sprintf("hdfs://%s%s", hdfs_name_node, hdfs_file)
  airlines.hex <- h2o.importFile(url)
  n <- nrow(airlines.hex)
  print(paste("Imported n =", n, "rows"))

  heading(paste("Run k-means++ with k = 7 and max_iterations = 10"))
  myX <- c(1:8, 10, 12:16, 19:21, 25:29)
  airlines.km <- h2o.kmeans(training_frame = airlines.hex, x = myX, k = 7, init = "Furthest", max_iterations = 10, standardize = TRUE)
  airlines.km

  
}

doTest("K-means on Airlines dataset", check.kmeans_airlines)
