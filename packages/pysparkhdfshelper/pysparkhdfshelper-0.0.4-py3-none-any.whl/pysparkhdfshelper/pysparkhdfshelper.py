from logclshelper import LogClsHelper
from pysparkhelper import PySparkHelper
import itertools
from collections import deque

class PySparkHdfsHelper(LogClsHelper):
    _jh = None
    _jhconf = None
    _jhfs = None
    _jhpath = None

    @classmethod
    def jh(cls):
        if cls._jh is None:
            cls._jh = PySparkHelper.get_or_create_spark()._sc._jvm.org.apache.hadoop

        return cls._jh

    @classmethod
    def jhconf(cls):
        if cls._jhconf is None:
            cls._jhconf = cls.jh().conf.Configuration()

        return cls._jhconf

    @classmethod
    def jhfs(cls):
        if cls._jhfs is None:
            cls._jhfs = cls.jh().fs.FileSystem

        return cls._jhfs

    @classmethod
    def jhpath(cls):
        if cls._jhpath is None:
            cls._jhpath = cls.jh().fs.Path

        return cls._jhpath

    @classmethod
    def yield_path_isdir_tuples(cls, parent_dir="/"):
        path = cls.jhpath()(parent_dir)
        for file_status in cls.jhfs().get(cls.jhconf()).listStatus(path):
            yield (str(file_status.getPath()), file_status.isDir())

    @classmethod
    def walk_non_recursive(cls, parent_dir="/"):
        # cls.logger().debug(f'#beg# walk_non_recursive {parent_dir}')

        dirs = []
        files = []
        for path, is_dir in cls.yield_path_isdir_tuples(parent_dir=parent_dir):
            if is_dir:
                dirs.append(path)
            else:
                files.append(path)

        # cls.logger().debug(f'#end# walk_non_recursive {parent_dir, len(dirs), len(files)}')
        #print(f'#end# walk_non_recursive {parent_dir, len(dirs), len(files)}'.ljust(200, ' '), end = '\r')

        return dirs, files

    @classmethod
    def walk(cls, parent_dir="/", lambda_filter_walk = lambda path : True):
        cls.logger().debug(f"#beg# walk {parent_dir}")

        fifo = deque()
        fifo.appendleft((parent_dir, 0))

        while any(fifo):
            pdir, depth = fifo.pop()
            dirs, files = cls.walk_non_recursive(parent_dir=pdir)

            for next_dir in dirs:
                if(lambda_filter_walk(next_dir)):
                    fifo.appendleft((next_dir, depth + 1))

            yield (pdir, dirs, files, depth, fifo)

        cls.logger().debug(f"#end# walk {parent_dir}")

    @classmethod
    def yield_filtered_paths(
        cls,
        parent_dir="/",
        lambda_filter_path=lambda path: True,
        accept_dirs=True,
        accept_files=True,
        min_depth=None,
        max_depth=None,
        lambda_filter_walk = lambda path : True
    ):

        not_valid = (
            ((min_depth is not None) and (max_depth is not None))
            and ((min_depth > max_depth) or (max_depth < 0))
        ) or ((not accept_dirs) and (not accept_files))

        if lambda_filter_path is None:
            lambda_filter_path = lambda path: True

        if not not_valid:
            if(lambda_filter_walk(parent_dir)):
                for pdir, dirs, files, depth, fifo in cls.walk(parent_dir, lambda_filter_walk = lambda_filter_walk):
                    if (min_depth is not None) and (depth < min_depth):
                        continue

                    if (max_depth is not None) and (depth > max_depth):
                        break

                    accepted = (
                        itertools.chain(dirs, files)
                        if (accept_dirs and accept_files)
                        else (dirs if accept_dirs else (files if accept_files else []))
                    )

                    for file_or_dir in accepted:
                        if lambda_filter_path(file_or_dir):
                            yield file_or_dir
                            
    @classmethod
    def get_hdfs_server_url(cls):
        p = next(cls.yield_filtered_paths('/'))
        pattern_hdfs_server = r"(hdfs://[^/]*)/(.*)"
        match = re.search(pattern_hdfs_server, p)
        hdfs_server_url = ''
        if(match is not None):
            hdfs_server_url = match.group(1)
        return hdfs_server_url
                            
    @classmethod
    def get_part_value_from_path_part_name(cls, path, part_name = '(?s:.*)'):
        group1 = f"({part_name})"
        group2 = "([^/]+)"
        pattern = f"{group1}={group2}"
        match = re.search(pattern, path)
        return match.group(2) if (match) else None
                            
    @classmethod
    def get_grouped_filtered_paths_by_key(
        cls,
        parent_dir = "/",
        lambda_filter_path = lambda path: True,
        accept_dirs = True,
        accept_files = True,
        min_depth = None,
        max_depth = None,
        lambda_filter_walk = lambda path : True,
        lambda_key_from_path = lambda path : PySparkHdfsHelper.get_part_value_from_path_part_name(path, part_name = '(?s:.*)')
    ):
        paths = cls.yield_filtered_paths(
            parent_dir = parent_dir,
            lambda_filter_path = lambda_filter_path,
            accept_dirs = accept_dirs,
            accept_files = accept_files,
            min_depth = min_depth,
            max_depth = max_depth,
            lambda_filter_walk = lambda_filter_walk
        )
        
        grouped = {}
        for path in paths :
            key = lambda_key_from_path(path)
            if(key not in grouped):
                grouped[key] = [path]
            else:
                grouped[key].append(path)
                
        return grouped
    
    @classmethod 
    def normalize_hdfs_path(cls, hdfs_path, hdfs_server_url = None):
        if(hdfs_server_url is None):
            hdfs_server_url = cls.get_hdfs_server_url()
        return hdfs_path if hdfs_path.startswith(hdfs_server_url) else hdfs_server_url + hdfs_path
        
    @classmethod
    def exists(cls, path):
        #cls.logger().debug(f"#beg# exists {path}")

        res = cls.jhfs().get(cls.jhconf()).exists(cls.jhpath()(path))

        #cls.logger().debug(f"#end# exists {path, res}")

        return res

    @classmethod
    def move(cls, src_path, dst_path):
        #cls.logger().debug(f"#beg# rename {src_path, dst_path}")

        res = (
            cls.jhfs()
            .get(cls.jhconf())
            .rename(cls.jhpath()(src_path), cls.jhpath()(dst_path))
        )

        #cls.logger().debug(f"#end# rename {src_path, dst_path, res}")

        return res

    @classmethod
    def delete(cls, path):
        #cls.logger().debug(f"#beg# delete {path}")

        res = cls.jhfs().get(cls.jhconf()).delete(cls.jhpath()(path))

        #cls.logger().debug(f"#end# delete {path, res}")

        return res

    @classmethod
    def mkdir(cls, path):
        #cls.logger().debug(f"#beg# mkdir {path}")

        res = cls.jhfs().get(cls.jhconf()).mkdirs(cls.jhpath()(path))

        #cls.logger().debug(f"#end# mkdir {path, res}")

        return res






