Summary: Network File System Support Library
Name: nfs-utils-lib
Version: 1.1.5
Release: 13%{?dist}
URL: http://www.citi.umich.edu/projects/nfsv4/linux/
License: BSD

%define idmapvers 0.24
%define libnfsidmap libnfsidmap
%define rpcsecgssvers 0.18
%define librpcsecgss librpcsecgss

%define _docdir				%{_defaultdocdir}/%{name}-%{version}
%define librpcsecgss_docdir %{_docdir}/%{librpcsecgss}-%{rpcsecgssvers}
%define libnfsidmap_docdir  %{_docdir}/%{libnfsidmap}-%{idmapvers}

Source0: http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{libnfsidmap}-%{idmapvers}.tar.gz
Source1: http://www.citi.umich.edu/projects/nfsv4/linux/librpcsecgss/%{librpcsecgss}-%{rpcsecgssvers}.tar.gz

Patch00: nfs-utils-lib-changelicensetoBSD.patch
Patch01: nfs-utils-lib-1.1.5-libnfsidmap-0-25-rc1.patch
Patch02: nfs-utils-lib-1.1.5-ldapsupport.patch
Patch03: nfs-utils-lib-1.1.5-local-realms-logging.patch
Patch04: nfs-utils-lib-1.1.5-zeroids.patch
Patch05: nfs-utils-lib-1.1.5-nss.patch
Patch06: nfs-utils-lib-1.1.5-nobody.patch
Patch07: nfs-utils-lib-1.1.5-caseless-domain.patch
Patch08: nfs-utils-lib-1.1.5-multidomains.patch
Patch09: nfs-utils-lib-1.1.5-nssgssprinc.patch

Patch100: nfs-utils-lib-rhel-idmapd.conf-default.patch
Patch101: nfs-utils-lib-1.1.5-warnings.patch
Patch102: nfs-utils-lib-1.1.5-compile.patch
Patch103: nfs-utils-lib-1.1.5-autogen.patch

Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig, gettext, autoconf, automake, libtool
BuildRequires: libgssglue-devel, openldap-devel
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig
Requires: libgssglue, openldap, nfs-utils >= 1.2.1-11

%description
Support libraries that are needed by the commands and 
daemons the nfs-utils rpm.

%package devel
Summary: Development files for the nfs-utils-lib library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the nfs-utils-lib library.

%prep
%setup -c -q -a1
mv %{libnfsidmap}-%{idmapvers} %{libnfsidmap}
mv %{librpcsecgss}-%{rpcsecgssvers} %{librpcsecgss}

%patch00 -p1
%patch01 -p1

#
# RHEL6.2
#
# 711210 - libnfsidmap fails to include ldap support
%patch02 -p1

#
# RHEL6.4
#
# 804812 - idmapd logging of Local-Realms only lists the last realm
%patch03 -p1

#
# RHEL6.6
#
# 1043558 - chown does not respect NFSv4 no_root_squash
%patch04 -p1
# 1066153 - RFE: Make rpcidmap and NFS accept full qualified usernames as a user
%patch05 -p1

#
# RHEL6.7
#
# 1129792 - libnfsidmap: respect Nobody-User/Nobody-Group 
%patch06 -p1
# 1223465 - nss_getpwnam: does not ignore case when comparing domain names 
#
# RHEL6.9
#
%patch07 -p1
# 1410855 - NFSv4 id mapping issues in multi-domain environments
%patch08 -p1
# 1419780 - Cannot create file in it's directory using kerberos authentication
%patch09 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

%build

pushd  %{libnfsidmap}
./autogen.sh
%configure 
make %{?_smp_mflags} all
popd

pushd  %{librpcsecgss}
CFLAGS="`echo $RPM_OPT_FLAGS $ARCH_OPT_FLAGS -fno-strict-aliasing`"
%configure CFLAGS="$CFLAGS"
make %{?_smp_mflags} all
popd

%install
rm -rf %{buildroot}

pushd  %{libnfsidmap}
make install DESTDIR=%{buildroot}
popd

