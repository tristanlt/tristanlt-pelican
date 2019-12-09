UEFI PXE Ubuntu Installation
############################
:date: 2015-06-26 16:35
:author: tristanlt
:tags: Ubuntu
:slug: uefi-pxe-ubuntu-installation

Recently, I tried a network installation on a brand new rack server Dell
PowerEdge R730. I used the same procedure I have always used. This
server can't make a PXE boot on legacy boot mode (BIOS), UEFI mode can.
Ok, let's used UEFI !

Unfortunately, my PXE boot failed with :

::

    Boot failed : PXE Device 1 : Integrated NIC 1 Port 1 Partition 1

After some research, I found that Syslinux, which I used for booting
Ubuntu installer, isn't compatible with UEFI !
(http://www.syslinux.org/wiki/index.php/PXELINUX#UEFI)

::

    "The "(l)pxelinux.0" bootloaders are capable of netbooting BIOS-based clients"

| In order to enable PXE boot for UEFI we must provide 64bit version of
  syslinux.efi.
| First, download latest version of syslinux package on kernel.org.
  https://www.kernel.org/pub/linux/utils/boot/syslinux/
| Untar it inside a temporary directory.
| Next, copy these files inside your tftp server directory.

::

     cp syslinux-6.03/efi64/com32/elflink/ldlinux/ldlinux.e64 /tftpboot/
     cp syslinux-6.03/efi64/efi/syslinux.efi /tftpboot 

| Note : some UEFI devices tried 32bit boot, in this case, you should
  used efi32.
| In order to don't break configuration for PXE-BIOS boot, we need to
  take care of provide the good file for bios or UEFI.  ISC-Dhcp can.

In your /etc/dhcp/dhcpd.conf :

replace:

::

    filename "pxelinux.0"

by :

::

     option architecture-type code 93 = unsigned integer 16;
     if option architecture-type = 00:09 {
      filename "syslinux.efi";
      } elsif option architecture-type = 00:07 {
      filename "syslinux.efi";
      } else {
      filename "pxelinux.0";
     }

| 
| Hope this help,
| Tristan

References :

-  http://zewaren.net/site/?q=node/136
-  https://www.kernel.org/pub/linux/utils/boot/syslinux/
-  http://www.syslinux.org/wiki/index.php/PXELINUX#UEFI
