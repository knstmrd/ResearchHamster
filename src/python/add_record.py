import sqlite3
import argparse
from os import path
import hashlib
import datetime
import subprocess
import hashlib
import json

def add_record(cur,
               project_name,
               codename,
               path_to_source_code,
               path_to_executable,
               executable_version,
               executable_hash,
               run_timestamp, # yyyy_mm_dd_hh_mm_ss
               source_code_git_commit,
               path_to_input_file,
               input_file_hash,
               output_path_prefix,
               output_files,
               vis_output_prefix,
               vis_files,
               info,
               backup_paths,
               json_info):
    # this already assumes fully cleaned and corrected input
    pass

def convert_to_list(comma_separated_string):
    if comma_separated_string == "":
        return []
    else:
        return comma_separated_string.split(",")

def get_missing_and_add_record(cur,
                               project_name,
                               codename,
                               path_to_source_code,
                               path_to_executable,
                               run_timestamp, # yyyy_mm_dd_hh_mm_ss
                               path_to_input_file,
                               output_path_prefix,
                               output_files,
                               vis_output_prefix,
                               vis_files,
                               info,
                               backup_paths,
                               json_info):
    # get hashes, check and correct timestamp, etc.
    executable_version = get_executable_version(path_to_executable)
    executable_hash = get_file_hash(path_to_executable)
    run_timestamp = check_and_correct_timestamp(run_timestamp)
    source_code_git_commit = get_source_code_git_commit(path_to_source_code)
    input_file_hash = get_file_hash(path_to_input_file)

    # create empty lists, json dumps
    output_files = json.dumps(output_files)
    vis_files = json.dumps(vis_files)
    backup_paths = json.dumps(backup_paths)
    if json_info == "":
        json_info = {}
    json_info = json.dumps(json_info)

    add_record(cur,
               project_name,
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
               json_info)

def check_and_correct_timestamp(run_timestamp):
    # yy_mm_dd
    tsp = run_timestamp.split("_")
    if len(tsp) != 3 and len(tsp) != 6:
        raise ValueError(f"Incorrect format of timestamp {run_timestamp}")
    
    if len(tsp[0]) == 2:
        yearcorr = 2000
    else:
        yearcorr = 0

    tsp = [int(x) for x in tsp]
    d = datetime.date(yearcorr + tsp[0], tsp[1], tsp[2])
    t = datetime.time(*tsp[3:])
    dt = datetime.datetime.combine(d, t)
    return str(dt).replace("-", "_").replace(" ", "_").replace(":", "_")

def get_executable_version(path_to_executable):
    version = subprocess.run([path_to_executable, "--version"], capture_output=True)

    if version.returncode != 0:
        return "N/A"
    else:
        version = version.stdout.decode("UTF-8")
        if len(version) > 500:
            version = version[:500]  # in case some code produces nasty output
        return version

def get_file_hash(path_to_file):
    with open(path_to_file, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha1').hexdigest()

def get_source_code_git_commit(path_to_source_code):
    commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)

    if commit_hash.returncode != 0:
        return "N/A"

    commit_hash = commit_hash.stdout.decode("UTF-8")
    if commit_hash.endswith("\n"):
        commit_hash = commit_hash[:-1]

    uncommited_files = subprocess.run(["git", "ls-files", "-m"], capture_output=True)
    fileslist = uncommited_files.stdout.decode("UTF-8").split("\n")
    fileslist = [x for x in fileslist if x != ""]

    if len(fileslist) > 0:
        return commit_hash + f" + Uncommited changes in {fileslist}"
    else:
        return commit_hash


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='DBAddRecord',
                        description="Adds a record to an existing DB")

    parser.add_argument('-f', '--dbfilename', help="Path to file where database is located", required=True)

    parser.add_argument("--project", help="Project name", required=True)
    parser.add_argument("--codename", help="Name of code", required=True)
    parser.add_argument("--path_to_source_code", help="Path to source code", required=True)
    parser.add_argument("--path_to_executable", help="Path to executable (compiled code/julia or python executable)", required=True)
    parser.add_argument("--run_timestamp",
                        help="Timestamp of run (yy_mm_dd_hh_mm_ss or yy_mm_dd, year can be either yy or yyyy)",
                        required=True)
    parser.add_argument("--path_to_input_file", help="Path to input file (if any)", required=False, default="")
    parser.add_argument("--output_path_prefix", help="Directory where output is stored", required=True)
    parser.add_argument("--output_files", help="List of output files (if any), comma-separated", required=False, default="")
    parser.add_argument("--vis_output_prefix", help="Directory where visualization is stored (if any)", required=False, default="")
    parser.add_argument("--vis_files", help="List of visualization files (if any), comma-separated", required=False, default="")
    parser.add_argument("--info", help="Any additional info", required=True)
    parser.add_argument("--backup_paths", help="Paths to backups (if any), comma-separated", required=False, default="")
    parser.add_argument("--json_info", help="Any additional info in JSON format", required=False, default="")
    
    args = parser.parse_args()

    con = sqlite3.connect(args.dbfilename)
    cur = con.cursor()
    get_missing_and_add_record(cur, args.project, args.codename, args.path_to_source_code,
                               args.path_to_executable, args.run_timestamp, args.path_to_input_file,
                               args.output_path_prefix, args.output_files,
                               args.vis_output_prefix, args.vis_files,
                               args.info, args.backup_paths, args.json_info)
    con.commit()
    con.close()