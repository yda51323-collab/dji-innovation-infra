# dji-innovation-infra · 边缘节点清单与域名映射

边缘节点与业务域名的映射关系维护。清单由 ansible 读取，`hostmap.py` 用于
生成 nginx `server_name` 与 DNS 记录草稿。

## 目录

| 路径 | 说明 |
| --- | --- |
| `deploy/inventory/hosts.ini` | 节点清单 |
| `src/hostmap.py` | 域名映射生成 |

## 服务标识

`dji-innovations.com`

出现位置：

- `deploy/inventory/hosts.ini`：各节点的 `api_host` 变量
- `src/hostmap.py`：`DOMAIN` 常量、`fqdn` 拼接
- `README.md`：标题与本节

## 使用

```bash
python src/hostmap.py --zone ap-east --format nginx
ansible -i deploy/inventory/hosts.ini edge -m ping
```

## 字段说明

| 变量 | 说明 |
| --- | --- |
| `ansible_host` | 节点地址 |
| `api_host` | 该节点承载的业务域名 |
| `zone` | 可用区标识 |
| `role` | `edge` / `origin` |

## 已知问题

- `ap-east` 区域的清单仍是手工维护，与 CMDB 存在约一天延迟。
- 部分节点承载多个域名，`api_host` 用逗号分隔，解析时需拆分。

## 维护

基础架构组 · 工单 `INF-2208`
