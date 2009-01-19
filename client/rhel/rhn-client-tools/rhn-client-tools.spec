Summary: Support programs and libraries for Red Hat Network
License: GPLv2
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
Url: http://rhn.redhat.com
Name: rhn-client-tools
Source1: version
Version: %(echo `awk '{ print $1 }' %{SOURCE1}`)
Release: %(echo `awk '{ print $2 }' %{SOURCE1}`)%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: rhnlib >= 2.1
Requires: yum-rhn-plugin >= 0.5.3-30
Requires: rhpl >= 0.81-2
Requires: rpm >= 4.2.3-24_nonptl
Requires: rpm-python 
Requires: gnupg
Requires: sh-utils
Requires: dbus-python
Requires: hal
Requires: newt

Conflicts: up2date

BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: intltool

%description
Red Hat Network Client Tools provides programs and libraries to allow your
system to receive software updates from Red Hat Network.

%package -n rhn-check
Summary: Check for RHN actions
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description -n rhn-check
rhn-check polls a Red Hat Network server to find and execute scheduled actions.

%package -n rhn-setup
Summary: Configure and register an RHN client
Group: System Environment/Base
Requires: usermode >= 1.36
Requires: %{name} = %{version}-%{release}
Requires: rhnsd

%description -n rhn-setup
rhn-setup contains programs and utilities to configure a system to use
Red Hat Network, and to register a system with a Red Hat Network server.

%package -n rhn-setup-gnome
Summary: A GUI interface for RHN Registration
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: rhn-setup = %{version}-%{release}
Requires: pam >= 0.72
Requires: pygtk2 pygtk2-libglade gnome-python2 gnome-python2-canvas 
Requires: usermode-gtk

%description -n rhn-setup-gnome
rhn-setup-gnome contains a GTK+ graphical interface for configuring and
registering a system with a Red Hat Network server.


%prep
%setup -q 

%build
make -f Makefile.rhn-client-tools

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.rhn-client-tools install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT MANPATH=%{_mandir}

mkdir -p $RPM_BUILD_ROOT/var/lib/up2date

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root)
# some info about mirrors
%doc doc/ChangeLog 
%doc doc/mirrors.txt 
%doc doc/fedora-core-1 
%doc doc/updates-released
%doc doc/AUTHORS
%{_mandir}/man8/rhn-profile-sync.8*
%{_mandir}/man5/up2date.5*

%dir /etc/sysconfig/rhn
%dir /etc/sysconfig/rhn/clientCaps.d
%config(noreplace) /etc/sysconfig/rhn/up2date
%config(noreplace) /etc/logrotate.d/up2date
%config(noreplace) /etc/rpm/macros.up2date

# dirs
%dir /usr/share/rhn
%dir /usr/share/rhn/up2date_client

#files
/usr/share/rhn/up2date_client/__init__.*
/usr/share/rhn/up2date_client/config.*
/usr/share/rhn/up2date_client/haltree.*
/usr/share/rhn/up2date_client/hardware.*
/usr/share/rhn/up2date_client/up2dateUtils.*
/usr/share/rhn/up2date_client/up2dateLog.*
/usr/share/rhn/up2date_client/up2dateErrors.*
/usr/share/rhn/up2date_client/up2dateAuth.*
/usr/share/rhn/up2date_client/rpcServer.*
/usr/share/rhn/up2date_client/rhnserver.*
/usr/share/rhn/up2date_client/rpmUtils.*
/usr/share/rhn/up2date_client/rhnPackageInfo.*
/usr/share/rhn/up2date_client/rhnChannel.*
/usr/share/rhn/up2date_client/rhnErrata.*
/usr/share/rhn/up2date_client/rhnHardware.*
/usr/share/rhn/up2date_client/transaction.*
/usr/share/rhn/up2date_client/clientCaps.*
/usr/share/rhn/up2date_client/capabilities.*
/usr/share/rhn/up2date_client/rhncli.*
/usr/share/rhn/up2date_client/rhn_fcntl.*
/usr/share/rhn/up2date_client/rhnLockfile.*
/usr/share/rhn/__init__.*

/usr/sbin/rhn-profile-sync

#public keys and certificates
/usr/share/rhn/RHNS-CA-CERT

%files -n rhn-check
%defattr(-,root,root)
%dir /usr/share/rhn/actions
%{_mandir}/man8/rhn_check.8*

/usr/sbin/rhn_check

