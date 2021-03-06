%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-dom0-virtual-machines
Version:   %{version}
Release:   1%{?dist}
Summary:   Downloads, installs and configures template as well as creating and configuring virtual-machine AppVM's.
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-dom0

%define _builddir %(pwd)

%description
Downloads, installs and configures template as well as creating and configuring virtual-machine AppVM's.
Uses pillar data to define default VM names and configuration details.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Enable Pillar States
qubesctl top.enable qvm pillar=true -l quiet --out quiet > /dev/null || true

# Migrate enabled tops from dom0 to base environment
for top in sys-net sys-firewall sys-whonix anon-whonix personal work untrusted vault sys-usb sys-net-with-usb; do
    if [ -h /srv/salt/_tops/dom0/qvm.$top.top ]; then
        rm -f /srv/salt/_tops/dom0/qvm.$top.top
        qubesctl top.enable qvm.$top -l quiet --out quiet > /dev/null || true
    fi
done

if [ -r /srv/pillar/_tops/dom0/qvm.top ]; then
    rm -f /srv/pillar/_tops/dom0/qvm.top
fi

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/formulas/base/virtual-machines-formula
/srv/formulas/base/virtual-machines-formula/README.rst
/srv/formulas/base/virtual-machines-formula/LICENSE
/srv/formulas/base/virtual-machines-formula/qvm/anon-whonix.sls
/srv/formulas/base/virtual-machines-formula/qvm/anon-whonix.top
/srv/formulas/base/virtual-machines-formula/qvm/hide-usb-from-dom0.sls
/srv/formulas/base/virtual-machines-formula/qvm/personal.sls
/srv/formulas/base/virtual-machines-formula/qvm/personal.top
/srv/formulas/base/virtual-machines-formula/qvm/sys-firewall.sls
/srv/formulas/base/virtual-machines-formula/qvm/sys-firewall.top
/srv/formulas/base/virtual-machines-formula/qvm/sys-net.sls
/srv/formulas/base/virtual-machines-formula/qvm/sys-net.top
/srv/formulas/base/virtual-machines-formula/qvm/sys-net-with-usb.sls
/srv/formulas/base/virtual-machines-formula/qvm/sys-net-with-usb.top
/srv/formulas/base/virtual-machines-formula/qvm/sys-usb.sls
/srv/formulas/base/virtual-machines-formula/qvm/sys-usb.top
/srv/formulas/base/virtual-machines-formula/qvm/sys-whonix.sls
/srv/formulas/base/virtual-machines-formula/qvm/sys-whonix.top
/srv/formulas/base/virtual-machines-formula/qvm/template-debian-7.sls
/srv/formulas/base/virtual-machines-formula/qvm/template-debian-8.sls
/srv/formulas/base/virtual-machines-formula/qvm/template-fedora-21-minimal.sls
/srv/formulas/base/virtual-machines-formula/qvm/template-fedora-21.sls
/srv/formulas/base/virtual-machines-formula/qvm/template.jinja
/srv/formulas/base/virtual-machines-formula/qvm/template-whonix-gw.sls
/srv/formulas/base/virtual-machines-formula/qvm/template-whonix-ws.sls
/srv/formulas/base/virtual-machines-formula/qvm/untrusted.sls
/srv/formulas/base/virtual-machines-formula/qvm/untrusted.top
/srv/formulas/base/virtual-machines-formula/qvm/vault.sls
/srv/formulas/base/virtual-machines-formula/qvm/vault.top
/srv/formulas/base/virtual-machines-formula/qvm/work.sls
/srv/formulas/base/virtual-machines-formula/qvm/work.top

%attr(750, root, root) %dir /srv/pillar/base/qvm
%config(noreplace) /srv/pillar/base/qvm/init.sls
/srv/pillar/base/qvm/init.top

%config(noreplace) /etc/salt/minion.d/formula-virtual-machines.conf

%changelog
