Summary:        Ted, an easy Rich Text Processor
Name:           ted
Version:        2.17
Release:        %mkrel 3
License:	GPL
Group:          Office
Source:         ftp://ftp.nluug.nl/pub/editors/ted/%{name}-%{version}.src.tar.bz2
Source10:	%name-16.png
Source11:	%name-32.png
Source12:	%name-48.png
URL:            http://www.nllgg.nl/Ted/index.html
BuildRoot:	%_tmppath/%name-root
BuildRequires:  lesstif-devel
BuildRequires:  libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	png-devel
BuildRequires:	X11-devel

Summary(cs_CZ):	Ted, editor pro snadné formátovaní textu.
Summary(nl_NL):	Ted, een makkelijke 'Rich Text' verwerker

%description
Ted is an easy rich text processor. It can edit RTF files
in a wysiwyg manner. It supports multiple fonts and can
print to PostScript printers.

Ted consists of a general part: The program, something.afm files
and an American spelling checker. Additional packages with
spell checking dictionaries for different languages exist.

This package is the general part.

%description -l cs_CZ
Ted je jednoduchý textový procesor.
Umo¾òuje editovat RTF soubory WYSIWYG zpùsobem. Podporuje pou¾ití
více fontù a tisk na PostScriptové tiskárny.

Ted obsahuje v základní èásti: program, pár .afm souborù a americký
korektor pøeklepù. Existují i dal¹í balíèky obsahující slovníky
pro korekturu pøeklepù jiných jazykù.

Toto je základní èást.

%description -l nl_NL
Ted is een makkelijke 'Rich Text' verwerker. Je kan er RTF bestanden
op een visuele manier mee redigeren. Ted werkt met meedere lettertypes
en kan op PostScript printers afdrukken.

Ted bestaat uit een algemeen gedeelte: Het programma, allerlei.afm
bestanden en een Amerikaanse spellingwoordenlijst. Extra pakketten
met spellingwoordenlijsten voor andere talen zijn beschikbaar.

Dit pakket is het algemene gedeelte.

%prep
%setup -q -n Ted-%version

perl -pi -e 's!define\s*PKGDIR.*!define PKGDIR  "%_datadir/%name"!' appFrame/appFrameConfig.h.in
perl -pi -e 's!define\s*DOCUMENT_DIR.*!define DOCUMENT_DIR "%_datadir/%name/"!' Ted/tedConfig.h.in

%build

mkdir lib

for cible in bitmap libreg tedPackage ind appUtil appFrame Ted; do
(
cd $cible
%configure --with-MOTIF
%make
)

done

%if 0
%make CONFIGURE_OPTIONS="--with-MOTIF prefix=%_prefix"
%make package
%endif

# (cd Ted && %make Ted)

%install

mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_datadir/%name/{ind,afm}

( cd tedPackage ; tar xvf TedBindist.tar )

cp -a tedPackage/afm/* %buildroot%_datadir/%name/afm/
cp -a tedPackage/ind/* %buildroot%_datadir/%name/ind/
cp -a tedPackage/Ted/TedDocument-en_US.rtf %buildroot%_datadir/%name/
install -m 755 Ted/Ted %buildroot%_bindir

install -m 644 -D %SOURCE10 %buildroot%_iconsdir/hicolor/16x16/apps/%name.png
install -m 644 -D %SOURCE11 %buildroot%_iconsdir/hicolor/32x32/apps/%name.png
install -m 644 -D %SOURCE12 %buildroot%_iconsdir/hicolor/48x48/apps/%name.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Ted
Comment=Ted, Rich Text Processor
Exec=%{_bindir}/Ted
Icon=%{name}
Terminal=false
Type=Application
Categories=Motif;Office;Wordprocessor;
EOF

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr(-, root, root)
%doc README tedPackage/Ted/TedDocument-en_US.rtf
%_bindir/Ted
%_datadir/%name
%_iconsdir/hicolor/16x16/apps/%name.png
%_iconsdir/hicolor/32x32/apps/%name.png
%_iconsdir/hicolor/48x48/apps/%name.png
%{_datadir}/applications/mandriva-%{name}.desktop

