from functions.get_files_info import get_files_info
print(f"Result for '.' directory\n")
print(get_files_info("calculator", "."))
print(f"Result for 'pkg' directory\n")
print(get_files_info("calculator", "pkg"))
print(f"Result for '/bin' directory\n")
print(get_files_info("calculator", "/bin"))
print(f"Result for '../' directory\n")
print(get_files_info("calculator", "../"))