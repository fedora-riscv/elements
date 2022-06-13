Summary:        A C++/Python build framework
Name:           elements
Version:        6.0.1
Release:        3%{?dist}
License:        LGPLv3+
Source0:        https://github.com/astrorama/Elements/archive/%{version}/%{name}-%{version}.tar.gz
# Elements use this file to link the documentation to cppreference.com
# It is downloaded from:
# https://upload.cppreference.com/w/File:cppreference-doxygen-web.tag.xml
Source1:        cppreference-doxygen-web.tag.xml
URL:            https://github.com/degauden/Elements.git
# Remove Example programs and scripts, otherwise they will be installed
Patch0:         elements_remove_examples.patch
# Disable the compilation of PDF documentation
Patch3:         elements_disable_latex.patch
# Fix tests for Python 3.11
Patch4:         python-3.11.patch
# Fix a buggy test
Patch5:         elements_tests.patch

BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: fftw-devel
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: log4cpp-devel >= 1.1
BuildRequires: swig
BuildRequires: wcslib-devel
# Required for the generation of the documentation
BuildRequires: doxygen
BuildRequires: graphviz

BuildRequires: gcc-c++ > 4.7
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: python3-sphinx
BuildRequires: cmake >= 2.8.5

Requires: cmake-filesystem%{?_isa}

%global cmakedir %{_libdir}/cmake/ElementsProject

%global makedir %{_datadir}/Elements/make
%global confdir %{_datadir}/conf
%global auxdir %{_datadir}/auxdir
%global docdir %{_docdir}/Elements

%description
Elements is a C++/Python build framework. It helps to organize
the software into modules which are gathered into projects.

%package devel
Summary: The development part of the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The development part of the %{name} package.


%package doc
Summary: Documentation for package %{name}
License: LGPLv3+ and CC-BY-SA
BuildArch: noarch

%description doc
Documentation for package %{name}

%prep
%autosetup -n Elements-%{version} -p1

%build
export VERBOSE=1
# Build
%cmake -DELEMENTS_BUILD_TESTS=ON -DINSTALL_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF -DPYTHON_EXPLICIT_VERSION=3 --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} -DUSE_VERSIONED_LIBRARIES=ON \
    -DUSE_ENV_FLAGS=ON
# Copy cppreference-doxygen-web.tag.xml into the build directory
mkdir -p "%{_vpath_builddir}/doc/doxygen"
cp -v "%{SOURCE1}" "%{_vpath_builddir}/doc/doxygen"

%cmake_build

%install
export VERBOSE=1
%cmake_install
rm -rfv "%{buildroot}/%{confdir}/ElementsServices/testdata"
rm -fv "%{buildroot}/%{_bindir}/"*_test

%check
export ELEMENTS_CONF_PATH="%{_builddir}/ElementsKernel/auxdir/"
%ctest

%files
%{confdir}/
%dir %{cmakedir}
%{cmakedir}/ElementsEnvironment.xml

%{_libdir}/libElementsKernel.so.%{version}
%{_libdir}/libElementsServices.so.%{version}

%{_bindir}/CreateElementsProject
%{_bindir}/AddElementsModule
%{_bindir}/AddCppClass
%{_bindir}/AddCppProgram
%{_bindir}/AddPythonProgram
%{_bindir}/AddScript
%{_bindir}/AddPythonModule
%{_bindir}/RemoveCppClass
%{_bindir}/RemoveCppProgram
%{_bindir}/RemovePythonProgram
%{_bindir}/RemovePythonModule
%{_bindir}/ElementsNameCheck
%{_bindir}/GetElementsFiles

%{python3_sitearch}/ELEMENTS_VERSION.py
%{python3_sitearch}/ELEMENTS_INSTALL.py
%{python3_sitearch}/__pycache__/ELEMENTS_*.pyc

%{python3_sitearch}/ElementsKernel/
%{python3_sitearch}/ElementsServices/

%dir %{auxdir}
%{auxdir}/ElementsKernel/

%files devel
%{_libdir}/libElementsKernel.so
%{_libdir}/libElementsServices.so
%{_includedir}/ELEMENTS_VERSION.h
%{_includedir}/ELEMENTS_INSTALL.h
%{_includedir}/ElementsKernel_export.h
%{_includedir}/ElementsServices_export.h
%{_includedir}/ElementsKernel/
%{_includedir}/ElementsServices/

%{cmakedir}/ElementsBuildEnvironment.xml
%{cmakedir}/ElementsBuildFlags.cmake
%{cmakedir}/ElementsCoverage.cmake
%{cmakedir}/ElementsDefaults.cmake
%{cmakedir}/ElementsDocumentation.cmake
%{cmakedir}/ElementsLocations.cmake
%{cmakedir}/ElementsProjectConfig.cmake
%{cmakedir}/ElementsToolChain.cmake
%{cmakedir}/ElementsToolChainMacros.cmake
%{cmakedir}/ElementsUninstall.cmake
%{cmakedir}/ElementsUtils.cmake
%{cmakedir}/ElementsInfo.cmake
%{cmakedir}/ElementsExports-relwithdebinfo.cmake
%{cmakedir}/ElementsServicesExport.cmake
%{cmakedir}/SGSPlatform.cmake
%{cmakedir}/auxdir
%{cmakedir}/doc
%{cmakedir}/modules
%{cmakedir}/scripts
%{cmakedir}/tests
%{cmakedir}/ElementsExports.cmake
%{cmakedir}/ElementsPlatformConfig.cmake
%{cmakedir}/ElementsKernelExport.cmake
%{cmakedir}/ElementsConfigVersion.cmake
%{cmakedir}/ElementsConfig.cmake
%{cmakedir}/GetGitRevisionDescription.cmake

%{makedir}

%files doc
%license LICENSE.md
%{docdir}

%changelog
* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.0.1-3
- Rebuilt for Python 3.11

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 6.0.1-2
- Rebuilt for Boost 1.78

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12.0-10
- Fix tests for Python 3.11

* Thu Dec 16 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12.0-9
- Add patch number to version

* Wed Aug 11 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-8
- Rebuild after f35 branching

* Mon Aug 09 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-7
- Rebuild for gcc 11.2

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 5.12-6
- Rebuilt for Boost 1.76

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.12-4
- Rebuilt for Python 3.10

* Mon May 10 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-3
- Rebuild for gcc11.1

* Wed Apr 21 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-2
- Rebuild for Fedora 35

* Fri Feb 05 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-1
- Release 5.12

* Thu Feb 04 2021 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> - 5.10-8
- Rebuilt for cfitsio 3.490

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 5.10-6
- Rebuilt for Boost 1.75

* Mon Dec 07 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.10-5
- Rebuilt for gcc 11.0

* Thu Oct 15 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.10-4
- Rebuilt for Fedora 34

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.10-2
* Use new cmake macros

* Fri Jul 17 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.10-1
- Update for upstream release 5.10

* Fri May 29 2020 Jonathan Wakely <jwakely@redhat.com> - 5.8-10
- Rebuilt for Boost 1.73 and Python 3.9 together

* Thu May 28 2020 Jonathan Wakely <jwakely@redhat.com> - 5.8-9
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.8-8
- Rebuilt for Python 3.9

* Wed Feb 26 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.8-7
- Rebuild for Fedora 33

* Mon Feb 03 2020 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.8-6
- Remove flag max-page-size

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.8-4
- Initial RPM
