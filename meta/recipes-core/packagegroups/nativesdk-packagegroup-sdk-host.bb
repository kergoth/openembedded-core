#
# Copyright (C) 2007 OpenedHand Ltd
#

SUMMARY = "Host packages for the standalone SDK or external toolchain"
PR = "r12"

inherit packagegroup nativesdk

PACKAGEGROUP_DISABLE_COMPLEMENTARY = "1"

RDEPENDS_${PN} = "\
    nativesdk-pkgconfig \
    nativesdk-unfs3 \
    nativesdk-opkg \
    nativesdk-libtool \
    nativesdk-autoconf \
    nativesdk-automake \
    nativesdk-shadow \
    nativesdk-makedevs \
    nativesdk-cmake \
    nativesdk-meson \
    ${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'nativesdk-wayland', '', d)} \
    nativesdk-sdk-provides-dummy \
    nativesdk-bison \
    nativesdk-flex \
    "
LIBC_RDEPENDS = "nativesdk-pseudo nativesdk-qemu nativesdk-qemu-helper"
LIBC_RDEPENDS_libc-musl = ""
RDEPENDS_${PN} += "${LIBC_RDEPENDS}"

RDEPENDS_${PN}_darwin = "\
    nativesdk-pkgconfig \
    nativesdk-opkg \
    nativesdk-libtool \
    "