pushd  %{librpcsecgss}
make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}/%{librpcsecgss_docdir}
pushd %{librpcsecgss}
for file in AUTHORS ChangeLog NEWS README ; do
	install -m 644 $file %{buildroot}/%{librpcsecgss_docdir}
done
popd

mkdir -p %{buildroot}/%{libnfsidmap_docdir}
pushd %{libnfsidmap}
for file in AUTHORS ChangeLog NEWS README ; do
	install -m 644 $file %{buildroot}/%{libnfsidmap_docdir}
done
popd

mkdir -p %{buildroot}/etc
install -m 644 %{libnfsidmap}/idmapd.conf $RPM_BUILD_ROOT/etc/idmapd.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir  %{_docdir}

%{_libdir}/librpcsecgss.so.*
%dir %{librpcsecgss_docdir}
%{librpcsecgss_docdir}/*

%config(noreplace) /etc/idmapd.conf
%{_libdir}/libnfsidmap*.so.*
%{_libdir}/libnfsidmap/*.so
%dir %{libnfsidmap_docdir}
%{libnfsidmap_docdir}/*
%{_mandir}/*/*

%files devel
%defattr(0644,root,root,755)
%{_libdir}/librpcsecgss.a
%{_libdir}/librpcsecgss.so
%dir %{_includedir}/rpcsecgss
%dir %{_includedir}/rpcsecgss/rpc
%{_libdir}/pkgconfig/librpcsecgss.pc
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_includedir}/rpcsecgss/rpc/auth.h
%{_includedir}/rpcsecgss/rpc/auth_gss.h
%{_includedir}/rpcsecgss/rpc/svc.h
%{_includedir}/rpcsecgss/rpc/svc_auth.h
%{_includedir}/rpcsecgss/rpc/rpc.h
%{_includedir}/rpcsecgss/rpc/rpcsecgss_rename.h
%{_includedir}/nfsidmap.h
%{_libdir}/libnfsidmap*.so
%{_libdir}/libnfsidmap*.a
%{_libdir}/libnfsidmap*.la
%{_libdir}/libnfsidmap/*.a
%{_libdir}/libnfsidmap/*.la
%{_libdir}/librpcsecgss.la

%changelog
* Wed Feb  8 2017 Steve Dickson <steved@redhat.com>  1.1.5-13
- Fixed stripping realm problem in nss_gss_princ routines (bz 1419780)

* Tue Jan 10 2017 Steve Dickson <steved@redhat.com>  1.1.5-12
- Add options to aid id mapping in multi domain environments (bz 1410855)

* Wed May 20 2015 Steve Dickson <steved@redhat.com>  1.1.5-11
- Make domain comparing case-less (bz 1223465)

* Thu Feb 12 2015 Steve Dickson <steved@redhat.com>  1.1.5-10
- Respect the setting of the local Nobody-User/Nobody-Group (bz 1129792)

* Thu May 22 2014 Steve Dickson <steved@redhat.com>  1.1.5-9
- Rebuild: nfs-utils-lib-1.1.5-nss.patch was corrupted (bz 1066153)

* Thu May 22 2014 Steve Dickson <steved@redhat.com>  1.1.5-8
- nss: strrchr() instead of strchr() to get the last occurrence of "@" (bz 1066153)

* Thu May  1 2014 Steve Dickson <steved@redhat.com>  1.1.5-7
- id_as_chars() fails zero value ids. (bz 1043558)

* Thu Nov  1 2012 Steve Dickson <steved@redhat.com>  1.1.5-6
- Fixed a typo in how the patches were being applied (bz 804812)

* Thu Oct 11 2012 Steve Dickson <steved@redhat.com>  1.1.5-5
- Fix the printing of local realms (bz 804812)

* Tue Aug 23 2011 Steve Dickson <steved@redhat.com>  1.1.5-4
- Added in "config.h" to enable ldap support (bz 711210)

* Wed Feb  2 2011 Steve Dickson <steved@redhat.com>  1.1.5-3
- Removed more warnings in the RPMdiff run (bz 594279)

* Fri Jan 14 2011 Steve Dickson <steved@redhat.com>  1.1.5-2
- Updated to latest upstream release: libnfsidmap-0.24-rc1 (bz 650970)
- Reset default values in /etc/idmap.conf (bz 650997)
- Remove some warnings in the RPMdiff run (bz 594279)

* Fri Feb 12 2010 Steve Dickson <steved@redhat.com>  1.1.5-1
- Updated to latest upstream release: libnfsidmap-0.23 (bz 561504)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.1.4-8.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Steve Dickson <steved@redhat.com> 1.1.4-7
- Added a debug line to log when the local realm is not found

* Tue May 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.4-6
- Replace the Sun RPC license with the BSD license, with the explicit permission of Sun Microsystems

* Mon Apr 13 2009  Steve Dickson <steved@redhat.com> 1.1.4-5
- Moved the .pc files into the -devel rpm (bz 489173)

* Wed Apr  1 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1.4-4
- Fix unowned header directories (#483464).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 24 2008 Steve Dickson <steved@redhat.com> 1.1.4-2
- Incorporated from upstream as to how  how nss deals 
  with Local Realms 

* Sat Oct 18 2008 Steve Dickson <steved@redhat.com> 1.1.4-1
- Fixed a bad assumtion in nss code.

* Wed Aug 27 2008 Steve Dickson <steved@redhat.com> 1.1.3-2
- Upgraded librpcsecgss to latest upstream version: 0.18

* Wed Aug 27 2008 Steve Dickson <steved@redhat.com> 1.1.3-1
- Upgraded libnfsidmap to latest upstream version: 0.21

* Fri Jun 27 2008 Steve Dickson <steved@redhat.com> 1.1.1-4
- In idmapd.conf, commented out 'Domain' so DNS will be
  used to define the domainname. (bz 447237)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-3
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Steve Dickson <steved@redhat.com> 1.1.1-2
- Changed the file mode on documentation files (bz 427827)
- Chagned how the doc directories are created so they
  are owned by the package. (bz 211001)

* Thu Jan 24 2008 Steve Dickson <steved@redhat.com> 1.1.1-1
- Updated librpcsecgss to the 0.17 release

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-4
 - Rebuild for openldap bump

* Tue Oct 16 2007 Steve Dickson <steved@redhat.com> 1.1.0-3
- Switch the libgssapi dependency to libgssglue
- Updated  librpcsecgss to the 0.16 release

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-2
- Rebuild for selinux ppc32 issue.

* Sat Jul 28 2007  Steve Dickson <steved@redhat.com> 1.1.0-1
- Updated libnfsidmap to the 0.20 release
- Added rules to install/remove /etc/idmap.conf

* Mon Mar 12 2007  Steve Dickson <steved@redhat.com> 1.0.8-9
- Removed the --prefix=$RPM_BUILD_ROOT from the %%configure (bz 213152)

* Tue Feb 20 2007 Steve Dickson <steved@redhat.com> 1.0.8-8
- Updated libnfsidmap to the 0.19 release

* Fri Dec  1 2006 Steve Dickson <steved@redhat.com> 1.0.8-7.3
- Fixed typo in the package description (bz 189652)

* Wed Aug 30 2006 Steve Dickson <steved@redhat.com> 1.0.8-7.2
- added automake to BuildRequires:

* Wed Aug 30 2006 Steve Dickson <steved@redhat.com> 1.0.8-7.1
- rebuild

* Wed Aug  2 2006 Steve Dickson <steved@redhat.com> 1.0.8-7
- Updated librpcsecgss to -0.14

* Wed Jul 26 2006 Steve Dickson <steved@redhat.com> 1.0.8-6
- Added GSSLIBS to the linking of librpcsecgss (bz 198238)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.8-5.1
- rebuild

* Tue Jun 20 2006 Steve Dickson <steved@redhat.com> 1.0.8-3.1
- Updated libnfsidmap and  librpcsecgss to latest upstream version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.8-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Florian La Roche <laroche@redhat.com> 1.0.8-3
- remove empty scripts

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.8-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Steve Dickson <steved@redhat.com> 1.0.8-2
- Added debugging routines to libnfsidmap

* Fri Jan  6 2006 Steve Dickson <steved@redhat.com> 1.0.8-1
- Initial commit
