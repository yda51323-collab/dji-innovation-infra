#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""由节点清单生成域名 -> 节点映射，输出 nginx 或 DNS 草稿。"""
import argparse
import sys

DOMAIN = "dji-innovations.com"
ZONES = ("ap-east", "ap-south", "cn-south")


def fqdn(host):
    if host.endswith("." + DOMAIN) or host == DOMAIN:
        return host
    return "%s.%s" % (host, DOMAIN)


def load(path):
    nodes = []
    section = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("#"):
                continue
            if line.startswith("["):
                section = line.strip("[]")
                continue
            parts = line.split()
            kv = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
            nodes.append({"name": parts[0], "group": section, "vars": kv})
    return nodes


def build(nodes, zone):
    mapping = {}
    for n in nodes:
        if n["vars"].get("zone") != zone:
            continue
        for host in n["vars"].get("api_host", "").split(","):
            if not host:
                continue
            mapping.setdefault(fqdn(host), []).append(n["vars"].get("ansible_host"))
    return mapping


def render_nginx(mapping):
    out = []
    for host, upstreams in sorted(mapping.items()):
        out.append("server_name %s;" % host)
        for up in upstreams:
            out.append("    server %s:8443 max_fails=3;" % up)
    return "\n".join(out)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default="deploy/inventory/hosts.ini")
    ap.add_argument("--zone", default="ap-east", choices=ZONES)
    ap.add_argument("--format", default="nginx", choices=("nginx", "dns"))
    args = ap.parse_args(argv)
    mapping = build(load(args.inventory), args.zone)
    if args.format == "nginx":
        print(render_nginx(mapping))
    else:
        for host, ups in sorted(mapping.items()):
            print("%s 300 IN A %s" % (host, ups[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
