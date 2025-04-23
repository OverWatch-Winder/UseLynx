import json
import os
import requests
import sys
import subprocess
import tarfile
import io

def get_current_commit_title():
    try:
        result = subprocess.run(['git', 'log', '-1', '--pretty=format:%s'], capture_output=True, text=True, check=True)
        commit_title = result.stdout.strip()
        return commit_title
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"unknow error: {e}")
        return None

def get_package_version():
    package_json_path = os.path.join(os.path.dirname(os.getcwd()), 'package.json')
    with open(package_json_path, 'r') as f:
        package_info = json.load(f)
    return package_info.get('version')

def get_major_minor(version):
    parts = version.split('.')
    return '.'.join(parts[:2])


def get_latest_matching_version(major_minor, package_name):
    # 请求 npm 包信息
    url = f'https://registry.npmjs.org/{package_name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        versions = list(data.get('versions', {}).keys())
        matching_versions = [v for v in versions if v.startswith(major_minor + '.')]
        if matching_versions:

            matching_versions.sort(key=lambda x: list(map(int, x.split('.'))))
            return matching_versions[-1]
    return None

def get_tarball_url(package_name, version):
    url = f"https://registry.npmjs.org/{package_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["versions"][version]["dist"]["tarball"]
    except (requests.RequestException, KeyError):
        print("tarball link error")
        return None

def extract_changelog(tarball_url):
    try:
        response = requests.get(tarball_url)
        response.raise_for_status()
        with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
            changelog_files = [
                member for member in tar.getmembers()
                if "CHANGELOG" in member.name.upper()
            ]
            if changelog_files:
                changelog_file = tar.extractfile(changelog_files[0])
                return changelog_file.read().decode("utf-8")
            return "unknown CHANGELOG file"
    except (requests.RequestException, tarfile.TarError, UnicodeDecodeError):
        print("extract CHANGELOG error")
        return None

def increment_patch_version(version):
    if version:
        parts = list(map(int, version.split('.')))
        parts[2] += 1
        return '.'.join(map(str, parts))
    return None


def append_to_changelog(new_version):
    changelog_path = 'changelog'
    with open(changelog_path, 'a') as f:
        f.write(f"{new_version}\n")


def main():
    if len(sys.argv) < 2:
        print("use package_name params。")
        sys.exit(1)
    package_name = sys.argv[1]
    package_version = get_package_version()
    major_minor = get_major_minor(package_version)
    latest_version = get_latest_matching_version(major_minor, package_name)
    tarball_url = get_tarball_url(package_name, latest_version)
    if tarball_url:
        changelog = extract_changelog(tarball_url)
    if latest_version:
        new_version = increment_patch_version(latest_version)
    else:
        new_version = f"{major_minor}.0"
    commit_title = get_current_commit_title()
    lines = changelog.split('\n' , 1)
    append_to_changelog(f"{lines[0]}\n\n ## {new_version}\n- {commit_title}\n {lines[1]}")
    print(f"new version append to changelog: {new_version}")


if __name__ == "__main__":
    main()
