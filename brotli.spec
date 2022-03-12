%global optflags %{optflags} -O3

# brotli is used by curl, curl is used by systemd,
# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 1
%define comlib %mklibname brotlicommon %{major}
%define enclib %mklibname brotlienc %{major}
%define declib %mklibname brotlidec %{major}
%define devname %mklibname brotli -d
%define comlib32 libbrotlicommon%{major}
%define enclib32 libbrotlienc%{major}
%define declib32 libbrotlidec%{major}
%define devname32 libbrotli-devel

Name:		brotli
Summary:	Brotli compression format
Version:	1.0.9
Release:	3
License:	MIT
Group:		Archiving/Compression
Url:		https://github.com/google/brotli
Source0:	https://github.com/google/brotli/archive/v%{version}/%{name}-%{version}.tar.gz
#Patch0:		brotli-1.0.2-no-static-brotli.patch
#Patch1:		python3.8.patch
Patch10:	https://src.fedoraproject.org/rpms/brotli/raw/rawhide/f/09b0992b6acb7faa6fd3b23f9bc036ea117230fc.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%package -n %{comlib}
Summary:	Shared data used by libbrotlienc and libbrotlidec libraries
Group:		System/Libraries

%description -n %{comlib}
Shared data used by libbrotlienc and libbrotlidec libraries.

%package -n %{enclib}
Summary:	Brotli encoder library
Group:		System/Libraries

%description -n %{enclib}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%package -n %{declib}
Summary:	Brotli decoder library
Group:		System/Libraries

%description -n %{declib}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%package -n %{devname}
Summary:	Development files and headers for %{name}
Group:		Development/Other
Requires:	%{comlib} = %{version}-%{release}
Requires:	%{enclib} = %{version}-%{release}
Requires:	%{declib} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files and headers for %{name}.

%if %{with compat32}
%package -n %{comlib32}
Summary:	Shared data used by libbrotlienc and libbrotlidec libraries (32-bit)
Group:		System/Libraries

%description -n %{comlib32}
Shared data used by libbrotlienc and libbrotlidec libraries.

%package -n %{enclib32}
Summary:	Brotli encoder library (32-bit)
Group:		System/Libraries

%description -n %{enclib32}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%package -n %{declib32}
Summary:	Brotli decoder library (32-bit)
Group:		System/Libraries

%description -n %{declib32}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%package -n %{devname32}
Summary:	Development files and headers for %{name} (32-bit)
Group:		Development/Other
Requires:	%{devname} = %{EVRD}
Requires:	%{comlib32} = %{version}-%{release}
Requires:	%{enclib32} = %{version}-%{release}
Requires:	%{declib32} = %{version}-%{release}

%description -n %{devname32}
Development files and headers for %{name}.
%endif

%package -n python-%{name}
Summary:	Python3 module for %{name}
Group:		Development/Python
%{?python_provide:%python_provide python-%{name}}

%description -n python-%{name}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%prep
%autosetup -p1

# fix permissions
find c/ \( -name "*.c" -o -name "*.h" \) -exec chmod 644 {} \;

%build
%py_build

%global build_ldflags %(echo %{build_ldflags} |sed -e 's,-m64,,g')
%if %{with compat32}
%cmake32
%make_build
cd ..
%endif

%cmake
%make_build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%py_install

# man page
install -Dpm644 docs/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -Dpm644 docs/decode.h.3 %{buildroot}%{_mandir}/man3/%{name}-decode.h.3
install -Dpm644 docs/encode.h.3 %{buildroot}%{_mandir}/man3/%{name}-encode.h.3
install -Dpm644 docs/types.h.3 %{buildroot}%{_mandir}/man3/%{name}-types.h.3

# we don't want these
find %{buildroot} -name "*.a" -delete

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1*

%files -n %{comlib}
%license LICENSE
%{_libdir}/libbrotlicommon.so.%{major}{,.*}

%files -n %{enclib}
%license LICENSE
%{_libdir}/libbrotlienc.so.%{major}{,.*}

%files -n %{declib}
%license LICENSE
%{_libdir}/libbrotlidec.so.%{major}{,.*}

%files -n %{devname}
%doc README.md CONTRIBUTING.md
%{_includedir}/%{name}/
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlienc.so
%{_libdir}/libbrotlidec.so
%{_libdir}/pkgconfig/libbrotli*.pc
%doc %{_mandir}/man3/%{name}-*.h.3*

%files -n python-%{name}
%{python_sitearch}/Brotli-%{version}-py%{python_version}.egg-info
%{python_sitearch}/*.so
%{python_sitearch}/brotli.py*

%if %{with compat32}
%files -n %{comlib32}
%{_prefix}/lib/libbrotlicommon.so.%{major}{,.*}

%files -n %{enclib32}
%{_prefix}/lib/libbrotlienc.so.%{major}{,.*}

%files -n %{declib32}
%{_prefix}/lib/libbrotlidec.so.%{major}{,.*}

%files -n %{devname32}
%{_prefix}/lib/libbrotlicommon.so
%{_prefix}/lib/libbrotlienc.so
%{_prefix}/lib/libbrotlidec.so
%{_prefix}/lib/pkgconfig/libbrotli*.pc
%endif
