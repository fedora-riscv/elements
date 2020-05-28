Summary:        A C++/Python build framework
Name:           elements
Version:        5.8
Release:        9%{?dist}
License:        LGPLv3+
Source0:        https://github.com/degauden/Elements/archive/%{version}/%{name}-%{version}.tar.gz
# Elements use this file to link the documentation to cppreference.com
# It is downloaded from:
# https://upload.cppreference.com/w/File:cppreference-doxygen-web.tag.xml
Source1:        cppreference-doxygen-web.tag.xml
URL:            https://github.com/degauden/Elements.git
# Remove Example programs and scripts, otherwise they will be installed
Patch0:         elements_remove_examples.patch
# Elements try to guess itself the lib directory, but it does not consider
# 64 bits architectures supported by Fedora. It will override CMAKE_LIB_INSTALL_SUFFIX,
# and stick to its mistaken guess (i.e. /usr/lib for anything that is not x86_64),
# unless this patch is applied
# https://github.com/degauden/Elements/pull/5
Patch1:         elements_do_not_force_install_suffix.patch
# Create libraries with sonames, and versioned name
# https://github.com/degauden/Elements/pull/6
Patch2:         elements_soversion.patch
# Disable the compilation of PDF documentation
Patch3:         elements_disable_latex.patch
# Make sure this script runs both with Python 2 and 3
# Backport from upstream develop branch
Patch4:         elements_CTestXML2HTML_py23.patch
# Should not set max-page-size. Reported to upstream, they will fix this.
Patch5:         elements_flags_remove_page_size.patch

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
BuildRequires: texlive-latex 
BuildRequires: texlive-newunicodechar
BuildRequires: texlive-dvips

BuildRequires: gcc-c++ > 4.7
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: cmake >= 2.8.5

Requires: cmake-filesystem%{?_isa}

%global cmakedir %{_libdir}/cmake/ElementsProject

%global makedir %{_datadir}/Elements/make
%global confdir %{_datadir}/Elements
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
EXTRA_CMAKE_FLAGS="-DPYTHON_EXPLICIT_VERSION=3 -DUSE_ENV_FLAGS=ON"
mkdir build
# Copy cppreference-doxygen-web.tag.xml into the build directory
mkdir -p build/doc/doxygen
cp "%{SOURCE1}" "build/doc/doxygen"
# Make sure auxiliary files used only for testing are not installed
rm -r "ElementsKernel/auxdir/ElementsKernel/tests"
# Build
cd build
%cmake -DELEMENTS_BUILD_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF -DPYTHON_EXPLICIT_VERSION=3 --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} -DUSE_VERSIONED_LIBRARIES=ON \
    ..
%make_build

%install
export VERBOSE=1
cd build
%make_install

%check
export PYTHONPATH="%{buildroot}%{python3_sitearch}"
%{buildroot}/%{_bindir}/CreateElementsProject --help


%files
%dir %{confdir}
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
%{_includedir}/ElementsKernel/
%{_includedir}/ElementsServices/

%{cmakedir}/ElementsBuildEnvironment.xml
%{cmakedir}/ElementsBuildFlags.cmake
%{cmakedir}/ElementsCoverage.cmake
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

%{makedir}

%files doc
%license LICENSE.md
%{docdir}

%changelog
* Thu May 28 2020 Jonathan Wakely <jwakely@redhat.com> - 5.8-9
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.8-8
- Rebuilt for Python 3.9

* Wed Feb 26 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.8-7
- Rebuild for Fedora 33

* Mon Feb 03 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.8-6
- Remove flag max-page-size

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.8-4
- Initial RPM
