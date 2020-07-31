Summary:        A C++/Python build framework
Name:           elements
Version:        5.10
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
BuildRequires: texlive-latex
%if 0%{?fedora} >= 30
BuildRequires: texlive-newunicodechar
%endif
BuildRequires: texlive-dvips

BuildRequires: gcc-c++ > 4.7
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: cmake >= 2.8.5
BuildRequires: which

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
mkdir "%{_vpath_builddir}"
pushd "%{_vpath_builddir}"
%cmake -DELEMENTS_BUILD_TESTS=ON -DINSTALL_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF -DPYTHON_EXPLICIT_VERSION=3 --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} -DUSE_VERSIONED_LIBRARIES=ON \
    -DUSE_ENV_FLAGS=ON "${OLDPWD}"
popd
# Copy cppreference-doxygen-web.tag.xml into the build directory
mkdir -p "%{_vpath_builddir}/doc/doxygen"
cp -v "%{SOURCE1}" "%{_vpath_builddir}/doc/doxygen"

%make_build -C "%{_vpath_builddir}"

%install
export VERBOSE=1
%make_install -C "%{_vpath_builddir}"
rm -rfv "%{buildroot}/%{confdir}/ElementsServices/testdata"

%check
export ELEMENTS_CONF_PATH="%{_builddir}/ElementsKernel/auxdir/"
pushd "%{_vpath_builddir}"
ctest
popd

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
* Fri Jul 31 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 5.10-1
- Initial RPM for EPEL 8

