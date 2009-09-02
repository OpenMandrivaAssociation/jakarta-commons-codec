# Copyright (c) 2000-2007, JPackage Project
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

%define _with_gcj_support 0

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define base_name  codec
%define short_name commons-%{base_name}
%define section    free

Name:           jakarta-commons-codec
Version:        1.3
Release:        %mkrel 9.4.3
Summary:        Implementations of common encoders and decoders
License:        Apache Software License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Epoch:          0
URL:            http://jakarta.apache.org/commons/codec/
Source0:        commons-codec-%{version}-src.tar.gz
# svn export http://svn.apache.org/repos/asf/jakarta/commons/proper/codec/tags/CODEC_1_3/
# cd CODEC_1_3
# tar czvf commons-codec-1.3-src.tar.gz .

Patch0:         jakarta-commons-codec-1.3-buildscript.patch
# Add OSGi manifest
Patch1:         %{name}-addosgimanifest.patch
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  java-javadoc
%if ! %{gcj_support}
BuildArch:      noarch
%endif
Provides:       %{short_name} = %{epoch}:%{version}-%{release}
Obsoletes:      %{short_name} <= %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders. Examples include Base64, Hex,
Phonetic and URLs.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       java-javadoc

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -c

# FIXME Remove SoundexTest which is failing
# and thus preventing the build to proceed.
# This problem has been communicated upstream Bug 31096
%patch0 -p1

# Add OSGi manifest
pushd src/conf
%patch1 -p0
popd

#fixes eof encoding
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' RELEASE-NOTES.txt

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
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

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
