Summary:	GNU Extension language
Summary(es):	Lenguaje de extensi�n de la GNU
Summary(ja):	���ץꥱ�������γ�ĥ�Τ���� GNU �ˤ�� Scheme �μ���
Summary(pl):	GNU Extension language
Summary(pt_BR):	Linguagem de extens�o da GNU
Summary(ru):	���� ���������� GNU
Summary(uk):	���� ��������� GNU
Name:		guile
Version:	1.4.1
Release:	5
Epoch:		5
License:	GPL
Group:		Development/Languages
Source0:	ftp://prep.ai.mit.edu/pub/gnu/guile/%{name}-%{version}.tar.gz
URL:		http://www.gnu.org/software/guile/guile.html
Patch0:		%{name}-info.patch
Patch1:		%{name}-fix_awk_patch.patch
Patch2:		%{name}-SCM_SITE_DIR_path.patch
Patch3:		%{name}-sizet.patch
Patch4:		%{name}-axp.patch
BuildRequires:	libltdl-devel
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
Requires:	umb-scheme
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libguile9

%description
Guile, a portable, embeddable Scheme implementation written in C.
Guile provides a machine independent execution platform that can be
linked in as a library when building extensible programs.

%description -l es
Guile es una implementaci�n de Scheme, que puede ser port�til y
empotrada, escrita en C. Guile provee una m�quina de ejecuci�n
independiente de plataforma, que puede ser linkada como una biblioteca
construyendo programas extensibles.

%description -l ja
GUILE (GNU's Ubiquitous Intelligent Language for Extension) �� Scheme
�ץ���ߥ󥰸����������� C �ǽ񤫤줿�饤�֥��Ǥ��� GUILE ��
�ޥ������¸�μ¹ԴĶ��ǡ��ץ����γ�ĥ�����󶡤��ޤ���

%description -l pl
Guile jest implementacj� Scheme napisan� w C.

%description -l pt_BR
Guile � um implementa��o de Scheme port�vel e embut�vel escrita em C.
Guile prov� uma m�quina de execu��o independente de plataforma, que
pode ser ligada como uma biblioteca construindo programas extens�veis.

%description -l ru
Guile - ��� �����������, ������������ ���������� ����� Scheme
���������� �� C. Guile ������������� ����������������� �����
����������, ������� ����� ���� ������������ � ���������� � ����
����������.

%description -l uk
Guile - �� ���������� �� ����������� ���̦��æ� ���� Scheme ��������
�� C. Guile ��������դ ��������������� ���������� ���������, ��� ����
���� ������������ � ��������� � �����Ħ ¦�̦�����.

%package devel
Summary:	Guile's header files, etc
Summary(es):	Bibliotecas de Guile, archivos de inclusi�n, etc
Summary(ja):	GUILE ��ĥ���饤�֥���ѤΥ饤�֥��ȥإå��ե�����
Summary(pl):	Pliki nag��wkowe i dokumentacja Guile
Summary(pt_BR):	Bibliotecas da Guile, arquivos de inclus�o, etc
Summary(ru):	����� ��� ���������� �������� � Guile
Summary(uk):	����� ��� �������� ������� � Guile
Group:		Development/Libraries
Requires:	m4
Requires:	%{name} = %{version}
Requires:	ncurses-devel >= 5.2
Requires:	readline-devel >= 4.2
Obsoletes:	libguile9-devel

%description devel
What's needed to develop apps linked w/ guile

%description devel -l es
Este paquete contiene todo lo necesario para desarrollar aplicaciones
usando Guile.

%description -l ja
guile-devel �ѥå������ϥ饤�֥���إå��ե����롢����¾...���ʤ���
GUILE ��ĥ���饤�֥����󥯤����ץ������������Τ�ɬ�פ�
�ե�������󶡤��ޤ���

%description devel -l pl
Pliki nag��wkowe i dokumentacja Guile.

%description devel -l pt_BR
Este pacote cont�m o que � necess�rio para desenvolver aplica��es
usando a Guile.

%description devel -l ru
���, ��� ����� ��� ���������� ����������, ������������� � guile.

%description devel -l uk
���, �� ���Ҧ��� ��� �������� �������, �� ������������ � guile.

%package static
Summary:	Guile static libraries
Summary(pl):	Biblioteka statyczna Guile
Summary(pt_BR):	Bibliotecas est�ticas para desenvolvimento com guile
Summary(ru):	����������� ���������� Guile
Summary(uk):	������Φ ¦�̦����� Guile
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Guile static library.

%description static -l pl
Biblioteka statyczna Guile.

%description static -l pt_BR
Bibliotecas est�ticas para desenvolvimento com guile

%description static -l ru
����������� ���������� guile.

%description static -l uk
������Φ ¦�̦����� guile.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# I wouldn't apply it, it breaks other programs, but I have fixed it, so
# if you convince me... (but remember about perl, python, tcl and ruby ) (filon)
#%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
#rm -f missing
#libtoolize --copy --force
#aclocal -I guile-config
#autoconf
#automake -a -c -f
#cd guile-readline
#libtoolize --copy --force
#aclocal
#autoconf
#automake -a -c -f
#cd -
%configure \
	--with-threads

%{__make}
#	THREAD_LIBS_LOCAL=`pwd`/qt/.libs/libqthreads.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/guile/site,%{_libdir}/guile}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	aclocaldir=%{_aclocaldir}

# this is a hack :-)
# libtool while installing links libguilereadline with installed libguile, so (in most
# cases) we get libguilereadline.so linked with (old) libguile.so.9 (!!!) and we cannot
# install it, so I had to fix it :-) (filon)
cd guile-readline
%{__cc} -shared readline.lo -Wl,--rpath -Wl,%{_libdir} ../libguile/.libs/libguile.so \
-L%{_libdir} -lreadline -lncurses -Wl,-soname -Wl,libguilereadline.so.0 \
-o $RPM_BUILD_ROOT%{_libdir}/libguilereadline.so.0.0.1
cd -

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
%attr(755,root,root) %{_libdir}/*.so.*.*
%{_libdir}/guile
%{_datadir}/guile

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog GUILE-VERSION HACKING NEWS README
%attr(755,root,root) %{_bindir}/guile-config
%attr(755,root,root) %{_bindir}/guile-snarf
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_infodir}/*info*
%{_includedir}/*
%{_aclocaldir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
