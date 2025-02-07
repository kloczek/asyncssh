#!/usr/bin/env python3.7
#
# Copyright (c) 2013-2024 by Ron Frederick <ronf@timeheart.net> and others.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v2.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-2.0/
#
# This program may also be made available under the following secondary
# licenses when the conditions for such availability set forth in the
# Eclipse Public License v2.0 are satisfied:
#
#    GNU General Public License, Version 2.0, or any later versions of
#    that license
#
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

import asyncio
import asyncssh
import sys
from typing import Optional

class MySSHTCPSession(asyncssh.SSHTCPSession):
    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        # We use sys.stdout.buffer here because we're writing bytes
        sys.stdout.buffer.write(data)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('Direct connection error:', str(exc), file=sys.stderr)

async def run_client() -> None:
    async with asyncssh.connect('localhost') as conn:
        chan, session = await conn.create_connection(MySSHTCPSession,
                                                     'www.google.com', 80)

        # By default, TCP connections send and receive bytes
        chan.write(b'HEAD / HTTP/1.0\r\n\r\n')
        chan.write_eof()

        await chan.wait_closed()

try:
    asyncio.run(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
