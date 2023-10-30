# nonebot-plugin-bili-push-koon

B 订阅推送插件 for Kook

支持 Kook 协议

原项目：[bili-push for Onebot](https://github.com/SuperGuGuGu/nonebot_plugin_bili_push)

## --不要配置“使用\[链接]推送“，不然可能会导致触发敏感词导致账号封禁--

## 示例

![输入图片描述](README_md_files/9cf89890-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)
![输入图片描述](README_md_files/7fd7ee50-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)

## 安装

（以下方法二选一）

一.命令行安装：

```python
nb plugin install nonebot-plugin-bili-push-kook
```

二.pip 安装：

1.执行此命令

```python
pip install nonebot-plugin-bili-push-kook
```

2.修改 pyproject.toml 使其可以加载插件

```python
plugins = [”nonebot-plugin-bili-push-kook“]
```

## 配置

在 nonebot2 项目的`.env`文件中选填配置

1.配置管理员账户，只有管理员才能添加订阅

```markup
SUPERUSERS=["12345678"] # 配置 NoneBot 超级用户
```

2.插件数据存放位置，默认为 “./”。

```markup
bilipush_basepath="./"
```

3.命令前缀，默认为"/"

```markup
COMMAND_START=["/"]
```

详细配置方法- [详细配置](https://github.com/SuperGuGuGu/nonebot_plugin_bili_push_kook/blob/master/Config.md)

## To-Do

- [ ] 从 OB 迁移至 Kook

- [ ] at_all 功能

## 交流

- 交流群[鸽子窝里有鸽子（291788927）](https://qm.qq.com/cgi-bin/qm/qr?k=QhOk7Z2jaXBOnAFfRafEy9g5WoiETQhy&jump_from=webapi&authKey=fCvx/auG+QynlI8bcFNs4Csr2soR8UjzuwLqrDN9F8LDwJrwePKoe89psqpozg/m)

- 有疑问或者建议都可以进群唠嗑唠嗑。
