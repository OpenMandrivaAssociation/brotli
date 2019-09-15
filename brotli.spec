%define major	1
%define comlib	%mklibname brotlicommon %{major}
%define enclib	%mklibname brotlienc %{major}
%define declib	%mklibname brotlidec %{major}
%define devname	%mklibname brotli -d

Name:		brotli
Summary:	Brotli compression format
Version:	1.0.7
Release:	1
License:	MIT
Group:		Archiving/Compression
Url:		https://github.com/google/brotli
Source0:	https://github.com/google/brotli/archive/v%{version}/%{name}-%{version}.tar.gz
#Patch0:		brotli-1.0.2-no-static-brotli.patch
#Patch1:		python3.8.patch
BuildRequires:	cmake
BuildRequires:	python-devel
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

%package -n python-%{name}
Summary:        Python3 module for %{name}
Group:          Development/Python
%{?python_provide:%python_provide python-%{name}}

%description -n python-%{name}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in RFC 7932.

%prep
%setup -q
%autopatch -p1

# fix permissions
find c/ \( -name "*.c" -o -name "*.h" \) -exec chmod 644 {} \;

%build
%py_build

%cmake
%make_build

%install
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
%{_mandir}/man1/%{name}.1*

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
%{_mandir}/man3/%{name}-*.h.3*

%files -n python3-%{name}
%{python3_sitearch}/Brotli-%{version}-py%{python3_version}.egg-info/
%{python3_sitearch}/__pycache__/brotli.*
%{python3_sitearch}/*.so
%{python3_sitearch}/brotli.py*
