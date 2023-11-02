# author: wangye(Wayne)
# license: Apache Licence
# file: gettool.py
# time: 2023-11-01-22:47:10
# contact: wang121ye@hotmail.com
# site:  wangyendt@github.com
# software: PyCharm
# code is far away from bugs.


import argparse
import tempfile
import shutil
import subprocess
import os

tool_map = {
    'pangolin': 'visualization/pangolin'
}


def fetch_tool(tool_name, target_dir=None):
    cwd = os.getcwd()
    if target_dir is None:
        target_dir = os.path.join(cwd, tool_map[tool_name])
    print(target_dir)
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the repository
        subprocess.run(["git", "clone", "--sparse", "https://github.com/wangyendt/cpp_tools", temp_dir])
        # Change to the temporary directory
        os.chdir(temp_dir)
        # Enable sparse-checkout
        subprocess.run(["git", "sparse-checkout", "set", tool_map[tool_name]])
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        # Copy the tool to the target directory
        shutil.copytree(tool_map[tool_name], target_dir)
        print(f"Tool has been copied to {target_dir}")
    os.chdir(cwd)


def main():
    parser = argparse.ArgumentParser(description='Tool fetcher.')

    parser.add_argument('name_pos', nargs='?', default=None, help='Name of the tool (positional)')
    parser.add_argument('-n', '--name', default=None, help='Name of the tool')
    parser.add_argument('-U', '--upgrade', action='store_true', help='Upgrade the tool')
    parser.add_argument('-f', '--force', action='store_true', help='Force action')

    args = parser.parse_args()

    # 如果通过 -n 或 --name 提供了名称，则使用它，否则使用位置参数提供的名称
    tool_name = args.name if args.name is not None else args.name_pos

    # 检查是否提供了名称
    if tool_name is None:
        parser.error("the following arguments are required: name")

    fetch_tool(tool_name)

    print(f"Fetching tool: {tool_name}")
    if args.upgrade:
        print("(not implemented yet)")
    if args.force:
        print("(not implemented yet)")


if __name__ == '__main__':
    main()
