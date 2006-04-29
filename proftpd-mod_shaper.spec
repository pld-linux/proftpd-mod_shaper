%define		mod_name	mod_shaper
Summary:	PROfessional FTP Daemon with apache-like configuration syntax
Name:		proftpd-%{mod_name}
Version:	0.5.6
Release:	0.1
License:	GPL v2+
Group:		Daemons
Source0:	http://www.castaglia.org/proftpd/modules/proftpd-mod-shaper-%{version}.tar.gz
# Source0-md5:	a81c3ed2d45f7c938416a970fd559703
URL:		http://www.castaglia.org/proftpd/modules/mod_shaper.html
BuildRequires:	proftpd-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	proftpd >= 1:1.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/ftpd
%define		_libexecdir		%{_prefix}/%{_lib}/proftpd

%description
The mod_shaper module is designed to split overall rates, both
download and upload, for the proftpd daemon among all connected FTP
clients, shaping each session to use only a portion of the overall
rate. mod_shaper shapes both transmitted traffic, e.g. bits being
downloaded via the RETR command, and received traffic, e.g. bits being
uploaded via the APPE, STOR, and STOU commands.

%prep
%setup -q -n %{mod_name}

%build
%{__cc} %{rpmcflags} -I/usr/include/proftpd %{mod_name}.c -shared -o %{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_sysconfdir}/conf.d}
install %{mod_name}.so $RPM_BUILD_ROOT%{_libexecdir}
echo 'LoadModule        %{mod_name}.c' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	if grep -iEqs "^ServerType[[:space:]]+inetd" %{_sysconfdir}/proftpd.conf; then
		%service -q rc-inetd reload
	elif grep -iEqs "^ServerType[[:space:]]+standalone" %{_sysconfdir}/proftpd.conf; then
		%service -q proftpd restart
	fi
fi

%postun
if [ "$1" = "0" ]; then
	if grep -iEqs "^ServerType[[:space:]]+inetd" %{_sysconfdir}/proftpd.conf; then
		%service -q rc-inetd reload
	elif grep -iEqs "^ServerType[[:space:]]+standalone" %{_sysconfdir}/proftpd.conf; then
		%service -q proftpd restart
	fi
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{mod_name}.conf
%attr(755,root,root) %{_libexecdir}/%{mod_name}.so
