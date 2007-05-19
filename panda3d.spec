#
Summary:	Panda3D -  a library of subroutines for 3D rendering and game development.-
Name:		panda3d
Version:	1.3.2
Release:	0.1
License:	other
Group:		Applications
Source0:	http://panda3d.org/download/panda3d-1.3.2/%{name}-%{version}.tar.gz
# Source0-md5:	2332e4a625d6beb3d480aa4825b2ee89
URL:		http://panda3d.org/
Requires:	python
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Panda3D is a 3D engine: a library of subroutines for 3D rendering and
game development. The library is C++ with a set of Python bindings.
Game development with Panda3D usually consists of writing a Python
program that controls the the Panda3D library.

Panda3D is unusual in that its design emphasis is on supporting a
short learning curve and rapid development. It is ideal whenever
deadlines are tight and turnaround time is of the essence.

%prep
%setup -q

%build
%{__python} makepanda/makepanda.py \
		--version 1.3.2 \
		--everything

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{py_dyndir}
install -d $RPM_BUILD_ROOT%{py_sitedir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d

sed -e 's@$THIS_PRC_DIR/[.][.]@%{_datadir}/%{name}@' < built/etc/Config.prc > $RPM_BUILD_ROOT%{_sysconfdir}/Config.prc

cp built/etc/Confauto.prc    $RPM_BUILD_ROOT%{_sysconfdir}/Confauto.prc
cp --recursive built/include $RPM_BUILD_ROOT%{_includedir}/%{name}
cp --recursive direct        $RPM_BUILD_ROOT%{_datadir}/%{name}/direct
cp --recursive built/pandac  $RPM_BUILD_ROOT%{_datadir}/%{name}/pandac
cp --recursive built/Pmw     $RPM_BUILD_ROOT%{_datadir}/%{name}/Pmw
cp built/direct/__init__.py  $RPM_BUILD_ROOT%{_datadir}/%{name}/direct/__init__.py
cp --recursive SceneEditor   $RPM_BUILD_ROOT%{_datadir}/%{name}/SceneEditor
cp --recursive built/models  $RPM_BUILD_ROOT%{_datadir}/%{name}/models
cp --recursive samples       $RPM_BUILD_ROOT%{_datadir}/%{name}/samples
cp --recursive built/lib     $RPM_BUILD_ROOT%{_libdir}/%{name}
cp doc/LICENSE               $RPM_BUILD_ROOT%{_libdir}/%{name}/LICENSE
cp doc/LICENSE               $RPM_BUILD_ROOT%{_datadir}/%{name}/LICENSE
cp doc/LICENSE               $RPM_BUILD_ROOT%{_includedir}/%{name}/LICENSE
cp doc/ReleaseNotes          $RPM_BUILD_ROOT%{_datadir}/%{name}/ReleaseNotes
echo "%{_libdir}/%{name}" >    $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/panda3d.conf
echo "%{_datadir}/%{name}" >  $RPM_BUILD_ROOT%{py_sitedir}/panda3d.pth
cp built/bin/*               $RPM_BUILD_ROOT%{_bindir}

for x in built/lib/* ; do
  base=`basename $x`
  ln -sf %{_libdir}/%{name}/$base $RPM_BUILD_ROOT%{py_dyndir}/$base
done
for x in $RPM_BUILD_ROOT%{_datadir}/%{name}/direct/src/* ; do
  if [ `basename $x` != extensions ] ; then
    python -c "import compileall; compileall.compile_dir('$x')"
  fi
done
python -c "import compileall ; compileall.compile_dir('$RPM_BUILD_ROOT%{_datadir}/%{name}/Pmw');"
python -c "import compileall ; compileall.compile_dir('$RPM_BUILD_ROOT%{_datadir}/%{name}/SceneEditor');"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/LICENSE doc/README doc/ReleaseNotes 
%{_datadir}/%{name}
%{_sysconfdir}/ld.so.conf.d/panda3d.conf
%{_libdir}/*
%{_includedir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
