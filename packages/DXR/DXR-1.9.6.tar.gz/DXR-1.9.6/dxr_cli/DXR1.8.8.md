# dxr CLI 工具

dxr 是一个命令行界面 (CLI) 工具，旨在帮助您执行各种任务，例如运行 Python 脚本，与 GPT-3 交流，并执行云端 Bash 脚本。本文档将详细介绍如何使用此工具。

## 功能

1. 使用 GPT-3 或 GPT-4 与用户进行交互式聊天。
2. 自动执行云端 Bash 脚本。
3. 输入 Git 问题并获取有关 Git 命令的建议。
4. 直接运行 Python 脚本并从 OpenAI 获得解决错误的建议。
5. 运行任意命令并在出现错误时捕获并显示错误输出及其上下文。

## 如何使用

首先，确保已安装以下库：

```bash
pip install click rich requests DXR openai tiktoken
```

你可以从主菜单中选择不同的功能。以下是每个功能的详细说明。

### 1. chat

使用 GPT-3 或 GPT-4 与用户进行交互式聊天。运行以下命令：

```bash
dxr chat --model gpt-3.5-turbo --maxtoken 4096
```
或者，您可以直接使用以下命令：
```bash
dxr chat
```

选项：

- `--model`: 选择 GPT 模型，默认为 "gpt-3.5-turbo"
- `--maxtoken`: 单个提示的最大令牌数，默认为 4096

### 2. bash

执行云端上的脚本。运行以下命令：

```bash
dxr bash
```


### 3. git

询问有关 Git 的问题, 并向用户提供 Git 命令建议。运行以下命令：

```bash
dxr git --model gpt-3.5-turbo --maxtoken 4096
```
或者，您可以直接使用以下命令：
```bash
dxr git
```

选项：

- `--model`: 选择 GPT 模型，默认为 "gpt-3.5-turbo"
- `--maxtoken`: 单个提示的最大令牌数，默认为 4096

### 4. python

用于直接运行Python脚本，并获取运行时的错误输出，将错误输出发送给 OpenAI，让 OpenAI 帮助解决问题。运行以下命令：

```bash
dxr python --model gpt-3.5-turbo --maxtoken 4096 script.py
```
或者，您可以直接使用以下命令：
```bash
dxr python script.py
```

选项：

- `--model`: 选择 GPT 模型，默认为 "gpt-3.5-turbo"
- `--maxtoken`: 单个提示的最大令牌数，默认为 4096
- `script`: 要执行的 Python 脚本文件

### 5. run

接收不固定参数的命令并执行它们。如果发生错误，将捕获并显示错误输出及其上下文。运行以下命令：

```bash
dxr run --model gpt-3.5-turbo --maxtoken 4096 --lines 100 your-command here
```
或者，您可以直接使用以下命令：
```bash
dxr run your-command here
```

选项：

- `--model`: 选择 GPT 模型，默认为 "gpt-3.5-turbo"
- `--maxtoken`: 单个提示的最大令牌数，默认为 4096
- `--lines`: 在错误上下文中捕获的前后行数，默认为 100

## 总结

dxr CLI 工具提供了一种功能丰富且易于使用的方式，可帮助用户执行各种任务。无论是与 GPT-3 聊天、运行 Python 脚本，还是执行云端 Bash 脚本，dxr 都能帮助您更有效地完成工作。尝试一下吧，看看它能如何改善您的工作流程！