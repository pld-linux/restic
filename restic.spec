Summary:	Fast, secure, efficient backup program
Name:		restic
Version:	0.18.1
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://github.com/restic/restic/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cf7ba497eb68cca53e75b263efea73aa
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	49df8d14de99db7a2024da47e5f15714
URL:		https://restic.net/
BuildRequires:	golang >= 1.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
restic is a backup program which allows saving multiple revisions of
files and directories in an encrypted repository stored on different
backends.

%prep
%setup -q -a1

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
