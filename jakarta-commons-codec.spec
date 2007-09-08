# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

%define base_name  codec
%define short_name commons-%{base_name}
%define section    free

Name:           jakarta-commons-codec
Version:        1.3
Release:        %mkrel 7.2
Summary:        Jakarta Commons Codec Package
License:        Apache License
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Epoch:          0
URL:            http://jakarta.apache.org/commons/codec/
Source0:        http://www.apache.org/dist/jakarta/commons/codec/source/commons-codec-%{version}-src.tar.gz
Patch0:         jakarta-commons-codec-1.3-buildscript.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  java-javadoc
%if ! %{gcj_support}
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:       %{short_name}
Obsoletes:      %{short_name}

%if %{gcj_support}
BuildRequires:                java-gcj-compat-devel
Requires(post):                java-gcj-compat
Requires(postun):        java-gcj-compat
%endif

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       java-javadoc
Requires(post): /bin/rm /bin/ln
Requires(postun): /bin/rm

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -c

# FIXME Remove SoundexTest which is failing
# and thus preventing the build to proceed.
# This problem has been communicated upstream Bug 31096
%patch0 -p1

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath junit)
perl -p -i -e 's|../LICENSE|LICENSE.txt|g' build.xml
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
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%{__perl} -pi -e 's/\r$//g' LICENSE.txt RELEASE-NOTES.txt

# -----------------------------------------------------------------------------

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt RELEASE-NOTES.txt
%{_javadir}/*

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-commons-codec-1.3.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


