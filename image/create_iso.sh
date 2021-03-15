#!/bin/bash
set -e

iso_root=$(dirname "$0")
version=$(date +%Y%m%d)
iso_name="skydd-ics-${version}.iso"
iso_dir="${iso_root}/foss"
packages="${iso_root}"/isolinux/Packages

function download_packages {
  if [ -d "${packages}" ]; then
    rm "${packages}" -rf
  fi
  mkdir -p "${packages}"
  # Get all depend from spec files
  all_depend=()
  for i in /vagrant/specs/*.spec; do
      pre_depend=($(grep -h 'equires(pre):' "${i}" | sed -e s/Requires://g|sed -e s/,//g | tr -d '\n'))
      depend=($(grep -h 'Requires:' "${i}" | sed -e s/Requires://g|sed -e s/,//g | tr -d '\n'))
      all_depend=("${all_depend[@]}" "${depend[@]}" "${pre_depend[@]}")
  done
  all_depend=($(echo "${all_depend[@]}" | tr ' ' '\n' | sort -bu))
  # Get a list of all packages needed to build all type installations
  needed_packages=($(sort "${iso_root}"/isolinux/ks/*.packages | uniq | tr '\n' ' '))
  all_packages=( "${all_depend[@]}" "${needed_packages[@]}" )
  # Download all packages and the dependencies
  skydd_ics_packages=($(awk  '/%define name/{ print $3 }' /vagrant/specs/*))
  /usr/bin/repotrack --arch=x86_64 --download_path="${packages}" "${all_packages[@]} "${skydd_ics_packages[@]}""
  # repotrack may download both 32 and 64 bits packages, remove all 32 bits
  rm "${packages}"/*.i686.rpm || true
  # Create repo database
  createrepo -g comps.xml "${iso_root}/isolinux/"
}
function get_iso {
  if [ ! -e "${iso_root}/centos.iso" ]; then
    curl -s -o "${iso_root}/centos.iso" https://skyddics.msb.se/repos/CentOS-7-x86_64-Minimal-2003.iso
  fi
  if ! mount | grep centos.iso >/dev/null; then
    mkdir -p "${iso_root}/mnt"
    sudo mount -o loop "${iso_root}/centos.iso" "${iso_root}/mnt" || true
  fi
  cp -rp "${iso_root}/mnt/"* "${iso_dir}"
}
function sanity {
  if [ -d "${iso_dir}" ]; then
    rm -rf "${iso_dir}"
  fi
  mkdir -p "${iso_dir}"

  cnt=$(find "${iso_root}/../docs" -name "*html" | wc -l)
  if [[ "$cnt" == 0 ]] && [[ "X$1" != "X1" ]]; then
    echo "Du har inte byggt nagon dokumentation! gor cd ../docs och skriv make"
    echo "..eller kor ./create_iso.sh 1 om du vill strunta i det.."
    exit 1
  fi
  if [ ! -d "${iso_dir}/isolinux/ks" ]; then
    mkdir -p "${iso_dir}/isolinux/ks"
  fi
  if [ ! -d "${iso_root}/isolinux/Packages" ]; then
    mkdir -p "${iso_root}/isolinux/Packages"
  fi
  if [ -f "${iso_root}/${iso_name}" ];then
    rm -f "${iso_root}/${iso_name}"
  fi
  if [ ! -f /bin/createrepo ];then
    sudo yum -y install createrepo
  fi
  if [ ! -f /bin/mkisofs ];then
    sudo yum install mkisofs -y
  fi
  if [ ! -f /usr/bin/isohybrid ];then
    sudo yum install syslinux -y
  fi
  if [ ! -f /usr/lib/grub/x86_64-efi/gfxterm_background.mod ];then
    sudo yum install grub2-efi-x64-modules -y
  fi
}
function create_efi_boot {
    mkdir -p "${iso_root}/EFI/BOOT/x86_64-efi"
    cp -f /usr/lib/grub/x86_64-efi/gfxterm_background.mod "${iso_root}/EFI/BOOT/x86_64-efi"
    cp -f "${iso_root}/EFI/BOOT/grub.cfg" "${iso_dir}"
    # set up efi boot image
    dd if=/dev/zero of="${iso_root}/efiboot.img" bs=1K count=9440
    mkdosfs -F 12 "${iso_root}/efiboot.img"
    MOUNTPOINT=$(mktemp -d)
    mount -o loop "${iso_root}/efiboot.img" "$MOUNTPOINT"
    cp -rf "${iso_root}/mnt/EFI" "${MOUNTPOINT}"
    cp -rf "${iso_root}/EFI" "${MOUNTPOINT}"
    umount "${MOUNTPOINT}"
    rmdir "${MOUNTPOINT}"
    mkdir -p "${iso_dir}/images"
    mv -f "${iso_root}/efiboot.img" "${iso_dir}/images"
}

cd "${iso_root}" || exit
sanity "$@"
get_iso
download_packages

# Need to rebuild the repo db to include our RPMs
createrepo -g comps.xml "${iso_root}/isolinux"

# copy from CentOS media
for i in initrd.img isolinux.bin memtest vesamenu.c32 vmlinuz; do
    [[ -e "${iso_dir}/isolinux/${i}" ]] || cp -rf "${iso_root}/mnt/isolinux/${i}" "${iso_dir}/isolinux"
done
[[ -e "${iso_dir}/isolinux/LiveOS" ]] || cp -rf "${iso_root}/mnt/LiveOS" "${iso_dir}/isolinux/"

# EFI
create_efi_boot

# Convert isolinux.cfg.utf8 to code page 850
/usr/bin/iconv -f utf8 -t CP850 -o "${iso_root}/isolinux/isolinux.cfg" "${iso_root}/isolinux/isolinux.cfg.utf8"
cp -rp "${iso_root}/isolinux/"* "${iso_dir}"
cp -rp "${iso_root}/isolinux/isolinux.cfg" "${iso_dir}/isolinux"
cp -rp "${iso_root}/EFI/BOOT/grub.cfg" "${iso_dir}"
cp -rp "${iso_root}/EFI" "${iso_dir}"

# Create iso image
/bin/mkisofs -U -A 'Skyddspaket ICS-SCADA' -V 'FOSS' \
    -volset 'FOSS' -J -joliet-long -r -v -T \
    -x ./lost+found -o "${iso_root}/${iso_name}" \
    -b isolinux/isolinux.bin -c isolinux/boot.cat \
    -input-charset utf-8 -no-emul-boot -boot-load-size 4 \
    -boot-info-table -eltorito-alt-boot \
    -e images/efiboot.img -no-emul-boot "${iso_dir}"

# Make the iso image hybrid, allows cd and usb installtions
/usr/bin/isohybrid --uefi "${iso_root}/${iso_name}"

/bin/implantisomd5 "${iso_root}/${iso_name}"
