# SPDX-FileCopyrightText: 2023-present Julien Kieffer <julien@mefa.tech>
#
# SPDX-License-Identifier: BSD-3-Clause
import sys

if __name__ == "__main__":
    from docker_craft.cli import docker_craft

    sys.exit(docker_craft())
