from .version import __version__
import sys, os

project_cmake = '''
cmake_minimum_required(VERSION 3.7.2)

set(SDK_ENV_NAME "MAIXCDK_PATH")
set(CUSTOM_COMPONENTS_PATH_ENV_NAME "MAIXCDK_EXTRA_COMPONENTS_PATH")

set(SDK_PATH_ENV $ENV{${SDK_ENV_NAME}})
set(CUSTOM_COMPONENTS_PATH_ENV $ENV{${CUSTOM_COMPONENTS_PATH_ENV_NAME}})

# Get SDK path
if(NOT SDK_PATH)
    get_filename_component(SDK_PATH ../../ ABSOLUTE)
    if(SDK_PATH_ENV)
        if(EXISTS ${SDK_PATH_ENV})
            set(SDK_PATH ${SDK_PATH_ENV})
        else()
            message(FATAL_ERROR "Env variable '${SDK_ENV_NAME}' set, but '${SDK_PATH_ENV}', path not exists")
        endif()
    endif()
endif()
if(NOT MAIXCDK_EXTRA_COMPONENTS_PATH)
    if(CUSTOM_COMPONENTS_PATH_ENV)
        if(EXISTS ${CUSTOM_COMPONENTS_PATH_ENV})
            set(MAIXCDK_EXTRA_COMPONENTS_PATH ${CUSTOM_COMPONENTS_PATH_ENV})
        else()
            message(FATAL_ERROR "Env variable '${CUSTOM_COMPONENTS_PATH_ENV_NAME}' set, but '${CUSTOM_COMPONENTS_PATH_ENV}', path not exists")
        endif()
    endif()
endif()

# Check SDK Path
if(NOT EXISTS ${SDK_PATH})
    message(FATAL_ERROR "SDK path Error, Please set SDK_PATH or ${SDK_ENV_NAME} variable")
endif()

# Get Toolchain path
if(NOT CONFIG_TOOLCHAIN_PATH)
    if(EXISTS $ENV{MY_TOOLCHAIN_PATH})
        set(CONFIG_TOOLCHAIN_PATH $ENV{MY_TOOLCHAIN_PATH})
    endif()
endif()

## Add preprocessor definitions for whole project
# add_definitions(-DAAAAA=1)

# Call compile
include(${SDK_PATH}/tools/cmake/compile.cmake)


# Project Name, default the same as project directory name
get_filename_component(parent_dir ${CMAKE_PARENT_LIST_FILE} DIRECTORY)
get_filename_component(project_dir_name ${parent_dir} NAME)

set(PROJECT_NAME ${project_dir_name}) # change this var if don't want the same as directory's

message("-- PROJECT_NAME:${PROJECT_NAME}")
project(${PROJECT_NAME})


'''

def exec_project_py():
    sdk_env_name = "MAIXCDK_PATH"
    custom_component_path_name = "MAIXCDK_EXTRA_COMPONENTS_PATH"

    # check main component
    if not os.path.exists("main"):
        print("")
        print("Error: can not find main component, please execute this command in your project root directory")
        print("")
        sys.exit(1)

    project_path = os.path.abspath(os.getcwd())

    sdk_path = None
    # get SDK absolute path from MAIXCDK_PATH env
    try:
        if os.environ[sdk_env_name] and os.path.exists(os.environ[sdk_env_name]):
            sdk_path = os.environ[sdk_env_name]
    except Exception:
        pass
    # check if in MaixCDK repo, higher priority
    path = os.path.abspath("../../")
    if os.path.exists(path+"/tools/cmake/project.py"):
        sdk_path = path

    if not sdk_path or not os.path.exists(sdk_path):
        print("")
        print("Error: can not find MaixCDK, please set MAIXCDK_PATH env to MaixCDK repo path")
        print("")
        sys.exit(1)

    print("-- SDK_PATH:{}".format(sdk_path))

    # get custom components path
    custom_components_path = None
    try:
        if os.environ[custom_component_path_name] and os.path.exists(os.environ[custom_component_path_name]):
            custom_components_path = os.environ[custom_component_path_name]
    except Exception:
        pass
    print("-- MAIXCDK_EXTRA_COMPONENTS_PATH: {}".format(custom_components_path if custom_components_path else "not set"))

    # set STAGING_DIR env for openwrt cross compile
    # build dir asides current file
    build_path = "build"
    if not os.environ.get("STAGING_DIR"):
        os.environ["STAGING_DIR"] = build_path+"/staging_dir"

    # check if no cmakelist file, write one
    if not os.path.exists("CMakeLists.txt"):
        with open("CMakeLists.txt", "w") as f:
            f.write(project_cmake)

    # execute project script from SDK
    project_file_path = sdk_path+"/tools/cmake/project.py"
    vars = {
        "project_path": project_path,
        "sdk_path": sdk_path,
        "custom_components_path": custom_components_path,
    }
    with open(project_file_path) as f:
        exec(f.read(), vars)

def check_install_requirement():
    if "install_env" in sys.argv and os.path.exists("requirements.txt"):
        # get -i arg value
        index_url = None
        index = sys.argv.index("-i")
        if index >= 0:
            index += 1
            if index < len(sys.argv):
                index_url = sys.argv[index]
        import subprocess
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        if index_url:
            cmd += ["-i", index_url]
        subprocess.check_call(cmd)
        sys.exit(0)

def main():
    check_install_requirement()
    exec_project_py()


