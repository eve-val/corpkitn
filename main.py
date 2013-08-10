#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

import kitnirc.client
import kitnirc.contrib.admintools
import kitnirc.modular


def main():
    parser = argparse.ArgumentParser(description="CorpCat")
    parser.add_argument("config", help="Path to config file")
    args = parser.parse_args()

    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(name)s:%(lineno)04d - %(message)s")
    log_handler.setFormatter(log_formatter)

    _log = logging.getLogger()
    _log.addHandler(log_handler)
    _log.setLevel(logging.DEBUG)

    client = kitnirc.client.Client()
    controller = kitnirc.modular.Controller(client, args.config)

    def is_admin(controller, client, user):
        return any(user == admin for admin, level
                   in controller.config.items('admin'))
    kitnirc.contrib.admintools.is_admin = is_admin

    controller.start()

    c = lambda field: controller.config.get('server', field)
    client.connect(
        c('nick'),
        username=c('username'),
        realname=c('realname'),
        # Network-specific module provides auth
        host=c('host'),
        port=controller.config.getint('server', 'port'))

    client.run()


if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et:
