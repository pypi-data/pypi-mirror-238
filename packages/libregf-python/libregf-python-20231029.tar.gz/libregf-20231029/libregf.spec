Name: libregf
Version: 20231029
Release: 1
Summary: Library to access the Windows NT Registry File (REGF) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libregf
              
BuildRequires: gcc              

%description -n libregf
Library to access the Windows NT Registry File (REGF) format

%package -n libregf-static
Summary: Library to access the Windows NT Registry File (REGF) format
Group: Development/Libraries
Requires: libregf = %{version}-%{release}

%description -n libregf-static
Static library version of libregf.

%package -n libregf-devel
Summary: Header files and libraries for developing applications for libregf
Group: Development/Libraries
Requires: libregf = %{version}-%{release}

%description -n libregf-devel
Header files and libraries for developing applications for libregf.

%package -n libregf-python3
Summary: Python 3 bindings for libregf
Group: System Environment/Libraries
Requires: libregf = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libregf-python3
Python 3 bindings for libregf

%package -n libregf-tools
Summary: Several tools for reading Windows NT Registry Files (REGF)
Group: Applications/System
Requires: libregf = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libregf-tools
Several tools for reading Windows NT Registry Files (REGF)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libregf
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libregf-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libregf-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libregf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libregf-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libregf-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Oct 29 2023 Joachim Metz <joachim.metz@gmail.com> 20231029-1
- Auto-generated

