def diff_to_custom_format(diff):
    search_lines = []
    replace_lines = []
    in_search_block = False
    in_replace_block = False
    in_block = False
    lines = diff.splitlines(True)  # 保留换行符
    title=""
    for i, line in enumerate(lines):
        if line.startswith('---'):
            title=line[6:]
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            continue
        if line.startswith('-') or line.startswith('+'):
            in_block = True
        elif in_block == True:
            in_block= False
            for j in range(i+1, len(lines)):
                print(j,len(lines))
                if lines[j].startswith('-') or lines[j].startswith('+'):
                    in_block = True
                    
        if line.startswith('-'):
            search_lines.append(line[1:])  # 去掉 `-` 号，保留内容和空格
        elif line.startswith('+'):
            replace_lines.append(line[1:])  # 去掉 `+` 号，保留内容和空格
        else:
            if in_block:
                search_lines.append(line)
                replace_lines.append(line)

    # 如果最后还有未关闭的块，添加相应的结束标记
    if in_search_block and not in_replace_block:
        search_lines.append('>>>>>>> REPLACE\n')
    elif in_replace_block and not in_search_block:
        replace_lines.append('>>>>>>> REPLACE\n')

    # 拼接搜索和替换块
    search = ''.join(search_lines)
    replace = ''.join(replace_lines)
    # 最终结果
    result = f"""
```python
### {title}<<<<<<< SEARCH
{search}=======
{replace}>>>>>>> REPLACE
```"""
    return result

# 示例diff文本
diff_text = """diff --git a/django/template/backends/django.py b/django/template/backends/django.py
index 978ae57..dc7cd19 100644
--- a/django/template/backends/django.py
+++ b/django/template/backends/django.py
@@ -41,7 +41,13 @@ class DjangoTemplates(BaseEngine):
         applications and the supplied custom_libraries argument.
         libraries = get_installed_libraries()
-        libraries.update(custom_libraries)
+        for name, lib in custom_libraries.items():
+            if name in libraries:
                 raise ValueError(
+                    f"Template tag library '{name}' is already registered with {libraries[name]}. "
+                    f"Cannot register it with {lib}."
+                )
+            libraries[name] = lib
        return libraries
"""

# 转换为自定义格式
custom_format_output = diff_to_custom_format(diff_text)
print(custom_format_output)
