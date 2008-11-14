# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

%define tarball_name gspcav1-20071224

Name:           gspca-kmod
Version:        1.00.20
Release:        30%{?dist}.4
Summary:        gspca Webcam Kernel Module
Group:          System Environment/Kernel
License:        GPLv2+
URL:            http://mxhaard.free.fr/download.html
Source0:        http://mxhaard.free.fr/spca50x/Download/%{tarball_name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This RPM contains the gspca binary Linux kernel module build for %{kernel}. It 
provides support for up to 260 different webcams not included in the default
kernel


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

# go
%setup -q -c -T -a 0
for kernel_version  in %{?kernel_versions}; do
    cp -a %{tarball_name} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make V=1 -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*}
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/gspca.ko $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/gspca.ko
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.00.20-30.4
- rebuild for latest Fedora kernel;

* Wed Nov 12 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.00.20-30.3
- rebuild for latest Fedora kernel;

* Thu Oct 23 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.00.20-30.2
- rebuild for latest kernel; enable ppc again

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.20-30
- build for rpmfusion
- disable ppc

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.20-4
- build for f9

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.20-3
- rebuild for new kmodtools, akmod adjustments

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.20-2
- build akmods package

* Thu Dec 27 2007 Jonathan Dieter <jdieter@gmail.com> - 1.00.20-1
- Rebase to upstream

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.18-7
- rebuilt for 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.18-6
- remove leftover from old kmodtool
- add dist

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.18-5
- rebuilt for 2.6.23.8-63.fc8 2.6.21-2952.fc8xen
- enable debuginfo packages again and build verbosely 

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.00.18-4
- rebuilt for 2.6.23.1-49.fc8

* Mon Nov  5 2007 Thorsten Leemhuis <fedora [AT] leemhuis.info> - 1.00.18-3
- Fix copy call in prep, as it breaks when building for multiple kernels 
- adjust to recent kmod model in livna devel
- disable debuginfo, as xen build will fail otherwise

* Sun Nov  4 2007 Jonathan Dieter <jdieter@gmail.com> - 1.00.18-2
- Spec file cleanup

* Sun Oct 28 2007 Jonathan Dieter <jdieter@gmail.com> - 1.00.18-1
- Initial release
