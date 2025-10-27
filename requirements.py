import pkg_resources

packages = ["googletrans", "tqdm", "httpx", "wordfreq", "asyncio", "time"]

for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"{package}=={version}")
    except pkg_resources.DistributionNotFound:
        print(f"{package} is not installed or is a built-in module.")
