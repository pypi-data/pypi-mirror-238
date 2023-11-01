local function parse_commit_message(commit_msg)
    local pattern = "^(%a+):"
    local change_type = commit_msg:match(pattern)
    print("Commit message: " .. commit_msg)
    print("Change type: " .. tostring(change_type))
    return change_type
end

local function increment_version(version_str, change_type)
    local major, minor, patch = version_str:match("(%d+)%.(%d+)%.(%d+)")
    
    if change_type == "feat" or change_type == "Feat" then
        minor = tonumber(minor) + 1
    elseif change_type == "fix" or change_type == "Fix" then
        patch = tonumber(patch) + 1
    elseif change_type == "chore" or change_type == "Chore" then
        patch = tonumber(patch) + 1
    elseif change_type == "improv" or change_type == "Improv" or change_type == "improvement" or change_type == "Improvement" then
        patch = tonumber(patch) + 1
    elseif change_type == "major" or change_type == "Major" then
        major = tonumber(major) + 1
        minor = 0
        patch = 0
    else
        patch = tonumber(patch) + 1
    end

    return string.format("%s.%s.%d", major, minor, patch)
end

local function isempty(s)
    return s == nil or s == ''
end

local current_version = io.popen("git tag --sort=committerdate | tail -1"):read("*a")
local commit_msg = io.popen("git log -1 --pretty=%B"):read("*a")
print("current_version: " .. current_version)


if not isempty(current_version) and not isempty(commit_msg) then
    local change_type = parse_commit_message(commit_msg)
    
    -- convert v0.0.1-dev to 0.0.1
    current_version = current_version:gsub("v", "")
    current_version = current_version:gsub("-de", "")

    print("Current version: " .. current_version)

    local new_project_version = increment_version(current_version, change_type)
    io.open(os.getenv("GITHUB_OUTPUT"), "a"):write("version=" .. tostring(new_project_version) .. "\n")
    io.write("version=" .. tostring(new_project_version) .. "\n")
else
    print("Could not read current version or commit message")
    io.open(os.getenv("GITHUB_OUTPUT"), "a"):write("version=" .. tostring("0.0.1") .. "\n")
    io.write("version=" .. tostring("0.0.1") .. "\n")
end
