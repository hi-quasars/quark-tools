--[[
-- common library
--]]

function widthformater(number, width, ph)
    local ret = tostring(number)
    if string.len(ret) < width then
        ret = string.rep(ph, width - string.len(ret)) .. ret
    end
    return ret
end

function mkdir_until_success(dir)
    local dirname
    local suffix=""
    local tmpid=0
    repeat
        dirname = dir .. suffix
        local ret, errmsg, errno = lfs.mkdir(dirname)
        --[[
        print("ret   : " .. tostring(ret == true))
        if ret == nil then
            print("errmsg: " .. errmsg)
            print("errno : " .. tostring(errno))
        end
        --]]
        suffix = widthformater(tmpid, 5, '0')
        suffix = "-" .. suffix
        tmpid = tmpid + 1
    until( ret == true )
end
