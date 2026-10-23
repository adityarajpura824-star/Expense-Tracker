import os, re, sys
p = "android/app/build.gradle"
s = open(p).read()
run = os.environ.get("GITHUB_RUN_NUMBER", "1")
s = re.sub(r"versionCode \d+", "versionCode " + run, s, count=1)
s = re.sub(r'versionName "[^"]*"', 'versionName "1.0.' + run + '"', s, count=1)
if os.environ.get("SIGN") == "1":
    block = '''signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH"))
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {'''
    s = s.replace("buildTypes {", block, 1)
    s = s.replace("release {\n            minifyEnabled", "release {\n            signingConfig signingConfigs.release\n            minifyEnabled", 1)
    assert "signingConfig signingConfigs.release" in s
open(p, "w").write(s)
print(s[s.index("defaultConfig"):s.index("defaultConfig")+120])
