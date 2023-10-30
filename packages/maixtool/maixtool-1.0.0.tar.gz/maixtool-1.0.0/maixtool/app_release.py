import os
import shutil
import yaml
import zipfile
from datetime import datetime
import hashlib

def check_app_info(app_info, project_path):
    keys = ["id", "name", "version", "author", "desc", "files"]
    for key in keys:
        if key not in app_info:
            raise ValueError("app.yaml must contain {} keyword".format(key))
    # check version format, should be major.minor.patch
    version = app_info["version"]
    version = version.split(".")
    try:
        version = [int(x) for x in version]
    except Exception:
        raise ValueError("app.yaml version must be major.minor.patch, e.g. 1.0.0")
    # check icon
    if (not "icon" in app_info) or (not app_info["icon"]):
        return
    icon = app_info["icon"]
    ok = False
    for k, path in app_info["files"].items():
        is_dir = os.path.isdir(os.path.join(project_path, k))
        if is_dir:
            path0 = icon.replace(path, k)
            if os.path.exists(os.path.join(project_path, path0)):
                ok = True
                break
        elif path == icon:
            ok = True
            break
    if not ok:
        raise ValueError("app.yaml icon path({}) must be in files list's destination path".format(icon))

def get_app_info(project_path):
    app_info_path = os.path.join(project_path, "app.yaml")
    if not os.path.exists(app_info_path):
        app_info_path = os.path.join(project_path, "app.yml")
    if os.path.exists(app_info_path):
        # load app info from yaml file
        with open(app_info_path, "r") as f:
            app_info = yaml.load(f, Loader=yaml.FullLoader)
            check_app_info(app_info, project_path)
            return app_info
    return None

def copy_files(files, src_dir, dst_dir):
    for src, dst in files.items():
        if not os.path.exists(src):
            raise FileNotFoundError("file {} not found".format(src))
        if not os.path.isabs(src):
            src = os.path.join(src_dir, src)
        # check path, do not allow write to dangerous path
        dst_abs = os.path.abspath(os.path.join(dst_dir, dst))
        if not dst_abs.startswith(dst_dir):
            raise ValueError("file {} copy to {} is not allowed".format(src, dst_abs))
        os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
        if os.path.isdir(src):
            print("-- copy dir: {} -> {}".format(src, dst))
            shutil.copytree(src, dst_abs)
        else:
            print("-- copy file: {} -> {}".format(src, dst))
            shutil.copyfile(src, dst_abs)

def copy_app_files(app_info, project_path, dst_dir):
    '''
        copy project files to dst_dir, current dir is project_path
        app_info["files"]: list, file list to copy
    '''
    files = app_info.get("files", {})
    if not files:
        return
    copy_files(files, project_path, dst_dir)


def pack(project_path, bin_path="main.py", extra_files = {}):
    '''
        Find main.py and app.yaml in current directory, pack to dist/app_id_vx.x.x.zip,
        with a app_id directory in it.
    '''
    app_yaml = "app.yaml"
    app_info = get_app_info(project_path)
    if not app_info:
        raise FileNotFoundError("app.yaml not found in current directory")
    if not os.path.exists(bin_path):
        raise FileNotFoundError("{} not found".format(bin_path))
    app_id = app_info["id"]
    temp_dir = os.path.join(project_path, "dist", "pack", app_id)
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)
    # copy main.py
    if bin_path.endswith(".py"):
        bin_name = "main.py"
    elif bin_path.endswith(".sh"):
        bin_name = "main.sh"
    else:
        bin_name = app_id
    shutil.copyfile(bin_path, os.path.join(temp_dir, bin_name))
    # copy app.yaml
    shutil.copyfile(app_yaml, os.path.join(temp_dir, app_yaml))
    copy_app_files(app_info, project_path, temp_dir)
    copy_files(extra_files, project_path, temp_dir)
    # zip
    version_str = "_v" + app_info["version"]
    zip_path = os.path.join(project_path, "dist", app_id + version_str +".zip")
    os.chdir(os.path.dirname(temp_dir))
    if os.path.exists(zip_path):
        os.remove(zip_path)
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    with zipfile.ZipFile(zip_path,'w', zipfile.ZIP_DEFLATED) as target:
        for i in os.walk(os.path.basename(temp_dir)):
            for n in i[2]:
                target.write(os.path.join(i[0],n))
    os.chdir(project_path)

    release_info_path = os.path.join(project_path, "dist", "release_info_v{}.yaml".format(app_info["version"]))
    release_info = {
        "app_info": app_info,
        "path": zip_path,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sha256sum": hashlib.sha256(open(zip_path, "rb").read()).hexdigest(),
        "filename": os.path.basename(zip_path),
        "filesize": os.path.getsize(zip_path)
    }

    print("-- write release info to dist/release_info.yaml")
    with open(release_info_path, "w") as f:
        yaml.dump(release_info, f, encoding="utf-8", allow_unicode=True)

    return zip_path
