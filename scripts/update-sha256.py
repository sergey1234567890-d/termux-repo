#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

# Пути
repo_root = os.path.expanduser("~/termux-repo")
stable_dir = os.path.join(repo_root, "dists/stable")
release_path = os.path.join(stable_dir, "Release")

# Список файлов для хэшей
files = [
    "main/binary-all/Packages",
    "main/binary-all/Packages.gz",
    "main/binary-arm64/Packages",
    "main/binary-arm64/Packages.gz",
]

print("🔐 Пересчёт SHA256 контрольных сумм...")

# Считаем SHA256 и длину
checksums = []
for f in files:
    full_path = os.path.join(stable_dir, f)
    # Получаем sha256sum
    sha256 = subprocess.check_output(["sha256sum", full_path]).decode().split()[0]
    # Получаем размер файла
    size = subprocess.check_output(["stat", "-c%s", full_path]).decode().strip()
    checksums.append(f" {sha256} {size} {f}")

# Читаем текущий Release без старых SHA256
with open(release_path, "r") as f:
    lines = f.readlines()

new_lines = []
in_sha = False
for line in lines:
    if line.startswith("SHA256:"):
        in_sha = True
        continue
    if in_sha and (line.startswith(" ") or line.strip() == ""):
        continue
    in_sha = False
    new_lines.append(line)

# Добавляем новую секцию SHA256
new_lines.append("\nSHA256:\n")
for c in checksums:
    new_lines.append(c + "\n")

# Записываем обновлённый Release
with open(release_path, "w") as f:
    f.writelines(new_lines)

print("✅ Файл Release обновлён с новыми SHA256.")

# Подписываем
print("🔏 Подпись Release...")
subprocess.run(["gpg", "--clearsign", "-o", os.path.join(stable_dir, "InRelease"), release_path])
subprocess.run(["gpg", "-abs", "-o", os.path.join(stable_dir, "Release.gpg"), release_path])

# Коммит и push
print("🚀 Отправка в GitHub...")
subprocess.run(["git", "-C", repo_root, "add", "dists/stable"])
subprocess.run(["git", "-C", repo_root, "commit", "-m", "Update SHA256 checksums"])
subprocess.run(["git", "-C", repo_root, "push"])

print("🎯 Готово! Все SHA256 хэши обновлены, подписаны и запушены.")
