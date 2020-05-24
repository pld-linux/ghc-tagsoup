#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	tagsoup
Summary:	Parsing and extracting information from (possibly malformed) HTML/XML documents
Summary(pl.UTF-8):	Analiza i wydobywanie informacji z (niekoniecznie poprawnych) dokumentów HTML/XML
Name:		ghc-%{pkgname}
Version:	0.14.8
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/tagsoup
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	20f2c2d500086d113d19b7ca55f927a1
URL:		http://hackage.haskell.org/package/tagsoup
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-text
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-text-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-text
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
TagSoup is a library for parsing HTML/XML. It supports the HTML 5
specification, and can be used to parse either well-formed XML, or
unstructured and malformed HTML from the web. The library also
provides useful functions to extract information from an HTML
document, making it ideal for screen-scraping.

%description -l pl.UTF-8
TagSoup to biblioteka do analizy formatu HTML/XML. Obsługuje
specyfikację HTML 5 i może być używana do analizy dobrze
sformułowanego XML-a lub niestrukturalnego, źle sformułowanego HTML-a
z sieci. Biblioteka udostępnia także przydatne funkcje do wydobywania
informacji z dokumentów HTML, co czyni ją idealną do wycinków.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-text-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStagsoup-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStagsoup-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStagsoup-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/StringLike.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/StringLike.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup/*.dyn_hi


%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStagsoup-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/StringLike.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/HTML/TagSoup/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
