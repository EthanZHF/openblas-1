Name     : openblas
Version  : 0.2.15
Release  : 12
URL      : http://www.openblas.net/
Source0  : http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz
Summary  : The OpenBLAS linear algebra package
Group    : Development/Tools
License  : BSD-3-Clause

Patch1: lto.patch


#
# Note that this package currently does not have a -dev component.
# It seems that all users of BLAS stuff expect the whole thing to be there
#

BuildRequires : gfortran

%description
OpenBLAS is an optimized linear algebra library.


%prep
%setup -q -n OpenBLAS-%{version}
%patch1 -p1

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto -fno-semantic-interposition -O3 "
export CXXFLAGS="$CXXFLAGS -flto -fno-semantic-interposition -O3 "

sed -i -e "s/\-O2/\-O3/g" Makefile*

pushd ..
	cp -a OpenBLAS-%{version} openblas-noavx
	cp -a OpenBLAS-%{version} openblas-avx2

	pushd openblas-noavx
	make TARGET=SANDYBRIDGE SHARED=1 DYNAMIC_THREADS=1 NUM_THREADS=44 %{?_smp_mflags} 
	popd
	export CFLAGS="$CFLAGS -march=haswell "
	export FFLAGS="$FFLAGS -march=haswell -O3 "
	pushd openblas-avx2
	make TARGET=HASWELL SHARED=1 DYNAMIC_THREADS=1  NUM_THREADS=44 %{?_smp_mflags} 
	popd
popd


%install
rm -rf %{buildroot}
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto -ffunction-sections -fno-semantic-interposition -O3 "
export CXXFLAGS="$CXXFLAGS -flto -ffunction-sections -fno-semantic-interposition -O3 "

pushd ..

	pushd openblas-noavx
	make install DESTDIR=%{buildroot} PREFIX=/usr OPENBLAS_LIBRARY_DIR=/usr/lib64
	popd
	export CFLAGS="$CFLAGS -march=haswell "
	pushd openblas-avx2
	make install DESTDIR=%{buildroot} PREFIX=/usr OPENBLAS_LIBRARY_DIR=/usr/lib64/avx2
	popd
popd

#check
#pushd ..
#
#	pushd openblas-noavx
#	make -C test all
#	popd
#popd

%files
%defattr(-,root,root,-)
/usr/include/cblas.h
/usr/include/f77blas.h
/usr/include/lapacke.h
/usr/include/lapacke_config.h
/usr/include/lapacke_mangling.h
/usr/include/lapacke_utils.h
/usr/include/openblas_config.h
/usr/lib64/avx2/libopenblas.a
/usr/lib64/avx2/libopenblas.so
/usr/lib64/avx2/libopenblas.so.0
/usr/lib64/avx2/libopenblas_haswellp-r0.2.15.a
/usr/lib64/avx2/libopenblas_haswellp-r0.2.15.so
/usr/lib64/libopenblas.a
/usr/lib64/libopenblas.so
/usr/lib64/libopenblas.so.0
/usr/lib64/libopenblas_sandybridgep-r0.2.15.a
/usr/lib64/libopenblas_sandybridgep-r0.2.15.so
/usr/lib64/avx2/cmake/openblas/OpenBLASConfig.cmake
/usr/lib64/cmake/openblas/OpenBLASConfig.cmake