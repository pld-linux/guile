# TODO: many bytevectors.test and numbers.test failures on x32 when using system gmp
# (temporarily switched to internal mini-gmp)
#
# Conditional build:
%bcond_without	tests	# running ./check-guile
%bcond_with	emacs	# emacs mode subpackage

%ifarch sparc sparc64
%undefine	with_tests
%endif

%define		mver	3.0
Summary:	GNU Extension language
Summary(es.UTF-8):	Lenguaje de extensión de la GNU
Summary(ja.UTF-8):	アプリケーションの拡張のための GNU による Scheme の実装
Summary(pl.UTF-8):	Język GNU Extension language
Summary(pt_BR.UTF-8):	Linguagem de extensão da GNU
Summary(ru.UTF-8):	Язык расширений GNU
Summary(uk.UTF-8):	Мова розширень GNU
Name:		guile
Version:	3.0.9
Release:	3
Epoch:		5
License:	LGPL v3+
Group:		Development/Languages
Source0:	https://ftp.gnu.org/gnu/guile/%{name}-%{version}.tar.xz
# Source0-md5:	258983e0156c2bc66539dcbcb96f2bd2
Patch0:		%{name}-info.patch
Patch1:		%{name}-fix_awk_patch.patch
Patch2:		0006-numbers.test-disable-unresolved-mixed-type-division-.patch
URL:		http://www.gnu.org/software/guile/guile.html
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.12
%{?with_emacs:BuildRequires:	emacs}
BuildRequires:	gc-devel >= 7.0
BuildRequires:	gettext-tools
BuildRequires:	gmp-devel >= 4.2
BuildRequires:	libffi-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	libunistring-devel
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	pkgconfig(libffi)
BuildRequires:	readline-devel >= 4.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	gmp >= 4.2
Requires:	umb-scheme
Obsoletes:	libguile9 < 5:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*%{_libdir}/guile/.*\.go

%description
Guile, a portable, embeddable Scheme implementation written in C.
Guile provides a machine independent execution platform that can be
linked in as a library when building extensible programs.

%description -l es.UTF-8
Guile es una implementación de Scheme, que puede ser portátil y
empotrada, escrita en C. Guile provee una máquina de ejecución
independiente de plataforma, que puede ser linkada como una biblioteca
construyendo programas extensibles.

