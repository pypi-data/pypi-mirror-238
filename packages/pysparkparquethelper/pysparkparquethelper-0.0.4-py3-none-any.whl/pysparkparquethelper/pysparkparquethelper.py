from logclshelper import LogClsHelper
from pysparkhelper import PySparkHelper
from pysparkhdfshelper import PySparkHdfsHelper
import itertools
import re

class PySparkParquetHelper(LogClsHelper):
    
    @classmethod
    def yield_parquet_files_from_path(cls, path):
        files = PySparkHdfsHelper.yield_filtered_paths(
            parent_dir = path,
            accept_dirs = False,
            accept_files = True,
            min_depth = None,
            max_depth = None,
            lambda_filter_path = lambda p: ('/.' not in p) and ('/_' not in p) and p.endswith('.parquet'),
            lambda_filter_walk = lambda p : ('/.' not in p) and ('/_' not in p)
        )
        return files
    
    @classmethod
    def get_parquet_files_by_dir_from_path(cls, path):
        groups = PySparkHdfsHelper.get_grouped_filtered_paths_by_key(
            parent_dir = path,
            lambda_filter_path = lambda p: ('/.' not in p) and ('/_' not in p) and p.endswith('.parquet'),
            accept_dirs = False,
            accept_files = True,
            min_depth = None,
            max_depth = None,
            lambda_filter_walk = lambda p : ('/.' not in p) and ('/_' not in p),
            lambda_key_from_path = lambda path : os.path.dirname(path)
        )
        
        return groups
    
    @classmethod
    def read_parquet_from_file(cls, file):
        df = (
            PySparkHelper.get_or_create_spark()
            .read.option("basePath", PySparkPartHelper.get_basepath_from_path(file))
            .parquet(file)
        )

        return df
    
    @classmethod
    def union_df1_df2_by_colnames(cls, df1, df2):
        cols_for_df2 = [
            F.lit(None).cast(df1.schema[colname].dataType).alias(colname) 
            for colname in set(df1.columns) - set(df2.columns)
        ]

        cols_for_df1 = [
            F.lit(None).cast(df2.schema[colname].dataType).alias(colname) 
            for colname in set(df2.columns) - set(df1.columns)
        ]

        df = df1.select('*', *cols_for_df1).unionByName(df2.select('*', *cols_for_df2))
        return df
    
    @classmethod
    def union_dfs_by_colnames(cls, dfs):
        df = ft.reduce(lambda df1, df2: cls.union_df1_df2_by_colnames(df1, df2), dfs)
        return df
    




