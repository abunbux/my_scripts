from pathlib import Path


for dir_git in Path('.').rglob(r'.git*'):
    if dir_git.name == '.git':
        Path.rename(dir_git, Path.joinpath(dir_git.parent, ".git-backup"))
        print("Renamed " + str(dir_git.parent) + "/" + str(dir_git.name))
    elif dir_git.name == '.git-backup':
        Path.rename(dir_git, Path.joinpath(dir_git.parent, ".git"))
        print("Renamed " + str(dir_git.parent) + "/" + str(dir_git.name))
