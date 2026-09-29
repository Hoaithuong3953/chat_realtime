AI_LIMIT_SCRIPT = """
local daily_key = KEYS[1]

local daily_limit = tonumber(ARGV[1])
local daily_ttl = tonumber(ARGV[2])

local current_count = tonumber(redis.call("GET", daily_key) or "0")

if current_count >= daily_limit then
    return 1
end

redis.call("INCR", daily_key)

if current_count == 0 then
    redis.call("EXPIRE", daily_key, daily_ttl)
end

return 0
"""