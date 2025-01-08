@echo off
setlocal enabledelayedexpansion

set "date=What is the date?"
set "base_dest=C:\Where to store on desktop"

rem Define an array of source and destination folder pairs
set "sources[0]=S:\copy from"
set "sources[1]=S:\copy from"
rem etc...

set "destinations[0]=copy too"
set "destinations[1]=copy too"
rem etc...

rem Loop over the arrays from 0 to 8
for /L %%i in (0,1,8) do (
    set "src=!sources[%%i]!"
    set "dst=%base_dest%\!destinations[%%i]!\%date%"

    rem Create the destination directory if it doesn't exist
    if not exist "!dst!" (
        mkdir "!dst!"
    )

    rem Use robocopy to copy the files
    robocopy "!src!" "!dst!" /s /max:52428800
)

endlocal
