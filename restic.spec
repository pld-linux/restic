Summary:	Fast, secure, efficient backup program
Name:		restic
Version:	0.9.6
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://github.com/restic/restic/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d62fb532ca7b4aaabcc9eed202a48ce4
URL:		https://restic.net/
BuildRequires:	golang >= 1.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		_libexecdir	%{_prefix}/lib

%description
restic is a backup program which allows saving multiple revisions of
files and directories in an encrypted repository stored on different
backends.

%prep
%setup -q

%build

go run -mod=vendor build.go
mv README.rst README

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install -p restic $RPM_BUILD_ROOT%{_bindir}
cp -p doc/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
rm -rf doc/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CONTRIBUTING.md CHANGELOG.md doc/*.rst
%attr(755,root,root) %{_bindir}/restic
%{_mandir}/man1/*.1*
