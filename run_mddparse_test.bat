@ECHO OFF
SETLOCAL enabledelayedexpansion


@REM put your files here
SET "SYNTAX_FILE=tests\p2600752_mdata.mrs"




@REM adjust config options per your needs
@REM when using "if" in BAT files, "1==1" is true and "1==0" is false

SET "CONFIG_SOMETHING=1==0"







REM :: prepare helper config strings

SET "MDD_PARSE_CONFIG_SETTINGS="
@REM IF %CONFIG_SOMETHING% (
@REM     SET MDD_PARSE_CONFIG_SETTINGS=!MDD_PARSE_CONFIG_SETTINGS! --config-something somethinga
@REM ) ELSE (
@REM     SET MDD_PARSE_CONFIG_SETTINGS=!MDD_PARSE_CONFIG_SETTINGS! --config-something somethingb
@REM )
@REM SET MDD_PARSE_CONFIG_SETTINGS=!MDD_PARSE_CONFIG_SETTINGS!  --config-something-add somethingelse


@REM REM :: file names with file schemes in json
@REM SET "SYNTAX_FILE_JSON=%SYNTAX_FILE%.json"


ECHO -
ECHO 1. read and parse
ECHO read from: %SYNTAX_FILE%
ECHO write to: .json
python dist/mdmtoolsap_bundle.py --program parse_mdd_metadata --file "%SYNTAX_FILE%" %MDD_PARSE_CONFIG_SETTINGS%
if !ERRORLEVEL! NEQ 0 ( echo ERROR: Failure && pause && goto CLEANUP && exit /b !ERRORLEVEL! )


@REM ECHO -
@REM ECHO 7 del .json temporary files
@REM DEL "%SYNTAX_FILE%.json"

ECHO -
:CLEANUP
ECHO 999. Clean up
REM REM :: comment: just deleting trach .pyc files after the execution - they are saved when modules are loaded from within bndle file created with pinliner
REM REM :: however, it is necessary to delete these .pyc files before every call of the mdmtoolsap_bundle
REM REM :: it means, 6 more times here, in this script; but I don't do it cause I have this added to the linliner code - see my pinliner fork
DEL *.pyc
IF EXIST __pycache__ (
DEL /F /Q __pycache__\*
)
IF EXIST __pycache__ (
RMDIR /Q /S __pycache__
)

ECHO done!
exit /b !ERRORLEVEL!

