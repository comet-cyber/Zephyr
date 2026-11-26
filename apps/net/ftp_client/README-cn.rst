.. zephyr:code-sample:: ftp-client
   :name: FTP 客户端 Shell 示例
   :relevant-api: ftp_client

   通过 Zephyr Shell 与 FTP 服务器交互的 FTP 客户端示例。

概述
********

本示例演示如何使用 FTP 客户端库与主机上运行的 FTP 服务器进行交互。FTP 命令通过 Zephyr 提供的 FTP Shell 模块对外暴露。

环境要求
**************

- :ref:`networking_with_eth_qemu` 、 :ref:`networking_with_qemu` 或 :ref:`networking_with_native_sim`
- Linux 主机

构建与运行
********************

按如下方式构建 Zephyr 版本的应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ftp_client
   :board: <board_to_use>
   :goals: build
   :compact:

本示例需要一个正在运行的 FTP 服务器来进行交互。例如，可以通过运行内置 FTP 服务器功能的 Python `pyftpdlib`_ 模块来实现：

.. code-block:: bash

   pip install pyftpdlib
   mkdir file_root
   echo "some test data" > file_root/test_file.txt
   python3 -m pyftpdlib -p 2121 --write --directory=file_root

上述命令会安装所需的 Python 软件包，创建 FTP 服务器将暴露的根目录，并创建一个测试文件。请注意，该服务器将以写入模式（write-mode）运行，允许创建、删除和覆盖文件及目录——如果使用测试目录以外的其他根目录位置，请务必谨慎。

在 net-tools 中启动 :command:`net-setup.sh` ：

.. code-block:: bash

   ./net-setup.sh

针对 native_sim 构建并运行 FTP 客户端示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ftp_client
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:

示例将打印欢迎信息，并暴露可供交互的网络 Shell 模块：

.. code-block:: console

   [00:00:00.000,000] <inf> net_config: Initializing network
   [00:00:00.000,000] <inf> net_config: IPv4 address: 192.0.2.1
   [00:00:00.110,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:00.110,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:00.110,000] <inf> ftp_client_sample: Starting FTP client sample
   [00:00:00.110,000] <inf> ftp_client_sample: Network connectivity established.
   [00:00:00.110,000] <inf> ftp_client_sample: You can interact with FTP server via shell.

使用 ``net ftp connect`` 命令连接到 FTP 服务器。该服务器默认开放 ``anonymous`` 用户并使用占位密码：

.. code-block:: console

   uart:~$ net ftp connect anonymous null 192.0.2.2 2121
   220 pyftpdlib 2.1.0 ready.
   530 Log in with USER and PASS first.
   331 Username ok, send password.
   230 Login successful.

成功连接后，即可执行各种 FTP 命令与主机上的文件系统进行交互。

列出目录内容：

.. code-block:: console

   uart:~$ net ftp ls
   227 Entering passive mode (192,0,2,2,146,7).
   150 File status okay. About to open data connection.
   -rw-r--r--   1 user     domain users       15 Feb 20 11:16 test_file.txt
   226 Transfer complete.

读取文件内容：

.. code-block:: console

   uart:~$ net ftp get test_file.txt
   227 Entering passive mode (192,0,2,2,222,177).
   150 File status okay. About to open data connection.
   some test data
   226 Transfer complete.

创建新目录、切换工作目录并打印当前工作目录：

.. code-block:: console

   uart:~$ net ftp mkdir test_dir
   257 "/test_dir" directory created.
   uart:~$ net ftp cd test_dir
   250 "/test_dir" is the current directory.
   uart:~$ net ftp pwd
   257 "/test_dir" is the current directory.

创建新文件、打印其内容，然后将其删除：

.. code-block:: console

   uart:~$ net ftp put new_file.txt
   Input mode (max 2048 characters). End the line with \ to start a new one:
   New file content\

   227 Entering passive mode (192,0,2,2,131,169).
   150 File status okay. About to open data connection.
   226 Transfer complete.
   uart:~$ net ftp get new_file.txt
   227 Entering passive mode (192,0,2,2,140,157).
   150 File status okay. About to open data connection.
   New file content
   226 Transfer complete.
   uart:~$ net ftp rm new_file.txt
   250 File removed.

断开与服务器的连接：

.. code-block:: console

   uart:~$ net ftp disconnect
   221 Goodbye.

可以使用 ``--help`` 参数列出所支持 FTP 命令的完整列表：

.. code-block:: console

   uart:~$ net ftp --help
   ftp - FTP client commands
   Subcommands:
     connect     : Connect to FTP server.
                   Usage: connect <username> <password> <hostname> [<port> <sec_tag>]
     disconnect  : Disconnect from FTP server.
                   Usage: disconnect
     status      : Print connection status.
                   Usage: status
     pwd         : Print working directory.
                   Usage: pwd
     ls          : List information about folder or file.
                   Usage: ls [<options> <path>]
     cd          : Change working directory.
                   Usage: cd <path>
     mkdir       : Create directory.
                   Usage: mkdir <dir_name>
     rmdir       : Delete directory.
                   Usage: rmdir <dir_name>
     rename      : Rename a file.
                   Usage: rename <old_name> <new_name>
     rm          : Delete a file.
                   Usage: rm <file_name>
     get         : Read file content.
                   Usage: get <file_name>
     put         : Write to a file.
                   Usage: put <file_name> [<data>]
     append      : Append a file.
                   Usage: append <file_name> <data>
     mode        : Select transfer type.
                   Usage: mode <ascii/binary>

.. _pyftpdlib: https://github.com/giampaolo/pyftpdlib
