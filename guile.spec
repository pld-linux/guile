Summary:	GNU Extension language
Summary(pl.UTF-8):   GNU Extension language
Name:		guile
Version:	1.5.6
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://alpha.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz
BuildRequires:	libltdl-devel
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
Requires:	umb-scheme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libguile9

%description
Guile, a portable, embeddable Scheme implementation written in C.
Guile provides a machine independent execution platform that can be
linked in as a library when building extensible programs.

%description -l pl.UTF-8
Guile jest implementacją Scheme napisaną w C.

%package devel
Summary:	Guile's header files, etc
Summary(pl.UTF-8):   Pliki nagłówkowe i dokumentacja Guile
Group:		Development/Libraries
Requires:	m4
Requires:	%{name} = %{version}
Requires:	ncurses-devel >= 5.2
Requires:	readline-devel >= 4.2
Obsoletes:	libguile9-devel

%description devel
What's needed to develop apps linked w/ guile

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja Guile.

%package static
Summary:	Guile static libraries
Summary(pl.UTF-8):   Biblioteka statyczna Guile
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Guile static library.

%description static -l pl.UTF-8
Biblioteka statyczna Guile.

%prep
%setup -q

%build
%configure \
	--with-threads
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	aclocaldir=%{_aclocaldir}

gzip -9nf AUTHORS ChangeLog GUILE-VERSION HACKING NEWS README

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/guile
%attr(755,root,root) %{_bindir}/guile-tools
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_datadir}/guile

%files devel
%defattr(644,root,root,755)
%doc {AUTHORS,ChangeLog,GUILE-VERSION,HACKING,NEWS,README}.gz
%attr(755,root,root) %{_bindir}/guile-config
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la
%{_infodir}/*info*
%{_includedir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
