import os
import subprocess
from datetime import datetime

# Определяем путь к репозиторию относительно этого файла
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
POOL_PATH = os.path.join(REPO_PATH, "pool")
DIST_PATH = os.path.join(REPO_PATH, "dists", "stable", "main")
ARCHS = ["binary-arm64", "binary-all"]
def run(cmd):
    """Выполняет команду и показывает ошибки, если есть"""
    print(f"🛠️  {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Ошибка: {result.stderr}")
    else:
        print(result.stdout.strip())

def generate_packages():
    """Создаёт Packages и Packages.gz"""
    for arch in ARCHS:
        arch_path = os.path.join(DIST_PATH, arch)
        os.makedirs(arch_path, exist_ok=True)
        packages_file = os.path.join(arch_path, "Packages")
        run(f"apt-ftparchive packages {POOL_PATH} > {packages_file}")
        run(f"gzip -fk {packages_file}")

def generate_release():
    """Создаёт Release файл"""
    release_path = os.path.join(REPO_PATH, "dists", "stable", "Release")
    content = f"""Origin: Sergey Termux Repo
Label: termux-repo
Suite: stable
Codename: stable
Version: 1.0
Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC")}
Architectures: all arm64
Components: main
Description: Custom Termux APT repository
"""
    with open(release_path, "w") as f:
        f.write(content)
    print(f"✅ Release файл обновлён: {release_path}")

def git_commit_push():
    """Делает git add, commit и push"""
    os.chdir(REPO_PATH)
    run("git add dists/")
    run('git commit -m "Auto update Packages and Release" || echo "No changes"')
    run("git push")

def main():
    print("🚀 Обновление APT-репозитория Termux\n")
    generate_packages()
    generate_release()
    git_commit_push()
    print("\n✅ Репозиторий успешно обновлён и запушен!")

if __name__ == "__main__":
    main()
