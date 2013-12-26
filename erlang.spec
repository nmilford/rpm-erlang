# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# wget https://raw.github.com/nmilford/rpm-erlang/master/erlang.spec -O ~/rpmbuild/SPECS/erlang.spec
# wget http://www.erlang.org/download/otp_src_R16B03.tar.gz -O ~/rpmbuild/SOURCES/otp_src_R16B03.tar.gz
# wget http://www.erlang.org/download/otp_doc_html_R16B03.tar.gz -O ~/rpmbuild/SOURCES/otp_doc_html_R16B03.tar.gz 
# wget http://www.erlang.org/download/otp_doc_man_R16B03.tar.gz -O ~/rpmbuild/SOURCES/otp_doc_man_R16B03.tar.gz
# rpmbuild -bb ~/rpmbuild/SPECS/erlang.spec

%global erl_ver R16B
%global erl_rel 03
%global erl_dest /usr/

Name:     erlang
Version:  %{erl_ver}%{erl_rel}
Release:  1
Summary:  General-purpose concurrent, garbage-collected programming language and runtime system.
Group:    Development/Languages
License:  ERPL
URL:      http://www.erlang.org
Source0:  http://www.erlang.org/download/otp_src_%{erl_ver}%{erl_rel}.tar.gz
Source1:  http://www.erlang.org/download/otp_doc_html_%{erl_ver}%{erl_rel}.tar.gz
Source2:  http://www.erlang.org/download/otp_doc_man_%{erl_ver}%{erl_rel}.tar.gz
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  flex
BuildRequires:  m4
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Obsoletes:      esl-erlang
Obsoletes:      esl-erlang-compat
Obsoletes:      erlang-appmon
Obsoletes:      erlang-asn1
Obsoletes:      erlang-common_test
Obsoletes:      erlang-compiler
Obsoletes:      erlang-cosEvent
Obsoletes:      erlang-cosEventDomain
Obsoletes:      erlang-cosFileTransfer
Obsoletes:      erlang-cosNotification
Obsoletes:      erlang-cosProperty
Obsoletes:      erlang-cosTime
Obsoletes:      erlang-cosTransactions
Obsoletes:      erlang-crypto
Obsoletes:      erlang-debugger
Obsoletes:      erlang-dialyzer
Obsoletes:      erlang-diameter
Obsoletes:      erlang-docbuilder
Obsoletes:      erlang-edoc
Obsoletes:      erlang-erl_docgen
Obsoletes:      erlang-erl_interface
Obsoletes:      erlang-erts
Obsoletes:      erlang-et
Obsoletes:      erlang-eunit
Obsoletes:      erlang-examples
Obsoletes:      erlang-gs
Obsoletes:      erlang-hipe
Obsoletes:      erlang-ic
Obsoletes:      erlang-inets
Obsoletes:      erlang-inviso
Obsoletes:      erlang-jinterface
Obsoletes:      erlang-kernel
Obsoletes:      erlang-megaco
Obsoletes:      erlang-mnesia
Obsoletes:      erlang-observer
Obsoletes:      erlang-odbc
Obsoletes:      erlang-orber
Obsoletes:      erlang-os_mon
Obsoletes:      erlang-otp_mibs
Obsoletes:      erlang-parsetools
Obsoletes:      erlang-percept
Obsoletes:      erlang-pman
Obsoletes:      erlang-public_key
Obsoletes:      erlang-reltool
Obsoletes:      erlang-runtime_tools
Obsoletes:      erlang-sasl
Obsoletes:      erlang-snmp
Obsoletes:      erlang-ssh
Obsoletes:      erlang-ssl
Obsoletes:      erlang-stdlib
Obsoletes:      erlang-syntax_tools
Obsoletes:      erlang-test_server
Obsoletes:      erlang-toolbar
Obsoletes:      erlang-tools
Obsoletes:      erlang-tv
Obsoletes:      erlang-typer
Obsoletes:      erlang-webtool
Obsoletes:      erlang-wx
Obsoletes:      erlang-xmerl

%description
Erlang is a programming language used to build massively scalable soft real-time
systems with requirements on high availability.  Erlang's runtime system has
built-in support for concurrency, distribution and fault tolerance.

This is a monolithic package that installs the whole Erlang install.

Deal with it.

%prep
%setup -q -n otp_src_%{erl_ver}%{erl_rel}

# Fix RPATH issue... too lazy to maintain a patch... if stuff breaks, look here.
sed -i -e 's|SSL_DED_LD_RUNTIME_LIBRARY_PATH = @SSL_DED_LD_RUNTIME_LIBRARY_PATH@|SSL_DED_LD_RUNTIME_LIBRARY_PATH =|' %_builddir/otp_src_%{erl_ver}%{erl_rel}/lib/crypto/c_src/Makefile.in
sed -i -e 's|$(SO_LD) $(SO_LDFLAGS) -L$(SO_SSL_LIBDIR) -Wl,-R$(SO_SSL_LIBDIR) |$(SO_LD) $(SO_LDFLAGS) -L$(SO_SSL_LIBDIR) |' %_builddir/otp_src_%{erl_ver}%{erl_rel}/lib/crypto/priv/Makefile

%build
# CentOS 6.5 disables EC GF2m curves.
FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DOPENSSL_NO_EC=1"

%configure --enable-shared-zlib --prefix=%{erl_dest} 

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# Drop docs
tar -xf %_sourcedir/otp_doc_man_%{erl_ver}%{erl_rel}.tar.gz -C %{buildroot}/%{erl_dest}/%{_lib}/erlang/
tar -xf %_sourcedir/otp_doc_html_%{erl_ver}%{erl_rel}.tar.gz -C %{buildroot}/%{erl_dest}/%{_lib}/erlang/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{erl_dest}/bin/*
%{erl_dest}/%{_lib}/erlang/*

%changelog
* Wed Dec 25 2013 Nathan Milford <nathan@milford.io>
- Bumped to version R16B03.
- Added workaround for EC GF2m curves missing in CentOS 6.5 OpenSSL.
* Fri Dec 6 2013 Nathan Milford <nathan@milford.io>
- Bumped to version R16B02. 
* Mon Jul 1 2013 Nathan Milford <nathan@milford.io>
- First shot at an Erlang/OTP RPM, version R16B01. 
- Should be compatable with the ESL & EPEL-Erlang RPMs in that it obsoletes them.
