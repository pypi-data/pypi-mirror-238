import datetime

from delta.tables import DeltaTable
from pyspark.sql.functions import row_number, col, to_timestamp, lit
from pyspark.sql.window import Window

from com.phida.main.DataConfig import HVR_INTEG_KEY, SOURCE_OPERATION, SRC_COMMIT_TIME, UPDATESTAMP, \
    MON_DATE_YEAR_HR_MN_SEC, OPERATION_DELETE, OPERATION_PRE_UPDATE, MON_DATE_YEAR, ADLS_LOADED_DATE
from com.phida.main.Operations import tableExists, addDerivedColumns, createDeltaTable, alterDeltaTable, \
    dropColumns, schemaDiff, getKeyCols, buildJoinCondition, buildColumnsDict, hiveDDL, \
    schemaDataTypeDiff, hasColumn, initialMultilineRead, checkIfFirstRun, writeDataframeToTable
from com.phida.main.sparksession import spark, logger
from com.phida.main.utils import pathExists, convertStrToList, filePathExists


class SilverOperations:
    """
    A pipeline for cleansing and streaming incremental data from Bronze table and merge into Silver as well as
    transferring full load csv to silver delta

    args:
        srcFilePath: String - Source File (Raw Data File)
        srcDatabaseName: String - Source Database (typically Bronze)
        srcTableName: String - Source Table Name
        tgtDatabaseName: String - Target Database Name (Will be created if not exists)
        tgtTableName: String - Target Table Name (Will be created if not exists)
        tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
        tgtTablePath: String - Target Table Path (so that the table is created as external)
        tgtPartitionColumns: String - Target partition columns (optional)
        derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
        triggerOnce: String - Whether continuous streaming or just once
        dropColumnStr: String - Columns to be dropped from source table df
        pruneColumn: String - Column for applying the prune filter in the merge ON condition clause \
                              (to improve performance of the merge)
        containsTimestamp: String - Does the source file contain timestamp

    methods:
        silverCleansing
        prepareTarget
        upsertToDelta
        streamIntoDeltaTarget

    example:
        from com.phida.SilverMerge import SilverMerge
        silverMergeObj = SilverMerge(srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn)

    """

    def __init__(self, srcFilePath, srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn, containsTimestamp):
        """
        desc:
            Initialize the required class variables

        args:
            srcFilePath: String - Source File (Raw Data File)
            srcDatabaseName: String - Source Database (typically Bronze)
            srcTableName: String - Source Table Name
            tgtDatabaseName: String - Target Database Name (Will be created if not exists)
            tgtTableName: String - Target Table Name (Will be created if not exists)
            tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
            tgtTablePath: String - Target Table Path (so that the table is created as external)
            tgtPartitionColumns: String - Target partition columns (optional)
            derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
            triggerOnce: String - Whether continuous streaming or just once
            dropColumnStr: String - Columns to be dropped from source table df
            pruneColumn: String - Column to use for dynamic file pruning (future feature)
            containsTimestamp: String - Does the source file contain timestamp

        """

        logger.info("phida_log: Initialising class variables")
        self.srcFilePath = srcFilePath
        self.srcDatabaseName = srcDatabaseName
        self.srcTableName = srcTableName
        self.tgtDatabaseName = tgtDatabaseName
        self.tgtTableName = tgtTableName
        self.tgtCheckpoint = tgtCheckpoint
        self.tgtTablePath = tgtTablePath
        self.tgtPartitionColumns = tgtPartitionColumns
        self.derivedColExpr = derivedColExpr
        self.triggerOnce = triggerOnce
        self.dropColumnStr = dropColumnStr
        self.pruneColumn = pruneColumn
        self.containsTimestamp = (containsTimestamp == "Y")

        if self.containsTimestamp:

            logger.info(f"phida_log: Check if source table {self.srcDatabaseName}.{self.srcTableName} exists")

            if tableExists(self.srcDatabaseName, self.srcTableName):
                logger.info(f"phida_log: source table exists")

                logger.info(f"phida_log: initialising derived class variables")

                self.srcDF = spark.readStream.table(self.srcDatabaseName + "." + self.srcTableName)

                self.isDataSourceHVR = hasColumn(self.srcDF, HVR_INTEG_KEY)

                self.keyCols = getKeyCols(self.srcDatabaseName, self.srcTableName)

                self.keyColsList = convertStrToList(self.keyCols, ",")

                self.joinCondition = buildJoinCondition(self.keyColsList)

                self.condition = f"{self.pruneColumn} <> '' AND {self.joinCondition}" if self.pruneColumn.strip() \
                    else self.joinCondition

                self.dropColumnList = convertStrToList(self.dropColumnStr, ",")

                self.columnsDict = buildColumnsDict(self.srcDF, self.dropColumnList)
        else:
            if filePathExists(self.srcFilePath):
                logger.info(f"phida_log: source file exists")
                logger.info(f"phida_log: initialising derived class variables")

                utc_now = datetime.datetime.utcnow()
                self.currentDate = utc_now.strftime(MON_DATE_YEAR)

    def silverCleansing(self):
        """
        desc:
            A Method for reading from source table (Bronze) as a stream and apply cleansing transformations

        args:
            None

        return:
            silverCleansedDF: DataFrame - returns the bronze dataframe after cleansing

        example:
            silverCleansing()

        tip:
            N/A
        """
        logger.info(f"phida_log: applying cleansing rules on source dataframe ")

        if tableExists(self.srcDatabaseName, self.srcTableName):

            silverRawDF = self.srcDF

            if self.derivedColExpr:
                derivedColExprList = convertStrToList(self.derivedColExpr, "§")

                silverDerivedColumns = addDerivedColumns(silverRawDF, derivedColExprList)

            else:
                silverDerivedColumns = silverRawDF

            self.columnsDict = buildColumnsDict(silverDerivedColumns, self.dropColumnList)

            return silverDerivedColumns

    def prepareTarget(self, inDF):
        """
        desc:
            A Method for preparing the target delta table.
            Creates the delta table if it does not exists
            Raise error if there are missing column(s) 
            Raise error if data types are different between existing table and source table
            Alters the delta table if there is new column added in the source schema

        args:
            inDF: DataFrame - input spark dataframe (typically the output of silverCleansing())

        return:
            None - Does not return anything - Just creates or alters the target delta table

        example:
            prepareTarget(silverCleansedDF)

        tip:
            N/A
        """
        logger.info(f"phida_log: preparing the target delta table ")

        targetTableExists = tableExists(self.tgtDatabaseName, self.tgtTableName)

        targetPathExists = pathExists(self.tgtTablePath)

        inDF = dropColumns(inDF, self.dropColumnList)

        first_run = False if (targetTableExists & targetPathExists) else True

        if first_run:

            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            createDeltaTable(inDF,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

        else:

            existingDF = spark.read.table(self.tgtDatabaseName + "." + self.tgtTableName)

            diff2DF = schemaDiff(existingDF, inDF)

            if diff2DF.columns:
                raise Exception(f"Column(s) {diff2DF.columns} is(are) missing")

            mismatched_columns = schemaDataTypeDiff(existingDF, inDF)

            if mismatched_columns:
                raise Exception(f"There is data type mismatch in column(s): {mismatched_columns}")

            diffDF = schemaDiff(inDF, existingDF)

            addColumns = hiveDDL(diffDF)

            if addColumns:
                logger.info(f"phida_log: There seems to be a schema change in silver")
                logger.info(f"phida_log: Altering the target table {self.tgtDatabaseName}.{self.tgtTableName}")

                alterDeltaTable(self.tgtDatabaseName, self.tgtTableName, addColumns)

                logger.info(f"phida_log: newly added columns {addColumns}")

            else:
                logger.info(f"phida_log: There is no change in schema in silver")

    def upsertToDelta(self, microBatchOutputDF, batchId):
        """
        desc:
            A Function for merging the records from a given dataframe into delta Target table (foreachBatch)

        args:
            microBatchOutputDF: DataFrame -
            batchId: BigInt - required by the foreachBatch stream processor

        return:
            None - Does not return anything - This function is used by foreachbatch in streamIntoDeltaTarget

        example:
            N/A - see method streamIntoDeltaTarget() for usage

        tip:
            N/A
        """

        microBatchOutputDF = microBatchOutputDF.filter(f"{SOURCE_OPERATION} in (0,1,2,3)")

        if self.isDataSourceHVR:
            windowSpec = Window.partitionBy(self.keyColsList) \
                .orderBy(col(SRC_COMMIT_TIME).desc(), col(HVR_INTEG_KEY).desc())
        else:
            windowSpec = Window.partitionBy(self.keyColsList) \
                .orderBy(to_timestamp(col(UPDATESTAMP), MON_DATE_YEAR_HR_MN_SEC).desc())

        microBatchOutputDF = microBatchOutputDF.withColumn("latest_record", row_number().over(windowSpec)) \
            .filter("latest_record == 1").drop("latest_record")

        tgtDeltaTable = DeltaTable.forName(spark, self.tgtDatabaseName + "." + self.tgtTableName)

        tgtDeltaTable.alias("t").merge(microBatchOutputDF.alias("s"), self.condition) \
            .whenMatchedDelete(f"s.{SOURCE_OPERATION} in ({OPERATION_DELETE},{OPERATION_PRE_UPDATE})") \
            .whenMatchedUpdate(condition=f"s.{SOURCE_OPERATION} not in ({OPERATION_DELETE},{OPERATION_PRE_UPDATE})",
                               set=self.columnsDict) \
            .whenNotMatchedInsert(condition=f"s.{SOURCE_OPERATION} not in ({OPERATION_DELETE},{OPERATION_PRE_UPDATE})",
                                  values=self.columnsDict) \
            .execute()

    def streamIntoDeltaTarget(self):
        """
        desc:
            A Function for writing the given streaming dataframe into Delta Target table with foreachBatch merge
            Main layer the triggers/kicks off the entire process of reading from Bronze and merging into silver.
        args:
            None

        return:
            outputDF: DataFrame - Returns a spark streaming dataframe that writes into target delta table

        example:
            streamIntoDeltaTarget()

        tip:
            N/A
        """

        silverCleansedDF = self.silverCleansing()

        self.prepareTarget(silverCleansedDF)

        logger.info(f"phida_log: performing streaming merge on target {self.tgtDatabaseName}.{self.tgtTableName}")

        if self.triggerOnce == "Y":
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .trigger(once=True)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )
        else:
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )

        return outputDF

    def overwriteToDeltaTarget(self):
        """
        desc:
            A Function for writing the given source file into Delta Target table
        args:
            None

        return:
            None - Does not return anything

        example:
            overwriteToDeltaTarget()

        tip:
            Make sure the values provided in the notebook are correct
        """
        logger.info(f"phida_log: preparing the target delta table ")

        first_run = checkIfFirstRun(self.tgtDatabaseName, self.tgtTableName, self.tgtTablePath)

        source_df = initialMultilineRead(self.srcFilePath, "|", True)

        raw_refined_df = source_df.withColumn(ADLS_LOADED_DATE, lit(self.currentDate).cast("string"))

        if first_run:
            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            createDeltaTable(source_df,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

            writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, raw_refined_df,
                                  "overwriteSchema", "overwrite")

            logger.info(
                f"phida_log: first write into bronze table {self.tgtDatabaseName}.{self.tgtTableName} completed")
        else:
            delete_table = spark.sql(f'''Truncate table {self.tgtDatabaseName}.{self.tgtTableName}''')

            writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, raw_refined_df,
                                  "overwriteSchema", "overwrite")
