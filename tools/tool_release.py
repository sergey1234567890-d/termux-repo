import json
Release = {
    "format" : 1,
    "repo" : "termux-repo",
    "url" : "https://raw.githubusercontent.com/sergey1234567890-d/termux-repo/windows/pull",
    "architecture" : ["x86",],
}
def sev(data):
    with open(data, "w") as f:
        json.dump(Release, f, indent = 4,)


