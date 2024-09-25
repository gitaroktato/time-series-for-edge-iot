option task = {name: "latency_writes", every: 5s}
 
from(bucket: "home")
    |> range(start: -15s, stop: now())
    |> map(fn: (r) => ({r with _value: (int(v: now()) - int(v: r._time)) / 1000000}))
    |> last()
    |> to(bucket: "latency", org: "docs")