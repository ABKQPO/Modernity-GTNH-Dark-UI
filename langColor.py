import os

INPUT_DIR = "./"   # 放所有 .lang 文件的文件夹
OUTPUT_DIR = "output"      # 修改后的文件输出到这里

def modify_lang_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".lang"):
                lang_path = os.path.join(root, file)

                # 读取文件内容（尝试 utf-8，失败就用 latin-1）
                try:
                    with open(lang_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    with open(lang_path, "r", encoding="latin-1") as f:
                        lines = f.readlines()

                # 处理每一行
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

                # 保存到 output 文件夹，保持原文件名
                output_path = os.path.join(OUTPUT_DIR, file)
                with open(output_path, "w", encoding="utf-8", errors="ignore") as f:
                    f.writelines(new_lines)

                print(f"Modified: {output_path}")

if __name__ == "__main__":
    modify_lang_files()
    print("Done!")
