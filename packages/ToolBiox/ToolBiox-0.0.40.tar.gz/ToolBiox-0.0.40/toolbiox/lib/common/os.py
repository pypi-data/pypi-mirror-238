import re
import subprocess
import time
import os
import shutil
import uuid
import cloudpickle
from math import ceil
from multiprocessing import Pool, TimeoutError
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from toolbiox.lib.common.util import printer_list, logging_init, time_now, pickle_dump, pickle_load
from toolbiox.lib.common.fileIO import read_list_file

__author__ = 'Yuxing Xu'
SCRIPT_DIR_PATH = os.path.split(os.path.realpath(__file__))[0]


def mkdir(dir_name, keep=False):
    if keep is False:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
    else:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    return dir_name


def rmdir(dir_name):
    if os.path.exists(dir_name):
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
        else:
            os.remove(dir_name)


def have_file(file_name, null_is_ok=False):
    if os.path.exists(file_name):
        if null_is_ok:
            return True
        elif os.path.getsize(file_name):
            return True
    else:
        return False


def get_file_name(give_path):
    return os.path.basename(give_path)


def get_file_dir(file_path):
    abs_file_path = os.path.abspath(file_path)
    return os.path.dirname(abs_file_path)


def copy_file(source_path, target_path, keep=False):
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)

    if not os.path.exists(source_path):
        raise EnvironmentError("Can't find %s" % source_path)

    if os.path.isdir(source_path):
        new_path = shutil.copytree(source_path, os.path.join(
            target_path, get_file_name(source_path)))
    elif os.path.isfile(source_path):
        if os.path.isdir(target_path):
            target_path = os.path.join(target_path, get_file_name(source_path))

        if keep and have_file(target_path):
            new_path = target_path
        else:
            new_path = shutil.copy(source_path, target_path)

    return new_path


def ln_file(source_path, target_path):

    if os.path.isdir(target_path):
        target_path = target_path + "/" + get_file_name(source_path)

    os.symlink(os.path.abspath(source_path), target_path)

    return target_path


def move_file(source_path, target_path, keep=False):
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)

    new_path = shutil.move(source_path, target_path)

    return new_path


def merge_file(input_file_list, output_file):
    with open(output_file, 'w') as f:
        for input_file in input_file_list:
            fr = open(input_file, 'r').read()
            if len(fr) > 0 and fr[-1] != '\n':
                fr = fr+'\n'
            f.write(fr)


def gunzip_file(raw_file):
    raw_file = os.path.abspath(raw_file)

    cmd_string = "gunzip " + raw_file
    cmd_run(cmd_string, silence=True)

    gunzip_file = re.sub(".gz$", "", raw_file)

    return gunzip_file


def gzip_file(raw_file):
    raw_file = os.path.abspath(raw_file)

    cmd_string = "gzip " + raw_file
    cmd_run(cmd_string, silence=True)

    gzip_file = raw_file + ".gz"

    return gzip_file


def md5sum_check(file_name, original_md5):
    import hashlib

    if not os.path.exists(file_name):
        return False

    with open(file_name, "rb") as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()

    if original_md5 == md5_returned:
        return True
    else:
        return False


def remove_file_name_suffix(file_name, subsuffix_level=0):
    """
    remove the suffix for a file name
    :param file_name: give me a file name, like: "/home/xuyuxing/file.txt" or "~/work/file.txt" or just "file.txt"
    :param subsuffix_level: sometimes a file can have more than one suffix, like "~/work/file.txt.gz",
           how many you want to remove, 0 meanings remove all suffix
    :return: file without suffix, will keep dir_name as a path, to get base file name: os.path.basename(file_name)
    """

    file_name = os.path.abspath(file_name)
    dir_name = os.path.dirname(file_name)
    base_name = os.path.basename(file_name)
    base_name_split = base_name.split(".")
    if subsuffix_level == 0:
        subsuffix_level = len(base_name_split) - 1
    elif subsuffix_level > len(base_name_split) - 1:
        raise ValueError("There are not enough suffix level to remove")

    return dir_name + "/" + printer_list(base_name.split(".")[:-subsuffix_level], ".")