/usr/share/rhn/up2date_client/getMethod.*

# actions for rhn_check to run
/usr/share/rhn/actions/__init__.*
/usr/share/rhn/actions/hardware.*
/usr/share/rhn/actions/errata.*
/usr/share/rhn/actions/systemid.*
/usr/share/rhn/actions/reboot.*
/usr/share/rhn/actions/rhnsd.*
/usr/share/rhn/actions/up2date_config.*

%files -n rhn-setup
%defattr(-,root,root)
%{_mandir}/man8/rhnreg_ks.8*
%{_mandir}/man8/rhn_register.8*

%config(noreplace) /etc/security/console.apps/rhn_register
%config(noreplace) /etc/pam.d/rhn_register

/usr/bin/rhn_register
/usr/sbin/rhn_register
/usr/sbin/rhnreg_ks

/usr/share/rhn/up2date_client/rhnreg.*
/usr/share/rhn/up2date_client/tui.*
/usr/share/rhn/up2date_client/rhnreg_constants.*

# firstboot is smart enough now to skip these modules
# if the modules say to
/usr/share/firstboot/modules/rhn_activate_gui.*
/usr/share/firstboot/modules/rhn_login_gui.*
/usr/share/firstboot/modules/rhn_register_firstboot_gui_window.*
/usr/share/firstboot/modules/rhn_start_gui.*
/usr/share/firstboot/modules/rhn_choose_server_gui.*
/usr/share/firstboot/modules/rhn_provide_certificate_gui.*
/usr/share/firstboot/modules/rhn_create_profile_gui.*
/usr/share/firstboot/modules/rhn_choose_org_gui.*
/usr/share/firstboot/modules/rhn_review_gui.*
/usr/share/firstboot/modules/rhn_finish_gui.*

