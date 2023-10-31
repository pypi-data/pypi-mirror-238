outfmt6_fieldnames = ["query_id", "subject_id", "identity", "alignment_length", "mismatches", "gap_openings",
                        "q_start", "q_end", "s_start", "s_end", "e_value", "bit_score"]


if __name__ == '__main__':
    import argparse

    # argument parse
    parser = argparse.ArgumentParser(
        prog='FormatTools',
    )

    subparsers = parser.add_subparsers(
        title='subcommands', dest="subcommand_name")

    # argparse for blast2DB
    parser_a = subparsers.add_parser('blast2DB',
                                     help='save blast results into sqlite db')

    parser_a.add_argument('input_bls', type=str,
                          help='input file with outfmt 6')
    parser_a.add_argument('db_fasta', type=str, help='output database file')
    parser_a.add_argument('-g', "--gzip_flag",
                          help='if bls is gzipped', action='store_true')

    # argparse for MD5Checker
    parser_a = subparsers.add_parser('MD5Checker',
                                     help='check md5 files in whole dir')

    parser_a.add_argument('dir_path', type=str, help='path of dir to check')

    args = parser.parse_args()
    args_dict = vars(args)

    # ---------------------------------------------------------
    # command detail

    if args_dict["subcommand_name"] == "MD5Checker":
        import os
        from toolbiox.lib.common.os import cmd_run


        def check_md5(dir_path):
            dir_path = os.path.abspath(dir_path)

            file_dir_list = os.listdir(dir_path)
            for tmp_name in file_dir_list:
                tmp_name_full_path = dir_path + "/" + tmp_name
                if os.path.isdir(tmp_name_full_path):
                    check_md5(tmp_name_full_path)
                else:
                    tmp_list = tmp_name.split("_")
                    if len(tmp_list) > 1:
                        if tmp_list[0] == 'MD5':
                            cmd_string = "md5sum -c %s" % tmp_name
                            # print(dir_path)
                            # print(cmd_string)
                            flag, output, error = cmd_run(cmd_string, cwd=dir_path, retry_max=5, silence=True,
                                                          log_file=None)
                            print(output)

        check_md5(args.dir_path)

    elif args_dict["subcommand_name"] == "blast2DB":
        from toolbiox.api.common.genome.blast import blast_to_sqlite

        blast_to_sqlite(args.db_fasta, args.input_bls, None,
                        None, 6, None, None, None, False, args.gzip_flag)


    elif args_dict["subcommand_name"] == "id_replace":
        import re
        import sys

        target_file = sys.argv[1]
        map_file = sys.argv[2]
        output_file = sys.argv[3]

        replace_dict = {}
        with open(map_file, 'r') as f:
            for each_line in f:
                each_line.strip()
                a,b = each_line.split()
                replace_dict[a] = b

        with open(output_file, 'w') as fo:
            with open(target_file, 'r') as f:
                for each_line in f:
                    each_line.strip()
                    get_list = list(set(re.findall(r'[a-zA-Z]+_\d+', each_line)))
                    num = 0
                    
                    from_string = None
                    for i in get_list:
                        if i in replace_dict:
                            num += 1
                            from_string = i

                    if num > 1:
                        raise ValueError('two more match %s' % each_line)
                    elif num == 1:
                        to_string = replace_dict[from_string]
                        each_line = each_line.replace(from_string, to_string)

                    fo.write(each_line)



