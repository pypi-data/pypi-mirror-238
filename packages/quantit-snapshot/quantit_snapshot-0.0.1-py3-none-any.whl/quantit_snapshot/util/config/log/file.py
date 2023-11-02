from glob import glob
from os import path, makedirs


class FileLogger(object):
    def __init__(self, log_dir):
        self.__log_dir = path.join(log_dir, 'filelog')
        if not path.exists(self.__log_dir):
            makedirs(self.__log_dir)

    def log(self, name, f_names):
        """

        :param name:
        :param f_names:
        :return:
        """
        with open(path.join(self.__log_dir, "{}.log".format(name)), 'a') as f:
            if isinstance(f_names, (list, tuple, set)):
                for f_name in f_names:
                    f.write(f_name + '\n')
            elif isinstance(f_names, str):
                f.write(f_names + '\n')

    def get(self, name):
        """

        :param name:
        :return:
        """
        try:
            with open(
                    path.join(self.__log_dir, "{}.log".format(name)), 'r'
            ) as f:
                return set([l.strip() for l in f.readlines()])
        except FileNotFoundError:
            return set()

    def get_new_f_path_set(self, dirname: str, process_type: str, suffix: str='.csv'):
        """

        :param dirname:
        :param process_type:
        :param suffix:
        :return:
        """
        tot_f_paths = find_files(dirname, suffix)
        logged_f_paths = self.get(process_type)
        new_f_path_set = tot_f_paths - logged_f_paths
        return new_f_path_set


def find_files(dir_path, suffix):
    """

    :param dir_path:
    :param suffix:
    :return:
    """
    return set([
        path.join(dir_path, f) for f
        in glob(path.join(dir_path, '*' + suffix))
        if not f.endswith('.log')
    ])
