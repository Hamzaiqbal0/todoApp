@echo off
echo Preparing project for Vercel deployment...

REM Copy frontend files to root directory
xcopy /E /I /Y "frontend\*" .

echo Project prepared for Vercel deployment.
echo You can now deploy using 'vercel --prod' from this directory.