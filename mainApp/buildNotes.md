# GCC
```
cd PowerEditor\gcc\
cls & mingw32-make & "bin.x86_64\notepad++.exe" & TITLE shortcuts3cls & mingw32-make & "bin.x86_64\notepad++.exe" & TITLE shortcuts3
```

# VS 2019

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
