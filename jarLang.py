import os
import zipfile

INPUT_DIR = "mods1"
OUTPUT_DIR = "output"

def extract_lang_files():
    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".jar"):
                jar_path = os.path.join(root, file)
                with zipfile.ZipFile(jar_path, "r") as jar:
                    for entry in jar.namelist():
                        if entry.startswith("assets/") and entry.endswith(".lang") and "/lang/" in entry:
                            output_path = os.path.join(OUTPUT_DIR, entry)
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            with jar.open(entry) as src, open(output_path, "wb") as dst:
                                dst.write(src.read())
                            print(f"Extracted: {entry} -> {output_path}")

def modify_lang_files():
    for root, _, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(".lang"):
                lang_path = os.path.join(root, file)
                try:
                    with open(lang_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    with open(lang_path, "r", encoding="latin-1") as f:
                        lines = f.readlines()

                new_lines = []
                for line in lines:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        if not value.strip().startswith("§7"):
                            value = "§7" + value.strip()
                        else:
                            value = value.strip()
                        new_lines.append(f"{key}={value}\n")
                    else:
                        new_lines.append(line)

                with open(lang_path, "w", encoding="utf-8", errors="ignore") as f:
                    f.writelines(new_lines)
                print(f"Modified: {lang_path}")

if __name__ == "__main__":
    extract_lang_files()
    modify_lang_files()
    print("Done!")