%files -n rhn-setup-gnome
%defattr(-,root,root)
/usr/share/rhn/up2date_client/messageWindow.*
/usr/share/rhn/up2date_client/rhnregGui.*
/usr/share/rhn/up2date_client/rh_register.glade
/usr/share/rhn/up2date_client/gui.*
/usr/share/rhn/up2date_client/progress.*
/usr/share/pixmaps/*png
/usr/share/icons/hicolor/16x16/apps/up2date.png
/usr/share/icons/hicolor/24x24/apps/up2date.png
/usr/share/icons/hicolor/32x32/apps/up2date.png
/usr/share/icons/hicolor/48x48/apps/up2date.png

%changelog
* Fri Dec  5 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-17
- Resolves: #473429 #473425

* Tue Nov 18 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-15
- Resolves: #249425 #405671

* Wed Nov 12 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-10
- Resolves: #471245

* Tue Nov 11 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-9
- Resolves: #249425 #470496 #231902 #470481

* Wed Nov  5 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-8
- Resolves: #429334 #249425 #231902

* Mon Oct 27 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-6
- Resolves: #467887

* Fri Oct 24 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-5
- Resolves: #467705 #467870 #468039

* Fri Sep 26 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-4
- new build

* Thu Sep 18 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.4.19-2
- Resolves: #231902 #241209 #249127 #249425 #253596 
- Resolves: #385321 #405671 #429334 #430155 #430156 
- Resolves: #432426 #433097 #434550 #439383 #442923 
- Resolves: #442930 #450597 #451775 #452829 #457953  #460685

* Tue Apr 16 2008 Pradeep Kilambi <pkilambi@redhat.com> 
- Resolves: #442694

* Mon Mar 16 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.4.17-3
- Resolves:  #435177

* Wed Jan 16 2008 Pradeep Kilambi <pkilambi@redhat.com> - 0.4.17-1
- Resolves: #211127, #212539, #213587, #216225, #216951, #216959
- Resolves: #219814, #221912, #228240, #231041, #249426, #253031
- Resolves: #315421, #364171, #364181, #364191, #372771, #426851

* Thu Jun 07 2007 James Slagle <jslagle@redhat.com> - 0.4.16-1
- Resolves: #212300, #212407, #217857, #218860, #224633, #227399
- Resolves: #228028, #229785, #229951, #232567, #233067, #234238
- Resolves: #234880, #236925, #237300

* Thu Feb 08 2007 James Bowes <jbowes@redhat.com> - 0.4.13-1
- Add missing translations.
- Related: #211568

* Tue Feb 06 2007 James Bowes <jbowes@redhat.com> - 0.4.12-1
- Add missing translations.
- Related: #211568
- Fix 'rhn_register dies when calling activateHardwareInfo' (jesusr)
- Resolves: #227408
 
* Thu Feb 01 2007 James Bowes <jbowes@redhat.com> - 0.4.11-1
- Add missing translations.
- Related: #211568

* Thu Feb 01 2007 James Bowes <jbowes@redhat.com> - 0.4.10-1
- Updated code to use more robust UUID/virt_type discovery mechanisms, which
  allows us to workaround BZ 225203. (pvetere)
- Resolves: #225203

* Mon Jan 29 2007 James Bowes <jbowes@redhat.com> - 0.4.9-1
- Add missing code required by packages.verify
- Resolves: #224631

* Mon Jan 22 2007 James Bowes <jbowes@redhat.com> - 0.4.8-1
- Add messages for virt entitlements
- Client side support for sending uuid and virt type during registration
- Look for orgs and INs even on satellite
- Catch InvalidRegNumException for hardware numbers
- Resolves: #223322, #223860, #223295, #223307, #223359

* Wed Jan 17 2007 James Bowes <jbowes@redhat.com> - 0.4.7-1
- Update translations.
- Related: #211568

* Wed Jan 10 2007 James Bowes <jbowes@redhat.com> - 0.4.6-1
- Update translations.
- Related: #211568

* Mon Dec 18 2006 James Bowes <jbowes@redhat.com> - 0.4.5-1
- Remove the last of the references to the up2date text domain.
- Related: #211568

* Fri Dec 15 2006 James Bowes <jbowes@redhat.com> - 0.4.4-1
- Update translations.
- Make sure translations are used in all parts of the gui and tui
- Related: #211568

* Thu Dec 14 2006 John Wregglesworth <wregglej@redhat.com> - 0.4.3-1
- Update translations.
- Related: #211568, #215285

* Mon Dec 11 2006 James Bowes <jbowes@redhat.com> - 0.4.2-1
- Updated translations.
- Related: #211568

* Thu Dec 07 2006 James Slagle <jslagle@redhat.com> - 0.4.1-1
- Resolves: #218714

* Tue Dec 05 2006 James Bowes <jbowes@redhat.com> - 0.4.0-1
- Updated translations.

* Fri Dec 01 2006 James Bowes <jbowes@redhat.com> - 0.3.9-2
- Stop packaging unused png.

* Fri Dec 01 2006 James Bowes <jbowes@redhat.com> - 0.3.9-1
- Updated translations.

* Thu Nov 30 2006 James Bowes <jbowes@redhat.com> - 0.3.8-1
- Resolves: #212666, #216812, #215362, #210948, #216527, #213589

* Wed Nov 29 2006 James Slagle <jslagle@redhat.com> - 0.3.7-1
- Resolves: #212589, #212464

* Wed Nov 29 2006 James Slagle <jslagle@redhat.com> - 0.3.6-1
- Fixes for #212305, #212394

* Wed Nov 22 2006 James Slagle <jslagle@redhat.com> - 0.3.5-1
- Fixes for #213955, #212389, #212253

* Mon Nov 20 2006 James Bowes <jbowes@redhat.com> - 0.3.4-1
- Fixes for #213573, #215992, #215958, #214844, #214190

* Tue Nov 14 2006 James Bowes <jbowes@redhat.com> - 0.3.3-1
- Fixes for #213089, #213958, #214691, #215085, #414414, #213134, #214882 
- Fixes for #214844, #214523, #214609
- Include new manual pages and AUTHORS file.

* Mon Nov 06 2006 James Slagle <jslagle@redhat.com> - 0.3.2-1
- Fix for #213952

* Thu Nov 01 2006 James Bowes <jbowes@redhat.com> - 0.3.1-1
- Fixes for #212460, #211414, #213089

* Tue Oct 31 2006 Shannon Hughes <shughes@redhat.com> - 0.3.0-1
- up2date/rhn_register support for hicolor theme
- Fix for #212666
- Fixes for #213133, #213090, #212020

* Mon Oct 30 2006 James Slagle <jslagle@redhat.com> - 0.2.9-1
- Add noSidebar attribute to the firstboot modules (except the 1st one).
- Fix for #211696

* Mon Oct 30 2006 James Bowes <jbowes@redhat.com> - 0.2.8-1
- New and updated translations.
- Fixes for #211480, #211568, #212618, #212539, #211415, #210948, #211389
- Fixes for #212052, #212453, #211382, #212599

* Thu Oct 26 2006 James Bowes <jbowes@redhat.com> - 0.2.7-1
- Update to 0.2.7
- Fixes for #212212, #211132

* Wed Oct 25 2006 Peter Vetere <pvetere@redhat.com> - 0.2.6-1
- Update to 0.2.6
- Fixed rhnreg_ks call to registerSystem.  Used "token" arg instead of 
  "activationKey."

* Wed Oct 25 2006 James Bowes <jbowes@redhat.com> - 0.2.5-1
- Update to 0.2.5
- Fixes for #211407, #211291, #211888, #212088, #212027, #211456, #211855

* Tue Oct 24 2006 James Bowes <jbowes@redhat.com> - 0.2.4-1
- Update to 0.2.4
- Fixes for #212001, #211876, #211132, #211376, #211374, #211359, #211231,
  and #211186

* Fri Oct 20 2006 Daniel Benamy <dbenamy@redhat.com> - 0.2.3-1
- New version (some bugfixes and an added image file).

* Tue Oct 17 2006 James Bowes <jbowes@redhat.com> - 0.2.2-2
- Conflict up2date, since we install in the same location.

* Mon Oct 16 2006 James Bowes <jbowes@redhat.com> - 0.2.2-1
- New version.

* Mon Oct 16 2006 James Bowes <jbowes@redhat.com> - 0.2.1-1
- New version.

* Mon Oct 16 2006 James Bowes <jbowes@redhat.com> - 0.2.0-1
- New version.

* Fri Oct 13 2006 James Bowes <jbowes@redhat.com> - 0.1.9-1
- No longer provide or obsolete up2date

* Fri Oct 13 2006 James Bowes <jbowes@redhat.com> - 0.1.8-3
- reverted to desktop-file-install. It appears to be the preferred way.

* Thu Oct 12 2006 James Bowes <jbowes@redhat.com> - 0.1.8-2
- Update the summary and description of rhn-setup-gnome

* Thu Oct 12 2006 James Bowes <jbowes@redhat.com> - 0.1.8-1
- Fix for bz #210348
- use update-desktop-database rather than desktop-file-install

* Wed Oct 11 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.7-1
- Remove rhn_shared.py from firstboot stuff.

* Mon Oct 09 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.6-1
- New release for the milestone build that includes all the overhauling so far.

* Mon Oct 09 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.5-7
- Add rhn_review_gui firstboot module.

* Fri Oct 06 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.5-6
- Remove old new account and opt out firstboot modules.
- Add finish firstboot module.

* Wed Oct 04 2006 James Slagle <jslagle@redhat.com> - 0.1.5-5
- Add rhnreg_constants module.

* Wed Sep 27 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.5-4
- Add rhn_choose_org_gui firstboot module.

* Mon Sep 25 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.5-3
- Use rhn_start_gui firstboot module instead of rhn_choose_to_register_gui.

* Wed Sep 20 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.5-2
- Add file that firstboot create profile screen is moving to.

* Thu Sep 14 2006 James Bowes <jbowes@redhat.com> - 0.1.5-1
- Fix whitespace error in rhn-profile-sync.py

* Wed Sep 13 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.4-9
- Add file containing firstboot provide cert screen.

* Wed Sep 13 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.4-8
- Add file containing firstboot choose server screen.

* Tue Sep 12 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.4-7
- Add file containing firstboot screen asking if user wants to register.

* Mon Sep 11 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.4-6
- Add file containing base class for firstboot windows.

* Thu Sep 07 2006 James Bowes <jbowes@redhat.com> - 0.1.4-5
- Remove references to up2date-uuid.

* Wed Sep 06 2006 Daniel Benamy <dbenamy@redhat.com> - 0.1.4-4
- Remove configdlg and put needed functionality in rh_register.glade and 
  rhnregGui.py.

* Wed Aug 30 2006 James Bowes <jbowes@redhat.com> - 0.1.4-3
- Move messageWindow and tui from client-tools to setup-gnome
  and setup.
- Add haltree

* Mon Aug 28 2006 James Bowes <jbowes@redhat.com> - 0.1.4-2
- Remove python-optik requires.

* Fri Jul 28 2006 James Bowes <jbowes@redhat.com> - 0.1.4-1
- New release.

* Thu Jul 27 2006 James Bowes <jbowes@redhat.com> - 0.1.3-1
- New release.
- Remove sourcesConfig from the spec file.

* Fri Jul 21 2006 James Bowes <jbowes@redhat.com> - 0.1.2-1
- New release.
- Remove rhnDefines from package.

* Fri Jul 21 2006 James Bowes <jbowes@redhat.com> - 0.1.1-1
- New release.
- Remove mkdir /etc/sysconfig/rhn from install; this is done
  in the Makefile.

* Thu Jul 20 2006 James Bowes <jbowes@redhat.com> - 0.1.0-2
- Remove rhn_register obsoletes.

* Thu Jul 20 2006 James Bowes <jbowes@redhat.com> - 0.1.0-1
- New release.

* Thu Jul 20 2006 James Bowes <jbowes@redhat.com> - 0.0.9-1
- New release.

* Tue Jul 19 2006 James Bowes <jbowes@redhat.com> - 0.0.8-3
- Make sub-packages depend on the exact version and release of
  the master package.

* Tue Jul 18 2006 James Bowes <jbowes@redhat.com> - 0.0.8-2
- Point to the new docs location in the source tree.

* Fri Jul 14 2006 James Bowes <jbowes@redhat.com> - 0.0.8-1
- Generate a uuid file from scratch during post.

* Wed Jun 21 2006 James Bowes <jbowes@redhat.com> - 0.0.7-1
- Removed the packages action.

* Fri Jun 02 2006 James Bowes <jbowes@redhat.com> - 0.0.6-2
- Remove reference to cliUtils

* Fri Jun 02 2006 James Bowes <jbowes@redhat.com> - 0.0.6-1
- new rhn-profile-sync command for syncing package, hardware,
  and virtualization profiles with rhn.

* Tue May 30 2006 James Bowes <jbowes@redhat.com> - 0.0.5-1
- Remove unneeded imports and circular imports.

 Tue May 23 2006 Pete Vetere <pvetere@redhat.com> - 0.0.4-1
- Add support for sending virtualization info to RHN

* Mon May 22 2006 James Bowes <jbowes@redhat.com> - 0.0.3-2
- Properly link rhn_register and up2date-config

* Thu May 18 2006 James Bowes <jbowes@redhat.com> - 0.0.3-1
- Remove more unused code and data files.

* Tue May 09 2006 James Bowes <jbowes@redhat.com> - 0.0.2-1
- Remove non-up2date repo backends.

* Mon May 08 2006 James Bowes <jbowes@redhat.com> - 4.4.69-6
- bump required version of rhnlib for pkg/iso redirect.

* Tue May 02 2006 James Bowes <jbowes@redhat.com> - 4.4.69-3
- fix for #87837, inaccurate error message when missing '-f' for kernel updates
- fix for #125049, misleading usage message: "Please specify either -l, -u, ...
- fix for #126528, up2date +get source fails if no source available
- fix for #168312, up2date config file is not ignored in rpm -V
- fix for #171057, CRM# 696030 repomd error after up2date
- fix for #171643, repomd error after up2date
- fix for #s 179896, 179898  rpm verify fails due to config files in .spec not marked ...

* Mon Apr 24 2006 Bret McMillan <bretm@redhat.com> 4.4.69-1
- fix for #178498, #176123 -- make --channel limit the channel universes for various operations
- fix for #162106, RHN 'sync packages to system' installing i386 glibc on i686
- fix for #175593, up2date --whatprovides doesn't handle compat arch provides

* Tue Apr 11 2006 James Bowes <jbowes@redhat.com> 0.0.1-1
- Pull out rhnsd stuff so we can build as noarch.
- Make seperate rpms for rhn_check, and register.

* Wed Feb 01 2006 Adrian Likins <alikins@redhat.com> 4.4.6800000000000eleventybillion
- gratuitous version rev to test up2date of up2date

* Tue Jan 31 2006 Bret McMillan <bretm@redhat.com> 4.4.67-4
- fix release tag

* Fri Jan 27 2006 Adrian Likins <alikins@redhat.com> 4.4.67-3
- fix for #179110 - up2date fails to update xerces-j
- more fixed for #176195 "up2date-nox --configure changes current value of numeric attribute to Yes/No if 1/0 is selected"

* Fri Jan 27 2006 Bret McMillan <bretm@redhat.com> 4.4.65-3
- fix for #176195 "up2date-nox --configure changes current value of numeric attribute to Yes/No if 1/0 is selected"

* Thu Jan 19 2006 Adrian Likins <alikins@redhat.com> 4.4.63-4
- rest of fix for #169880 up2date --arch updates primary arch if package is out of date instead of arch specified.
- even better fix for #178261 "Invalid function call attempted" when installing a RHN proxy

* Thu Jan 19 2006 Bret McMillan <bretm@redhat.com> 4.4.60-4
- rebuild with fixes for:
- fix #169293 -- up2date unable to download very large rpms
- fix #177784 -- up2date gives error if select-all is checked
- fix #177786 -- up2date unselects all pakcages if select-all is checked and user selects 'back'

* Thu Jan 12 2006 Adrian Likins <alikins@redhat.com> 4.4.58
- fix for #165157 - firstboot 'Read our Privacy Statement' shows a blank text box

* Fri Jan 6 2006 Adrian Likins <alikins@redhat.com> 4.4.56-4.1
- rebuild for #176182 (new gcc)

* Thu Dec 8 2005 Adrian Likins <alikins@redhat.com> 4.4.55
- add bug fix for  #175321  rhnreg_ks cannot import name capabilities -- circular import

* Wed Nov 15 2005 Adrian Likins <alikins@redhat.com> 4.4.54
- revert orig fix for #165024 - "invalid function call" error on proxy installs
- add new bug fix for #165204
- revert "fix" for #169882, #159955 - up2date man page does not describe --undo option.
- add --unfo to man page fixing #169882, #159955


* Wed Nov 09 2005 Adrian Likins <alikins@redhat.com> 4.4.52
- fix #165024 - "invalid function call" error on proxy installs
- fix #169881, #167732 -  'up2date --configure' always saves changes if useNetwork is false on startup
 

* Mon Oct 10 2005 Adrian Likins <alikins@redhat.com> 4.4.51
- fix #169882, #159955 - up2date man page does not describe --undo option.
  (remove deprecated undo option)
- fix #170065, #166034 - up2date "forward" button disabled if packages selected via spacebar.
- fix #157087, #170055 - up2date --configure fails when failover serverURL is configured.

* Thu Sep 15 2005 Adrian Likins <alikins@redhat.com> 4.4.50-4
- new up2date.pot, synced up
- fix uncommitted changes that were causing string 
  translations not to show up
- more translations updates for #160608

* Mon Sep 12 2005 Adrian Likins <alikins@redhat.com> 4.4.45
- fix for #160602 (updated russian translations)


* Fri Aug 26 2005 Adrian Likins <alikins@redhat.com> 4.4.44
- fix for #166868 - fatal python error when  installing package

* Tue Aug 23 2005 Adrian Likins <alikins@redhat.com> 4.4.43
- more fixes for #144800

* Tue Aug 23 2005 Adrian Likins <alikins@redhat.com> 4.4.42
- more fixes for #159858/#157070

* Mon Aug 15 2005 Adrian Likins <alikins@redhat.com> 4.4.41
- fix #164660

* Thu Aug 11 2005 Adrian Likins <alikins@redhat.com> 4.4.40
- attempt "fix" for #165636 (require new rpm versions)

* Wed Aug 10 2005 Adrian Likins <alikins@redhat.com> 4.4.39
- more fix for #157070
- require newer rhnlib for #165360

* Thu Aug 4 2005 Adrian Likins <alikins@redhat.com> 4.4.38
- fix desktop files rpmdiff complained about

* Thu Aug 4 2005 Adrian Likins <alikins@redhat.com> 4.4.37
- fix specfile to work on ppc

* Wed Aug 3 2005 Adrian Likins <alikins@redhat.com> 4.4.36
- fix for #162701

* Wed Aug 3 2005 Adrian Likins <alikins@redhat.com> 4.4.35
- fix for #160602 (updated ru.po)

* Tue Aug 2 2005 Adrian Likins <alikins@redhat.com> 4.4.34
- fix for #144800

* Thu Jul 28 2005 Adrian Likins <alikins@redhat.com> 4.4.33
- fix for #149472

* Wed Jul 27 2005 Adrian Likins <alikins@redhat.com> 4.4.32
- fix for #144800
- fix for #137942

* Tue Jul 26 2005 Adrian Likins <alikins@redhat.com> 4.4.31
- fix for #155583

* Tue Jul 12 2005 Adrian Likins <alikins@redhat.com> 4.4.30
- more fixes for sources on RHEL-3
- have to include "3" as a release as well

* Mon Jul 11 2005 Adrian Likins <alikins@redhat.com> 4.4.28
- fix for issues with updating the package list after
  actions correctly #125790

* Thu Jul 7 2005 Jason Connor <jconnor@redhat.com> 4.4.27.2
- hotfix for bug 148952

* Tue Jun 7 2005 Adrian Likins <alikins@redhat.com> 4.4.25
- delay/avoid doing repomd if it's not in use

* Mon Jun 6 2005 Adrian Likins <alikins@redhat.com> 4.4.24
- dont require the old extended_packages cap

* Thu May 19 2005 Adrian Likins <alikins@redhat.com> 4.4.23
- change the way the version substitution works to pass pkg checker

* Thu May 19 2005 Adrian Likins <alikins@redhat.com> 4.4.22
- fix #158256 - up2date errors if yum isnt installed, but doesn't need to

* Thu May 19 2005 Adrian Likins <alikins@redhat.com> 4.4.20
- fix #154814 -  Selecting all packages in the GUI only selects first package

* Tue May 17 2005 Adrian Likins <alikins@redhat.com> 4.4.19
- fix #155583 - don't allow kernel-smp.x86_64 to be installed on ia32e
- fix #157070 - make yum/apt repos support proxies
- fix #148952 - patch from Jack Neely <jjneely@pams.ncsu.edu)

* Mon May 16 2005 Adrian Likins <alikins@redhat.com> 4.4.19
- fix #150418 – rhel-4 client machine capabilities not recognized sometimes
- fix #145554 – rhn_register fails if proxy username begins at '0'
- fix #154137 up2date does not always send the arch

* Mon May 9 2005 Adrian Likins <alikins@redhat.com> 4.4.18
- fix problem with missing import

* Wed Apr 27 2005 Adrian Likins <alikins@redhat.com> 4.4.17
- fix some bugs in the way repomdRepo creates the package lists

* Tue Apr 26 2005 Adrian Likins <alikins@redhat.com> 4.4.16
- support repomd repos (and use the yum config if it exists)
  bugzilla #135121

* Tue Apr 19 2005 Adrian Likins <alikins@redhat.com> 4.4.15
- fix #149444 up2date --dry-run --upgrade-to-release changes registered base channel
- fix #151328 (tracback when registering with *'s in password)
- added some general uncaught exception catching
- truncate rpm changelog (see up2date.spec.changelog)
- update translations

* Thu Apr 14 2005 Jason Connor <jconnor@redhat.com> 4.4.14
- fix #135121 - uncommented rpmmd registration, fixed api
- fix #149281 - added check for failed read

* Fri Apr 8 2005 Adrian Likins <alikins@redhat.com> 4.4.13
- update translations

* Thu Apr 7 2005 Adrian Likins <alikins@redhat.com> 4.4.12
- update translations

* Thu Mar 3 2005 Adrian Likins <alikins@redhat.com> 4.4.10
- fix #150210
- revert change for package list refresh for this
  release

* Tue Mar 1 2005 Adrian Likins <alikins@redhat.com> 4.4.9
- fix #149947

* Tue Feb 15 2005 Adrian Likins <alikins@redhat.com> 4.4.8
- fix #139537

* Fri Jan 14 2005 Adrian Likins <alikins@redhat.com> 4.4.7
- fix #136497
- fix #142750, #142589 (less deprecation warnings) 

* Mon Jan 10 2005 Adrian Likins <alikins@redhat.com> 4.4.6
- fix #144704

* Wed Dec 15 2004 Adrian Likins <alikins@redhat.com> 4.4.5
- fix #142406 (again)

* Wed Dec 15 2004 Adrian Likins <alikins@redhat.com> 4.4.4
- fix #142332
- fix #129909

* Tue Dec 14 2004 Adrian Likins <alikins@redhat.com> 4.4.3
- fix #142406

* Mon Dec 6 2004 Adrian Likins <alikins@redhat.com> 4.4.2
- fix #139495 (updated translations)

* Fri Dec 3 2004 Adrian Likins <alikins@redhat.com> 4.4.1
- fix #141820 (add kernel-devel to list of packages to
  intall not update)

* Fri Dec 3 2004 Adrian Likins <alikins@redhat.com> 4.4.0
- rev to 4.4.0
