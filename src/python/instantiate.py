import sqlite3
import argparse
from os import path

def instantiate_db(sqlite_filename):
    if path.isfile(sqlite_filename):
        raise FileExistsError(f"Database file {sqlite_filename} already exists")

    print(f"Creating SQLITE3 database {sqlite_filename}")
    con = sqlite3.connect(sqlite_filename)
    cur = con.cursor()

    cur.execute("""CREATE TABLE simdata(project,
                codename,
                path_to_source_code,
                path_to_executable,
                executable_version,
                executable_hash,
                run_timestamp,
                source_code_git_commit,
                path_to_input_file,
                input_file_hash,
                output_path_prefix,
                output_files,
                vis_output_prefix,
                vis_files,
                info,
                backup_paths,
                json_info
                )""")

    con.commit()
    con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='DBInstantiater',
                        description='Creates an empty SQLITE3 database with all the required columns')

    parser.add_argument('-f', '--dbfilename', help="Path to file where database will be", required=True)

    args = parser.parse_args()
    instantiate_db(args.dbfilename)