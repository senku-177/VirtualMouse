@echo off
:: Run Python script as administrator
powershell -Command "Start-Process 'python' -ArgumentList 'Virtual_Mouse.py' -Verb RunAs"
