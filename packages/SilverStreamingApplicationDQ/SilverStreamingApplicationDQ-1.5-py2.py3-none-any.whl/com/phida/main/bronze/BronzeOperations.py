import datetime

from pyspark.sql import Window
from pyspark.sql.functions import lit, to_timestamp, row_number, col

from com.phida.main.DataConfig import SOURCE_OPERATION, ADLS_LOADED_DATE, OPERATION_INSERT, SRC_KEY_COLS, \
    OPERATION_UPDATE, UPDATESTAMP, MON_DATE_YEAR_HR_MN_SEC, OPERATION_DELETE, MON_DATE_YEAR
from com.phida.main.Operations import createDeltaTable, hiveDDL, initialMultilineRead, multilineRead, checkIfFirstRun, \
    writeDataframeToTable, checkForSchemaChanges
from com.phida.main.sparksession import logger, spark
from com.phida.main.utils import filePathExists, convertStrToList


class BronzeOperations:
    """
    A pipeline to help transfer full load data from RAW csv files to delta Bronze tables

    args:
        srcFilePath: String - Source File (Raw Data File)
        tgtDatabaseName: String - Target Database Name (Will be created if not exists)
        tgtTableName: String - Target Table Name (Will be created if not exists)
        tgtTablePath: String - Target Table Path (so that the table is created as external)
        tgtTableKeyColumns: String - Column names separated by comma to help identify the primary key for the
                                     target table
        tgtPartitionColumns: String - Target partition columns (optional)
        containsTimestamp: String - Does the source file contain timestamp(Y or N)

    methods:
        bronzeCleansing
        prepareTarget

    example:
        from com.phida.main.bronze.BronzeAppend import BronzeAppend
        bronzeAppendObj = BronzeAppend(srcFilePath, tgtDatabaseName, tgtTableName,
                                        tgtTablePath, tgtTableKeyColumns, tgtPartitionColumns, containsTimestamp)

    """

    def __init__(self, srcFilePath, tgtDatabaseName, tgtTableName, tgtTablePath, tgtTableKeyColumns,
                 tgtPartitionColumns, containsTimestamp):
        """
        desc:
            Initialize the required class variables

        args:
            srcFilePath: String - Source File Path(Raw Data File. Currently, supports only .csv files)
            tgtDatabaseName: String - Target Database Name (Will be created if not exists)
            tgtTableName: String - Target Table Name (Will be created if not exists)
            tgtTablePath: String - Target Table Path (so that the table is created as external)
            tgtTableKeyColumns: String - Column names separated by comma to help identify the primary key
                                         for the target table
            tgtPartitionColumns: String - Target partition columns (optional)
            containsTimestamp: String - Does the source file contain timestamp(Y or N)

        """

        logger.info("phida_log: Initialising class variables for raw to bronze delta transfer")

        self.srcFilePath = srcFilePath
        self.tgtDatabaseName = tgtDatabaseName
        self.tgtTableName = tgtTableName
        self.tgtTablePath = tgtTablePath
        self.tgtTableKeyColumns = tgtTableKeyColumns
        self.tgtPartitionColumns = tgtPartitionColumns
        self.containsTimestamp = (containsTimestamp == "Y")

        if filePathExists(self.srcFilePath):
            logger.info(f"phida_log: source file exists")
            logger.info(f"phida_log: initialising derived class variables")

            self.keyColsList = convertStrToList(self.tgtTableKeyColumns, ",")

            utc_now = datetime.datetime.utcnow()
            self.currentDate = utc_now.strftime(MON_DATE_YEAR)

            if self.containsTimestamp:
                self.columnsToBeAppendedInBronze = [SOURCE_OPERATION, SRC_KEY_COLS, ADLS_LOADED_DATE]
            else:
                self.columnsToBeAppendedInBronze = [ADLS_LOADED_DATE]

    def appendInsertsToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify inserts b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendInsertsToBronze(source_df, target_df)

        tip:
            N/A
        """
        inserts_df = source_df.join(target_df, self.keyColsList, "leftanti") \
            .withColumn(SOURCE_OPERATION, lit(OPERATION_INSERT)) \
            .withColumn(SRC_KEY_COLS, lit(self.tgtTableKeyColumns)) \
            .withColumn(ADLS_LOADED_DATE, lit(self.currentDate))

        writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, inserts_df, "mergeSchema", "append")

        logger.info(f"phida_log: Inserts data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendUpdatesToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify updates b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendDeletesToBronze(source_df, target_df)

        tip:
            N/A
        """
        updates_df = source_df.alias("source") \
            .join(target_df.alias("target"), self.keyColsList) \
            .select("source.*") \
            .filter(to_timestamp(col(f"source.{UPDATESTAMP}"), MON_DATE_YEAR_HR_MN_SEC) >
                    to_timestamp(col(f"target.{UPDATESTAMP}"), MON_DATE_YEAR_HR_MN_SEC)) \
            .withColumn(SOURCE_OPERATION, lit(OPERATION_UPDATE)) \
            .withColumn(SRC_KEY_COLS, lit(self.tgtTableKeyColumns)) \
            .withColumn(ADLS_LOADED_DATE, lit(self.currentDate))

        writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, updates_df, "mergeSchema", "append")

        logger.info(f"phida_log: Appends data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendDeletesToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify deletes b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendDeletesToBronze(source_df, target_df)

        tip:
            N/A
        """
        deletes_df = target_df.join(source_df, self.keyColsList, "leftanti") \
            .withColumn(SOURCE_OPERATION, lit(OPERATION_DELETE)) \
            .withColumn(SRC_KEY_COLS, lit(self.tgtTableKeyColumns)) \
            .withColumn(ADLS_LOADED_DATE, lit(self.currentDate))

        writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, deletes_df, "mergeSchema", "append")

        logger.info(f"phida_log: Deletes data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendChangesToBronze(self, source_df):
        """
        desc:
            A Function to help in appending change data into the bronze target

        args:
            None

        return:
            None - Does not return anything

        example:
            appendChangesToBronze()

        tip:
            N/A
        """
        target_df = spark.read.table(f"{self.tgtDatabaseName}.{self.tgtTableName}")

        window_spec = Window.partitionBy(*self.keyColsList).orderBy(
            to_timestamp(target_df.UPDATESTAMP, MON_DATE_YEAR_HR_MN_SEC).desc())

        target_filtered_df = target_df.withColumn("row_num", row_number().over(window_spec)) \
            .filter("row_num == 1") \
            .filter(target_df.source_operation != OPERATION_DELETE) \
            .drop("row_num")

        self.appendInsertsToBronze(source_df, target_filtered_df)
        self.appendUpdatesToBronze(source_df, target_filtered_df)
        self.appendDeletesToBronze(source_df, target_filtered_df)

    def ingestToBronzeTarget(self):
        """
        desc:
            A Function for appending the records from the source into delta Target table

        args:
            None

        return:
            None - Does not return anything

        example:
            ingestToBronzeTarget()

        tip:
            Make sure the values provided in the notebook are correct
        """

        logger.info(f"phida_log: preparing the target delta table ")

        first_run = checkIfFirstRun(self.tgtDatabaseName, self.tgtTableName, self.tgtTablePath)

        if first_run:
            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            source_df = initialMultilineRead(self.srcFilePath, "|", True)

            createDeltaTable(source_df,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

            if self.containsTimestamp:
                raw_refined_df = source_df.withColumn(SOURCE_OPERATION, lit(OPERATION_INSERT).cast("string")) \
                    .withColumn(SRC_KEY_COLS, lit(self.tgtTableKeyColumns).cast("string")) \
                    .withColumn(ADLS_LOADED_DATE, lit(self.currentDate).cast("string"))
            else:
                raw_refined_df = source_df.withColumn(ADLS_LOADED_DATE, lit(self.currentDate).cast("string"))

            writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, raw_refined_df,
                                  "overwriteSchema", "overwrite")

            logger.info(
                f"phida_log: first write into bronze table {self.tgtDatabaseName}.{self.tgtTableName} completed")
        else:
            existing_df = spark.read.table(self.tgtDatabaseName + "." + self.tgtTableName)
            ddl_schema = hiveDDL(existing_df, self.columnsToBeAppendedInBronze)
            source_df = multilineRead(self.srcFilePath, ddl_schema, "|", True)

            checkForSchemaChanges(source_df, existing_df, self.tgtDatabaseName, self.tgtTableName,
                                  self.columnsToBeAppendedInBronze)

            logger.info(f"phida_log: Appending data change to bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

            if self.containsTimestamp:
                self.appendChangesToBronze(source_df)
            else:
                writeDataframeToTable(self.tgtDatabaseName, self.tgtTableName, source_df, "mergeSchema", "append")
