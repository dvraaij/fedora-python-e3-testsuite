# OPEN-ISSUE: Documentation license is missing.

# Optionally build the docs.
%bcond_with docs

# Upstream source information.
%global upstream_owner    AdaCore
%global upstream_name     e3-testsuite
%global upstream_version  26.0
%global upstream_gittag   v%{upstream_version}

# Python Package Index name.
%global pypi_name %{upstream_name}

Name:           python-%{pypi_name}
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        Generic testsuite framework in Python

License:        GPL-3.0-only

URL:            https://github.com/%{upstream_owner}/%{upstream_name}
Source:         %{url}/archive/%{upstream_gittag}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-tox
%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-latex
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  latexmk
BuildRequires:  make
%endif

%global common_description_en \
A testsuite driver for the e3 build system.

%description %{common_description_en}


#################
## Subpackages ##
#################

%package -n python3-%{pypi_name}
Summary:    %{summary}

%description -n python3-%{pypi_name} %{common_description_en}


%if %{with docs}
%package doc
Summary:        Documentation for e3-testsuite
BuildArch:      noarch

%description doc %{common_description_en}

This package contains the documentation in HTML.
%endif


#############
## Prepare ##
#############

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -p1


############################
## Generate BuildRequires ##
############################

%generate_buildrequires
%pyproject_buildrequires -t


###########
## Build ##
###########

%build

# Build the package.
%pyproject_wheel

# Build the documentation.
%if %{with docs}
make -C doc html
%endif


#############
## Install ##
#############

%install

# Need to disable the -P flag, but not sure why. The flag is being added to the
# shebang line as of Fedora 37, but causes the testsuite fail. The -P flag
# prevents the path of the executable to be added to the path. Maybe this causes
# problems for scripts being executed using e3.os.process.Run(...)?
%undefine _py3_shebang_P

%pyproject_install
%pyproject_save_files e3

# Copy the documentation.
%if %{with docs}
mkdir --parents %{buildroot}%{_pkgdocdir}/html
cp --recursive --preserve=timestamps \
   doc/_build/html/* %{buildroot}%{_pkgdocdir}/html
%endif


###########
## Check ##
###########

%check
%tox


###########
## Files ##
###########

%files -n python3-%{pypi_name} -f %pyproject_files
%license LICENSE
%doc README* NEWS*
%{_bindir}/e3-find-skipped-tests
%{_bindir}/e3-test
%{_bindir}/e3-testsuite-report
%{_bindir}/e3-opt-parser
%{_bindir}/e3-run-test-fragment
%{_bindir}/e3-convert-xunit
%{python3_sitelib}/e3_testsuite-*-py3.*-nspkg.pth


%if %{with docs}
%files doc
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
# Remove Sphinx-generated files that aren't needed in the package.
%exclude %{_pkgdocdir}/html/objects.inv
%exclude %{_pkgdocdir}/html/objects.inv
%endif


###############
## Changelog ##
###############

%changelog
* Sun Jan 21 2024 Dennis van Raaij <dvraaij@fedoraproject.org> - 26.0-1
- Updated to v26.0.
- Documentation now optional: missing license, missing Spinx AutoAPI extension.

* Sun Oct 02 2022 Dennis van Raaij <dvraaij@fedoraproject.org> - 25.0-1
- Updated to v25.0.

* Sun Sep 04 2022 Dennis van Raaij <dvraaij@fedoraproject.org> - 24.0-1
- New package.
