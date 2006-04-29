Summary:	PROfessional FTP Daemon with apache-like configuration syntax
Name:		proftpd-mod_shaper
Version:	0.5.6
Release:	0.1
License:	GPL v2+
Group:		Daemons
Source0:	http://www.castaglia.org/proftpd/modules/proftpd-mod-shaper-%{version}.tar.gz
# Source0-md5:	a81c3ed2d45f7c938416a970fd559703
URL:		http://www.castaglia.org/proftpd/modules/mod_shaper.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/ftpd
%define		_localstatedir	/var/run
%define		_libexecdir		%{_prefix}/%{_lib}/%{name}

%description
The mod_shaper module is designed to split overall rates, both
download and upload, for the proftpd daemon among all connected FTP
clients, shaping each session to use only a portion of the overall
rate. mod_shaper shapes both transmitted traffic, e.g. bits being
downloaded via the RETR command, and received traffic, e.g. bits being
uploaded via the APPE, STOR, and STOU commands.

%prep
%setup -q -n mod_shaper

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
