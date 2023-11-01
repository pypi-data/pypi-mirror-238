from logclshelper import LogClsHelper
from pyspark.sql import SparkSession

class PySparkHelper(LogClsHelper):
    _spark = None

    @classmethod
    def get_or_create_spark(cls):
        if cls._spark is None:
            cls.logger().debug(f'#beg# get_or_create_spark')
            
            cls._spark = SparkSession.builder.getOrCreate()
            
            cls.logger().debug(f"#end# get_or_create_spark {cls._spark}")

        return cls._spark

    @classmethod
    def stop_spark(cls):
        cls.logger().debug(f"#beg# stop_spark {cls._spark}")

        if cls._spark is not None:
            cls._spark.stop()
            cls._spark = None

        cls.logger().debug(f"#end# stop_spark {cls._spark}")

    @classmethod
    def clear_spark_cache(cls):
        cls.logger().debug(f"#beg# clear_spark_cache")

        cls.get_or_create_spark().catalog.clearCache()

        cls.logger().debug(f"#end# clear_spark_cache")
        
    @classmethod
    def get_application_id(cls):
        return cls.get_or_create_spark()._sc._jsc.sc().applicationId()




