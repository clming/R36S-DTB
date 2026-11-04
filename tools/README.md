# 设备树工具

完整使用说明统一维护在[项目指南第 6.6 节](../docs/PROJECT_GUIDE.zh-CN.md#66-仓库自带工具使用说明)，包含 Windows/Linux 命令、批量转换、文件对比和候选排序示例。

| 文件 | 用途 |
| --- | --- |
| `dt_tools.py` | Python 3.6+ 命令行入口，仅使用标准库 |
| `bin/windows-x86_64/dtc.exe` | Windows x64 的 DTC 1.7.2 |
| `bin/linux-x86_64/dtc` | Linux x86_64 的 DTC 1.7.2，首次使用需赋执行权限 |
| `vendor/manifest.json` | 下载来源、版本、源码归档地址和本地文件 SHA-256 |
| `vendor/DTC-LICENSE.txt` | 上游随二进制发布的 GPL v2 许可证 |
| `vendor/dtc-build-source.zip` | 对应发布标签的源码归档，含 DTC 源码、构建脚本和原始许可声明 |

DTC 上游为 [dgibson/dtc](https://github.com/dgibson/dtc)；本目录的两个可执行文件来自 [MathWorks 发布页](https://github.com/mathworks/dtc-build/releases)，发布标签和哈希见清单。第三方程序保留自身许可，仓库原有 README 许可声明不变。

Windows 版已在当前环境执行验证；Linux 版已核对 ELF x86_64 文件头及下载包 SHA-256，尚未在 Linux 上运行。Linux ARM 掌机应安装对应架构的 `dtc`，通过 `--dtc` 指定，不能执行这里的 x86_64 程序。
