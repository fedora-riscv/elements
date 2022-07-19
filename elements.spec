Summary:        A C++/Python build framework
Name:           elements
Version:        6.0.1
Release:        1%{?dist}
License:        LGPLv3+
Source0:        https://github.com/degauden/Elements/archive/%{version}/%{name}-%{version}.tar.gz
# Elements use this file to link the documentation to cppreference.com
# It is downloaded from:
# https://upload.cppreference.com/w/File:cppreference-doxygen-web.tag.xml
Source1:        cppreference-doxygen-web.tag.xml
URL:            https://github.com/degauden/Elements.git
# Remove Example programs and scripts, otherwise they will be installed
Patch0:         elements_remove_examples.patch
# gcc 4.8 fails to cast a unique_ptr
Patch1:         elements_return_unique_ptr.patch
# sphinx not installed as part of the build
Patch2:         elements_squeezed_install_test.patch
# Disable the compilation of PDF documentation
Patch3:         elements_disable_latex.patch

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
%if 0%{?fedora} >= 30
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
%else
BuildRequires: python2
BuildRequires: python2-pytest
BuildRequires: python2-devel
BuildRequires: python-enum34
Requires:      python-enum34
%endif
BuildRequires: cmake >= 2.8.5
BuildRequires: which

%if 0%{?rhel} <= 7
Requires: cmake%{?_isa}
%else
Requires: cmake-filesystem%{?_isa}
%endif

%global cmakedir %{_libdir}/cmake/ElementsProject

%global makedir %{_datadir}/Elements/make
%global confdir %{_datadir}/conf
%global auxdir %{_datadir}/auxdir
%global docdir %{_docdir}/Elements

%if 0%{?fedora} >= 30
%global python_sitearch %{python3_sitearch}
%else
%global python_sitearch %{python2_sitearch}
%endif

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
EXTRA_CMAKE_FLAGS="-DUSE_ENV_FLAGS=ON"
%if 0%{?fedora} >= 30
EXTRA_CMAKE_FLAGS="${EXTRA_CMAKE_FLAGS} -DPYTHON_EXPLICIT_VERSION=3"
%else
EXTRA_CMAKE_FLAGS="${EXTRA_CMAKE_FLAGS} -DPYTHON_EXPLICIT_VERSION=2"
%endif
mkdir build
# Copy cppreference-doxygen-web.tag.xml into the build directory
mkdir -p build/doc/doxygen
cp "%{SOURCE1}" "build/doc/doxygen"
# Build
cd build
%cmake -DELEMENTS_BUILD_TESTS=ON -DINSTALL_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} -DUSE_VERSIONED_LIBRARIES=ON ${EXTRA_CMAKE_FLAGS}\
    ..
%make_build

%install
export VERBOSE=1
cd build
%make_install
rm -rfv "%{buildroot}/%{confdir}/ElementsServices/testdata"
rm -fv "%{buildroot}/%{_bindir}/"*_test

%check
export PYTHONPATH="%{buildroot}%{python_sitearch}"
export ELEMENTS_CONF_PATH="%{_builddir}/ElementsKernel/auxdir/"
cd build
make test

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

%{python_sitearch}/ELEMENTS_VERSION.py
%{python_sitearch}/ELEMENTS_INSTALL.py
%if 0%{?fedora} >= 30
%{python_sitearch}/__pycache__/ELEMENTS_*.pyc
%else
%{python_sitearch}/ELEMENTS_*.py?
%endif

%{python_sitearch}/ElementsKernel/
%{python_sitearch}/ElementsServices/

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
* Tue Jul 19 2022 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 6.0.1-1
- Elements 6.0.1

* Fri Feb 05 2021 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> - 5.12-1
- Release 5.12

* Mon Jul 20 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.10-1
- Update for upstream release 5.10

* Fri Mar 06 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.8-6
- Remove flag max-page-size

* Fri Jan 03 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.8-5
- Fix dependency for /usr/lib*/cmake on EPEL

* Mon Oct 28 2019 Alejandro Alvarez Ayllon <aalvarez@fedoraproject.org> 5.8-4
- Initial RPM
