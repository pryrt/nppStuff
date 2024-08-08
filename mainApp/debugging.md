# Debugging

Use [OutputDebugStringW()](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-outputdebugstringw) and the SysInternals [DebugView](https://learn.microsoft.com/en-us/sysinternals/downloads/debugview) (`dbgview64.exe`) utility

**example**: how to use a wstring plus `L""`-strings to make a single-line message (each of `name` and `indexName` and `keyWords` are `wchar_t*`):
```cpp
					std::wstring _pryrt(L"PRYRT: ");
					_pryrt += name;
					_pryrt += L" | ";
					_pryrt += indexName;
					_pryrt += L": (";
					_pryrt += (kwVal ? keyWords : L"<no keywords>");
					_pryrt += L")";
					OutputDebugStringW(_pryrt.c_str());
```
**example**: use swprintf_s():
```cpp
					wchar_t _pryrt2[512];
					swprintf_s(_pryrt2, L"ALTERNATE PRYRT: %d %s", 1, name);					
					OutputDebugStringW(_pryrt2);
```
