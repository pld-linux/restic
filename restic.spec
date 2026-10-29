%define		vendor_ver	%{version}-2

Summary:	Fast, secure, efficient backup program
Name:		restic
Version:	0.19.1
Release:	2
License:	BSD
Group:		Applications/System
Source0:	https://github.com/restic/restic/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5081e2130959861a7731714c3bc41464
# cd %{name}-%{version}
# patch -p1 < %{name}-deps-security.patch
# go mod vendor
# tar cJf ../%{name}-vendor-%{vendor_ver}.tar.xz vendor
Source1:	%{name}-vendor-%{vendor_ver}.tar.xz
# Source1-md5:	d52f92d325baada76997e9f4ad84e705
# vendored modules bumped past their security fixes (x/net, x/crypto,
# x/text, klauspost/compress, grpc, otel)
Patch0:		%{name}-deps-security.patch
URL:		https://restic.net/
# go.mod go directive; with GOTOOLCHAIN=auto an older go tries to download a toolchain
BuildRequires:	golang >= 1.26.0
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	_debugsource_packages

%description
restic is a backup program which allows saving multiple revisions of
files and directories in an encrypted repository stored on different
backends.

%prep
%setup -q -a1
%patch -P0 -p1

%build
%__go run -v -mod=vendor build.go

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install -p restic $RPM_BUILD_ROOT%{_bindir}
cp -p doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md CHANGELOG.md doc/*.rst
%attr(755,root,root) %{_bindir}/restic
%{_mandir}/man1/*.1*
