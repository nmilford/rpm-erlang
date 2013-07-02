rpm-erlang
==========

An RPM spec file to build and install the Erlang programming language.

Should be compatable with the ESL & EPEL-Erlang RPMs in that it obsoletes them.

To Build:

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install ncurses-devel openssl-devel zlib-devel flex m4`

`wget https://raw.github.com/nmilford/rpm-erlang/master/erlang.spec -O ~/rpmbuild/SPECS/erlang.spec`

`wget http://www.erlang.org/download/otp_src_R16B01.tar.gz -O ~/rpmbuild/SOURCES/otp_src_R16B01.tar.gz`

`wget http://www.erlang.org/download/otp_doc_html_R16B01.tar.gz -O ~/rpmbuild/SOURCES/otp_doc_html_R16B01.tar.gz`

`wget http://www.erlang.org/download/otp_doc_man_R16B01.tar.gz -O ~/rpmbuild/SOURCES/otp_doc_man_R16B01.tar.gz`

`rpmbuild -bb ~/rpmbuild/SPECS/erlang.spec`