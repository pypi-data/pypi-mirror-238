import subprocess, sys

def build():
	for url_path in sys.path:
		if "site-packages" in url_path:
			this_path = f"{url_path}/proxiestor/pytor.cpp"
			break
	subprocess.run(["cythonize", this_path, "build_ext", "--inplace", "--force", "-j", "5"])
	print(this_path)
