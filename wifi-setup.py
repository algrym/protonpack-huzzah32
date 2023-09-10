# This will overwrite local settings when pasted into REPL
f = open('settings.toml', 'w')
f.write("CIRCUITPY_WIFI_SSID = \"CHANGE THIS\"\n")
f.write("CIRCUITPY_WIFI_PASSWORD = \"CHANGE THIS\"\n")
f.write("CIRCUITPY_WEB_API_PASSWORD = \"REDACTED_FOR_GITHUB\"\n")
f.close()
