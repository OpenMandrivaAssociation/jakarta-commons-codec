%define gcj_support 0

%define base_name  codec
%define short_name commons-%{base_name}

Name:		jakarta-commons-codec
Version:	1.4
Release:	3
Summary:	Implementations of common encoders and decoders
License:	Apache Software License
Group:		Development/Java
Url:		https://jakarta.apache.org/commons/codec/
Source0:	http://archive.apache.org/dist/commons/codec/source/commons-codec-%{version}-src.tar.gz
# svn export http://svn.apache.org/repos/asf/jakarta/commons/proper/codec/tags/CODEC_1_3/
# cd CODEC_1_3
# tar czvf commons-codec-1.3-src.tar.gz .

%if ! %{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant >= 0:1.6.2
BuildRequires:	ant-junit
BuildRequires:	junit
BuildRequires:	java-javadoc
BuildRequires:	jpackage-utils
%rename		%{short_name}

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
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' RELEASE-NOTES.txt

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath junit)
#perl -p -i -e 's|../LICENSE|LICENSE.txt|g' build.xml
%ant \
	-Dbuild.sysclasspath=first \
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

%gcj_compile

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
%doc LICENSE.txt RELEASE-NOTES.txt
%{_javadir}/*
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

