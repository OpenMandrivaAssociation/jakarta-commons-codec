

%define gcj_support 0

%define base_name  codec
%define short_name commons-%{base_name}

Name:		jakarta-commons-codec
Version:	1.4
Release:	%mkrel 3
Summary:	Implementations of common encoders and decoders
License:	Apache Software License
Group:		Development/Java
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Epoch:		0
URL:		http://jakarta.apache.org/commons/codec/
Source0:        http://archive.apache.org/dist/commons/codec/source/commons-codec-%{version}-src.tar.gz
# svn export http://svn.apache.org/repos/asf/jakarta/commons/proper/codec/tags/CODEC_1_3/
# cd CODEC_1_3
# tar czvf commons-codec-1.3-src.tar.gz .

BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant >= 0:1.6.2
BuildRequires:	ant-junit
BuildRequires:	junit
BuildRequires:	java-javadoc
BuildRequires:	jpackage-utils
%if ! %{gcj_support}
BuildArch:	noarch
%endif
Provides:	%{short_name} = %{epoch}:%{version}-%{release}
Obsoletes:	%{short_name} <= %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders. Examples include Base64, Hex,
Phonetic and URLs.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires:	java-javadoc

%description javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -qn %{short_name}-%{version}-src

#fixes eof encoding
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' RELEASE-NOTES.txt

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath junit)
#perl -p -i -e 's|../LICENSE|LICENSE.txt|g' build.xml
%{ant} -Dbuild.sysclasspath=first \
  -Dconf.home=src/conf \
  -Dbuild.home=build \
  -Dsource.home=src/java \
  -Dtest.home=src/test \
  -Ddist.home=dist \
  -Dcomponent.title=%{short_name} \
  -Dcomponent.version=%{version} \
  -Dfinal.name=%{name}-%{version} \
  -Dextension.name=%{short_name} \
  test jar javadoc

# -----------------------------------------------------------------------------

%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p dist/%{name}-%{version}.jar %{buildroot}%{_javadir}
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%{gcj_compile}

%clean
rm -rf %{buildroot}

# -----------------------------------------------------------------------------

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt RELEASE-NOTES.txt
%{_javadir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
# -----------------------------------------------------------------------------


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.4-2mdv2011.0
+ Revision: 606048
- rebuild

* Sun Feb 21 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0:1.4-1mdv2010.1
+ Revision: 508887
- update to new version 1.4
- drop both patches, not needed
- spec file clean

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.3-9.4.3mdv2010.0
+ Revision: 425396
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.3-9.4.2mdv2009.1
+ Revision: 351268
- rebuild

* Sun Aug 10 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.3-9.4.1mdv2009.0
+ Revision: 270142
- update OSGi manifest

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.3-8.2.3mdv2009.0
+ Revision: 167934
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3-8.2.3mdv2008.1
+ Revision: 120903
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3-8.2.2mdv2008.0
+ Revision: 87400
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 15 2007 David Walluck <walluck@mandriva.org> 0:1.3-8.2.1mdv2008.0
+ Revision: 85882
- sync with latest fc
- own the gcj dir

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.3-7.2mdv2008.0
+ Revision: 82897
- rebuild


* Wed Apr 04 2007 David Walluck <walluck@mandriva.org> 0:1.3-7.1mdv2007.1
+ Revision: 150660
- sync with jpackage

* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 0:1.3-4.2mdv2007.1
+ Revision: 143755
- rebuild for 2007.1
- Import jakarta-commons-codec

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.3-4.1mdv2007.0
- bump release

* Mon Jun 05 2006 David Walluck <walluck@mandriva.org> 0:1.3-2.2mdv2007.0
- rebuild for libgcj.so.7
- aot compile

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:1.3-2.1mdk
- release

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> 0:1.3-2jpp_1fc
- Build into Fedora.

* Fri May 06 2005 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp_1rh
- First Red Hat build

* Thu Sep 09 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-2jpp
- Do not stop on test failure

* Wed Sep 08 2004 Fernando Nasser <fnasser@redhat.com> 0:1.3-1jpp
- Upgrade to 1.3
- Rebuilt with Ant 1.6.2

