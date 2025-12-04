# GCC
```
cd PowerEditor\gcc\
cls & mingw32-make & "bin.x86_64\notepad++.exe" & TITLE Build Notepad++
```

Note, since I use Strawberry Perl's gcc environment, I have found difficulty with the newer.  I need to set
```
PATH=c:\usr\local\apps\gcc_perl538\bin;%PATH%
```
before running the above in order to get it to work.  

- Perl 5.38 comes with gcc 13.1.0 and mingw32-make 4.4.1
- Perl 5.40 comes with gcc 13.2.0 and mingw32-make 4.4.1 (same for 5.42)

With gcc 13.2.0, it appears to internally call `sh.exe -c ...`, which fails, since I don't have `sh.exe` in my path, not being on MSYS2.  I don't know why it has a built-in requirement of sh.exe, nor how that version works to build Perl modules if it's inherent to the compiler; but that's what my experience shows... For now, use perl5.38's gcc if I want to do gcc-builds

# VS 2019

_not using 2019 any more, but keep this for reference_

Since VisualStudio 2019 is outdated, it cannot build the v143 project, so need the following changes:

- For each of the 3 projects in the solution: **Properties > General > Platform Toolset** = `v142`
- **Project `Notepad++` > Properties > C/C++ > General > Treat Warnings as Errors** = `No (/WX-)`
- `src/NppDarkMode.cpp`: search for `DWMWA_USE_IMMERSIVE_DARK_MODE` and insert:
  ```
  #ifndef DWMWA_USE_IMMERSIVE_DARK_MODE
  #define DWMWA_USE_IMMERSIVE_DARK_MODE 20
  #endif
  ```
- `src/json/json.cpp`: search for `token_type scan_number()` and insert:
  **before**:
  ```
  #pragma warning ( push )
  #pragma warning ( disable: 26438 )
  ```
  **after**:
  ```
  #pragma warning ( pop )
  ```

**IMPORTANT**: Make sure these changes are not committed to GitHub
