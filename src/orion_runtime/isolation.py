"""Fail-closed worker network isolation for the supported Linux target."""

from __future__ import annotations

import ctypes
import errno
import platform
import socket
import sys


class WorkerIsolationError(RuntimeError):
    """Raised when the mandatory worker isolation boundary cannot be installed."""


class _SockFilter(ctypes.Structure):
    _fields_ = (
        ("code", ctypes.c_ushort),
        ("jt", ctypes.c_ubyte),
        ("jf", ctypes.c_ubyte),
        ("k", ctypes.c_uint),
    )


class _SockFprog(ctypes.Structure):
    _fields_ = (
        ("length", ctypes.c_ushort),
        ("filter", ctypes.POINTER(_SockFilter)),
    )


_BPF_LD_W_ABS = 0x20
_BPF_JMP_JEQ_K = 0x15
_BPF_RET_K = 0x06
_SECCOMP_RET_ALLOW = 0x7FFF0000
_SECCOMP_RET_ERRNO = 0x00050000
_SECCOMP_RET_KILL_PROCESS = 0x80000000
_PR_SET_NO_NEW_PRIVS = 38
_PR_SET_SECCOMP = 22
_SECCOMP_MODE_FILTER = 2
_AUDIT_ARCH = {
    "x86_64": 0xC000003E,
    "aarch64": 0xC00000B7,
}

_NETWORK_SYSCALLS = {
    "x86_64": (
        41,   # socket
        42,   # connect
        43,   # accept
        44,   # sendto
        45,   # recvfrom
        46,   # sendmsg
        47,   # recvmsg
        48,   # shutdown
        49,   # bind
        50,   # listen
        51,   # getsockname
        52,   # getpeername
        53,   # socketpair
        54,   # setsockopt
        55,   # getsockopt
        288,  # accept4
        299,  # recvmmsg
        307,  # sendmmsg
    ),
    "aarch64": (
        198,  # socket
        199,  # socketpair
        200,  # bind
        201,  # listen
        202,  # accept
        203,  # connect
        204,  # getsockname
        205,  # getpeername
        206,  # sendto
        207,  # recvfrom
        208,  # setsockopt
        209,  # getsockopt
        210,  # shutdown
        211,  # sendmsg
        212,  # recvmsg
        242,  # accept4
        243,  # recvmmsg
        269,  # sendmmsg
    ),
}


def install_worker_network_isolation() -> str:
    """Deny all socket syscalls before any frozen Core module is imported."""
    if sys.platform == "linux":
        _install_linux_seccomp()
        return "linux-seccomp"
    _install_nonproduction_socket_guard()
    return "nonproduction-socket-guard"


def assert_network_isolated() -> None:
    """Fail closed unless TCP, UDP, and Unix socket creation are all denied."""
    attempts = (
        (socket.AF_INET, socket.SOCK_STREAM),
        (socket.AF_INET, socket.SOCK_DGRAM),
        (socket.AF_UNIX, socket.SOCK_STREAM),
    )
    for family, kind in attempts:
        try:
            candidate = socket.socket(family, kind)
        except (PermissionError, OSError):
            continue
        candidate.close()
        raise WorkerIsolationError(
            f"worker socket creation remained available: {family}/{kind}"
        )


def _install_linux_seccomp() -> None:
    machine = platform.machine().lower()
    syscalls = _NETWORK_SYSCALLS.get(machine)
    audit_arch = _AUDIT_ARCH.get(machine)
    if syscalls is None or audit_arch is None:
        raise WorkerIsolationError(
            f"unsupported Linux worker architecture: {machine or 'unknown'}"
        )

    instructions: list[_SockFilter] = [
        _SockFilter(_BPF_LD_W_ABS, 0, 0, 4),  # seccomp_data.arch
        _SockFilter(_BPF_JMP_JEQ_K, 1, 0, audit_arch),
        _SockFilter(_BPF_RET_K, 0, 0, _SECCOMP_RET_KILL_PROCESS),
        _SockFilter(_BPF_LD_W_ABS, 0, 0, 0),  # seccomp_data.nr
    ]
    denied = _SECCOMP_RET_ERRNO | errno.EPERM
    for syscall_number in syscalls:
        instructions.append(_SockFilter(_BPF_JMP_JEQ_K, 0, 1, syscall_number))
        instructions.append(_SockFilter(_BPF_RET_K, 0, 0, denied))
        if machine == "x86_64":
            instructions.append(
                _SockFilter(
                    _BPF_JMP_JEQ_K,
                    0,
                    1,
                    syscall_number | 0x40000000,
                )
            )
            instructions.append(_SockFilter(_BPF_RET_K, 0, 0, denied))
    instructions.append(_SockFilter(_BPF_RET_K, 0, 0, _SECCOMP_RET_ALLOW))

    array_type = _SockFilter * len(instructions)
    filters = array_type(*instructions)
    program = _SockFprog(len(instructions), filters)
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        error = ctypes.get_errno()
        raise WorkerIsolationError(
            f"PR_SET_NO_NEW_PRIVS failed with errno {error}"
        )
    if libc.prctl(
        _PR_SET_SECCOMP,
        _SECCOMP_MODE_FILTER,
        ctypes.byref(program),
    ) != 0:
        error = ctypes.get_errno()
        raise WorkerIsolationError(
            f"PR_SET_SECCOMP failed with errno {error}"
        )
    assert_network_isolated()


def _install_nonproduction_socket_guard() -> None:
    class NoNetworkSocket(socket.socket):
        def __new__(cls, *args: object, **kwargs: object) -> "NoNetworkSocket":
            raise PermissionError("worker network access is disabled")

    def blocked(*args: object, **kwargs: object) -> None:
        raise PermissionError("worker network access is disabled")

    socket.socket = NoNetworkSocket
    socket.create_connection = blocked
    socket.getaddrinfo = blocked
    assert_network_isolated()
