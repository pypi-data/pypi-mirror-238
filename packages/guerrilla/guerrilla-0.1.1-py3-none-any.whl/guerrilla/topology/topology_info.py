import os

import yaml


def prepare_json(context, file_name=None):
    # try:
    #     lib_path = os.path.abspath(os.environ['PYTHONPATH'])
    # except:
    #     raise Exception("PYTHONPATH not found!")
    abs_path = os.getcwd()
    print("abspath:", abs_path)
    try:
        with open(f"{abs_path}/{file_name}.yaml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except Exception:
        print("topology can not be found, so use default instead")
        with open(f"{abs_path}/default.yaml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

    context.dut = {}
    context.hosts = {}
    context.dut_info = data["dut_info"]
    context.host_info = data["host_info"]
    context.generator_info = data["generator_info"]