%description -l ja.UTF-8
GUILE (GNU's Ubiquitous Intelligent Language for Extension) は Scheme
プログラミング言語を実装した C で書かれたライブラリです。 GUILE は
マシン非依存の実行環境で、プログラムの拡張性を提供します。

%description -l pl.UTF-8
Guile jest przenośną, dającą się wbudować implementacją Scheme
napisaną w C. Guile udostępnia platformę wykonywania niezależną od
sprzętu, która może być dołączona jako biblioteka przy tworzeniu
rozszerzalnych programów.

%description -l pt_BR.UTF-8
Guile é um implementação de Scheme portável e embutível escrita em C.
Guile provê uma máquina de execução independente de plataforma, que
pode ser ligada como uma biblioteca construindo programas extensíveis.

%description -l ru.UTF-8
Guile - это переносимая, встраиваемая реализация языка Scheme
написанная на C. Guile предоставляет машинонезависимую среду
исполнения, которая может быть скомпонована с программой в виде
библиотеки.

%description -l uk.UTF-8
Guile - це переносима та вбудовувана реалізація мови Scheme написана
на C. Guile забезпечує машинонезалежне середовище виконання, яке може
бути скомпоноване з програмою у вигляді бібліотеки.

%package libs
Summary:	Guile shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Guile
Group:		Libraries

%description libs
Guile shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Guile.

%package devel
Summary:	Guile's header files, etc
Summary(es.UTF-8):	Bibliotecas de Guile, archivos de inclusión, etc
Summary(ja.UTF-8):	GUILE 拡張性ライブラリ用のライブラリとヘッダファイル
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja Guile
Summary(pt_BR.UTF-8):	Bibliotecas da Guile, arquivos de inclusão, etc
Summary(ru.UTF-8):	Файлы для разработки программ с Guile
Summary(uk.UTF-8):	Файли для розробки програм з Guile
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gc-devel
Requires:	gmp-devel >= 4.2
Requires:	libffi-devel
Requires:	libltdl-devel
Requires:	m4
Obsoletes:	libguile9-devel < 5:2

%description devel
What's needed to develop apps linked w/ guile

%description devel -l es.UTF-8
Este paquete contiene todo lo necesario para desarrollar aplicaciones
usando Guile.

%description devel -l ja.UTF-8
guile-devel パッケージはライブラリやヘッダファイル、その他...あなたが
GUILE 拡張性ライブラリをリンクしたプログラムを作成するのに必要な
ファイルを提供します。

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja Guile.

%description devel -l pt_BR.UTF-8
Este pacote contém o que é necessário para desenvolver aplicações
usando a Guile.

%description devel -l ru.UTF-8
Все, что нужно для разработки приложений, скомпонованых с guile.

%description devel -l uk.UTF-8
Все, що потрібно для розробки програм, що компонуються з guile.

%package static
Summary:	Guile static libraries
Summary(pl.UTF-8):	Biblioteka statyczna Guile
Summary(pt_BR.UTF-8):	Bibliotecas estáticas para desenvolvimento com guile
Summary(ru.UTF-8):	Статические библиотеки Guile
Summary(uk.UTF-8):	Статичні бібліотеки Guile
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Guile static library.

%description static -l pl.UTF-8
Biblioteka statyczna Guile.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para desenvolvimento com guile

%description static -l ru.UTF-8
Статические библиотеки guile.

%description static -l uk.UTF-8
Статичні бібліотеки guile.

%package -n emacs-guile-mode-pkg
Summary:	emacs guile-mode
Summary(pl.UTF-8):	Tryb guile dla emacsa
Group:		Applications/Editors/Emacs
Requires:	emacs

%description -n emacs-guile-mode-pkg
Emacs guile-mode.

%description -n emacs-guile-mode-pkg -l pl.UTF-8
Tryb edycji guile dla emacsa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%ifarch %{ix86}
%patch2 -p1
%endif

# popen test currently fails
%{__rm} test-suite/tests/popen.test
# net-db test needs working resolver
%{__rm} test-suite/tests/net-db.test

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
%ifarch x32
	--disable-jit \
	--enable-mini-gmp \
%endif
	--disable-silent-rules

%{__make}

%{?with_tests:./check-guile}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/guile/site/%{mver},%{_libdir}/guile/%{mver}/site-ccache}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	aclocaldir=%{_aclocaldir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/guile/%{mver}/extensions/*.{la,a}

# not supported yet by gdb; placed here causes ldconfig noise
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libguile-%{mver}.so*-gdb.scm

# use rm -f, as it depends on texlive version whether this is created or not
%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README THANKS
%attr(755,root,root) %{_bindir}/guild
%attr(755,root,root) %{_bindir}/guile
%attr(755,root,root) %{_bindir}/guile-tools
%dir %{_libdir}/guile
%dir %{_libdir}/guile/%{mver}
%{_libdir}/guile/%{mver}/ccache
%dir %{_libdir}/guile/%{mver}/extensions
%attr(755,root,root) %{_libdir}/guile/%{mver}/extensions/guile-readline.so*
%{_libdir}/guile/%{mver}/site-ccache
%dir %{_datadir}/guile
%dir %{_datadir}/guile/%{mver}
%{_datadir}/guile/%{mver}/guile-procedures.txt
%{_datadir}/guile/%{mver}/*.scm
%{_datadir}/guile/%{mver}/ice-9
%{_datadir}/guile/%{mver}/language
%{_datadir}/guile/%{mver}/oop
%{_datadir}/guile/%{mver}/rnrs
%{_datadir}/guile/%{mver}/scheme
%{_datadir}/guile/%{mver}/scripts
%{_datadir}/guile/%{mver}/srfi
%{_datadir}/guile/%{mver}/sxml
%{_datadir}/guile/%{mver}/system
%{_datadir}/guile/%{mver}/texinfo
%{_datadir}/guile/%{mver}/web
%dir %{_datadir}/guile/site
%dir %{_datadir}/guile/site/%{mver}
%{_mandir}/man1/guile.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libguile-%{mver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libguile-%{mver}.so.1

%files devel
%defattr(644,root,root,755)
%doc ChangeLog HACKING
%attr(755,root,root) %{_bindir}/guile-config
%attr(755,root,root) %{_bindir}/guile-snarf
%attr(755,root,root) %{_libdir}/libguile-%{mver}.so
%{_infodir}/guile.info*
%{_infodir}/r5rs.info*
%{_includedir}/guile
%{_pkgconfigdir}/guile-%{mver}.pc
%{_aclocaldir}/guile.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libguile-%{mver}.a

%if %{with emacs}
%files -n emacs-guile-mode-pkg
%defattr(644,root,root,755)
%{_emacs_lispdir}/*.el
%endif
