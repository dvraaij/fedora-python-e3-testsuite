# Upstream source information.
%global upstream_owner    AdaCore
%global upstream_name     e3-testsuite
%global upstream_version  24.0
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
# Upstream uses Sphinx 3.2 to format the documentation.
BuildRequires:  python3-sphinx
# Make is used to build the documentation.
BuildRequires:  make

# [Fedora-specific] PyPI package `pytest-catchlog` has been merged into the `pytest` core package.
Patch:          %{name}-pytest-catchlog-is-merged-into-core.patch


%global common_description_en \
A testsuite driver for the e3 build system.

%description %{common_description_en}


#################
## Subpackages ##
#################

%package -n python3-%{pypi_name}
Summary:    %{summary}

%description -n python3-%{pypi_name} %{common_description_en}


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
# -- cannot build the docs: missing `sphinx_rtd_theme`
# make -C docs html


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

# Show installed files (to ease debugging based on build server logs).
find %{buildroot} -exec stat --format "%A %n" {} \;


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
%{python3_sitelib}/e3_testsuite-*-py3.*-nspkg.pth


###############
## Changelog ##
###############

%changelog
* Sun Sep 04 2022 Dennis van Raaij <dvraaij@fedoraproject.org> - 24.0-1
- New package.
