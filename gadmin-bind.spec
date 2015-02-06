# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	A GTK+ administation tool for ISC BIND
Name:		gadmin-bind
Version:	0.2.5
Release:	3
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:  desktop-file-utils
Requires:	bind >= 9.3.2
Requires:	usermode-consoleonly
Obsoletes:	gbindadmin
Provides:	gbindadmin
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gadmin-Bind is a fast and easy to use GTK+ administration tool for
ISC BIND.

%prep
%setup -q

%build
%configure2_5x

perl -pi -e 's|^#define CHROOT_PATH .*|#define CHROOT_PATH \"%{_localstatedir}/lib/named-chroot\"|g' config.h
perl -pi -e 's|^#define SYSLOG_PATH .*|#define SYSLOG_PATH \"/var/log/messages\"|g' config.h
perl -pi -e 's|^#define NAMED_USER .*|#define NAMED_USER \"named\"|g' config.h

%make

%install
rm -rf %{buildroot}

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# locales
%find_lang %name

# Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-BIND,Gadmin-Bind,g' desktop/%{name}.desktop
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_iconsdir}/hicolor/*/apps/%{name}.png



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.5-2mdv2011.0
+ Revision: 610785
- rebuild

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 0.2.5-1mdv2010.1
+ Revision: 525948
- update to new version 0.2.5

* Fri Feb 12 2010 Funda Wang <fwang@mandriva.org> 0.2.4-1mdv2010.1
+ Revision: 504474
- new version 0.2.4

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.2.3-4mdv2010.0
+ Revision: 437612
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.2.3-3mdv2009.1
+ Revision: 324131
- install consolehelper link to /usr/bin not /usr/sbin, so it works right
- don't use ALL CAPS in menu entry
- fd.o icons
- clean description a bit
- new license policy
- disable Werror (if I try and fix it, it crashes on startup)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.2.3-2mdv2009.0
+ Revision: 283233
- fix consolehelper

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.2.3-1mdv2009.0
+ Revision: 283212
- import gadmin-bind