def md5sum_maker(file_name):
    import hashlib

    if not os.path.exists(file_name):
        FileNotFoundError("No such file or directory: %s" % file_name)

    with open(file_name, "rb") as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()

    return md5_returned


def cmd_run(cmd_string, cwd=None, retry_max=5, silence=False, log_file=None):
    module_logger = logging_init("cmd_run", log_file)
    module_logger.info("Calling a bash cmd with retry_max %d: %s" %
                       (retry_max, cmd_string))
    if not silence:
        print("Running " + str(retry_max) + " " + cmd_string)
    p = subprocess.Popen(cmd_string, shell=True,
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
    output, error = p.communicate()
    if not silence:
        print(error.decode())
    returncode = p.poll()
    module_logger.info("Finished bash cmd with returncode as %d" % returncode)
    if returncode == 1:
        if retry_max > 1:
            retry_max = retry_max - 1
            cmd_run(cmd_string, cwd=cwd, retry_max=retry_max)
    del module_logger.handlers[:]

    output = output.decode()
    error = error.decode()

    return (not returncode, output, error)


def multiprocess_running(f, args_list, pool_num, log_file=None, silence=True, args_id_list=None, timeout=None):
    """
    :param f: function name
    :param args_list: a list include every args in a tuple
    :param pool_num: process num of running at same time
    :param silence:
    :return:

    example

    def f(x, y):
        time.sleep(1)
        return x * y

    args_list = list(zip(range(1,200),range(2,201)))
    pool_num = 5

    multiprocess_running(f, args_list, pool_num, log_file='/lustre/home/xuyuxing/Work/Other/saif/Meth/tmp/log')

    """
    num_tasks = len(list(args_list))

    module_log = logging_init(f.__name__, log_file)
    if not silence:
        print('args_list have %d object and pool_num is %d' %
              (num_tasks, pool_num))
    module_log.info('running with mulitprocess')
    module_log.info('args_list have %d object and pool_num is %d' %
                    (num_tasks, pool_num))

    p_dict = {}

    if len(args_list) > 0:
        f_with_para = partial(get_more_para, f)

        start_time = time.time()
        if not silence:
            print(time_now() + '\tBegin: ')
        module_log.info('Begin: ')

        if timeout is None:
            with Pool(processes=pool_num) as pool:
                # for i, output in enumerate(pool.imap_unordered(f_with_para, args_list, chunksize=1)):
                for i, output in enumerate(pool.imap(f_with_para, args_list, chunksize=1)):
                    if args_id_list:
                        job_id = args_id_list[i]
                    else:
                        job_id = 'ID_' + str(i)

                    p_dict[job_id] = {
                        'args': args_list[i],
                        'output': output,
                        'error': None
                    }
                    # print(i)
                    round_time = time.time()
                    if round_time - start_time > 5:
                        if not silence:
                            print(time_now() + '\t%d/%d %.2f%% parsed' %
                                  (i, num_tasks, i / num_tasks * 100))
                        module_log.info('%d/%d %.2f%% parsed' %
                                        (i, num_tasks, i / num_tasks * 100))
                        start_time = round_time
                    # module_log.info('%d/%d %.2f%% parsed' % (i, num_tasks, i / num_tasks * 100))
        else:
            abortable_func = partial(
                abortable_worker, f_with_para, timeout=timeout)

            # with Pool(processes=pool_num, maxtasksperchild=1) as pool:
            with Pool(processes=pool_num) as pool:
                # for i, output in enumerate(pool.imap_unordered(f_with_para, args_list, chunksize=1)):
                it = pool.imap(abortable_func, args_list, chunksize=1)
                i = -1
                while 1:
                    i += 1
                    try:
                        output = it.next()
                        if args_id_list:
                            job_id = args_id_list[i]
                        else:
                            job_id = 'ID_' + str(i)

                        if output == "Aborting due to timeout":
                            p_dict[job_id] = {
                                'args': args_list[i],
                                'output': None,
                                'error': "timeout"
                            }
                        else:
                            p_dict[job_id] = {
                                'args': args_list[i],
                                'output': output,
                                'error': None
                            }

                        round_time = time.time()
                        if round_time - start_time > 5:
                            if not silence:
                                print(time_now() + '\t%d/%d %.2f%% parsed' %
                                      (i, num_tasks, i / num_tasks * 100))
                            module_log.info('%d/%d %.2f%% parsed' %
                                            (i, num_tasks, i / num_tasks * 100))
                            start_time = round_time

                    except StopIteration:
                        break

        module_log.info('%d/%d %.2f%% parsed' %
                        (i, num_tasks, i / num_tasks * 100))
        module_log.info('All args_list task finished')

        if not silence:
            print(time_now() + '\t%d/%d %.2f%% parsed' %
                  (i, num_tasks, i / num_tasks * 100))
            print(time_now() + '\tAll args_list task finished')

    del module_log.handlers[:]

    return p_dict


# def multiprocess_running_onestep(f, args_list, pool_num, silence=True, args_id_list=None, timeout=None, start_job_num=0, num_tasks=0, module_log=None):
#     if num_tasks == 0:
#         num_tasks = len(list(args_list))

#     p_dict = {}

#     if len(args_list) > 0:
#         f_with_para = partial(get_more_para, f)

#         start_time = time.time()

#         if timeout is None:
#             with Pool(processes=pool_num) as pool:
#                 # for i, output in enumerate(pool.imap_unordered(f_with_para, args_list, chunksize=1)):
#                 for i, output in enumerate(pool.imap(f_with_para, args_list, chunksize=1)):
#                     if args_id_list:
#                         job_id = args_id_list[i]
#                     else:
#                         job_id = 'ID_' + str(i+start_job_num)

#                     p_dict[job_id] = {
#                         'args': args_list[i],
#                         'output': output,
#                         'error': None
#                     }
#                     # print(i)
#                     round_time = time.time()
#                     if round_time - start_time > 5:
#                         if not silence:
#                             print(time_now() + '\t%d/%d %.2f%% parsed' %
#                                   (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))
#                         module_log.info(time_now() + '\t%d/%d %.2f%% parsed' %
#                                         (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))

#                         start_time = round_time
#                     # module_log.info('%d/%d %.2f%% parsed' % (i, num_tasks, i / num_tasks * 100))
#         else:
#             abortable_func = partial(
#                 abortable_worker, f_with_para, timeout=timeout)

#             # with Pool(processes=pool_num, maxtasksperchild=1) as pool:
#             with Pool(processes=pool_num) as pool:
#                 # for i, output in enumerate(pool.imap_unordered(f_with_para, args_list, chunksize=1)):
#                 it = pool.imap(abortable_func, args_list, chunksize=1)
#                 i = -1
#                 while 1:
#                     i += 1
#                     try:
#                         output = it.next()
#                         if args_id_list:
#                             job_id = args_id_list[i]
#                         else:
#                             job_id = 'ID_' + str(i+start_job_num)

#                         if output == "Aborting due to timeout":
#                             p_dict[job_id] = {
#                                 'args': args_list[i],
#                                 'output': None,
#                                 'error': "timeout"
#                             }
#                         else:
#                             p_dict[job_id] = {
#                                 'args': args_list[i],
#                                 'output': output,
#                                 'error': None
#                             }

#                         round_time = time.time()
#                         if round_time - start_time > 5:
#                             if not silence:
#                                 print(time_now() + '\t%d/%d %.2f%% parsed' %
#                                       (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))
#                             module_log.info(time_now() + '\t%d/%d %.2f%% parsed' %
#                                             (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))

#                             start_time = round_time

#                     except StopIteration:
#                         break

#         if not silence:
#             print(time_now() + '\t%d/%d %.2f%% parsed' %
#                   (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))
#         module_log.info(time_now() + '\t%d/%d %.2f%% parsed' %
#                         (i+start_job_num, num_tasks, (i+start_job_num) / num_tasks * 100))

#     return p_dict


# def multiprocess_running_step(f, args_list, pool_num, log_file=None, silence=False, args_id_list=None, timeout=None, step=50000):
#     """
#     :param f: function name
#     :param args_list: a list include every args in a tuple
#     :param pool_num: process num of running at same time
#     :param silence:
#     :return:

#     example

#     def f(x, y):
#         time.sleep(1)
#         return x * y

#     args_list = list(zip(range(1,200),range(2,201)))
#     pool_num = 5

#     multiprocess_running(f, args_list, pool_num, log_file='/lustre/home/xuyuxing/Work/Other/saif/Meth/tmp/log')

#     """
#     num_tasks = len(list(args_list))

#     module_log = logging_init(f.__name__, log_file)
#     if not silence:
#         print('args_list have %d object and pool_num is %d' %
#               (num_tasks, pool_num))
#     module_log.info('running with mulitprocess')
#     module_log.info('args_list have %d object and pool_num is %d' %
#                     (num_tasks, pool_num))

#     p_dict = {}

#     if not silence:
#         print(time_now() + '\tBegin: ')
#     module_log.info('Begin: ')

#     if len(args_list) > 0:
#         for ss in range(ceil(len(args_list)/step)):
#             ss = ss*step
#             sub_args_list = args_list[ss:ss+step]
#             if args_id_list:
#                 sub_args_id_list = args_id_list[ss:ss+step]

#             sub_p_dict = multiprocess_running_onestep(f, sub_args_list, pool_num, silence=silence, args_id_list=sub_args_id_list,
#                                                       timeout=timeout, start_job_num=ss, num_tasks=len(args_list), module_log=module_log)

#             for i in sub_p_dict:
#                 p_dict[i] = sub_p_dict[i]

#         if not silence:
#             print(time_now() + '\tAll args_list task finished')
#         module_log.info('All args_list task finished')

#     del module_log.handlers[:]

#     return p_dict


def get_more_para(f, para_tuple):
    return f(*para_tuple)


def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    p = ThreadPool(1)
    res = p.apply_async(func, args=args)
    try:
        out = res.get(timeout)  # Wait timeout seconds for func to complete.
        return out
    except TimeoutError:
        return "Aborting due to timeout"
        raise


# multijobs_submitter_shell = os.path.join(
#     SCRIPT_DIR_PATH, "multijobs_submitter2.sh")
# run_pickle_func_script = os.path.join(SCRIPT_DIR_PATH, "run_pickle_func.py")


# def multijobs_running(func, args_list, pool_num=8, args_id_list=None, timeout=0, work_dir="/tmp"):

#     mkdir(work_dir, True)
#     main_work_dir = "%s/mltjobs_%s" % (work_dir, uuid.uuid1().hex)
#     mkdir(main_work_dir)

#     func_pickle_file = "%s/func_pickle.pyb" % main_work_dir
#     with open(func_pickle_file, 'wb') as f:
#         cloudpickle.dump(func, f)

#     s = 50000
#     n = 0
#     print_num = 0
#     p_dict = {}

#     print(time_now() + '\tBegin: ')
#     print(time_now() + '\tThere are %d Jobs, work with %d threads in %s (%ds limit for single job)' %
#           (len(args_list), pool_num, main_work_dir, timeout))

#     for i in range(ceil(len(args_list)/s)):
#         i = i*s
#         sub_args_list = args_list[i:i+s]
#         if args_id_list:
#             sub_args_id_list = args_id_list[i:i+s]

#         # sub submitter
#         tmp_work_dir = "%s/jobs_%s" % (main_work_dir, uuid.uuid1().hex)
#         mkdir(tmp_work_dir)
#         log_file = tmp_work_dir + "/log"
#         print(time_now() + '\t%d/%d jobs are prepared for submission now' %
#               (print_num + len(sub_args_id_list), len(args_list)))
#         print(tmp_work_dir)

#         cmd_list_file = "%s/cmd_list_file" % tmp_work_dir
#         with open(cmd_list_file, 'w') as f:
#             for j in range(len(sub_args_list)):
#                 if args_id_list:
#                     args_id = sub_args_id_list[j]
#                 else:
#                     args_id = None

#                 p_dict[n] = {
#                     'args': sub_args_list[j],
#                     'args_pickle': "%s/args_%d.pyb" % (tmp_work_dir, n),
#                     'out_pickle': "%s/out_%d.pyb" % (tmp_work_dir, n),
#                     'output': None,
#                     'error': None,
#                     'args_id': args_id,
#                 }

#                 pickle_dump(p_dict[n]['args'], p_dict[n]['args_pickle'])

#                 f.write("python %s %s %s %s %d\n" % (run_pickle_func_script,
#                                                      func_pickle_file, p_dict[n]['args_pickle'], p_dict[n]['out_pickle'], n))

#                 n += 1

#         cmd_string = "bash %s %s %d %d True %s > %s" % (
#             multijobs_submitter_shell, cmd_list_file, pool_num, timeout, tmp_work_dir, log_file)

#         print(time_now() + '\t%d/%d jobs are running now' %
#               (print_num + len(sub_args_id_list), len(args_list)))
#         cmd_run(cmd_string, cwd=tmp_work_dir,
#                 retry_max=1, silence=True, log_file=None)
#         print(time_now() + '\t%d/%d jobs finished now' %
#               (print_num + len(sub_args_id_list), len(args_list)))

#         # get output
#         for f_name in os.listdir(tmp_work_dir):
#             match_list = re.findall(r'args_(\d+).pyb', f_name)

#             if len(match_list):
#                 job_id = int(match_list[0])

#                 if not os.path.exists(p_dict[job_id]['out_pickle']):
#                     p_dict[job_id]['error'] = 'timeout'
#                 else:
#                     p_dict[job_id]['output'] = pickle_load(
#                         p_dict[job_id]['out_pickle'])

#         rmdir(tmp_work_dir)

#         print_num += len(sub_args_id_list)

#     out_dict = {}
#     for i in p_dict:
#         if p_dict[i]['args_id']:
#             job_id = p_dict[i]['args_id']
#         else:
#             job_id = i

#         out_dict[job_id] = {
#             'args': p_dict[i]['args'],
#             'output': p_dict[i]['output'],
#             'error': p_dict[i]['error'],
#         }

#     rmdir(main_work_dir)

#     print(time_now() + '\tFinished')

#     return out_dict


# def job_info_parser(job_info_file):
#     info_dict = {}
#     with open(job_info_file, 'r') as f:
#         for each_line in f:
#             each_line = each_line.strip()
#             match_list = re.findall(r'(\S+): (.*)', each_line)
#             if len(match_list):
#                 info_tuple = match_list[0]
#                 info_dict[info_tuple[0]] = info_tuple[1]
#     return info_dict


if __name__ == "__main__":
    pass

    # from toolbiox.lib.common.util import pickle_dump, pickle_load
    # from toolbiox.lib.common.os import *
    # from toolbiox.api.xuyuxing.evolution.PAML_tools import quick_get_dNdS
    # import time
    # from joblib import Parallel, delayed
    # from tqdm import tqdm
    # import cloudpickle
    # from math import ceil
    # import os

    # args_list = pickle_load("args_list.pyb")
    # args_id_list = pickle_load("args_id_list.pyb")

    # def chunk_func(func, sub_args_list, sub_args_id_list, timeout=None):
    #     sub_p_dict = {}
    #     for i in range(len(sub_args_list)):
    #         if timeout:
    #             p = ThreadPool(1)
    #             res = p.apply_async(func, args=sub_args_list[i])
    #             try:
    #                 # Wait timeout seconds for func to complete.
    #                 out = res.get(timeout)
    #                 error = None
    #             except TimeoutError:
    #                 out = None
    #                 error = "timeout"
    #         else:
    #             out = func(*sub_args_list[i])
    #             error = None

    #         sub_p_dict[sub_args_id_list[i]] = {
    #             'args': sub_args_list[i],
    #             'output': out,
    #             'error': error
    #         }
    #     return sub_p_dict

    # def multiprocess_running_onestep(f, args_list, pool_num, silence=True, args_id_list=None, start_job_num=0, num_tasks=0, module_log=None, chunksize=1):
    #     if num_tasks == 0:
    #         num_tasks = len(list(args_list)) * chunksize

    #     p_dict = {}

    #     if len(args_list) > 0:
    #         f_with_para = partial(get_more_para, f)

    #         start_time = time.time()

    #         with Pool(processes=pool_num) as pool:
    #             # for i, output in enumerate(pool.imap_unordered(f_with_para, args_list, chunksize=1)):
    #             for i, output in enumerate(pool.imap(f_with_para, args_list, chunksize=1)):
    #                 if args_id_list:
    #                     job_id = args_id_list[i]
    #                 else:
    #                     job_id = 'ID_' + str(i+start_job_num)

    #                 p_dict[job_id] = {
    #                     'args': args_list[i],
    #                     'output': output,
    #                     'error': None
    #                 }
    #                 # print(i)
    #                 round_time = time.time()
    #                 if round_time - start_time > 5:
    #                     ok_job_num = (i+start_job_num)*chunksize
    #                     if not silence:
    #                         print(time_now() + '\t%d/%d %.2f%% parsed' %
    #                               (ok_job_num, num_tasks, ok_job_num / num_tasks * 100))
    #                     if module_log:
    #                         module_log.info(time_now() + '\t%d/%d %.2f%% parsed' %
    #                                         (ok_job_num, num_tasks, ok_job_num / num_tasks * 100))

    #                     start_time = round_time
    #                 # module_log.info('%d/%d %.2f%% parsed' % (i, num_tasks, i / num_tasks * 100))

    #         ok_job_num = (i+start_job_num)*chunksize
    #         if not silence:
    #             print(time_now() + '\t%d/%d %.2f%% parsed' %
    #                   (ok_job_num, num_tasks, ok_job_num / num_tasks * 100))
    #         if module_log:
    #             module_log.info(time_now() + '\t%d/%d %.2f%% parsed' %
    #                             (ok_job_num, num_tasks, ok_job_num / num_tasks * 100))

    #     return p_dict

    # def multiprocess_running(f, args_list, pool_num, log_file=None, silence=True, args_id_list=None, timeout=None, chunksize=1):
    #     chunk_arg_lol = []

    #     for i in range(ceil(len(args_list)/chunksize)):
    #         i = i*chunksize
    #         sub_args_list = args_list[i:i+chunksize]

    #         if args_id_list:
    #             sub_args_id_list = args_id_list[i:i+chunksize]
    #         else:
    #             sub_args_id_list = list(range(i, i+chunksize))

    #         chunk_arg_lol.append((f, sub_args_list, sub_args_id_list, timeout))

    #     mlt_out = multiprocess_running_onestep(
    #         chunk_func, chunk_arg_lol, pool_num, silence=silence, chunksize=chunksize)

    #     p_dict = {}
    #     for i in mlt_out:
    #         for j in mlt_out[i]['output']:
    #             p_dict[j] = mlt_out[i]['output'][j]

    #     return p_dict

    # # def my_func(x,y):
    # #     time.sleep(1)
    # #     return x+y

    # # args_list = [(i,i+1) for i in range(1000)]
    # # args_id_list = ["X%d" % i for i in range(1000)]

    # # %time a=multiprocess_running_onestep(my_func, args_list, 10, args_id_list=args_id_list, silence=False)

    # # %time a=chunk_func(my_func, args_list, args_id_list, timeout=1)

    # # a=multiprocess_running(my_func, args_list, 10, log_file=None, silence=False, args_id_list=args_id_list, timeout=None, chunksize=10)

    # a = multiprocess_running(quick_get_dNdS, args_list, 56, log_file=None,
    #                          silence=False, args_id_list=args_id_list, timeout=None, chunksize=1000)

    # s= 10000
    # for i in range(ceil(len(args_list)/s)):
    #     i = i*s
    #     sub_args_list = args_list[i:i+s]
    #     a=Parallel(n_jobs=56)(delayed(quick_get_dNdS)(*i) for i in tqdm(sub_args_list))

    # n = 0
    # for i in args_list:
    #     quick_get_dNdS(*i)
    #     n+=1
    #     print(n)

    # import os
    # os.system("echo 123")

    # func_pickle_file = "/lustre/home/xuyuxing/tmp/mlt/func_pickle.pyb"
    # with open(func_pickle_file, 'wb') as f:
    #     cloudpickle.dump(quick_get_dNdS, f)

    # s= 10000
    # for i in range(ceil(len(args_list)/s)):
    #     i = i*s
    #     sub_args_list = args_list[i:i+s]
    #     sub_args_list_file = "/lustre/home/xuyuxing/tmp/mlt/args.pyb"
    #     sub_outs_list_file = "/lustre/home/xuyuxing/tmp/mlt/outs.pyb"

    #     pickle_dump(sub_args_list, sub_args_list_file)

    #     cmd_string="python /lustre/home/xuyuxing/python_project/ToolBiox/toolbiox/lib/common/multijobs/multijobs_submitter.py 56 %s %s %s" % (func_pickle_file, sub_args_list_file, sub_outs_list_file)

    #     os.system(cmd_string)

    # import time
    # from toolbiox.lib.common.os import *

    # def plus_xy(x, y):
    #     z = x + y
    #     # time.sleep(z)
    #     return z

    # def shell_sleep(x, y):
    #     z = x + y
    #     cmd_run("sleep 0.01s", retry_max=1, silence=True)
    #     return z

    # func = plus_xy
    # args_list = [(i, i+2) for i in range(50000)]
    # work_dir = "/lustre/home/xuyuxing/tmp/mlt"
    # pool_num = 56
    # args_id_list = ["X%d" % i for i in range(50000)]
    # timeout = 0
    # log_file = "/lustre/home/xuyuxing/tmp/mlt/log"

    # multijobs_submitter_shell = "/lustre/home/xuyuxing/python_project/ToolBiox/toolbiox/lib/common/multijobs_submitter2.sh"

    # mlt_out_dict = multijobs_running(
    #     func, args_list, pool_num, args_id_list, timeout, work_dir)

    # multiprocess_running(func, args_list, pool_num, log_file=None,
    #                      silence=False, args_id_list=args_id_list, timeout=None)
    # multiprocess_running(shell_sleep, args_list, pool_num, log_file=None,
    #                      silence=False, args_id_list=args_id_list, timeout=None)

    # multiprocess_running_step(plus_xy, args_list, pool_num, silence=False,
    #                            args_id_list=None, timeout=None, start_job_num=2500, num_tasks=5000)

    # multiprocess_running_step(plus_xy, args_list, pool_num, silence=False,
    #                            args_id_list=None, timeout=None, start_job_num=2500, num_tasks=5000)

    # multiprocess_running_step(plus_xy, args_list, pool_num, log_file=log_file, silence=False, args_id_list=args_id_list, timeout=None, step=5000)
